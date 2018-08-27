import re
from time import gmtime, strptime

def main():
	age = input("Please Enter Birthdate (01/27/1998):")
	
	while not re.match('\d\d/\d\d/\d\d\d\d', age):
		age = input("Please Enter Birthdate (01/27/1998):")
	date = gmtime()
	age = strptime(age, "%m/%d/%Y")
	
	print("Age In Seconds:", ((date.tm_year - age.tm_year) * 365 + (date.tm_yday - age.tm_yday)) * 86400)
	
if __name__ == '__main__':
	main()