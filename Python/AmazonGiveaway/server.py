import pickle
from selenium import webdriver

driver = webdriver.Firefox()
fp = open('drv', 'wb')
pickle.dump(driver, fp)
driver.get("https://www.amazon.com/gp/giveaway/home/ref=aga_shrt_hm")
url = driver.command_executor._url
session_id = driver.session_id
driver = webdriver.Remote(command_executor=url, desired_capabilities={})
driver.session_id = session_id
fp = open('drv', 'wb')
pickle.dump(driver, fp)