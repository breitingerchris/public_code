import random

def main():
	with open('first.txt', 'r') as f:
		first = f.readlines()
		
	with open('last.txt', 'r') as f:
		last = f.readlines()
	with open('names.txt', 'a+') as f:
		i = 0
		while i <= 1000:
			i +=1
			f.write(''.join(random.choice(first).strip() + random.choice(last).strip() + str(random.randint(1,63)) + '\r\n'))
		

	
if __name__ == '__main__':
	main()