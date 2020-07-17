import matplotlib
matplotlib.use('Agg')
import numpy
import matplotlib.pyplot as plot

#this is a very simple code for plotting purposes
f = open('../data.txt','r')
lines = f.readlines()
f.close()

names = []
specz = []
for line in lines[0:200]:
    line = line.split(' ')
    names.append(line[0])
    specz.append(float(line[-1]))

photoz = []
pdf = {}
for name in names:
    f = open('%sprob.txt'%name,'r')
    lines = f.readlines()
    f.close()

    pdf[name] = []
    
    photoz.append(float(lines[2]))

    for line in lines[4:]:
        pdf[name].append(float(line.split('\n')[0]))

top = []
bottom = []
for name in names:
    prob = []
    prob = pdf[name]
    
    sum = 0
    for p in prob:
        sum = sum + p
    
    down = sum * 0.16
    up = sum * 0.84
    newSum = 0
    for i in range(len(prob)):
        newSum = newSum + prob[i]
        if newSum > down:
            #bottom.append(1.+(i-2)*0.01)
	    bottom.append((i-2)*0.01)
            break
    
    newSum = 0
    for i in range(len(prob)):
        newSum = newSum + prob[i]
        if newSum > up:
            #top.append(1.+(i+1)*0.01)
            top.append((i+1)*0.01)
	    break
          

###This is for switching between maximum likelihood z and median.
photoz = []
for i in range(len(names)):
    photoz.append( (float(top[i])+float(bottom[i]))/2. )

zs_template = numpy.arange(0.0,5.0,0.01)

c = 0
for name in names:
    plot.plot(zs_template,pdf[name])
    plot.axvline(x=specz[c],c = 'red')
    #lot.axvline(x=top[c],linestyle = '--')
    #plot.axvline(x=bottom[c],linestyle = '--')
    plot.xlabel('photo-z',fontsize=15)
    plot.ylabel(r'$p(z|\{m_{\alpha}^{obs}\})$',fontsize=15)
    plot.savefig('%snew.eps'%name,format = 'eps',dpi = 1000)
    plot.close()
    c = c + 1

downe = []
upe = []
for i in range(len(names)):
    downe.append(abs(photoz[i]-bottom[i]))
    upe.append(abs(photoz[i]-top[i]))


x = numpy.arange(0.0,5.0,0.01)
y2=[]
y3=[]
for i in range(len(x)):
    m = 0.15*(1+x[i])+x[i]
    n = -0.15*(1+x[i])+x[i]
    y2.append(n)
    y3.append(m)

plot.xlabel('True Redshift',fontsize = 14)
plot.ylabel('Photo-z',fontsize = 14)
plot.errorbar(specz,photoz,yerr=[downe,upe],marker='.',linestyle="None",markerfacecolor="red")
plot.plot(x,x,color='green')
plot.plot(x,y2,linestyle = '--',color = 'red')
plot.plot(x,y3,linestyle = '--',color = 'red')



plot.savefig('wrap.eps',format='eps',dpi=1000)

outlier = []
error = []
for i in range(len(names)):
    error.append(abs(specz[i]-photoz[i])/(1.+specz[i]))
    if abs(specz[i]-photoz[i])/(1.+specz[i]) > 0.15:
    	outlier.append(names[i])

outlierFraction = float(float(len(outlier))/float(len(names)))
print(outlierFraction)
sortedError = numpy.sort(error)
print(sortedError[136])

lines = 'outlier fraction = %s\nfirst sigma = %s'%(outlierFraction,sortedError[136])

f = open('outlier.txt','w')
f.writelines(lines)
f.close()
