import requests
import json
import re

requests.packages.urllib3.disable_warnings()

headers = {
	'Cookie': 'user_prefs=WFZeWTt2MAjlcnK57hpYk4EeX05jZACCyMAFE2F0tFJosIuSjlJ6Yk5OalElkJWapxsaDKRBRF5pTo6OEYTCQsQyAAA.; etsy_guest_pass=TOOID2vFnM5JtCc3SZhSVhsVNxpjZACCyMAFE2F0tVKGklV0bC0DAA..; st-v1-1-1-_etsy_com=2%3Ad496230adc9307af4cee10575eaf0b4f0983dee5%3A1498521792%3A1498521792%3A4c80307b1a965695e1e4a07ce8c9e79045de6e0c186e406a646669faa9af34cf5bd69a59a76e3252; bc-v1-1-1-_etsy_com=2%3Af894a1ec95028eee8095331d3da87675ca900002%3A1498521792%3A1498521792%3A8bf3f1f4141bc5b1a92dc32532bef1866dae6bc91c6399847836d9415c4a90db1b1d591438bdac2a; LD=1; compat_test=aOdOFwoT; xsa=Jz1HEnHzWgoZO00Si4p8DIXncopjZACCyMAFB2F0tVJicklmfp6SlVJOfnpmnpKOUmlxalF8ZoqSlaWRqYWxqbmhDkQqviC1qDizuCQ1r0TJqqSoNLWWAQA.; perf=wf:1; last_browse_page=https%3A%2F%2Fwww.etsy.com%2Fshop%2FHolisticJewels; ua=531227642bc86f3b5fd7103a0c0b4fd6; fve=1498521745.0; uaid=uaid%3DaOdOFwoTQF7h-iRVcHxZlrXgbBeb%26_now%3D1498582234%26_slt%3DfsqR_i19%26_kid%3D1%26_ver%3D1%26_mac%3DpCUS_DnQShESPa6jz-N9KMAO6RFJ8Ec4uBeuJopb7oo.; et-v1-1-1-_etsy_com=2%3A186c23328af11fe9c667d118cc704c1cc1863b37%3A1498582234%3A1498582234%3A4c80307b1a965695e1e4a07ce8c9e79045de6e0c186e406a646669faa9af34cf5bd69a59a76e3252',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
	'X-CSRF-TOKEN': '3:1498582134:XxOEzonHqHw2Xe2P-gGRKUmH7XY0:bd00e5c99d875247267a2169d68bedf57ff2ec8e580ace9bd3810df6ce0319e0'
}

def image(url):
	img = requests.get(url, verify=False)
	headers['X-File-Type'] = 'image/jpeg'
	r = requests.post(
		'https://www.etsy.com/your/image/upload/listings',
		img.content,
		headers=headers, 
		verify=False
	)
	js = json.loads(r.text)
	return [js['image_id'], js['image_url'], js['url_340x270']]

def up(t, d, u, p):
	m = image(u)
	f = open('format.txt', 'r')
	l = f.read()
	f.close()
	f = open('a.txt', 'w')
	f.write(l.format(p, d, m[0], t, m[1], m[2]))
	f.close()
	headers['X-Requested-With'] = 'XMLHttpRequest'
	headers['Content-Type'] = 'application/json'
	r = requests.post(
		'https://www.etsy.com/api/v3/ajax/shop/14878625/listings',
		l.format(p, d, m[0], t, m[1], m[2]),
		headers=headers, 
		verify=False
	)
	print(r.text)
	
def main():
	f = open('scrape.txt', 'r')
	l = f.readlines()
	f.close()
	for i in l:
		up(i.split('@')[0], i.split('@')[1].replace('"', ''), i.split('@')[2], i.split('@')[3].strip())
			

	
main()
#format(price, desc, imgid, title, imgurl, imgurl2)