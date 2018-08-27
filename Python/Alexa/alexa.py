import requests
import bs4
from threading import Thread
import Queue

def check(q):
    while True:
        domain = q.get()
        r = requests.get(
                    'http://data.alexa.com/data?cli=10&dat=s&url={0}'.format(domain),
                    verify=False
                )
        if 'REACH RANK=' in r.text:
            rank = bs4.BeautifulSoup(r.text, "xml").find("REACH")['RANK']
            with open('ranks.txt', 'a') as f:
                f.write(domain.strip() + " - " + rank + '\n')
            print domain + ' - ' + rank
        q.task_done()
            
            

    
def main():
    with open('domains.txt', 'r') as f:
        domains = f.readlines()
        
    queue = Queue.Queue()
    for _ in range(int(15)):
        worker = Thread(target=check, args=(queue,))
        worker.start()
    for d in domains:
        queue.put(d.strip())
        
if __name__ == '__main__':
    main()