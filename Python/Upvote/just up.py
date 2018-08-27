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

turl = '4v1l0l'
l = 'videos'
def check(q):
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
					proxies=proxies
				)
		if 'data' in json.loads(r.text)['json']:
			headers['X-Modhash'] = json.loads(r.text)['json']['data']['modhash']
			headers['Cookies'] = json.loads(r.text)['json']['data']['cookie']
			
			r = s.get(
						'https://www.reddit.com/r/{1}/comments/{0}/'.format(turl, l),
						verify=False,
						headers=headers,
						proxies=proxies
					)
			uh = re.findall('uh" value="(.*?)"', r.text)[0]
			vote = {
						'dir': 1,
						'id': url,
						'isTrusted': True,
						'r': l,
						'uh': uh
					}
			r = s.post(
						'https://www.reddit.com/api/vote?dir=1&id={0}&sr={1}'.format(url, l),
						vote,
						verify=False,
						headers=headers,
						proxies=proxies
					)
			if '{}' in r.text:
				work = True
		
		q.task_done()

def main():
	queue = Queue.Queue()

	with codecs.open('accounts.txt', 'r') as f:
		users = f.readlines()
	for _ in range(13):
		worker = Thread(target=check, args=(queue,))
		worker.start()

	num = 0		
	for user in shuffle(users):
		if num >= 1111:
			break
		queue.put(user.strip())
		num += 1
	time.sleep(10)
if __name__ == '__main__':
	main()