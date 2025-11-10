import ROOT
from PhysicsTools.NanoAODTools.postprocessing.get_file_fromdas import *
import numpy as np 
from samples import *
from PhysicsTools.NanoAODTools.postprocessing.AndreaThesis.utilities.dataset import *

list_files = get_files_string(TT_hadr_2024,  option ='global')
# print(num_files)

# print(list_files)
file_0  = list_files[0] 
# print(file_0)
# file_0 = 'Zto2Nu-4Jets_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-ZJetsToNuNu_HT800to1500_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER'
file = ROOT.TFile.Open('root://cms-xrd-global.cern.ch//' + file_0, 'READ')

tree= file.Get('Events')
tree.Print('FatJetP*')
# tree.Print('Index*')