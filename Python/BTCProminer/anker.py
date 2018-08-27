import random
import requests
import codecs
import json
import re
import Queue
import time
from threading import Thread

requests.packages.urllib3.disable_warnings()

proxy = '127.0.0.1:8888'
with codecs.open('proxies.txt', 'r', encoding='utf-8') as f:
	proxies = f.readlines()
def sec(q):
	while True:
		proxy = random.choice(proxies)
		c = q.get()
		c = c.split('"')[1]
		headers = {
			'Accept': 'application/json, text/javascript, */*; q=0.01',
			'Referer': 'https://btcprominer.life/272192',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2767.4 Safari/537.36',
			'Content-Type': 'application/x-www-form-urlencoded',
			'X-Requested-With': 'XMLHttpRequest',
			}
		try:
			work = False
			prozy = {
				'http': proxy,
				'https': proxy
			}
			s = requests.session()
			r = s.get(
				"https://btcprominer.life/272192",
				verify=False,
				timeout=6,
				proxies=prozy,
				headers=headers
			)
			print r.text
			r = s.post(
				"https://btcprominer.life/ajax/sign",
				'address={0}&pin=1111'.format(c),
				verify=False,
				timeout=6,
				proxies=prozy,
				headers=headers
			)
			if '[]' in r.text:
				print 1
		except Exception, e:
			pass


def main():
	with codecs.open('addrs.txt', 'r', encoding='utf-8') as f:
		addr = f.readlines()
	queue = Queue.Queue()
	
	for _ in xrange(50):
		worker = Thread(target=sec, args=(queue,))
		worker.start()
	for user in addr:
		queue.put(user.strip().encode('ascii', 'ignore'))

if __name__ == '__main__':
	main()