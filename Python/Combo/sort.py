import os
import re

for file in os.listdir("./combos"):
	print file
	results = []
	if file.endswith(".txt"):
		l = open("./combos/{0}".format(file), "r")
		c = l.readlines()
		l.close()
		for a in c:
			if len(results) >= 1000:
				results = []
			a = re.sub('@.*:', ':', a)
			if ':' not in a and '	' in a:
				a = a.replace('	', ':')
			if a.split(':')[0] not in ''.join(results):
				results.append(a)
				r = a.strip()
				f = open('./combos.txt', "a")
				f.write('{0}\n'.format(r))
				f.close()

print 'done'