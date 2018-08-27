import os
import fnmatch
import re

def findFiles (path, filter):
	for root, dirs, files in os.walk(path):
		for file in fnmatch.filter(files, filter):
			yield os.path.join(root, file)
			
for textFile in findFiles(r'D:\Cracking\Combos', '*.txt'):
		print textFile
		with open(textFile, 'r') as f:
			l = f.readlines()
		for a in l:
			n = re.findall('^([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}:.*?)$', a)
			if n:
				with open('emails.txt', 'a') as f:
					f.write(n[0] + "\n")