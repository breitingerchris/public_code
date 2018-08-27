import requests
from bs4 import BeautifulSoup

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
}
def grab(url):
	r = requests.get(
				url,
				headers=headers,
				verify=False
			)
	bs4 = BeautifulSoup(r.text, 'html.parser')
	p = bs4.find('section', {'class': 'new the-article'}).find('article').find_all('p')
	for i in p:
		print i
	
grab('http://listverse.com/2017/04/06/10-horrifying-ways-the-un-is-to-blame-for-the-rwandan-genocide/')
