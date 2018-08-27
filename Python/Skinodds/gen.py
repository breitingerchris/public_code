import string
ul = string.ascii_lowercase + string.ascii_uppercase

fi = open("alpha.txt", "a")
mmm = []
for a in ul:
	for b in ul:
		for c in ul:
			for d in ul:
				for e in ul:
					for f in ul:
						for g in ul:
							for h in ul:
								for i in ul:
									for j in ul:
										fi.write('{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}'.format(a,b,c,d,e,f,g,h,i,j))
										


fi.close()