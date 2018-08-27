import os
import re

for file in os.listdir("./combos"):
	print file
	if file.endswith(".txt"):
		l = open("./combos/{0}".format(file), "r")
		c = l.readlines()
		l.close()
		for a in c:
			if ':' in a:
				f = open('./pass.txt', "a")
				f.write('{0}\n'.format(a.split(':')[1].strip()))
				f.close()

print 'done'