import requests
import Queue
import codecs
import json
import random
import re
import time
from threading import Thread
from random import choice
from random import randint

requests.packages.urllib3.disable_warnings()

proxies = {
    'http': '127.0.0.1:8888',
    'https': '127.0.0.1:8888'
}

def shuffle(x):
    x = list(x)
    random.shuffle(x)
    return x

def subz(headers, s):
    r = s.get(
                'https://www.reddit.com/r/LeagueOfLegends',
                verify=False,
                headers=headers,
                #proxies=proxies
            )
    uh = re.findall('uh" value="(.*?)"', r.text)
    print uh
    r = s.post(
                'https://www.reddit.com/api/subscribe',
                'sr=t5_2rfxx&action=sub&r=leagueoflegends&uh={0}&renderstyle=html'.format(uh[0]),
                verify=False,
                headers=headers,
                #proxies=proxies
            )


def check(q, turl, purl):
    while True:
        url = 't3_{0}'.format(turl)
        user = q.get()
        work = False
        s = requests.session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
        }
        log = {'user': user.split(':')[0],
              'passwd': user.split(':')[1],
              'api_type': 'json'}
        r = s.post(
                    'http://www.reddit.com/api/login',
                    log,
                    verify=False,
                    headers=headers,
                    ##proxies=proxies
                )
        headers['X-Modhash'] = json.loads(r.text)['json']['data']['modhash']
        headers['Cookies'] = json.loads(r.text)['json']['data']['cookie']
        vote = {'dir': 1,
                'id': url}
        r = s.post(
                    'http://www.reddit.com/api/vote',
                    vote,
                    verify=False,
                    headers=headers,
                    #proxies=proxies
                )
        if '{}' in r.text:
            work = True
        comments = [
            'Wow, this actually worked lol...', 'Thanks man!', 'I got a lot from this heh c:<', 'thank you sooooo much', 'this is FREAKING unbelievable! It WORKED!!!!!', 'Wow, didnt think it would actually work lol', 'Cant believe this worked... what?'
        ]
        if random.randint(0, 10) is 2:
            
            print purl
            if 'leagueoflegend' in purl:
                subz(headers, s)
            r = s.get(
                        purl,
                        verify=False,
                        headers=headers,
                        #proxies=proxies
                    )
            uh = re.findall('uh" value="(.*?)"', r.text)
            etd = re.findall('id="form-t3_{0}(.*?)"><input type="hidden" name="thing_id"'.format(turl), r.text)
            r = s.post(
                        'https://www.reddit.com/api/comment',
                        'thing_id=t3_{0}&text={2}!&id=%23form-t3_{0}{3}&r=leagueoflegends&uh={1}&renderstyle=html'.format(turl, uh[0], random.choice(comments), etd[0]),
                        verify=False,
                        headers=headers,
                        #proxies=proxies
                    )
        q.task_done()

def post(user, sub, url, text):
    try:
        s = requests.session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
        }
        log = {'user': user.split(':')[0],
              'passwd': user.split(':')[1].strip("\n").strip("\r\n"),
              'api_type': 'json'}
        r = s.post(
                    'http://www.reddit.com/api/login',
                    log,
                    verify=False,
                    headers=headers,
                    #proxies=proxies
                )
        if not 'data' in json.loads(r.text)['json']:
            return False
        elif not 'modhash' in json.loads(r.text)['json']['data'] and not 'cookie' in json.loads(r.text)['json']['data']:
            return False
        
        headers['X-Modhash'] = json.loads(r.text)['json']['data']['modhash']
        headers['Cookies'] = json.loads(r.text)['json']['data']['cookie']
        
        if 'LeagueOfLegends' in sub:
            subz(headers, s)
        data = {'api_type': 'json',
                'kind': 'link',
                'sendreplies': False,
                'title': text,
                'sr': sub,
                'url': url}
        r = s.post(
                    'https://www.reddit.com/api/submit',
                    data,
                    verify=False,
                    headers=headers,
                    #proxies=proxies
                )
        if not 'data' in json.loads(r.text)['json']:
            return False
        elif not 'url' in json.loads(r.text)['json']['data']:
            return False
        purl = json.loads(r.text)['json']['data']['url']
        turl = re.findall('comments/(.*?)/', purl)
        print turl
        with codecs.open('urls.txt', 'a') as f:
            f.write('{0}\n'.format(purl))
        with codecs.open('accounts.txt', 'r') as f:
            users = f.readlines()
        queue = Queue.Queue()
        
        for _ in range(13):
            worker = Thread(target=check, args=(queue, turl[0], purl))
            worker.start()
        
        num = 0        
        for user in shuffle(users):
            if num >= 80:
                break
            queue.put(user.strip())
            num += 1
        time.sleep(10)
        return True
    except Exception, err:
        print err
        return False
    
