import requests
import Queue
import codecs
import json
import random
import re
import time
from threading import Thread

requests.packages.urllib3.disable_warnings()

with codecs.open('proxies.txt', 'r', encoding='utf-8') as f:
	proxies = f.readlines()
def check(q):
	while True:
		try:
			work = False
			proxy = '127.0.0.1:8888'
			#proxy = random.choice(proxies).strip()
			prozy = {
				'http': proxy,
				'https': proxy
			}
			user = q.get()
			s = requests.session()
			headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
			}
			r = s.post(
						'https://club.pokemon.com/api/profile/verify-screenname',
						json={"name":user},
						verify=False,
						headers=headers,
						#proxies=prozy
					)
			#print r.text
			if 'inuse":false' in r.text and 'valid":true' in r.text:
				print user, 'works!'
				f = open("valid.txt", "a")
				f.write('{0}\n'.format(user))
				f.close()
			elif 'With the exciting launch ' in r.text:
				q.put(user.strip())
			elif 'inuse":true' in r.text:
				f = open("inuse.txt", "a")
				f.write('{0}\n'.format(user))
				f.close()
				print user, 'in use!'
			time.sleep(1.23)
			q.task_done()
		except Exception, e:
			q.put(user.strip())
			proxy = random.choice(proxies)

def main():
	queue = Queue.Queue()

	with codecs.open('names.txt', 'r') as f:
		users = f.readlines()
	for _ in range(1):
		worker = Thread(target=check, args=(queue,))
		worker.start()
	for user in users:
		queue.put(user.strip())
		
if __name__ == '__main__':
	main()