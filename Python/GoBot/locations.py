import requests
import Queue
import codecs
import json
import random
import re
import time
from threading import Thread

requests.packages.urllib3.disable_warnings()

with codecs.open('pokemon.txt', 'r', encoding='utf-8') as f:
	pokemon = f.readlines()

def main():
	while True:
			work = True
			proxy = ''
			user =  random.choice(pokemon).strip() + str(random.randint(9999,99999))
			print user
			passw = 'playtime2'
			prozy = {
				'http': proxy,
				'https': proxy
			}
			s = requests.session()
			headers = {
				'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.8 Safari/537.36',
				'Content-Type': 'application/x-www-form-urlencoded',
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
				'Referer': 'https://club.pokemon.com/us/pokemon-trainer-club/parents/sign-up'
			}
			r = s.get(
						'https://club.pokemon.com/us/pokemon-trainer-club/sign-up',
						verify=False,
						headers=headers,
						proxies=prozy
					)
			while 'With the exciting launch of' in r.text:
				r = s.get(
							'https://club.pokemon.com/us/pokemon-trainer-club/sign-up',
							verify=False,
							headers=headers,
							proxies=prozy
						)
					
			csrf = re.findall("csrfmiddlewaretoken' value='(.*?)'", r.text)[0]
			data = "csrfmiddlewaretoken={0}&dob=1998-01-27&undefined=0&undefined=1998&country=US&country=US".format(
							csrf
						)
			r = s.post(
						'https://club.pokemon.com/us/pokemon-trainer-club/sign-up/',
						data,
						verify=False,
						headers=headers,
						proxies=prozy
					)
			requests.cookies.merge_cookies(s.cookies, {'dob': '1998-01-27'})
			data = "csrfmiddlewaretoken={3}&username={0}&password={1}&confirm_password={1}&email={0}@dispostable.com&confirm_email={0}@dispostable.com&public_profile_opt_in=True&screen_name={2}&terms=on".format(
							user, 
							passw, 
							user,
							csrf
						)
			r = s.post(
						'https://club.pokemon.com/us/pokemon-trainer-club/parents/sign-up',
						data,
						verify=False,
						headers=headers,
						proxies=prozy
					)
			if 'Thank you for creating an account' in r.text:
				print user, 'created!'
				with open("accounts.txt", "a") as f:
					f.write('{0}:{1}\n'.format(user, passw))
					f.close()
				work = False
			time.sleep(1.23)
		
if __name__ == '__main__':
	main()