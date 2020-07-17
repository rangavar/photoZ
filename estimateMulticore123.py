#reading the estimate.py, which is responsible for  estimating the photometric redshift on one cpu core (one object)
f = open('estimate.py','r')
lines = f.readlines()
f.close()

#producing multiple copies of the estimate.py to make it possible to run a multi-core version of the core (on 50 cores here, but you can change the number to use fewer/more cores)
for i in range(50):
	lines[11] = 'coreNumber = %s\n'%i #setting an ID-number to each core/each estimate code 
	f = open('%score.py'%i,'w')
	f.writelines(lines)
	f.close()
	
