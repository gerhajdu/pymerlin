#!/usr/bin/env python2.7

import numpy as np
import pickle
from sys import argv, exit
from os import path

try:
    npzfile = np.load(path.dirname(__file__)+'/coefs_pca.npz')
    harmonic_coef_k = npzfile['k']
except:
    print "Coefficient file not found"
    exit()

try:
    clfs = pickle.load( open( path.dirname(__file__)+"/pymerlin-regressors.pkl", "rb" ))
except:
    print "pymerlin-regressors.pkl not found!"
    exit()

try:
    npzfile = np.load(path.dirname(__file__)+'/scaler_params.npz')
    scale   = npzfile['scale']
    mean    = npzfile['mean']
except:
    print "scaler_params.npz file not found"
    exit()

try:
    FILE = argv[1]
except:
    print "Usage: python",argv[0],"FILE_PATH"
    print "FILE_PATH: the path to the file containing the period and light-curve"
    print "The file must contain at least six columns, with the first six being:"
    print "1: the name of the variable"
    print "2: the period of the variable"
    print "3 - 6: the principal component amplitudes U1..U4 in the K-band"
    exit()

try:
    names, periods = np.loadtxt(FILE,
                              usecols=[0,1],
                              unpack=True,
                              dtype='|S30,<f8')
    Us = np.loadtxt(FILE,
                    usecols=[2,3,4,5],
                    unpack=True)
except:
    print "Error reading datafile; check format"
    exit()

def return_harmonic_amplitude(coefs2):
    return np.sqrt(coefs2[0]**2 + coefs2[1]**2)

def return_harmonic_phase(coefs2):
    return np.arctan2(-coefs2[0], coefs2[1])

def return_epoch_independent_phase_diff(phase_1, phase_n, n):
    return (phase_n - n * phase_1) % (2*np.pi)

for i in xrange(names.size):
    coefs = (Us[:,i]*harmonic_coef_k.T).T.sum(axis=0)

    A1 = return_harmonic_amplitude(coefs[0:2])
    A2 = return_harmonic_amplitude(coefs[2:4])
    A3 = return_harmonic_amplitude(coefs[4:6])

    phi1  = return_harmonic_phase(coefs[0:2])
    phi2  = return_harmonic_phase(coefs[2:4])
    phi3  = return_harmonic_phase(coefs[4:6])

    phi21 = return_epoch_independent_phase_diff(return_harmonic_phase(coefs[0:2]),
                                          return_harmonic_phase(coefs[2:4]), 2)
    phi21 = (phi21-np.pi) % (2*np.pi) + np.pi

    phi31 = return_epoch_independent_phase_diff(return_harmonic_phase(coefs[0:2]),
                                          return_harmonic_phase(coefs[4:6]), 3)
    phi31 = (phi31-np.pi) % (2*np.pi) + np.pi

    X     = ((np.asarray((periods[i],A1,A2,A3,phi21,phi31))-mean)/scale).reshape(1,-1)

    preds = np.zeros(len(clfs))
    for j in xrange(len(clfs)):
        preds[j] = clfs[j].predict(X)

    print '{:s} {:+3.3f} {:.3f} {:+3.3f} {:.3f}'.format(names[i],
                                                        preds.mean(), preds.std(),
                                                        (1.044*preds-0.037).mean(), (1.044*preds-0.037).std())



