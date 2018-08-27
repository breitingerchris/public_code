# -*- coding: utf-8 -*-
__author__ = 'Furry~'
import concurrent.futures
import requests
import requests.exceptions
import json
import Tkinter as Tk
import ttk
import uuid
import sys
import hmac
import hashlib
import urllib
import re
import string
import random
import Queue
import sys
import tkMessageBox
from datetime import datetime
from tkFileDialog import askopenfilename
from cookielib import CookieJar
from random import choice


class App():
    def __init__(self, parent):
        # Check To See If You Purchased c:
        # self.ownercheck()

        # Check To See If There's An Update
        # self.updatecheck()

        # Setup Window
        self.window = parent
        self.window.title("FurForce: Checker")
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_rowconfigure(3, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.minsize(250, 125)
        self.window.geometry('250x125')

        # Set Variables
        self.fileopenoptions = dict(defaultextension='.txt', filetypes=[('Text file', '*.txt'), ('All files', '*.*')])
        self.saveavailablenames = 0
        self.names = Tk.StringVar(self.window)
        self.proxies = Tk.StringVar(self.window)
        self.boxselections = Tk.StringVar(self.window)
        self.v = Tk.StringVar(self.window)
        self.gmailwarning = 0
        self.instawarning = 0
        self.kongrwarning = 0
        self.tumbrwarning = 0
        self.runeswarning = 0
        self.services = [
            'App.net',
            'Ask.fm',
            'Blogger',
            'Club Nintendo',
            'DeviantArt',
            'Domains',
            'Formspring',
            # 'Gmail',
            'Instagram',
            'Kongregate',
            'Last.fm',
            'League of Legends',
            'Likes',
            # 'Minecraft',
            'Major League Gaming',
            'Neopets',
            'Pastebin',
            'Pheed',
            'Reddit',
            'Roblox',
            'Runescape',
            'Soundcloud (Usernames)',
            'Soundcloud (PermaLinks)',
            'Spotify',
            'Steam',
            'Tinychat',
            'Tumblr',
            'Twitch',
            'Twitter',
            'UMGGaming',
            'YouTube'
        ]

        # Make Widgets
        self.scrollbar = Tk.Scrollbar(self.window)
        self.tree = ttk.Treeview(self.window, yscrollcommand=self.scrollbar.set, height=25, show='headings')
        self.tree["columns"] = (
            "Name",
            "Service"
        )
        self.tree.tag_configure('good', background='green')
        self.tree.tag_configure('bad', background='red')
        self.tree.column("Name", width=100)
        self.tree.column("Service", width=150)
        self.tree.heading("Name")
        self.tree.heading("Service")
        self.scrollbar.config(command=self.tree.yview)
        self.loadednames = Tk.Label(self.window, text="Names Loaded: 0")
        self.loadedproxies = Tk.Label(self.window, text="Proxies Loaded: 0")
        self.labelcombo = Tk.Label(self.window, text="Select Service: ")
        self.startbutton = Tk.Button(self.window, text="Start!", command=self.start)
        self.namebutton = Tk.Button(self.window, text="Open Name File!", command=self.setnames)
        self.proxybutton = Tk.Button(self.window, text="Open Proxy File!", command=self.setproxies)
        self.combobox = ttk.Combobox(self.window, textvariable=self.boxselections, state='readonly', height=25)

        # Set Combo List Items
        self.combobox['values'] = self.services
        self.combobox.current(0)

        # Place Widgets
        self.loadednames.grid(row=0, column=0, sticky=Tk.W)
        self.namebutton.grid(row=0, column=1, sticky=Tk.E)
        self.loadedproxies.grid(row=1, column=0, sticky=Tk.W)
        self.proxybutton.grid(row=1, column=1, sticky=Tk.E)
        self.labelcombo.grid(row=2, column=0, sticky=Tk.W)
        self.combobox.grid(row=2, column=1, columnspan=1, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.startbutton.grid(row=3, column=0, columnspan=2, sticky=Tk.W+Tk.E+Tk.N+Tk.S)

    def ownercheck(self):
        r = requests.get('http://checker.net63.net/hwid.php?hwid={0}'.format(str(uuid.getnode())),
                         proxies={})
        if 'truelikeurmum' in r.text:
            print "You own this c:!"
        else:
            print "You do not own this. Please go away :c!"
            sys.exit("ur poop")

    def updatecheck(self):
        r = requests.get('http://checker.net63.net/version.xml',
                         proxies={})
        if '3.0.0.0' in r.text:
            print "Up to date!"
        else:
            print "Please visit http://checker.net63.net/ to update"

    def setnames(self):
        filename = askopenfilename(**self.fileopenoptions)
        self.names.set(filename)
        with open(filename, 'r') as f:
            self.loadednames.config(text="Names Loaded: {0}".format(str(len(f.readlines()))))

    def setproxies(self):
        filename = askopenfilename(**self.fileopenoptions)
        self.proxies.set(filename)
        with open(filename, 'r') as f:
            self.loadedproxies.config(text="Proxies Loaded: {0}".format(str(len(f.readlines()))))

    def start(self):
        print 'tetst'
        global names
        if self.names.get() == '':
            print 'You didn\'t add any names!'
        else:
            f = open(self.names.get(), 'r')
            names = f.readlines()
            f.close()
        service = self.combobox.get()
        if self.proxies.get() == '':
            pass
        else:
            f = open(self.proxies.get(), 'r')
            global proxies
            proxies = f.readlines()
            f.close()
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            for name in names:
                if service == "App.net":
                    executor.submit(self.checkappnet, name)
                elif service == "Ask.fm":
                    executor.submit(self.checkaskfm, name)
                elif service == "Blogger":
                    executor.submit(self.checkblogger, name)
                elif service == "Club Nintendo":
                    executor.submit(self.checknintendo, name)
                elif service == "DeviantArt":
                    executor.submit(self.checkdeviantart, name)
                elif service == "Domains":
                    executor.submit(self.checkdomains, name)
                elif service == "Formspring":
                    executor.submit(self.checkformspring, name)
                elif service == "Gmail":
                    if self.gmailwarning == 0:
                        tkMessageBox.showwarning('Gmail Warning', 'Please Use Proxies That Are URL Passed By '
                                                                  'GatherProxy')
                        self.gmailwarning = 1
                    executor.submit(self.checkgmail, name)
                elif service == "Instagram":
                    if self.instawarning == 0:
                        tkMessageBox.showwarning('Instagram Warning', 'Please Use Proxies That Are URL Passed By '
                                                                      'GatherProxy')
                        self.instawarning = 1
                    executor.submit(self.checkinstagram, name)
                elif service == "Kongregate":
                    if self.kongrwarning == 0:
                        tkMessageBox.showwarning('Kongregate Warning', 'Please Use Proxies That Are URL Passed By '
                                                                       'GatherProxy')
                        self.kongrwarning = 1
                    executor.submit(self.checkkongregate, name)
                elif service == "Last.fm":
                    executor.submit(self.checklastfm, name)
                elif service == "League of Legends":
                    executor.submit(self.checklol, name)
                elif service == "Likes":
                    executor.submit(self.checklikes, name)
                elif service == "Minecraft":
                    executor.submit(self.checkminecraft, name)
                elif service == "Major League Gaming":
                    executor.submit(self.checkmlg, name)
                elif service == "Neopets":
                    executor.submit(self.checkneopets, name)
                elif service == "Pastebin":
                    executor.submit(self.checkpastebin, name)
                elif service == "Pheed":
                    executor.submit(self.checkpheed, name)
                elif service == "Reddit":
                    executor.submit(self.checkreddit, name)
                elif service == "Roblox":
                    executor.submit(self.checkroblox, name)
                elif service == "Runescape":
                    if self.runeswarning == 0:
                        tkMessageBox.showwarning('Runescape Warning', 'Please Use Proxies That Are URL Passed By '
                                                                       'GatherProxy')
                        self.runeswarning = 1
                    executor.submit(self.checkrunescape, name)
                elif service == "Soundcloud (Usernames)":
                    executor.submit(self.checksoundcloud, name)
                elif service == "Soundcloud (PermaLinks)":
                    executor.submit(self.checksoundcloudp, name)
                elif service == "Spotify":
                    executor.submit(self.checkspotify, name)
                elif service == "Steam":
                    executor.submit(self.checksteam, name)
                elif service == "Tinychat":
                    executor.submit(self.checktinychat, name)
                elif service == "Tumblr":
                    executor.submit(self.checktumblr, name)
                elif service == "Twitch":
                    executor.submit(self.checktwitch, name)
                elif service == "Twitter":
                    executor.submit(self.checktwitter, name)
                    time.sleep(0.5)
                elif service == "UMGGaming":
                    executor.submit(self.checkumg, name)
                elif service == "YouTube":
                    executor.submit(self.checkyoutube, name)

    def generate_signature(self, data):
        key = "b4a23f5e39b5929e0666ac5de94c89d1618a2916"
        h = hmac.new(key, '', hashlib.sha256)
        h.update(data)
        return h.hexdigest()

    def checkappnet(self, item):
        item = item.strip()
        data = {'value': item}
        headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0',
                   'X-CSRFToken': 'zGpoV5PJ9IKquTQasJ6oVw9AwdKHUJ32',
                   'Referer': 'https://join.app.net/signup',
                   'Cookie': 'csrftoken=zGpoV5PJ9IKquTQasJ6oVw9AwdKHUJ32'}
        work = True
        while work:
            try:
                r = requests.post('https://join.app.net/ajax/v1/validation/makana_username_check',
                                  data=data,
                                  headers=headers,
                                  verify=False)
                if not 'This username is already taken' in r.text:
                    print item, "is available for App.net!"
                    with open('Available App.net.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for App.net!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checkaskfm(self, item):
        item = item.strip()
        work = True
        while work:
            try:
                r = requests.get('http://ask.fm/users/check_username?login={0}'.format(item))
                if not 'already taken' in r.text:
                    print item, "is available for Ask.fm!"
                    with open('Available Askfm.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for Ask.fm!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checkblogger(self, item):
        item = item.strip()
        work = True
        while work:
            try:
                r = requests.get('http://{0}.blogspot.com'.format(item))
                if 404 == r.status_code:
                    print item, "is available for Blogger!"
                    with open('Available Blogger.txt', 'a') as f:
                        f.write('{0}.blogspot.com\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for Blogger!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checknintendo(self, item):
        item = item.strip()
        work = True
        while work:
            try:
                data = {'username': item}
                headers = {
                    'Referer': 'https://club.nintendo.com/registration.do;jsessionid=514968823CE41CF2E4AB46AB15D0D1FB'
                }
                r = requests.post('https://club.nintendo.com/api/account/validate/username',
                                  data=data,
                                  verify=False,
                                  headers=headers)
                if not item in r.text:
                    print item, "is available for Club Nintendo!"
                    with open('Available ClubNintendo.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for Club Nintendo!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checkdeviantart(self, item):
        item = item.strip()
        headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0',
                   'X-CSRFToken': 'zGpoV5PJ9IKquTQasJ6oVw9AwdKHUJ32',
                   'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                   'Referer': 'https://www.deviantart.com/join/?joinpoint=standard',
                   'Cookie': 'userinfo=__e136e2cb994765c4ac4b%3B%7B%22username%22%3A%22%22%2C%22uniqueid%22%3A%221bfb3'
                             '4ac7b6b6225939778787a8a9fd4%22%2C%22vd%22%3A%221401050699%2C1401050699%2C1401050699%2C1%'
                             '2C0%2C%2C1%2C0%2C1%2C1401050699%2C1401050699%2C0%2C0%2C0%2C0%2C4%22%7D; _ga=GA1.2.114334'
                             '899.1401050702; __qca=P0-1609614420-1401050701723'}
        work = True
        while work:
            try:
                r = requests.post('https://www.deviantart.com/global/difi/?',
                                  data='ui=__e136e2cb994765c4ac4b%3B%7B%22username%22%3A%22%22%2C%22uniqueid%22%3A%221b'
                                       'fb34ac7b6b6225939778787a8a9fd4%22%2C%22vd%22%3A%221401050699%2C1401050699%2C140'
                                       '1050699%2C1%2C0%2C%2C1%2C0%2C1%2C1401050699%2C1401050699%2C0%2C0%2C0%2C0%2C4%22'
                                       '%7D&c%5B%5D=%22User%22%2C%22usernameAvailable%22%2C%5B%22{0}%22%5D&t=jso'
                                       'n'.format(item),
                                  headers=headers,
                                  verify=False)
                if '"response":{"status":"SUCCESS","content":true}' in r.text:
                    print item, "is available for DeviantArt!"
                    with open('Available DeviantArt.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for DeviantArt!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checkdomains(self, item):
        item = item.strip()
        work = True
        while work:
            try:
                r = requests.get('http://freedomainapi.com/?key=kwgvk2dlnl&domain={0}'.format(item))
                js = json.loads(r.text)
                if js['available']:
                    print item, "is available for Domains!"
                    with open('Available Domains.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for Domains!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checkformspring(self, item):
        item = item.strip()
        work = True
        while work:
            try:
                headers = {'Referer': 'http://new.spring.me/'}
                data = {'username': item}
                r = requests.post('https://api.spring.me/register/checkusername/', data=data, verify=False,
                                  headers=headers)
                js = json.loads(r.text)
                if 'ok' in js['status']:
                    print item, "is available for Formspring!"
                    with open('Available Formspring.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for Formspring!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checkgmail(self, item):
        item = item.strip()
        work = True
        while work:
            proxy = choice(proxies)
            proxie = {
                'https': 'http://{0}'.format(proxy.strip()),
                'http': 'http://{0}'.format(proxy.strip())
            }
            try:
                r = requests.get(
                    'https://accounts.google.com/CheckAvailability?'
                    'Email={0}&'
                    'service=mail&'
                    'FirstName=FirstName&'
                    'LastName=LastName'.format(item),
                    verify=False,
                    proxies=proxie,
                    timeout=7.5)
                if '>is available<' in r.text:
                    print item, "is available for Gmail!"
                    with open('Available Gmail.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                    work = False
                elif 'Letters are not case-sensitive' in r.text:
                    print "Changing Proxies!"
                    work = True
                    proxies.remove(proxy)
                elif 'Error' in r.text:
                    print "Changing Proxies!"
                    work = True
                    proxies.remove(proxy)
                else:
                    print item, 'isn\'t available for Gmail!'
                    work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
                proxies.remove(proxy)
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True
                proxies.remove(proxy)
            except requests.exceptions.Timeout:
                print "Timeout Error!"
                work = True
                proxies.remove(proxy)

    def checkinstagram(self, item):
        item = item.strip()
        work = True
        while work:
            proxy = choice(proxies).strip()
            proxie = {
                'http': 'http://{0}'.format(proxy)
            }
            try:
                headers = {'User-agent': 'Instagram 3.4.0 Android (10/2.3.3; 240dpi; 480x800; motorola; XT68'
                                         '7; XT687; smdkc110; en_US)'}
                item = item.strip()
                fields = urllib.urlencode({'{"username"': '"%s"}' %item})
                fields = fields.replace("=", "%3A")
                signed_body = 'signed_body=' + self.generate_signature('{"username":"%s"}' % item) + '.' + \
                              fields + '&ig_sig_key_version=4'
                response = requests.post("http://instagram.com/api/v1/users/check_username/", signed_body, verify=False,
                                         headers=headers, proxies=proxie, timeout=7.5)
                if '"available":true,' in response.text:
                    print item + " is available for Instagram!"
                    with open("Available Instagram.txt", "a") as myfile:
                        myfile.write('{0}\n'.format(item))
                else:
                    print item + " isn't available for Instagram!"
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True
            except requests.exceptions.Timeout:
                print "Timeout Error!"
                work = True

    def checkkongregate(self, item):
        item = item.strip()
        work = True
        while work:
            try:
                headers = {
                    'Cookie': 'kong_svid=e8e72a72-8c68-4cc4-a6d6-7688a13c2443; _kongregate_session=BAh7C0kiD3Nlc3Npb25f'
                              'aWQGOgZFVEkiJWQ1NTYyMzI2NWEzMTUwNTFhODczODBjMDUyMDU3Y2FkBjsAVEkiCWluaXQGOwBGVEkiD3RyYW5z'
                              'bGF0b3IGOwBGRkkiEF9jc3JmX3Rva2VuBjsARkkiMUxPdXYrYkxvbHlLNlBSYVpENms2ZXFsMjB6WjIxa3pENXpY'
                              'MllQdDBrV2M9BjsARkkiEW9yaWdpbmFsX3VyaQY7AEYiH2h0dHA6Ly93d3cua29uZ3JlZ2F0ZS5jb20vSSIKZmxh'
                              'c2gGOwBUbzolQWN0aW9uRGlzcGF0Y2g6OkZsYXNoOjpGbGFzaEhhc2gJOgpAdXNlZG86CFNldAY6CkBoYXNoewY6'
                              'EnRyYWNraW5nX2NvZGVUOgxAY2xvc2VkRjoNQGZsYXNoZXN7BjsKSSJHL2FjY291bnRzL2NyZWF0ZV9lcnJvci91'
                              'c2VybmFtZSxwYXNzd29yZCxlbWFpbF9hZGRyZXNzLGJpcnRoX2RhdGUsBjsAVDoJQG5vdzA%3D--aaafb8784c53'
                              '3966283bca678e514fbeb297b1c9; sourced_visit_recorded=true; __utma=1.1153717640.140111800'
                              '2.1401118002.1401118002.1; __utmb=1.5.9.1401118031027; __utmc=1; __utmz=1.1401118002.1.1'
                              '.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __gads=ID=99eb06ed736322f2:T=1401118003:'
                              'S=ALNI_MYgvVF-F_ymVgQUmjbLHjlcknTZig; kong_flash_messages=%7B%22tracking_code%22%3A%22%2'
                              'Faccounts%2Fcreate_error%2Fusername%2Cpassword%2Cemail_address%2Cbirth_date%2C%22%7D; __'
                              'ar_v4=%7CWT26QJGCSRCB3DTS6L4C54%3A20140525%3A1%7CK4TGNDGRN5BBLEIDMF2Q6O%3A20140525%3A1%7'
                              'CIKQIDV5C7NGPXCUZIANR2X%3A20140525%3A1'
                }
                r = requests.get(
                    'http://www.kongregate.com/accounts/availability?username={0}'.format(item),
                    verify=False,
                    headers=headers,
                    timeout=7.5
                )
                if '"success":true' in r.text:
                    print item + " is available for Kongregate!"
                    with open("Available Kongregate.txt", "a") as myfile:
                        myfile.write('{0}\n'.format(item))
                else:
                    print item + " isn't available for Kongregate!"
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True
            except requests.exceptions.Timeout:
                print "Timeout Error!"
                work = True

    def checktumblr(self, item):
        item = item.strip()
        work = True
        proxy = choice(proxies)
        while work:
            proxie = {
                'https': 'http://{0}'.format(proxy)
            }
            try:
                header = {
                    'User-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2159.4 Safari/537.36',
                    'Cookie': 'tmgioct=541cdf42a6c7700438393370; anon_id=KCYTPLRYEAGDBGKUZMOEVQTLHWKSFUWK; devicePixelRatio=1; documentWidth=1920; _ga=GA1.2.1294977336.1411178308; __qca=P0-1711917068-1411178308561; pfs=PU4zvrZuFiAZNRlLxvh57eQ3Kro; __utma=189990958.1294977336.1411178308.1411178308.1411178308.1; __utmb=189990958.11.10.1411178308; __utmc=189990958; __utmz=189990958.1411178308.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
                    'Referer': 'https://www.tumblr.com/',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Accept-Encoding': 'gzip,deflate'
                }
                cook = requests.get('https://www.tumblr.com/', verify=False, proxies=proxie, headers=header)
                reg = re.search("\"form_key\" value=\"(.*?)\"", cook.text)
                print reg
                r = requests.post(
                    'https://www.tumblr.com/svc/account/register',
                    verify=False,
                    data='user%5Bemail%5D=tsest%40test.net&user%5Bpassword%5D=dsfdasfsfdasfasd&tumblelog%5Bname%5D={0}&user%5Bage%5D=&context=no_referer&version=STANDARD&follow=&form_key={1}&seen_suggestion=0&used_suggestion=0&used_auto_suggestion=0&action=signup_account&tracking_url=%2F&tracking_version=modal'.format(item, reg.groups()[0]),
                    proxies=proxie,
                    headers=header,
                    timeout=7.5
                )
                print r.text
                if not 'Someone has already claimed this username' in r.text:
                    print item, "is available for Tumblr!"
                    with open('Available Tumblr.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for Tumblr!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True
            except requests.exceptions.Timeout:
                print "Timeout Error!"
                work = True

    def checklastfm(self, item):
        item = item.strip()
        work = True
        while work:
            try:
                r = requests.get('http://www.last.fm/ajax/nametaken?username={0}'.format(item))
                if 'false' in r.text:
                    print item, "is available for Last.fm!"
                    with open('Available Lastfm.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for Last.fm!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checklol(self, item):
        item = item.strip()
        work = True
        while work:
            try:
                r = requests.get('http://www.lolking.net/search?region=NA&name={0}'.format(item), verify=False)
                if not 'summoner' in r.url:
                    print item, "is available for League of Legends!"
                    with open('Available League of Legends.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for League of Legends!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checklikes(self, item):
        item = item.strip()
        work = True
        while work:
            try:
                data = {
                    'ajax': 'true',
                    'email': '',
                    'name': '',
                    'password': '',
                    'age': '',
                    'gender': '',
                    'redirect_url': '%2F',
                    'error_redirect': '',
                    'token': '',
                    'referer_url': '',
                    'referral_code': '',
                    'signup_action': 'undefined',
                    'partner': '',
                    'invited': '',
                    'nickname': '{0}'.format(item)
                }
                r = requests.post('http://likes.com/api/signupprocess', data=data)
                if not 'That username is not available' in r.text:
                    print item, "is available for Likes!"
                    with open('Available Likes.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for Likes!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checkminecraft(self, item):
        item = item.strip()
        work = True
        while work:
            try:
                r = requests.get('https://account.minecraft.net/buy/frame/checkName/{0}'.format(item),
                                 verify=False)
                if 'OK' in r.text:
                    print item, "is available for Minecraft!"
                    with open('Available Minecraft.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for Minecraft!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checkmlg(self, item):
        item = item.strip()
        work = True
        while work:
            try:
                r = requests.get('https://accounts.majorleaguegaming.com/account/exists?login={0}'.format(item),
                                 verify=False)
                if '{"ok":true,"message":""}' in r.text:
                    print item, "is available for Majoy League Gaming!"
                    with open('Available MLG.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for  Majoy League Gaming!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checkneopets(self, item):
        item = item.strip().lower()
        work = True
        while work:
            try:
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Referer': 'http://www.neopets.com/signup/index.phtml'
                }
                r = requests.post('http://www.neopets.com/signup/ajax.phtml', 'method=checkAvailability&username='
                                                                              '{0}'.format(item),
                                  verify=False,
                                  headers=headers)
                if '"success":true' in r.text:
                    print item, "is available for Neopets!"
                    with open('Available Neopets.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for Neopets!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checkpastebin(self, item):
        item = item.strip()
        work = True
        while work:
            try:
                r = requests.get('http://pastebin.com/ajax/check_username.php', data='action=check_username&username={0'
                                                                                     '}'.format(item), verify=False)
                if 'Username OK!' in r.text:
                    print item, "is available for Pastebin!"
                    with open('Available Pastebin.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for Pastebin!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checkpheed(self, item):
        item = item.strip()
        work = True
        while work:
            try:
                r = requests.get('http://www.pheed.com/join/validate_url?url={0}'.format(item))
                js = json.loads(r.text)
                if js['valid']:
                    print item, "is available for Pheed!"
                    with open('Available Pheed.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for Pheed!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checkreddit(self, item):
        item = item.strip()
        work = True
        while work:
            try:
                r = requests.get('http://www.reddit.com/api/username_available.json?user={0}'.format(item))
                if 'true' in r.text:
                    print item, "is available for Reddit!"
                    with open('Available Reddit.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for Reddit!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checkroblox(self, item):
        item = item.strip()
        work = True
        while work:
            try:
                r = requests.get('http://www.roblox.com/UserCheck/checkifinvalidusernameforsignup?username={0}'.format(
                    item))
                if '0' in r.text:
                    print item, "is available for Roblox!"
                    with open('Available Roblox.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for Roblox!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checkrunescape(self, item):
        item = item.strip()
        work = True
        while work:
            proxy = choice(proxies).strip()
            proxie = {
                'http': 'http://{0}'.format(proxy)
            }
            try:
                r = requests.get(
                    'http://rscript.org/lookup.php?type=namecheck&name={0}'.format(item),
                    verify=False,
                    proxies=proxie,
                    timeout=7.5
                )
                if 'NAMECHECK: AVALIBLE' in r.text:
                    print item + " is available for Runescape!"
                    with open("Available Runescape.txt", "a") as myfile:
                        myfile.write('{0}\n'.format(item))
                else:
                    print item + " isn't available for Runescape!"
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True
            except requests.exceptions.Timeout:
                print "Timeout Error!"
                work = True

    def checksoundcloud(self, item):
        item = item.strip()
        work = True
        while work:
            try:
                r = requests.get('http://soundcloud.com/users/unique_username?user[username]={0}'.format(
                    item))
                if not 'false' in r.text:
                    print item, "is available for Soundcloud Username!"
                    with open('Available Soundcloud Username.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for Soundcloud Username!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checksoundcloudp(self, item):
        item = item.strip()
        work = True
        while work:
            try:
                r = requests.get('https://api.soundcloud.com/resolve?url=https%3A//soundcloud.com/{0}&_status_code_map['
                                 '302]=200&_status_format=json&client_id=b45b1aa10f1ac2941910a7f0d10f8e28&app_version=c'
                                 '55dc662'.format(item))
                if '404 - Not Found' in r.text:
                    print item, "is available for Soundcloud PermaLink!"
                    with open('Available Soundcloud PermaLink.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for Soundcloud PermaLink!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checkspotify(self, item):
        item = item.strip()
        work = True
        while work:
            try:
                r = requests.get('https://www.spotify.com/us/xhr/json/isUsernameAvailable.php?username={0}'.format(item)
                                 , verify=False)
                if not 'false' in r.text:
                    print item, "is available for Spotify!"
                    with open('Available Spotify.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for Spotify!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checksteam(self, item):
        item = item.strip()
        work = True
        while work:
            try:
                r = requests.get('http://soundcloud.com/users/unique_username?user[username]={0}'.format(item))
                if not 'false' in r.text:
                    print item, "is available for Steam!"
                    with open('Available Steam.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for Steam!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checktinychat(self, item):
        item = item.strip()
        work = True
        while work:
            try:
                r = requests.get('http://tinychat.com/api/usernameCheck.php?username={0}'.format(item))
                if '1' in r.text:
                    print item, "is available for Tinychat!"
                    with open('Available Tinychat.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for Tinychat!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checktwitch(self, item):
        item = item.strip()
        work = True
        while work:
            try:
                r = requests.get('https://api.twitch.tv/kraken/users/{0}'.format(item),
                                 verify=False)
                if r.status_code == 404:
                    print item, "is available for Twitch!"
                    with open('Available Twitch.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for Twitch!'
                work = False
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checktwitter(self, item):
        item = item.strip()
        work = True
        while work:
            try:
                r = requests.get('https://twitter.com/users/username_available?username={0}'.format(item),
                                 verify=False)
                js = json.loads(r.text)
                if 'Available!' in js['desc']:
                    print item, "is available for Twitter!"
                    with open('Available Twitter.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for Twitter!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checkumg(self, item):
        item = item.strip()
        work = True
        while work:
            try:
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
                }
                r = requests.post(
                    'http://www.umggaming.com/forminput.php?action=signup_username',
                    'username={0}'.format(item),
                    verify=False,
                    headers=headers
                )
                if '"valid":true' in r.text:
                    print item, "is available for UMGGaming!"
                    with open('Available UMGGaming.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for UMGGaming!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def checkyoutube(self, item):
        item = item.strip()
        work = True
        while work:
            try:
                r = requests.get('http://www.youtube.com/user_ajax?action_check_username=1&user={0}'.format(item))
                js = json.loads(r.text)
                if 'vailable' in js['username_status']:
                    print item, "is available for Youtube!"
                    with open('Available Youtube.txt', 'a') as f:
                        f.write('{0}\n'.format(item))
                        f.close()
                else:
                    print item, 'isn\'t available for Youtube!'
                work = False
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

if __name__ == "__main__":
    root = Tk.Tk()
    app = App(root)
    root.mainloop()