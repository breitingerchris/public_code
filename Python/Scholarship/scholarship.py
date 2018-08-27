import requests
import random
from threading import Thread

requests.packages.urllib3.disable_warnings()

def vote():
    while True:
        try:
            print 'Trying!'
            with open('proxies.txt', 'r') as f:
                p = f.readlines()
            prox = random.choice(p).strip()

            proxy = {
                'http': prox,
                'https': prox
            }
            s = requests.session()
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
                'Accept-Encoding': 'gzip',
                'Referer': 'https://www.wyzant.com/scholarships/Voting/134632'
            }
            r = s.get(
                        'https://www.wyzant.com/scholarships/Voting/134632',
                        verify=False,
                        headers=headers,
                        proxies=proxy
                    )

            with open('names.txt', 'r') as f:
                names = f.readlines()
            one = random.choice(names).strip()
            two = random.choice(names).strip()
            print one, two
            data = 'Voter.EssayId=134632&SubmittedEssayModel.FirstName=Chris&SubmittedEssayModel.StudentId=1646088&SubmittedEssayModel.Title=Self-Inspiration&Voter.FirstName={0}&Voter.Email={0}.{1}@mailinator.net&Voter.VoterType={2}'.format(
                one, two, random.randint(0, 4)
            )

            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            r = s.post(
                        'https://www.wyzant.com/Scholarships/Voting/134632',
                        data,
                        verify=False,
                        headers=headers,
                        proxies=proxy
                    )
            print 'Prolly worked!'
        except:
            print 'Error or something'
            pass


def main():
    for _ in range(57):
        worker = Thread(target=vote)
        worker.start()

if __name__ == '__main__':
    main()