# -*- coding: utf-8 -*-
import requests
import time
import addrgen.py
from threading import Thread

requests.packages.urllib3.disable_warnings()


def check():
	while True:
	
		proxy = {
			#'http': '127.0.0.1:8888',
			#'https': '127.0.0.1:8888'
		}
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
			'X-Requested-With': 'XMLHttpRequest',
			'x-csrf-token': 'VDQWWtGqjlie',
			'Accept-Encoding': 'gzip',
			'Cookie': '__cfduid=dd868bb6cf95ffa9b92df2d220a1746e51455856889; referrer=1503444; btc_address=1LYN4bkmwUpNyeVZHNEDHVjwG2Gr72f6W6; password=e08c0ef240ee9490d3c5cf9f7a46a72cfc7361599100125af05fc4baacd5eba0; have_account=1; sm_dapi_session=1; csrf_token=VDQWWtGqjlie; ref_website=https%3A%2F%2Ffreebitco.in%2F%3Fop%3Dhome; __utmt=1; __utma=120334047.1292455034.1455856899.1455856899.1455856899.1; __utmb=120334047.1.10.1455856899; __utmc=120334047; __utmz=120334047.1455856899.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); default_free_play_captcha=recaptcha_v1; last_play=1455856918'
		}
		s = requests.session()
		r = s.get(
					'https://freebitco.in/cgi-bin/bet.pl?m=lo&client_seed=30Tzd8eyQYmtmBTB&jackpot=1&stake=0.0000005&multiplier=1.06&rand=0.14164369320496917&csrf_token=VDQWWtGqjlie',
					verify=False,
					headers=headers,
					proxies=proxy
				)
		l = r.text.split(":")
		if 's1' in l[0]:
			if 'w' in l[1]:
				print 'Win:', l[3]
			elif '8888' in l[2]:
				print 'Jackpot:', l[3]
			else:
				print 'Lose:', l[3]
		time.sleep(0.005)
	
def main():
	for _ in range(4):
		worker = Thread(target=check)
		worker.start()
			
if __name__ == '__main__':
	print addrgen.get_addr(gen_eckey())
	main()