def main():
    xsubs = ['xbox360', 'xbox', 'consoledeals', 'GreatXboxDeals', 'MinecraftOne']
    psubs = ['PS3', 'PS4', 'ps3deals', 'PS4Deals', 'consoledeals']
    lsubs = ['LeagueOfLegends', 'League_Of_Legends_', 'LeagueOfMemes', 'summoners', 'LeagueOfLegendsUK']
    ssubs = ['gaming', 'Games', 'skyrim', 'GameDeals']
    isubs = ['ios', 'swift', 'AppleWatch', 'BestOfStreamingVideo', 'appleswap']
    tsubs = ['WorldofTanks', 'WorldofTanksXbox', 'WorldOfTanksPS4', 'WorldofTanksVideos']
    gsubs = ['GrandTheftAutoV', 'GTAV', 'ps3gtav', 'gta5', 'grandtheftauto5', 'GTAV_Cruises', 'gtaonline']
    while True:
        for x in xsubs:
            print x
            with codecs.open('postaccs.txt', 'r') as f:
                p = f.readlines()
            done = False
            while not done:
                if post(choice(p), x, 'http://memeguy.xyz/?to=bit.ly/1YLKpRs?{0}'.format(randint(99999,9999999999)), 'Free Xbox Live!'):
                    done = True
            time.sleep(605)
        for x in psubs:
            print x
            with codecs.open('postaccs.txt', 'r') as f:
                p = f.readlines()
            done = False
            while not done:
                if post(choice(p), x, 'http://memeguy.xyz/?to=bit.ly/1YLKpRs?{0}'.format(randint(99999,9999999999)), 'Free PS+ & PSN Points!'):
                    done = True
                    print 'Done!'
            time.sleep(605)
        for x in ssubs:
            print x
            with codecs.open('postaccs.txt', 'r') as f:
                p = f.readlines()
            done = False
            while not done:
                if post(choice(p), x, 'http://memeguy.xyz/?to=bit.ly/1YLKpRs?{0}'.format(randint(99999,9999999999)), 'Free Skyrim Game (Steam Key)!'):
                    done = True
            time.sleep(605)
        for x in lsubs:
            print x
            with codecs.open('postaccs.txt', 'r') as f:
                p = f.readlines()
            done = False
            while not done:
                if post(choice(p), x, 'http://memeguy.xyz/?to=bit.ly/1YLKpRs?{0}'.format(randint(99999,9999999999)), 'Free Riot Points!'):
                    done = True
            time.sleep(605)
        for x in isubs:
            print x
            with codecs.open('postaccs.txt', 'r') as f:
                p = f.readlines()
            done = False
            while not done:
                if post(choice(p), x, 'http://memeguy.xyz/?to=bit.ly/1YLKpRs?{0}'.format(randint(99999,9999999999)), 'Free iTunes Codes!'):
                    done = True
            time.sleep(605)
        for x in tsubs:
            print x
            with codecs.open('postaccs.txt', 'r') as f:
                p = f.readlines()
            done = False
            while not done:
                if post(choice(p), x, 'http://memeguy.xyz/?to=bit.ly/1YLKpRs?{0}'.format(randint(99999,9999999999)), 'Free World Of Tanks Hack!'):
                    done = True
            time.sleep(605)
        for x in gsubs:
            print x
            with codecs.open('postaccs.txt', 'r') as f:
                p = f.readlines()
            done = False
            while not done:
                if post(choice(p), x, 'http://memeguy.xyz/?to=bit.ly/1YLKpRs?{0}'.format(randint(99999,9999999999)), 'Free GTA V Steam Key!'):
                    done = True
            time.sleep(605)
        time.sleep(600)
if __name__ == '__main__':
    main()