# -*- coding: utf-8 -*-
import requests
import re
import os
import codecs
import time
from threading import Thread

requests.packages.urllib3.disable_warnings()
    
def main():
    proxy = {
             'http': '127.0.0.1:8888',
             'https': '127.0.0.1:8888'
    }
    s = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
        'Accept-Encoding': 'gzip'
    }
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    r = s.get(
                'https://namecheap.com/',
                verify=False,
                headers=headers,
                proxies=proxy
            )
    data = 'LoginUserName={0}&LoginPassword={1}&hidden_LoginPassword='.format('mememe420', 'playtime2')
    r = s.post(
                'https://www.namecheap.com/myaccount/login.aspx',
                data,
                verify=False,
                headers=headers,
                proxies=proxy
            )
    for f in os.listdir("./email"):
        l = open("./email/{0}".format(f), "r")
        c = l.read()
        l.close()
        url = re.findall('DomainPush/(.*?)/invitation', c.replace('\r', '').replace('=', '').replace('\n', ''))
        if url:
            print url[0]
            r = s.get(
                    'https://ap.www.namecheap.com/Domains/DomainPush/{0}/accept'.format(url[0]),
                    verify=False,
                    headers=headers,
                    proxies=proxy
                )
            f = open("domains.txt", "a")
            f.write(url[0].split("/")[0] + '\n')
            f.close()
            
            
if __name__ == '__main__':
    main()
        