import requests
import re
import Queue
import codecs
from threading import Thread

requests.packages.urllib3.disable_warnings()

def check(q):
	s = requests.session()
	while True:
		proxy = q.get()
		work = False
		print 'Checking {0}!'.format(proxy)
		try:
			headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
			}
			prozy = {
				'http': proxy,
				'https': proxy
			}
			r = s.get(
						'https://dynamisonline.ca/account',
						verify=False,
						proxies=prozy,
						timeout=12,
						headers=headers
					)
			#print r.text
			if 'Account' in r.text:
				work = True
			del r
		except Exception:
			work = False
		if work:
			f = open("Proxies Working.txt", "a")
			f.write("{0}\n".format(proxy))
			f.close()
		q.task_done()
	
def main():
	with codecs.open('proxies.txt', 'r') as f:
		proxies = f.readlines()
	queue = Queue.Queue()
	
	for _ in range(150):
		worker = Thread(target=check, args=(queue,))
		worker.start()
		
	for proxy in proxies:
		queue.put(proxy.strip())
			
if __name__ == '__main__':
	main()