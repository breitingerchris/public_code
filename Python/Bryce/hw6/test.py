def checkSymbols(l):
	symbols = "!,?.;:'\"$#[]*="
	for i in symbols:
		l = l.replace(i, '')
	n = []
	if '-' in l:
		n = l.split('-')
	elif '(' in l and ')' in l:
		n = [l.split('(')[1].replace(')', '')]
	elif '((' in l:
		n = [l.split('(')[1].replace(')', '')]
	elif '(' in l:
		n = [l.split('(')[1]]
	elif ')' in l:
		n = [l.split(')')[0]]
	elif l.isdigit():
		n = []
	else:
		n = [l]
		
	return n
	
	

def main():
	wap = []
	stopWordDict = []
	wordConcordanceDict = {}
	
	with open('stop_words.txt', 'r') as f:
		stopWordDict = f.read()
	
	with open('WarAndPeace.txt', 'r') as f:
		wap = f.readlines()
	i = 0
	
	while i < len(wap):
		for l in wap[i].split(' '):
			l = checkSymbols(l.strip().lower())
			for a in l:
				if a not in stopWordDict:
					if a in wordConcordanceDict:
						wordConcordanceDict[a] += ' ' + str(i + 1)
					else:
						wordConcordanceDict[a] = str(i + 1)
		i += 1
	with open('out.txt', 'a') as f:
		for key in sorted(wordConcordanceDict.iterkeys()):
			f.write(key + ': ' + wordConcordanceDict[key] + "\n")
		
	
if __name__ == '__main__':
	main()