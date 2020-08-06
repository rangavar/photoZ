import matplotlib
matplotlib.use('Agg')
import numpy as np
import os
import h5py
import operator
import pickle
import random
import matplotlib.pyplot as plot

nsim = 4 #sets the number of objects ran on each cpu core: here 4. means it is going to estimate the photometric redshift for 4 objects on this core
coreNumber = 0 #set an ID-number to the core, for future identification purposes

#Setting the grid points which are going to be used to estimate the likelihood of redshift in the future
tn_template = np.arange(0.,7.,0.001) #producing the tn grids with required resoultion 0.001.
zs_template = np.arange(0.,5.,0.01) #producing the zs grids with required resoultion 0.001. For this experiment .01 is enough resolution on redshift

#loading the photometry templates, which are previously produced and saved as .pickle. Multi-band photometry template can be parametrized with only two parameters: spectroscopic redshift (zs) and template number (tn). Saving them in templateScale
templateScale = {}
for i in range(50):
    with open('%stemplatez01t001.pickle'%i, 'rb') as handle:
        templateScale.update(pickle.load(handle))

#loading each band's magnitude and its corresponding error for each object, also reading spectroscopic redshift for future comparison and plotting
f = open('data.txt','r')
lines = f.readlines()
f.close()

#defining the photometry bands and their magnitudes, and each magnitudes uncertainty
filtnames = {}
source_mags = {}
scatter_sig = {}
bands = ('g', 'r', 'i', 'z', 'y')
zp = {}
for band in bands:
    filtnames[band] = 'HSC-%s.txt'%band
    source_mags[band] = np.zeros(nsim) #mags
    scatter_sig[band] = np.zeros(nsim) #uncertainties
    zp[band] = 27. #defining the zero point magnitude

name = [] #ID
specz = [] #spectroscopic redshift 
n = 0
for i in range(coreNumber*nsim,(coreNumber+1)*nsim):
    name.append(lines[i].split(' ')[0])

    source_mags['g'][n] = float(lines[i].split(' ')[1])
    source_mags['r'][n] = float(lines[i].split(' ')[3])
    source_mags['i'][n] = float(lines[i].split(' ')[5])
    source_mags['z'][n] = float(lines[i].split(' ')[7])
    source_mags['y'][n] = float(lines[i].split(' ')[9])

    scatter_sig['g'][n] = float(lines[i].split(' ')[2])
    scatter_sig['r'][n] = float(lines[i].split(' ')[4])
    scatter_sig['i'][n] = float(lines[i].split(' ')[6])
    scatter_sig['z'][n] = float(lines[i].split(' ')[8])
    scatter_sig['y'][n] = float(lines[i].split(' ')[10])

    specz.append(float(lines[i].split(' ')[11]))
    n = n + 1

#defining chi squared
def xaiSquared(mObserved,tScale,b):
    y = ( mObserved + 2.5*np.log10(tScale) + 2.5*np.log10(b) )**2.
    return y

#define probability from xai2
def prob(xai):
    p = np.exp( -xai/2. )
    return p

#minimizing chi2 over scattered points 
maxL = {}
xaiCatalogue = {}
for n in range(nsim):

    for z in range(len(zs_template)):

        print(zs_template[z])

        for t in range(len(tn_template)): #marginalizing over tn: marginalizing over template number. this is the parameter we are not interested in, so we marginalize over it to achieve a probability distribution for redshift

            up = 0.
            down = 0.

            for band in bands:
                #finding the sums of observed fluxes and template fluxes
                up  = up + (source_mags[band][n] + 2.5*np.log10(templateScale['%s %s %s'%(band,t,z)]))/(scatter_sig[band][n]**2.)
                down = down + 1./(scatter_sig[band][n]**2.)

            #minimizing over normalization factor
            b = 10.**(-up/(2.5*down))
            #print(b)

            sumXaiOverBands = 0.
            for band in bands:
                xai = xaiSquared(source_mags[band][n],templateScale['%s %s %s'%(band,t,z)],b)/(scatter_sig[band][n]**2.)
                sumXaiOverBands = sumXaiOverBands + xai

            xaiCatalogue['%s %s'%(z,t)] = sumXaiOverBands

    minXai = min(xaiCatalogue.values())

    pZ = {}

    for z in range(len(zs_template)):

        sumPOverTN = 0.

        for t in range(len(tn_template)):

            p = prob(xaiCatalogue['%s %s'%(z,t)]-minXai)
            sumPOverTN = sumPOverTN + p

        pZ['%.2f'%(zs_template[z])] = sumPOverTN

    maxL['%s'%n] = max(pZ.items(), key=operator.itemgetter(1))[0]

    probs = []
    probSum = 0.
    for i in range(len(zs_template)):
        #plot.scatter( zs_template[i] , pZ['%.2f'%zs_template[i]] )
        probs.append( pZ['%.2f'%zs_template[i]] )
        probSum = probSum + pZ['%.2f'%zs_template[i]]

    for i in range(len(zs_template)):
        probs[i] = probs[i] * (1./probSum)

    plot.plot(zs_template,probs)
    plot.axvline(x=specz[n])
    plot.xlabel('z')
    plot.ylabel('p')
    plot.savefig('probPlots/%s.png'%name[n])
    plot.close()

    lines = []
    lines.append('specz maxL probs\n')
    lines.append('%s\n'%specz[n])
    lines.append('%s\n\n'%maxL['%s'%n])
    for i in range(len(probs)):
        line = '%s\n'%probs[i]
        lines.append(line)

    f = open('probPlots/%sprob.txt'%name[n],'w')
    f.writelines(lines)
    f.close()

#saving dictionaries
with open('outputs/%smaxL.pickle'%coreNumber, 'wb') as handle:
    pickle.dump(maxL, handle, protocol=pickle.HIGHEST_PROTOCOL)
