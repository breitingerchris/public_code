import requests

s = requests.session()
headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
	'Accept-Encoding': 'gzip',
	'Cookie': 'cid=om6fileu1nG0U-u1453467101; cid=om6fileu1nG0U-u1453467101; cmn=as0; cmn=as0'
}
x = [1,2,3,4,5,6,7,8,9,10,11,12]
y = [2017,2018,2019,2020,2021,2022,2023,2024,2025]
for a in y:
	for b in x:
		for c in xrange(1,31)
			r = s.get(
						'http://www.astro.com/cgi/hk.cgi?lang=e&fwnhor=1&btyp=hk0&hkdn=2&nhor=1&imonth=' + b + '&syear=' + a + '&day' + c + '.x=13',
						headers=headers
					)