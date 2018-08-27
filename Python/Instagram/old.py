import requests
import Queue
import codecs
import urllib
import hmac
import hashlib
from threading import Thread
from random import choice

requests.packages.urllib3.disable_warnings()

def generate_signature(self, data):
    key = "b4a23f5e39b5929e0666ac5de94c89d1618a2916"
    h = hmac.new(key, '', hashlib.sha256)
    h.update(data)
    return h.hexdigest()

def check(q):
    with codecs.open('proxies.txt', 'r') as f:
        proxies = f.readlines()
    while True:
        user = q.get()
        work = False
        s = requests.session()
        p = choice(proxies).strip()
        proxy = {
            'http': p,
            'https': p
        }
        headers = {'User-agent': 'Instagram 3.4.0 Android (10/2.3.3; 240dpi; 480x800; motorola; XT687; XT687; smdkc110; en_US)'}
        fields = urllib.urlencode({'{"username"': '"{0}"}'.format(user)})
        fields = fields.replace("=", "%3A")
        signed_body = 'signed_body=' + generate_signature('{"username":"{0}"}.{1}&ig_sig_key_version=4'.format(user, fields))
        response = requests.post("http://instagram.com/api/v1/users/check_username/", 
                                 signed_body, 
                                 verify=False,
                                 headers=headers, 
                                 proxies=proxy, 
                                 timeout=7.5)
        if '"available":false,' in response.text:
            work = True
        if work:
            print user, 'is registered!'
            f = open("Registered.txt", "a")
            f.write("{0}\n".format(user))
            f.close()
        q.task_done()
    
def main():
    with codecs.open('accounts.txt', 'r') as f:
        users = f.readlines()
        
    queue = Queue.Queue()
    
    for _ in range(15):
        worker = Thread(target=check, args=(queue,))
        worker.start()
    for user in users:
        queue.put(user.strip())
            
if __name__ == '__main__':
    main()