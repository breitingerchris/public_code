# -*- coding: utf-8 -*-
import requests
import Queue
import codecs
import os
import base64
from threading import Thread
from Crypto.Cipher import AES

requests.packages.urllib3.disable_warnings()


def check(q):
    while True:
        try:
            c = q.get()
            user = c.split(':')[0]
            passw = c.split(':')[1]
            work = False
            proxy = {
            }
            s = requests.session()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
                'Accept-Encoding': 'gzip',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'X-Requested-With': 'XMLHttpRequest'
            }
            r = s.get(
                        'https://www.namecheap.com/Cart/ajax/DomainSelection.ashx?action=checkuser&username={0}'.format(user),
                        verify=False,
                        headers=headers,
                        proxies=proxy
                    )
            if 'UserExist' in r.text:
                print user, 'is registered!'
                f = open("registered.txt", "a")
                f.write('{0}\n'.format(c))
                f.close()
            else:
                print user, 'does not work!'
        except Exception, e:
            print e
            raw_input("Please Send Me The Error Message!")
        q.task_done()
    
def main():
    with codecs.open('tocheck.txt', 'r', encoding='utf-8') as f:
        users = f.readlines()
    with codecs.open('regthreads.txt', 'r', encoding='utf-8') as f:
        threads = f.read()
        
    queue = Queue.Queue()
    for _ in range(int(threads)):
        worker = Thread(target=check, args=(queue,))
        worker.start()
    for user in users:
        queue.put(user.strip().encode('ascii', 'ignore'))
            
def main():
    with codecs.open('tocheck.txt', 'r') as f:
        users = f.readlines()
    with codecs.open('regthreads.txt', 'r') as f:
        threads = f.read()
        
    queue = Queue.Queue()
    for _ in range(int(threads)):
        worker = Thread(target=check, args=(queue,))
        worker.start()
    for user in users:
        queue.put(user.strip())
            
if __name__ == '__main__':
    main()
        