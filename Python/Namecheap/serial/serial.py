import string
import random

f = open("data.txt", "w")
f.write(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(32)))
f.close()