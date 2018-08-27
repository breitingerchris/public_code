import requests
import json

with open('redurl.txt', 'r') as f:
	l = f.readlines()
	
for i in l:
	js = json.loads(i)['data']['children']
	for n in js:
		print(n['data']['title'])
		if len(n['data']['title']) <= 16:
			with open('./posts/{0}.txt'.format(n['data']['title']
			.replace('?', '')
			.replace('&amp;', 'AND')
			.replace('/r/', '')
			.replace('r/', '')
			), 'w+') as f:
				pass