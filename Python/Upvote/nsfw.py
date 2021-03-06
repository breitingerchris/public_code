import requests
import Queue
import codecs
import json
import random
import re
import time
from threading import Thread
from random import choice
from random import randint

requests.packages.urllib3.disable_warnings()

proxies = {
	'http': '127.0.0.1:8888',
	'https': '127.0.0.1:8888'
}

def shuffle(x):
	x = list(x)
	random.shuffle(x)
	return x
	
def comment(q, purl):
	user = q.get()
	s = requests.session()
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
	}
	log = {'user': user.split(':')[0],
		  'passwd': user.split(':')[1],
		  'api_type': 'json'}
	r = s.post(
				'http://www.reddit.com/api/login',
				log,
				verify=False,
				headers=headers,
				#proxies=proxies
			)
	headers['X-Modhash'] = json.loads(r.text)['json']['data']['modhash']
	headers['Cookies'] = json.loads(r.text)['json']['data']['cookie']
	comments = [
		'Beautiful', 'Great', 'Im in love'
	]
	r = s.get(
				purl,
				verify=False,
				headers=headers,
				#proxies=proxies
			)
	uh = re.findall('uh" value="(.*?)"', r.text)
	etd = re.findall('id="form-t3_{0}(.*?)"><input type="hidden" name="thing_id"'.format(turl), r.text)
	r = s.post(
				'https://www.reddit.com/api/comment',
				'thing_id=t3_{0}&text={2}&id=%23form-t3_{0}{3}&r=leagueoflegends&uh={1}&renderstyle=html'.format(turl, uh[0], random.choice(comments), etd[0]),
				verify=False,
				headers=headers,
				#proxies=proxies
			)
	
def check(q, turl, purl):
	while True:
		url = 't3_{0}'.format(turl)
		user = q.get()
		work = False
		s = requests.session()
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
		}
		log = {'user': user.split(':')[0],
			  'passwd': user.split(':')[1],
			  'api_type': 'json'}
		r = s.post(
					'http://www.reddit.com/api/login',
					log,
					verify=False,
					headers=headers,
					#proxies=proxies
				)
		headers['X-Modhash'] = json.loads(r.text)['json']['data']['modhash']
		headers['Cookies'] = json.loads(r.text)['json']['data']['cookie']
		vote = {'dir': 1,
				'id': url}
		r = s.post(
					'http://www.reddit.com/api/vote',
					vote,
					verify=False,
					headers=headers,
					#proxies=proxies
				)
		if '{}' in r.text:
			work = True
		q.task_done()

def post(user, sub, url, text):
	try:
		s = requests.session()
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
		}
		log = {'user': user.split(':')[0],
			  'passwd': user.split(':')[1].strip("\n").strip("\r\n"),
			  'api_type': 'json'}
		r = s.post(
					'http://www.reddit.com/api/login',
					log,
					verify=False,
					headers=headers,
					#proxies=proxies
				)
		if not 'data' in json.loads(r.text)['json']:
			return False
		elif not 'modhash' in json.loads(r.text)['json']['data'] and not 'cookie' in json.loads(r.text)['json']['data']:
			return False
		
		headers['X-Modhash'] = json.loads(r.text)['json']['data']['modhash']
		headers['Cookies'] = json.loads(r.text)['json']['data']['cookie']
		
		data = {'api_type': 'json',
				'kind': 'link',
				'sendreplies': False,
				'title': text,
				'sr': sub,
				'url': url}
		r = s.post(
					'https://www.reddit.com/api/submit',
					data,
					verify=False,
					headers=headers,
					#proxies=proxies
				)
		if 'Your account has been locked' in r.text:
			return false
		elif not 'data' in json.loads(r.text)['json']:
			return False
		elif not 'url' in json.loads(r.text)['json']['data']:
			return False
		purl = json.loads(r.text)['json']['data']['url']
		turl = re.findall('comments/(.*?)/', purl)
		with codecs.open('urls.txt', 'a') as f:
			f.write('{0}\n'.format(purl))
		with codecs.open('accounts.txt', 'r') as f:
			users = f.readlines()
		queue = Queue.Queue()
		
		for _ in range(13):
			worker = Thread(target=check, args=(queue, turl[0], purl))
			worker.start()
		
		num = 0		
		for user in shuffle(users):
			if num >= 80:
				break
			queue.put(user.strip())
			num += 1
		comment(queue, purl)
		time.sleep(10)
		return True
	except Exception, err:
		print err
		return False
	
def main():
	subs = ['nba', 'movies', 'BlackPeopleTwitter', 'AdviceAnimals', 'mildlyinteresting', 'pics', 'ImGoingToHellForThis', 'nsfw_videos', 'The_Best_NSFW_GIFS', 'nsfw_gifs', 'RedheadGifs', 'nsfw_girlfriend_pics', 'hotness', 'topless', 'exmormon_nsfw', 'nsfw_wtf', 'NSFW_Comics', 'NSFW_nospam', 'Best_NSFW_Content', 'nsfw_selfie', 'NSFW_showcase']
	posts = [
		'Cute Amateur Posing Beautifully',
		'Cute Amateur Being Sexy'
		'Cute Amateur Posing Seductively',
		'Cute Amateur Being Beautiful'
		'Cute Amateur Posing Sexily',
		'Sexy Amateur Posing Beautifully',
		'Sexy Amateur Being Sexy'
		'Sexy Amateur Posing Seductively',
		'Sexy Amateur Being Beautiful'
		'Beautiful Amateur Posing Sexily',
		'Beautiful Amateur Posing Beautifully',
		'Beautiful Amateur Being Beautiful'
		'Beautiful Amateur Posing Seductively',
		'Beautiful Amateur Being Beautiful'
		'Beautiful Amateur Posing Sexily'
	]
	while True:
		for x in subs:
			print x
			with codecs.open('postaccs.txt', 'r') as f:
				p = f.readlines()
			done = False
			while not done:
				if post(choice(p), x, 'http://memeguy.xyz/?i={0}.jpg?{1}'.format(randint(1, 66), randint(99999,9999999999)), random.choice(posts)):
					done = True
			time.sleep(605)
		time.sleep(600)
if __name__ == '__main__':
	main()