from random import choice

with open('dictionary.txt', 'r') as f:
	words = f.readlines()

list = {}
	
for i in words:
	i = i.strip()
	if len(i) in list:
		list[len(i)].append(i)
	else:
		list[len(i)] = [i]
t = True	
while t:
	try:	
		i = raw_input('Enter a number between 1 and 28 that\'s not 26 or 27: ')
		t = True
		if int(i) >= 1 and int(i) <= 28 and int(i) is not 26 and int(i) is not 27 and not i.isalpha():
			i = int(i)
			t = False
	except:
		pass
		
word = choice(list[i])
guesses = 0
gword = []
for _ in xrange(i):
	gword.append('_')
lost = False
print 'Word:', ''.join(gword)
over = False
while not over:
	t = 0
	for a in xrange(i):
		if word[a].find(gword[a]) < 0:
			break
		else:
			t += 1
	if t is len(word):
		over = True
	elif guesses > 10:
		print "You lost! The word was:", word
		lost = True
		over = True
	else:
		g = raw_input('Please guess a single letter: ')
		t = True
		while t:
			if len(g) is not 1:
				g = raw_input('Please guess a SINGLE letter: ')
			elif not g.isalpha():
				g = raw_input('Please guess a single LETTER: ')
			else:
				t = False
		g = g.lower()
		if g in word:
			l = 0
			while gword.count(g) is not word.count(g):
				ind = word.find(g, l)
				l = ind + 1
				gword[ind] = g
			print 'Correct Guess!', ''.join(gword)
		else:
			print "Incorrect guess"
			print "Additional Guesses left: ", 10-guesses
			guesses += 1
if not lost:
	print 'You won!'