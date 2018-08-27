def toF(C):
	return C*1.8+32

def toC(F):
	return (F-32)/1.8

def main():
	print(toC(68.2))
	print(toF(30))

if __name__ == '__main__':
	main()