import random
import requests
import codecs
import json
import re
import Queue
import time
from threading import Thread

inviteCode = '05ea9c50be4fe7c82248'
requests.packages.urllib3.disable_warnings()


with codecs.open('proxies.txt', 'r', encoding='utf-8') as f:
	proxies = f.readlines()
	
with codecs.open('names.txt', 'r', encoding='utf-8') as f:
	names = f.readlines()

	
def sec(inv):
	headers = {
		'Referer': 'https://lbry.io/get?r=XxP0K'.format(inv),
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2767.4 Safari/537.36',
		'Content-Type': 'application/json',
		'X-Requested-With': 'XMLHttpRequest'
	}
	try:
		c = '{0} {1}'.format(random.choice(names).strip(), random.choice(names).strip())
		work = False
		proxy = random.choice(proxies).strip()
		prozy = {
			'http': proxy,
			'https': proxy
		}
		data = {
			'register_source': 'https%3A%2F%2Fwww.anker.com%2Fdeals%2F20m_credit%3Fic%3D{0}'.format(inv),
			'user': {
				'login': '{0}{1}@gmail.com'.format(c.split(' ')[0], random.randint(1000, 99999)),
				'uid': '{0}{1}'.format(random.randint(1000000000, 9999999999), random.randint(1000000000, 9999999999)),
				'third_party': 'google',
				"nick_name": c,
				"inviter_code": '{0}'.format(inv)
			}
		}
		r = requests.post(
			"https://www.anker.com/api/content?path=/api/sessions/third_party_login",
			json.dumps(data),
			verify=False,
			timeout=6,
			proxies=prozy,
			headers=headers
		)
		print r.text
		if '"is_first_login":true' in r.text:
			print 'Secondary Account'
		time.sleep(random.randint(300,500))
	except Exception, e:
		proxy = random.choice(proxies)
	
def reg(inv, first):
	headers = {
		'Referer': 'https://www.anker.com/deals/20m_credit?ic={0}'.format(inv),
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2767.4 Safari/537.36',
		'Content-Type': 'application/json',
		'X-Requested-With': 'XMLHttpRequest'
	}
	while True:
		try:
			c = '{0} {1}'.format(random.choice(names).strip(), random.choice(names).strip())
			work = False
			proxy = random.choice(proxies).strip()
			prozy = {
				'http': proxy,
				'https': proxy
			}
			proxy = random.choice(proxies).strip()
			prozy = {
				'http': proxy,
				'https': proxy
			}
			data = {
				'register_source': 'https%3A%2F%2Fwww.anker.com%2Fdeals%2F20m_credit%3Fic%3D{0}'.format(inv),
				'user': {
					'login': '{0}{1}@gmail.com'.format(c.split(' ')[0], random.randint(1000, 99999)),
					'uid': '{0}{1}'.format(random.randint(1000000000, 9999999999), random.randint(1000000000, 9999999999)),
					'third_party': 'google',
					"nick_name": c,
					"inviter_code": '{0}'.format(inv)
				}
			}
			r = requests.post(
				"https://www.anker.com/api/content?path=/api/sessions/third_party_login",
				json.dumps(data),
				verify=False,
				timeout=6,
				proxies=prozy,
				headers=headers
			)
			print r.text
			if '"is_first_login":true' in r.text:
				print 'Success!'
				if first:
					tok = re.findall('invitation_code":"(.*?)"', r.text)
					for _ in xrange(random.randint(1,14)):
						sec(tok)
				else:
					print 'Secondary Account'
			time.sleep(random.randint(300,500))
		except Exception, e:
			proxy = random.choice(proxies)
			

def main():
	for _ in xrange(25):
		worker = Thread(target=reg, args=(inviteCode, True,))
		worker.start()

if __name__ == '__main__':
	main()