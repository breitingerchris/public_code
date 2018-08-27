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
	with codecs.open('captchas.txt', 'r', encoding='utf-8') as f:
		captch = f.readlines()
	s = requests.session()
	while True:
		er = True
		while er:
			s.cookies.clear()
			try:
				email = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(9))
				proxy = '127.0.0.1:8888'
				prozy = {
					'http': proxy,
					'https': proxy
				}
				works = False
				headers = {
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2810.2 Safari/537.36',
					'Accept-Encoding': 'gzip, deflate, br',
					'Accept-Language': 'en-US,en;q=0.8',
					'Referer': 'https://upmcoins.com/signup'
				}
				r = s.get(
					'https://upmcoins.com/?ref=27960',
					verify=False,
					proxies=prozy,
					timeout=16,
					headers=headers
				)
				r = s.get(
					'https://upmcoins.com/signup',
					verify=False,
					proxies=prozy,
					timeout=16,
					headers=headers
				)
				csrf = re.findall('csrfmiddlewaretoken" type="hidden" value="(.*?)"', r.text)[0]
				capt = random.choice(captch)
				headers['Content-Type'] = 'application/x-www-form-urlencoded'
				r = s.post(
					'https://upmcoins.com/signup',
					'csrfmiddlewaretoken={0}&email={1}@mailinator.com&captcha_0={2}&captcha_1={3}'.format(csrf, email, capt.split(':')[0], capt.split(':')[1]),
					verify=False,
					proxies=prozy,
					timeout=16,
					headers=headers
				)
				if 'Invalid CAPTCHA' in r.text:
					print 'ivali'
				elif 'Please save the login data in a safe place' in r.text:
					r = s.get(
								'https://upmcoins.com/server/0',
								verify=False,
								proxies=prozy,
								timeout=16,
								headers=headers
							)
					pas = re.findall('Password: (.*?)<', r.text)[0]
					pin = re.findall('PIN: (.*?)<', r.text)[0]
					capt = re.findall('class="captcha" src="(.*?)"', r.text)[0]
					fi = './captchas/' + capt.split('/')[3]
					with open(fi, 'wb') as out_file:
						shutil.copyfileobj(requests.get('https://upmcoins.com{0}'.format(capt), stream=True).raw, out_file)
				
					csrf = re.findall('csrfmiddlewaretoken" type="hidden" value="(.*?)"', r.text)[0]
					captcha = client.decode(fi, 20)
					if captcha:
						# The CAPTCHA was solved; captcha["captcha"] item holds its
						# numeric ID, and captcha["text"] item its text.
						print "CAPTCHA solved: %s" % (captcha["text"])
						f = open("captchas.txt", "a")
						f.write('{0}:{1}\n'.format(capt.split('/')[3], captcha["text"]))
						f.close()
					r = s.post(
								'https://upmcoins.com/server/0',
								'csrfmiddlewaretoken={0}&pin={1}&server=0&captcha_0={2}&captcha_1={3}'.format(csrf, pin, capt.split('/')[3], captcha["text"]),
								verify=False,
								proxies=prozy,
								timeout=16,
								headers=headers
							)
					if 'Working ' in r.text:
						print 'Done!'
						works = True
									
				if works:
					f = open("accounts.txt", "a")
					f.write('{0}:{1} - {2}\n'.format(email, pas, pin))
					f.close()
			except Exception, e:
				print e
	
def main():
	for _ in range(int(10)):
		worker = Thread(target=check)
		worker.start()
			
if __name__ == '__main__':
	main()