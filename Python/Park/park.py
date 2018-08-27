# -*- coding: utf-8 -*-
import requests
import Queue
import codecs
import time
import json
import sys
from threading import Thread

requests.packages.urllib3.disable_warnings()


def check(q, s, headers):
    while True:
        try:
            c = q.get()
            work = False
            proxy = {
                     'http': '127.0.0.1:8888',
                     'https': '127.0.0.1:8888'
            }
            headers['Accept'] = 'application/json, text/plain, */*'
            headers['_NcCompliance'] = s.cookies.get_dict()['_NcCompliance']
            data = {"nameServersList": "NS1.SEDOPARKING.COM,NS2.SEDOPARKING.COM,",
                    "dnsType": "Custom",
                    "domainName": c}
            headers['Content-Type'] = 'application/json;charset=UTF-8'
            r = s.post(
                    'https://ap.www.namecheap.com/Domains/DomainDetails/SetNameServers',
                    json.dumps(data),
                    verify=False,
                    headers=headers,
                    proxies=proxy
                )
            if 'Result":true' in r.text:
                print c, 'parked successfully!'
                f = open("parked.txt", "a")
                f.write(c + '\n')
                f.close()
            else:
                print c, 'not parked!'
            time.sleep(0.005)
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print exc_type, exc_value, exc_traceback
            raw_input("Please Send Me The Error Message!")
        q.task_done()
    
def main():
    with codecs.open('domains.txt', 'r', encoding='utf-8') as f:
        users = f.readlines()
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
    if 'Your account has been locked for' in r.text:
        print 'locked'
    elif 'Last logged in ' in r.text:
        queue = Queue.Queue()
        for _ in range(int(5)):
            worker = Thread(target=check, args=(queue, s, headers,))
            worker.start()
        for user in users:
            queue.put(user.strip().encode('ascii', 'ignore'))
            
if __name__ == '__main__':
    main()
        