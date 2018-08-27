# -*- coding: utf-8 -*-
import requests
import re
import Queue
import random
import codecs
import string
from threading import Thread

proxy = '127.0.0.1:8888'
prozy = {
	'http': proxy.strip(),
	'https': proxy.strip()
}
requests.packages.urllib3.disable_warnings()

def buy(mkt, amt, prc):
	try:
		s = requests.session()
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
			'Accept-Encoding': 'gzip',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Accept': 'application/json, text/javascript, */*; q=0.01',
			'X-Requested-With': 'XMLHttpRequest',
			'Cookie': '__cfduid=d022cfd24cb4eeb71d26b8d0e4fed0c221484593176; ASP.NET_SessionId=e0vfwekyetyn2xblhl2cohxz; __RequestVerificationToken=QKY7jdyak1EYC-POIyoN3UKr92kH7UueU4KzDqkNQ2v-tGCnfEUiet0JoG8EJAnSlBkJvKPAY52YsojK8yxoN1546cU1; .AspNet.ApplicationCookie=JiQmIyBO3mqOy0qnzLmZaK_UhDwhlV_q1JDhEorM4wMPZFQ5aen_3vK0y59xT_jOQHKeRnYS7Qd9LXP9j6CA1uVABkjzwsZZn1ymgDJ0DcReD49DZNHHyAwJ8I3wtXQpOpbkSJhRx2PW9oao1zoJnRuIhy9nR_4-aOFvC6bkpcKT9d9iDp3LV5ST3WjOX49sSzTUGUUHGwvrtvQ_Gxl_CevCJEmkxFofvhpPMOp-IwE4SU5oCeknYF1vs5EK71JfZKACOblcfUC_j6IXBgM1Qr8i3Og3qyHeCdBK9zxgAlE4NWf0nmUy0MQkMMtWzvocgEMIJ6pMJh29biMXdAh0n9RsNdjRGhLQ8cPP77Ziu5R93-bCD0bnw-4PwuAGkbai9hU0KHCaHlGdjIa3hAMORsSlX50l-Kq_IF0VssAshyRe3vOnpyh9N6bhS4MoljoW7YNSg57E03bWjglL5HEjAxM98leueOQ2441_nivo13arF1kp'
		}
		r = s.get(
					'https://bittrex.com/Market/Index?MarketName=' + mkt,
					verify=False,
					proxies=prozy,
					timeout=12,
					headers=headers
				)
				
		tkn = re.findall('__RequestVerificationToken" type="hidden" value="(.*?)"', r.text)[0]
		r = s.post(
					'https://bittrex.com/api/v2.0/auth/market/TradeBuy',
					data='MarketName={0}&OrderType=LIMIT&Quantity={1}&Rate={2}&TimeInEffect=GOOD_TIL_CANCELLED&ConditionType=NONE&Target={2}&__RequestVerificationToken={3}'.format(mkt, amt, prc, tkn),
					verify=False,
					proxies=prozy,
					timeout=12,
					headers=headers
				)
	except Exception, e:
		print e
		pass
	
def main():
	blk = '607801'
	a = {
		'0': 'IOP',
		'1': 'IOP',
		'2': 'IOP',
		'3': 'SNRG',
		'4': 'IOP',
		'5': 'IOP',
		'6': 'IOP',
		'7': 'IOP',
		'8': 'IOP',
		'9': 'IOP',
	}
	n = True
	try:
		while n:
			r = requests.get(
						'http://ltc.blockr.io/api/v1/block/info/' + blk,
						verify=False,
						proxies=prozy,
						timeout=12
					)
		hs = re.findall(',"hash":"(.*?)"', r.text)[0][0]
		if a[hs] is not "":
			n = False
		print a[hs]
		Thread.sleep(0.5)
	except:
		pass
	#buy('BTC-XMR',  '0.03930583', '0.01302014')

if __name__ == '__main__':
	main()