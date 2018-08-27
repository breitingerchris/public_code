import random
import requests
import codecs
import json
import re
import queue
import time
from threading import Thread

requests.packages.urllib3.disable_warnings()

proxy = '127.0.0.1:8888'
def sec():
	while True:
		headers = {
			'Referer': 'https://www.achievemint.com/signup?referral=1&utm_campaign=YOaBLXQNLBg%3D%0A',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2767.4 Safari/537.36',
			'Content-Type': 'application/x-www-form-urlencoded'
		}
		try:
			c = '{0}@gmail.com'.format(random.randint(999999,999999999999))
			work = False
			prozy = {
				'http': proxy,
				'https': proxy
			}
			s = requests.session()
			r = s.get(
				"http://tinyurl.com/k44xy3f",
				verify=False,
				timeout=6,
				proxies=prozy,
				headers=headers
			)
			auth = re.findall('authenticity_token" value="(.*?)"', r.text)[0]
			va = re.findall('acceptedTos" type="checkbox" value="(.*?)"', r.text)[0]
			r = s.post(
				"https://www.achievemint.com/",
				'utf8=%e2%9c%93&authenticity_token={0}&after_sign_up_path=&user[confirmation_token]=&user[signup_token]=&user[email]={1}&user[password]=dsfdsf@D&user[accepted_tos]=1&user[accepted_tos]={2}&button='.format(auth, c, va),
				verify=False,
				timeout=6,
				proxies=prozy,
				headers=headers
			)
			if 'Welcome to Achievemint!' in r.text:
				print(1)
		except:
			pass


def main():
	for _ in range(3):
		worker = Thread(target=sec, args=())
		worker.start()

if __name__ == '__main__':
	main()