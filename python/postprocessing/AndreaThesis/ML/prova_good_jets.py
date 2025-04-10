import ROOT
import math
import numpy as np
from array import array
ROOT.PyConfig.IgnoreCommandLineOptions = True
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event, InputTree
from PhysicsTools.NanoAODTools.postprocessing.tools import *

inFile_to_open = '/eos/user/a/apuglia/thesis/Datasets/nano_mcRun3_ttsl1_Prova.root'

rfile         = ROOT.TFile.Open(inFile_to_open)

tree          = InputTree(rfile.Get("Events"))

for i in range(tree.GetEntries()):
    event = Event(tree,i)
    # tree.GetEntry(i)
    jets = Collection(event, "Jet")
    fatjets = Collection(event, "FatJet")
    goodjets, goodfatjets  = presel(jets, fatjets)
    jets_pt, goodjets_pt = [], []
    jets_id = []
    goodjets_idx = []
    fatjets_pt, goodfatjets_pt = [],[]
    for index, jet in enumerate(jets):
        jets_pt.append(jet.pt)
        jets_id.append(jet.jetId)
        # print(index)
    
    print(jets_pt)
    
    print(jets_id)
    print('GOOD JETS')
    for good_jet in goodjets:
        goodjets_pt.append(good_jet.pt)
        goodjets_idx.append(good_jet.jetIdx)
        # print(good_jet.jetIdx)
    print(goodjets_pt)
    print(goodjets_idx)
    
    print('-------------FINE EVENTO ', i, '-----------------------')
    if i == 10:
        break

