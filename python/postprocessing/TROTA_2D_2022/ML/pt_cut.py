# import numpy as np
seed_value= 0
import os
os.environ['PYTHONHASHSEED']=str(seed_value)
import random
random.seed(seed_value)
import numpy as np
np.random.seed(seed_value)
import os
import sys
import pickle as pkl
import ROOT
import json
import argparse


ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

inFile = '/eos/user/a/apuglia/Master_Thesis/pkls/training_dataset_1.pkl'

with open(inFile,'rb') as fpkl:
    dataset = pkl.load(fpkl)
components = dataset.keys()
categories = ['3j1fj', '3j0fj', '2j1fj']

print(f'components: {components}')


for c in components:
    for cat in categories: 
        print('prima del taglio component: ', c, ' category: ', cat, 'len 0', len(dataset[c][cat][0]), 'len 1: ', len(dataset[c][cat][1]), 'len 2: ', len(dataset[c][cat][2]), 
        'len 3: ',len(dataset[c][cat][3]), 'lent 4:', len(dataset[c][cat][4]), 'len 4:', len(dataset[c][cat][5]))
        top_values = dataset[c][cat][2]
        idx_todrop = []
        for idx_top in range(len(top_values)):

            if top_values[idx_top,2] <= 170:
                idx_todrop.append(idx_top)

        dataset[c][cat][0] = np.delete(dataset[c][cat][0], idx_todrop, axis = 0)
        dataset[c][cat][1] = np.delete(dataset[c][cat][1], idx_todrop, axis = 0)
        dataset[c][cat][2] = np.delete(dataset[c][cat][2], idx_todrop, axis = 0)
        dataset[c][cat][3] = np.delete(dataset[c][cat][3], idx_todrop, axis = 0)
        dataset[c][cat][4] = np.delete(dataset[c][cat][4], idx_todrop, axis = 0)
        dataset[c][cat][5] = np.delete(dataset[c][cat][5], idx_todrop, axis = 0)

        print('dopo del taglio component: ', c, ' category: ', cat, 'len 0', len(dataset[c][cat][0]), 'len 1: ', len(dataset[c][cat][1]), 'len 2: ', len(dataset[c][cat][2]), 
        'len 3: ',len(dataset[c][cat][3]), 'lent 4:', len(dataset[c][cat][4]), 'len 5:', len(dataset[c][cat][5]))
                
path_to_pkl = '/eos/user/a/apuglia/Thesis/pkls/training_dataset_1_ptcut.pkl'
if path_to_pkl is not None:
    print(path_to_pkl)
    with open(path_to_pkl, "wb") as f:
        pkl.dump(dataset, f)