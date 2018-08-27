from collections import Counter

with open('nums.txt', 'r') as f:
	l = f.read()
n = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
for i in l.split(' '):
	with open('lets.txt', 'a+') as f:
		l = f.write(n[int(i) - 88])
with open('lets.txt', 'r') as f:
	l = f.read()
print(Counter(l))