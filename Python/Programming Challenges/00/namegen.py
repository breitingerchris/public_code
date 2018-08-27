import random

def main():
	with open('first.txt', 'r') as f:
		first = f.readlines()
		
	with open('last.txt', 'r') as f:
		last = f.readlines()
		
	print(random.choice(first).strip(), random.choice(last).strip())
	
if __name__ == '__main__':
	main()