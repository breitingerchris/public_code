import requests
import Queue
import codecs
from threading import Thread

requests.packages.urllib3.disable_warnings()


def check(q):
    while True:
        user = q.get()
        work = False
        s = requests.session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'
        }
        r = s.get(
                    'https://www.reddit.com/api/username_available.json?user={0}'.format(user.split(':')[0]),
                    verify=False,
                    headers=headers
                )
        if 'false' in r.text:
            work = True
        if work:
            print user.split(':')[0], 'is registered!'
            f = open("Registered.txt", "a")
            f.write("{0}\n".format(user))
            f.close()
        q.task_done()
    
def main():
    with codecs.open('accounts.txt', 'r') as f:
        users = f.readlines()
        
    queue = Queue.Queue()
    
    for _ in range(75):
        worker = Thread(target=check, args=(queue,))
        worker.start()
    for user in users:
        queue.put(user.strip())
            
if __name__ == '__main__':
    main()