import re
import requests
import codecs
import random
import time

requests.packages.urllib3.disable_warnings()

class Satoshi(object):

    def __init__(self):
        global bet
        global url
        global mines
        global tiles
        global profit
        global rand
        global num
        global martingale
        global mbet
        global mode

        print 'Furz Satoshimine Bot'

        with codecs.open('settings.ini', 'r', encoding='utf-8') as f:
            info = f.readlines()
        for i in info:
            if 'url' in i:
                url = i.split('=')[1].strip()
            elif 'bet' in i:
                bet = i.split('=')[1].strip()
            elif 'mode' in i:
                mode = i.split('=')[1].strip()
            elif 'mines' in i:
                mines = i.split('=')[1].strip()
            elif 'random' in i:
                rand = i.split('=')[1].strip()
            elif 'tiles' in i:
                num = i.split('=')[1].strip()
            elif 'max' in i:
                mbet = i.split('=')[1].strip()

        tiles = list()
        while len(tiles) <= int(num) - 1:
            t = random.randint(0, 24)
            if t not in tiles:
                tiles.append(t)

    def start(self):
        if 'N' in mode:
            self.play()
        elif 'L' in mode:
            self.L()
        elif 'M' in mode:
            self.martingale()

    def play(self):
        profit = 0
        while True:
            s = requests.session()

            proxy = {
                'http': '127.0.0.1:8888',
                'https': '127.0.0.1:8888'
            }

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
                'Accept-Encoding': 'gzip'
            }

            r = s.get(
                url,
                verify=False,
                headers=headers,
                proxies=proxy
            )

            bdval = re.findall("bdval = '(.*?)'", r.text)[0]
            bal = re.findall('num".*?>(.*?)<', r.text)[0]
            hash = re.findall("playerhash = '(.*?)'", r.text)[0]
            data = 'bd={0}&player_hash={1}&bet={2:.6f}&num_mines={3}'.format(bdval, hash, float(int(bet) * 0.000001), bombs)

            print '----------------------------------'
            print '[+] Starting New Game!'
            print '[+] Current Profit:', profit, 'bits'
            print '[+] Balance:', bal

            headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
            headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            headers['Accept-Language'] = 'en-US,en;q=0.8'
            headers['Referer'] = url
            headers['X-Requested-With'] = 'XMLHttpRequest'

            r = s.post(
                'https://satoshimines.com/action/newgame.php',
                data,
                verify=False,
                headers=headers,
                proxies=proxy
            )
            if not 'error' in r.text:
                game = re.findall('game_hash":"(.*?)"', r.text)[0]

                print '[+] Current Bet:{0:.6f}'.format(float(int(bet) * 0.000001))

                if rand:
                    tiles = list()
                    while len(tiles) <= int(num) - 1:
                        t = random.randint(0, 24)
                        if t not in tiles:
                            tiles.append(t)
                for t in tiles:
                    t += 1
                    bomb = True
                    data = 'game_hash={0}&guess={1}&v04=1'.format(game, t)

                    r = s.post(
                            'https://satoshimines.com/action/checkboard.php',
                            data,
                            verify=False,
                            headers=headers,
                            proxies=proxy
                        )
                    if 'outcome":"bitcoins' in r.text:
                        print '[-] Tile', t, 'safe!'
                        bomb = False
                    elif 'outcome":"bomb' in r.text:
                        print '[-] Tile', t, 'bomb!'
                        break

                data = 'game_hash={0}'.format(game)

                if not bomb:
                    r = s.post(
                        'https://satoshimines.com/action/cashout.php',
                        data,
                        verify=False,
                        headers=headers,
                        proxies=proxy
                    )
                    if 'win' in r.text:
                        print re.findall('win":(.*?),', r.text)[0].split('e-')[0].replace('.', '').replace(',', '')
                        bits = int(re.findall('win":(.*?),', r.text)[0].split('e-')[0].replace('.', '').replace(',', ''))
                        profit += bits - int(bet)
                        print '[-] Won: +{0} bits'.format(bits)
                    else:
                        profit -= int(bet)
                        print '[-] Lost: -{0} bits'.format(int(bet))
            else:
                print '[!] Error!'

            print '----------------------------------\n'
            time.sleep(0.5)

    def L(self):
        obet = bet
        profit = 0
        while True:
            s = requests.session()

            proxy = {
                'http': '127.0.0.1:8888',
                'https': '127.0.0.1:8888'
            }

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
                'Accept-Encoding': 'gzip'
            }

            r = s.get(
                url,
                verify=False,
                headers=headers,
                proxies=proxy
            )

            bdval = re.findall("bdval = '(.*?)'", r.text)[0]
            bal = re.findall('num".*?>(.*?)<', r.text)[0]
            hash = re.findall("playerhash = '(.*?)'", r.text)[0]
            data = 'bd={0}&player_hash={1}&bet={2:.6f}&num_mines={3}'.format(bdval, hash, float(bet * 0.000001), mines)

            print '----------------------------------'
            print '[+] Starting New Game!'
            print '[+] Current Profit:', profit, 'bits'
            print '[+] Balance:', bal

            headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
            headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            headers['Accept-Language'] = 'en-US,en;q=0.8'
            headers['Referer'] = url
            headers['X-Requested-With'] = 'XMLHttpRequest'

            r = s.post(
                'https://satoshimines.com/action/newgame.php',
                data,
                verify=False,
                headers=headers,
                proxies=proxy
            )
            if not 'error' in r.text:
                game = re.findall('game_hash":"(.*?)"', r.text)[0]

                print '[+] Current Bet:{0:.6f}'.format(float(bet * 0.000001))

                tiles = [[1,6,11,16,21,22,23,24],[1,2,3,4,5,10,15,20]]
                for t in tiles[random.randint(0,1)]:
                    t += 1
                    bomb = True
                    data = 'game_hash={0}&guess={1}&v04=1'.format(game, t)

                    r = s.post(
                        'https://satoshimines.com/action/checkboard.php',
                        data,
                        verify=False,
                        headers=headers,
                        proxies=proxy
                    )
                    if 'outcome":"bitcoins' in r.text:
                        print '[-] Tile', t, 'safe!'
                        bomb = False
                    elif 'outcome":"bomb' in r.text:
                        print '[-] Tile', t, 'bomb!'
                        profit -= bet
                        print '[-] Lost: -{0} bits'.format(bet)
                        bet *= 1.12
                        break

                data = 'game_hash={0}'.format(game)
                if bomb:
                    bet = bet * 2
                elif bomb:
                    bet = obet
                    r = s.post(
                        'https://satoshimines.com/action/cashout.php',
                        data,
                        verify=False,
                        headers=headers,
                        proxies=proxy
                    )
                    if 'win' in r.text:
                        print re.findall('win":(.*?),', r.text)[0].split('e-')[0].replace('.', '').replace(',', '')
                        bits = int(re.findall('win":(.*?),', r.text)[0].split('e-')[0].replace('.', '').replace(',', ''))
                        profit += bits - bet
                        print '[-] Won: +{0} bits'.format(bits)
            else:
                print '[!] Error!'

            print '----------------------------------\n'
            time.sleep(0.5)

    def martingale(self):
        profit = 0
        loss = 0
        bet = 30
        mines = 3
        obet = 30
        while True:
            num = random.randint(2, 4)
            s = requests.session()

            proxy = {
                'http': '127.0.0.1:8888',
                'https': '127.0.0.1:8888'
            }

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
                'Accept-Encoding': 'gzip'
            }

            r = s.get(
                url,
                verify=False,
                headers=headers,
                proxies=proxy
            )

            bdval = re.findall("bdval = '(.*?)'", r.text)[0]
            bal = re.findall('num".*?>(.*?)<', r.text)[0]
            hash = re.findall("playerhash = '(.*?)'", r.text)[0]
            data = 'bd={0}&player_hash={1}&bet={2:.6f}&num_mines={3}'.format(bdval, hash, float(bet * 0.000001), mines)

            print '----------------------------------'
            print '[+] Starting New Game!'
            print '[+] Current Profit:', profit, 'bits'
            print '[+] Current Bet:{0:.6f}'.format(float(bet * 0.000001))
            print '[+] Balance:', bal
            print '[+] Mode: M' \
                  ''
            print '[+] Max Bet:', mbet

            headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
            headers['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
            headers['Accept-Language'] = 'en-US,en;q=0.8'
            headers['Referer'] = url
            headers['X-Requested-With'] = 'XMLHttpRequest'

            r = s.post(
                'https://satoshimines.com/action/newgame.php',
                data,
                verify=False,
                headers=headers,
                proxies=proxy
            )
            if not 'error' in r.text:
                game = re.findall('game_hash":"(.*?)"', r.text)[0]


                if rand:
                    tiles = list()
                    while len(tiles) <= int(num) - 1:
                        t = random.randint(0, 24)
                        if t not in tiles:
                            tiles.append(t)
                for t in tiles:
                    t += 1
                    bomb = False
                    data = 'game_hash={0}&guess={1}&v04=1'.format(game, t)

                    r = s.post(
                        'https://satoshimines.com/action/checkboard.php',
                        data,
                        verify=False,
                        headers=headers,
                        proxies=proxy
                    )
                    if 'outcome":"bitcoins' in r.text:
                        print '[-] Tile', t, 'safe!'
                    elif 'outcome":"bomb' in r.text:
                        print '[-] Tile', t, 'bomb!'
                        bomb = True
                        break

                data = 'game_hash={0}'.format(game)

                if bomb:
                    loss += 1
                    if loss == 1:
                        bet *= 2
                    elif loss == 3:
                        bet *= 2
                    elif loss == 7:
                        bet *= 2
                    elif loss == 15:
                        bet *= 2
                    elif loss == 31:
                        bet = obet
                        loss = 0
                else:
                    loss = 0
                    bet = obet
                    r = s.post(
                        'https://satoshimines.com/action/cashout.php',
                        data,
                        verify=False,
                        headers=headers,
                        proxies=proxy
                    )
                    if 'win' in r.text:
                        bits = int(
                            re.findall('win":(.*?),', r.text)[0].split('e-')[0].replace('.', '').replace(',', ''))
                        profit += bits - bet
                        print '[-] Won: +{0} bits'.format(bits)
                    else:
                        profit -= bet
                        print '[-] Lost: -{0} bits'.format(bet)
            else:
                print '[!] Error!'

            print '----------------------------------\n'
            time.sleep(0.5)


def main():
    cli = Satoshi()
    cli.start()

if __name__ == '__main__':
    main()