import requests
import re
import Queue
import random
import time
import codecs
import deathbycaptcha
import shutil
import string
from threading import Thread

requests.packages.urllib3.disable_warnings()

def check():
	s = requests.session()
	while True:
		er = True
		while er:
			s.cookies.clear()
			try:
				headers = {
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2810.2 Safari/537.36',
					'Accept-Encoding': 'gzip, deflate, br',
					'Accept-Language': 'en-US,en;q=0.8',
					'Referer': 'https://upmcoins.com/signup'
				}
				r = s.get(
					'https://upmcoins.com/?ref=27960',
					verify=False,
					timeout=16,
					headers=headers
				)
			except Exception, e:
				print e
	
def main():
	for _ in range(int(25)):
		worker = Thread(target=check)
		worker.start()
			
if __name__ == '__main__':
	main()