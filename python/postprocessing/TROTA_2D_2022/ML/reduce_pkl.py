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
from tqdm import tqdm 


ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)


usage = 'python3 reduce_pkl.py -i TT_hadr_2024'
parser = argparse.ArgumentParser(usage)
# parser.add_argument('-s', '--samples'   , dest = 'samples'   , required = True  )
parser.add_argument('-i', '--inDir'    , dest = 'inDir'    , required = True  )
# # parser.add_argument('-o', '--multiscore', dest = 'multiscore', required = True  )
# # parser.add_argument('-m', '--outModel'  , dest = 'outModel'  , required = False, default = './model_prova.h5' )
# # parser.add_argument('-j', '--outJson'   , dest = 'outJson'   , required = False)
# # parser.add_argument('-g', '--graphics'  , dest = 'graphics'  , required = False, default= './grafiche/model_prova')
# parser.add_argument('-v', '--verbose'   , dest = 'verbose'   , required = False, default = True )
# # parser.add_argument('-l', '--label'     , dest = 'label'     , required= True  )

args          = parser.parse_args()
# samples       = args.samples.split(',')
inDir        = args.inDir
# # outModel      = args.outModel
# # path_outJson  = args.outJson
# # path_graphics = args.graphics
# verbose       = args.verbose
# # multiscore    = args.multiscore
# # label         = args.label
verbose = True
path_pkls = '/eos/user/a/apuglia/Tprime/pkls/'+inDir+'/'

for fileName in os.listdir(path_pkls):

    inFile = path_pkls + fileName

    with open(inFile,'rb') as fpkl:
        dataset = pkl.load(fpkl)
    components = dataset.keys()
    categories = ['3j1fj', '3j0fj', '2j1fj']
    if verbose:
        print(f'components: {components}')

    components_todrop = []
    for c in components:
        for cat in categories:
            print('prima del taglio component: ', c, ' category: ', cat, 'len 0', len(dataset[c][cat][0]), 'len 1: ', len(dataset[c][cat][1]), 'len 2: ', len(dataset[c][cat][2]), 
            'len 3: ',len(dataset[c][cat][3]), 'lent 4:', len(dataset[c][cat][4]))
            if dataset[c][cat] == 0:
                components_todrop.append(c)
                break
    for c_todrop in components_todrop:
        dataset.pop(c_todrop)

    for c in components:
        for cat in categories: 
            idx_truetop  = [i for i,x in enumerate(dataset[c][cat][3] == 1) if x == True]
            idx_falsetop = [i for i,x in enumerate(dataset[c][cat][3] == 0) if x == True]

            # print('selezionando i top per: ', c, ' ', cat)
            # print('False tops: ', len(idx_falsetop), ' True tops: ', len(idx_truetop))

            if len(idx_truetop) == 0:
                print('NO TRUE TOPS')
                idx_todrop = random.sample(idx_falsetop, int(len(idx_falsetop)*(0.9)))
            elif len(idx_falsetop)>2*len(idx_truetop):
                idx_todrop = random.sample(idx_falsetop, len(idx_falsetop)-2*len(idx_truetop))
            else:
                idx_todrop = []

            dataset[c][cat][0] = np.delete(dataset[c][cat][0], idx_todrop, axis = 0)
            dataset[c][cat][1] = np.delete(dataset[c][cat][1], idx_todrop, axis = 0)
            dataset[c][cat][2] = np.delete(dataset[c][cat][2], idx_todrop, axis = 0)
            dataset[c][cat][3] = np.delete(dataset[c][cat][3], idx_todrop, axis = 0)
            dataset[c][cat][4] = np.delete(dataset[c][cat][4], idx_todrop, axis = 0)
            # dataset[c][cat][5] = np.delete(dataset[c][cat][5], idx_todrop, axis = 0)
            

            idx_truetop  = [i for i,x in enumerate(dataset[c][cat][3]==1) if x == True]
            idx_falsetop = [i for i,x in enumerate(dataset[c][cat][3]==0) if x == True]

            # print('selezionando i top per: ', c, ' ', cat)
            # print('False tops: ', len(idx_falsetop), ' True tops: ', len(idx_truetop))
            print('dopo del taglio component: ', c, ' category: ', cat, 'len 0', len(dataset[c][cat][0]), 'len 1: ', len(dataset[c][cat][1]), 'len 2: ', len(dataset[c][cat][2]), 
            'len 3: ',len(dataset[c][cat][3]), 'lent 4:', len(dataset[c][cat][4]))


    path_to_pkl = '/eos/user/a/apuglia/Tprime/pkls/training_dataset_pt_cut_600/' 

    if not os.path.exists(path_to_pkl):
        os.makedirs(path_to_pkl)
    print(path_to_pkl)
    with open(path_to_pkl + fileName, "wb") as f:
        pkl.dump(dataset, f)