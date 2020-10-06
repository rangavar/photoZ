import matplotlib
matplotlib.use('Agg')
import numpy as np
import emcee
import h5py
import matplotlib.pyplot as plt
import pickle
import os
os.mkdir('dump')

fileName = 'noncorrectedMags'
nBands = 5
ndim = nBands
nwak = 20
nsteps = 100
objects = 500

#producing a new input file - only first object_number of objects
f = open('%s_original.txt'%fileName,'r')
lines = f.readlines()
f.close()
f = open('dump/%s.txt'%fileName,'w')
f.writelines(lines[0:objects])
f.close()

#defining the MCMC function
def log_prob(par,truth):
    for w in par:
        if w < -0.200 or w > 0.200:return np.NINF

    g_off = par[0]
    r_off = par[1]
    i_off = par[2]
    z_off = par[3]
    y_off = par[4]

    newFileName = '%1.5f_%1.5f_%1.5f_%1.5f_%1.5f' %(g_off,r_off,i_off,z_off,y_off)

    #reading the bpz .columns file to modify it with the new offsets
    f = open('%s.columns'%fileName,'r')
    lines = f.readlines()
    f.close()

    lines[1] = 'KiDSVIKING_g2         2, 3   AB        0.01     %s\n' %g_off
    lines[2] = 'KiDSVIKING_r2         4, 5   AB        0.01     %s\n' %r_off
    lines[3] = 'KiDSVIKING_i2         6, 7   AB        0.01     %s\n' %i_off
    lines[4] = 'KiDSVIKING_Z2         8, 9   AB        0.01     %s\n' %z_off
    lines[5] = 'KiDSVIKING_Y2        10,11   AB        0.01     %s\n' %y_off

    f = open('dump/%s.columns'%newFileName,'w')
    f.writelines(lines)
    f.close()

    os.system('python2.7 $BPZPATH/bpz.py dump/%s.txt -INTERP 2 -COLUMNS dump/%s.columns -OUTPUT dump/%s.bpz'%(fileName,newFileName,newFileName))

    f = open('plot.py','r')
    lines = f.readlines()
    f.close()
    lines[4] = 'fileName = \'dump/%s\'\n'%newFileName
    f = open('dump/plot_%s.py'%newFileName,'w')
    f.writelines(lines)
    f.close()

    os.system('python dump/plot_%s.py'%newFileName)

    f = open('dump/%s_outlier.txt'%newFileName,'r')
    lines = f.readlines()
    f.close()

    outlierFraction = float(lines[0].split()[3].split('\n')[0])

    diff = (outlierFraction - 0.0)
    return -0.5 * np.dot(diff, diff)

#starting value all random between -0.5 and 0.5
par0 = np.random.rand(nwak,ndim)*0.5 - 0.25

filename = "chain.h5"
backend = emcee.backends.HDFBackend(filename)
backend.reset(nwak, ndim)

from multiprocessing import Pool
#multiprocessing.cpu_count()

data = 0.0

with Pool() as pool:
    sampler = emcee.EnsembleSampler(nwak,ndim,log_prob,args=[data],pool=pool,backend=backend)
    pos, prob, stat = sampler.run_mcmc(par0,nsteps,progress=True)

#sampler = emcee.EnsembleSampler(nwak,ndim,log_prob,args=[data],backend=backend)
#state = sampler.run_mcmc(par0, nsteps)

np.save('pos.npy', pos)

#state = sampler.run_mcmc(par0,100)

samples = sampler.get_chain(flat=True)
walkerValues = []
error = []
for i in range(nBands):
    sample = samples[:,i]
    #sample = np.sort(sample)
    peak = sample[int(nwak*50./100.)]
    down = sample[int(nwak*16./100.)]
    up = sample[int(nwak*84./100.)]
    diff = np.abs(up-down)
    error.append(diff)
    walkerValues.append(peak)

bands = ['g','r','i','z','y']
plt.close()
for i in range(nBands):
    plt.hist((samples[:,i]),nwak,color="k",histtype="step")
    #plt.xscale('log')
    plt.savefig('%s_parameter.png'%bands[i])
    plt.close()
