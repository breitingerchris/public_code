import codecs
import re

def main():
    with codecs.open('reddit.txt', 'r') as f:
        accounts = f.readlines()
    
    for account in accounts:
        account = account.strip()
        info = re.findall('(.*?) - Link: (.*?) - Comment: (.*?) - Date: (.*?)$', account)
        int1 = info[0][1].replace(',', '').replace(' ', '').replace('.', '')
        int2 = info[0][2].replace(',', '').replace(' ', '').replace('.', '')
        date = re.findall(' (\d{4,})$', account)
        if int(int1) >= 50000 or int(int2) >= 50000:
            with codecs.open('./lists/50k.txt', 'a') as f:
                f.write("{0}\n".format(account))
        elif int(int1) >= 25000 or int(int2) >= 25000:
            with codecs.open('./lists/25k.txt', 'a') as f:
                f.write("{0}\n".format(account))
        elif int(int1) >= 10000 or int(int2) >= 10000:
            with codecs.open('./lists/10k.txt', 'a') as f:
                f.write("{0}\n".format(account))
        elif int(int1) >= 5000 or int(int2) >= 5000:
            with codecs.open('./lists/5k.txt', 'a') as f:
                f.write("{0}\n".format(account))
        elif int(int1) >= 2000 or int(int2) >= 2000:
            with codecs.open('./lists/2k.txt', 'a') as f:
                f.write("{0}\n".format(account))
        elif int(int1) >= 1000 or int(int2) >= 1000:
            with codecs.open('./lists/1k.txt', 'a') as f:
                f.write("{0}\n".format(account))
        elif int(int1) >= 100 or int(int2) >= 100:
            with codecs.open('./lists/200.txt', 'a') as f:
                f.write("{0}\n".format(account))
        else:
            with codecs.open('./lists/non.txt', 'a') as f:
                f.write("{0}\n".format(info[0][0]))
    
    
    with codecs.open('sell list.txt', 'r') as f:
        sellz = f.readlines()
    
    one = []
    two = []
    five = []
    ten = []
    tfive = []
    fiveo = []
    th = []
    
    for account in sellz:
        account = account.strip()
        info = re.findall('(.*?) - Link: (.*?) - Comment: (.*?) - Date: (.*?)$', account)
        print info
        int1 = info[0][1].replace(',', '').replace(' ', '').replace('.', '')
        int2 = info[0][2].replace(',', '').replace(' ', '').replace('.', '')
        date = re.findall(' (\d{4,})$', account)
        if int(int1) >= 50000 or int(int2) >= 50000:
            fiveo.append('Link: {0} - Comment: {1} - Reg: {2}'.format(info[0][1], info[0][2], date[0]))
        elif int(int1) >= 25000 or int(int2) >= 25000:
            tfive.append('Link: {0} - Comment: {1} - Reg: {2}'.format(info[0][1], info[0][2], date[0]))
        elif int(int1) >= 10000 or int(int2) >= 10000:
            ten.append('Link: {0} - Comment: {1} - Reg: {2}'.format(info[0][1], info[0][2], date[0]))
        elif int(int1) >= 5000 or int(int2) >= 5000:
            five.append('Link: {0} - Comment: {1} - Reg: {2}'.format(info[0][1], info[0][2], date[0]))
        elif int(int1) >= 2000 or int(int2) >= 2000:
            two.append('Link: {0} - Comment: {1} - Reg: {2}'.format(info[0][1], info[0][2], date[0]))
        elif int(int1) >= 1000 or int(int2) >= 1000:
            one.append('Link: {0} - Comment: {1} - Reg: {2}'.format(info[0][1], info[0][2], date[0]))
        elif int(int1) >= 200 or int(int2) >= 200:
            th.append('Link: {0} - Comment: {1} - Reg: {2}'.format(info[0][1], info[0][2], date[0]))
                
    with codecs.open('sellable.txt', 'w') as f:
        f.write('')
                
    with codecs.open('sellable.txt', 'a') as f:
        f.write("50k - $25\n-----------------------------------------\n")
        for l in fiveo:
            f.write("{0}\n".format(l))
        f.write("-----------------------------------------\n\n\n")
        f.write("25k - $15\n-----------------------------------------\n")
        for l in tfive:
            f.write("{0}\n".format(l))
        f.write("-----------------------------------------\n\n\n")
        f.write("10k - $10\n-----------------------------------------\n")
        for l in ten:
            f.write("{0}\n".format(l))
        f.write("-----------------------------------------\n\n\n")
        f.write("5k - $5\n-----------------------------------------\n")
        for l in five:
            f.write("{0}\n".format(l))
        f.write("-----------------------------------------\n\n\n")
        f.write("2k - $2.50\n-----------------------------------------\n")
        for l in two:
            f.write("{0}\n".format(l))
        f.write("-----------------------------------------\n\n\n")
        f.write("1k - $0.50\n-----------------------------------------\n{0} Accounts".format(len(one)))

if __name__ == '__main__':
    main()