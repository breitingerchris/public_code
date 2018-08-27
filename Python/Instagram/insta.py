import requests
import Queue
from threading import Thread

requests.packages.urllib3.disable_warnings()


def check(q):
    while True:
        user = q.get()
        work = False
        s = requests.session()
        proxy = {
            'http': "127.0.0.1:8888",
            'https': "127.0.0.1:8888"
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
        }
        r = s.get(
                    'https://www.instagram.com/{0}/'.format(user.split(':')[0]),
                    verify=False,
                    headers=headers
                )
        if 'Sorry, this page' not in r.text:
            work = True
        if work:
            print user.split(':')[0], 'is registered!'
            f = open("Registered.txt", "a")
            f.write("{0}\n".format(user))
            f.close()
        q.task_done()
    
def main():
    with open('accounts.txt', 'r') as f:
        users = f.readlines()
        
    queue = Queue.Queue()
    
    for _ in range(35):
        worker = Thread(target=check, args=(queue,))
        worker.start()
    for user in users:
        queue.put(user.strip())
            
if __name__ == '__main__':
    main()