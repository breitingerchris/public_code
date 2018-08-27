import soundcloud
import Tkinter as Tk
import requests.exceptions
import json
import os.path
import uuid
import sys
from random import choice
from random import randint


class App():
    def __init__(self, parent):

        # Check To See If You Purchased c:
        self.ownercheck()

        # Check To See If There's An Update
        self.updatecheck()

        # Setup Window
        self.window = parent
        self.window.title('FurForce: SoundCloud')
        self.window.minsize(200, 150)
        self.window.geometry('250x150')
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_rowconfigure(3, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)

        # Set Variables
        self.username = Tk.StringVar(self.window)
        self.password = Tk.StringVar(self.window)
        self.clientid = Tk.StringVar(self.window)
        self.clientsecret = Tk.StringVar(self.window)
        self.count = 0
        self.count1 = 0

        # Make Widgets
        self.labelusername = Tk.Label(self.window, text="Username: ")
        self.labelpassword = Tk.Label(self.window, text="Password: ")
        self.labelclientid = Tk.Label(self.window, text="Client ID: ")
        self.labelclientsecret = Tk.Label(self.window, text="Client Secret: ")
        self.entryusername = Tk.Entry(self.window, textvariable=self.username)
        self.entryppassword = Tk.Entry(self.window, textvariable=self.password, show="*")
        self.entryclientid = Tk.Entry(self.window, textvariable=self.clientid)
        self.entryclientsecret = Tk.Entry(self.window, textvariable=self.clientsecret)
        self.startbutton = Tk.Button(self.window, text="Start!", command=self.start)

        # Grid Widgets
        self.labelusername.grid(row=0, column=0, columnspan=1, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.labelpassword.grid(row=1, column=0, columnspan=1, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.labelclientid.grid(row=2, column=0, columnspan=1, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.labelclientsecret.grid(row=3, column=0, columnspan=1, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.entryusername.grid(row=0, column=1, columnspan=1, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.entryppassword.grid(row=1, column=1, columnspan=1, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.entryclientid.grid(row=2, column=1, columnspan=1, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.entryclientsecret.grid(row=3, column=1, columnspan=1, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.startbutton.grid(row=4, column=0, columnspan=2, sticky=Tk.W+Tk.E+Tk.N+Tk.S)

        if os.path.isfile('settings.json'):
            with open('settings.json', 'r') as f:
                config = json.load(f)
                self.entryusername.insert(0, config['username'])
                self.entryppassword.insert(0, config['password'])
                self.entryclientid.insert(0, config['clientid'])
                self.entryclientsecret.insert(0, config['clientsecret'])

    def ownercheck(self):
        r = requests.get('http://coinsgo.in/soundcloud.php?hwid={0}'.format(str(uuid.getnode())),
                         proxies={})
        if 'truelikeurmum' in r.text:
            print "You own this c:!"
        else:
            print "You do not own this. Please go away :c!"
            sys.exit("ur poop")

    def updatecheck(self):
        r = requests.get('http://coinsgo.in/soundcloud_version.xml',
                         proxies={})
        if '1.0.0.0' in r.text:
            print "Up to date!"
        else:
            print "Please visit http://coinsgo.in/SoundCloud.rar to download the update"

    def start(self):
        config = {
            'username': self.username.get(),
            'password': self.password.get(),
            'clientid': self.clientid.get(),
            'clientsecret': self.clientsecret.get()
        }
        with open('settings.json', 'w') as f:
            json.dump(config, f)
        try:
            global client
            client = soundcloud.Client(
                client_id=self.clientid.get(),
                client_secret=self.clientsecret.get(),
                username=self.username.get(),
                password=self.password.get()
            )
            print 'Welcome,', client.get('/me').username
            tracks = client.get('/tracks', limit=randint(225, 275), order='hotness')
            for _ in xrange(len(tracks)):
                track = choice(tracks)
                client.put('/me/favorites/{0}'.format(track.id))
                print 'Now liking:', track.id
        except requests.exceptions.HTTPError, error:
            if '401 Client Error: Unauthorized' in error:
                print 'Failed to authenticate, please check your settings!'

if __name__ == "__main__":
    root = Tk.Tk()
    app = App(root)
    root.mainloop()