import os
import optparse
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *

usage = 'python Writer_outputFiles.py'
parser = optparse.OptionParser(usage)
parser.add_option('-d', '--dat', dest='dat', type=str, default = '', help='Please enter a dataset name')
(opt, args) = parser.parse_args()

def write(sample):
    infile = open("./macros/files/"+sample.label+"_.txt")
    strings = infile.readlines()
    outfile = open("./macros/files/"+sample.label+".txt", "w")
    for s in strings: 
        outfile.write(s.replace("root://cms-xrd-global.cern.ch/", "root://stormgf2.pi.infn.it/"))
    infile.close()
    outfile.close()
    os.remove("./macros/files/"+sample.label+"_.txt")

if not(opt.dat in sample_dict.keys()):
    print( sample_dict.keys())
dataset = sample_dict[opt.dat]

samples = []

if hasattr(dataset, 'components'): # How to check whether this exists or not
    samples = [sample for sample in dataset.components]# Method exists and was used.  
else:
    print("You are launching a single sample and not an entire bunch of samples")
    samples.append(dataset)

for sample in samples:
    print('Launching sample ' + sample.label)
    write(sample)
    