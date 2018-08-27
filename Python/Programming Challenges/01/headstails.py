import random

def main():
	int1 = random.randint(0, 9999)
	int2 = random.randint(0, 9999)
	if int1 >= int2:
		int = int2/int1
	else:
		int = int1/int2
	print(int)
	
	if int <= 0.5:
		print("Tails")
		return("Tails")
	else:
		print("Heads")
		return("Heads")
		
def count():
	heads = 1
	tails = 1
	count = 0
	while 1:
		if main() is "Tails":
			tails += 1
			count += 1
		else:
			heads += 1
			count += 1
		print("Heads Avg: ", (count/heads-1)/2)
		print("Tails Avg: ", (count/tails-1)/2)
		print("Tails: ", tails)
		print("Heads: ", heads)
		print("Count: ", count)
		
if __name__ == '__main__':
	count()