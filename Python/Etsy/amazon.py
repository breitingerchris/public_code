import requests
import re
from bs4 import BeautifulSoup
from threading import Thread
import queue

requests.packages.urllib3.disable_warnings()

def check(url):
	try:
		r = requests.get(
					url,
					verify=False
				)
		bs4 = BeautifulSoup(r.text, 'html.parser')
		price = int(bs4.find('span', id='priceblock_ourprice').get_text().replace('$', '').split('.')[0]) + 8
		desc = bs4.find(id="productTitle").get_text().strip()
		feat = bs4.find('div', id='feature-bullets').find('ul', {'class': 'a-unordered-list a-vertical a-spacing-none'}).findAll('span')
		img = bs4.find('div', id='imgTagWrapperId').find('img')['src']
		list = ''
		for a in feat:
			list += a.get_text().strip() + '\\n'
		with open('scrape.txt', 'a') as f:
			f.write('{0}@{1}@{2}@{3}\n'.format(desc, list, img, price))
		work = False
	except:
		pass
            
            

    
def main():
	f = open('urls.txt', 'r')
	l = f.readlines()
	f.close()
	for i in l:
		check(i)
        
if __name__ == '__main__':
    main()