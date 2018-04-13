#!/usr/bin/env python

from __future__ import print_function
from builtins import range
import numpy as np
import pickle
from sys import argv, exit, version_info
from os import path

is_python3 = version_info >= (3, 0)

try:
    npzfile = np.load(path.dirname(__file__)+'/pymerlin_coefs.npz')
    harmonic_coef_k = npzfile['k']
except:
    print("pymerlin_coefs.npz not found")
    exit()

if is_python3:
    regressors_path = path.dirname(__file__)+"/pymerlin_regressors_py3.pkl"
else:
    regressors_path = path.dirname(__file__)+"/pymerlin_regressors_py2.pkl"

try:
    clfs = pickle.load( open(regressors_path, "rb" ))
except:
    print("pymerlin_regressors.pkl_py2(3).pkl not found!")
    exit()

try:
    npzfile = np.load(path.dirname(__file__)+'/pymerlin_scaler_params.npz')
    scale   = npzfile['scale']
    mean    = npzfile['mean']
except:
    print("pymerlin_scaler_params.npz not found!")
    exit()

try:
    FILE = argv[1]
except:
    print("Usage: python",argv[0],"FILE_PATH")
    print("FILE_PATH: the path to the file containing the period and light-curve")
    print("The file must contain at least six columns, with the first six being:")
    print("1: the name of the variable")
    print("2: the period of the variable")
    print("3 - 6: the principal component amplitudes U1..U4 in the K-band")
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
    print("Error reading datafile; check format")
    exit()

def return_harmonic_amplitude(coefs2):
    return np.sqrt(coefs2[0]**2 + coefs2[1]**2)

def return_harmonic_phase(coefs2):
    return np.arctan2(-coefs2[0], coefs2[1])

def return_epoch_independent_phase_diff(phase_1, phase_n, n):
    return (phase_n - n * phase_1) % (2*np.pi)

for i in range(names.size):
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
    for j in range(len(clfs)):
        preds[j] = clfs[j].predict(X)

    if is_python3:
        name = names[i].decode('utf-8')
    else:
        name = names[i]
    print('{:s} {:+3.3f} {:.3f} {:+3.3f} {:.3f}'.format(name, preds.mean(), preds.std(),
                                                        (1.044*preds-0.037).mean(), (1.044*preds-0.037).std()))
