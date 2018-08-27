from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import time
def install_proxy(p):
		fp = webdriver.FirefoxProfile()
		PROXY_HOST = p.split(':')[0]
		PROXY_PORT = p.split(':')[1]
		fp.set_preference("network.proxy.type", 1)
		fp.set_preference("network.proxy.http",PROXY_HOST)
		fp.set_preference("network.proxy.http_port",int(PROXY_PORT))
		fp.set_preference("network.proxy.https",PROXY_HOST)
		fp.set_preference("network.proxy.https_port",int(PROXY_PORT))
		fp.set_preference("network.proxy.ssl",PROXY_HOST)
		fp.set_preference("network.proxy.ssl_port",int(PROXY_PORT))  
		fp.set_preference("network.proxy.ftp",PROXY_HOST)
		fp.set_preference("network.proxy.ftp_port",int(PROXY_PORT))   
		fp.set_preference("network.proxy.socks",PROXY_HOST)
		fp.set_preference("network.proxy.socks_port",int(PROXY_PORT))   
		fp.set_preference("general.useragent.override","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A")
		fp.update_preferences()
		return webdriver.Firefox(firefox_profile=fp)

with open('proxies.txt', 'r') as f:
	p = f.readlines()
	
while True:
	try:
		driver = webdriver.Firefox()
		driver.get("https://wn.nr/XsHwYE")
		assert "HELLC" in driver.title
		div = driver.find_element_by_xpath('//div[@id="em2397991"]')
		a = div.find_element_by_tag_name('a')
		a.click()
		div.find_element_by_id('contestant[name]').send_keys('meme {0}'.format(random.randint(99999999,999999999)))
		div.find_element_by_id('contestant[email]').send_keys('meme{0}@org.net'.format(random.randint(99999999,999999999)))
		div.find_element_by_tag_name('button').click()
		time.sleep(0.5)
		driver.close()
	except:
		driver.close()