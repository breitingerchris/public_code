import requests
import Queue
import codecs
import json
import random
import re
import time
import subprocess
from threading import Thread

requests.packages.urllib3.disable_warnings()

x = -124.05555
y = 45.5555
queue = Queue.Queue()

with codecs.open('accounts.txt', 'r', encoding='utf-8') as f:
	accounts = f.readlines()

def search():
	user = random.choice(accounts).strip()
	location = queue.get()
	p = subprocess.Popen(["runserver.py -a ptc -u {0} -p playtime2 -l {1} -t 25 -st 15 -k AIzaSyDx9vCLksk63kkufcUM5xbi7ayTv1BNqlk".format(user, location)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	time.sleep(305)
	p.kill()
	with open("done.txt", "a") as f:
		f.write('{0}\n'.format(location))
		f.close()
	queue.task_done()
	
if __name__ == '__main__':
	while y >= 43:
		y -= 0.05
		x = -124.05555
		while x <= -70:
			queue.put(str(y) + "," + str(x))
			x += 0.05
	for _ in range(5):
		worker = Thread(target=search, args=())
		worker.start()
	#main()