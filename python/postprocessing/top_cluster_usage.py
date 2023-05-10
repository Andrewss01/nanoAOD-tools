import os
import sys
import ROOT
import math
from array import array
import numpy as np
import ROOT
import numpy as np
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
import pickle as pkl
import matplotlib.pyplot as plt
import mplhep as hep 
hep.style.use(hep.style.CMS)
ROOT.gROOT.SetBatch()

trs_file = open("/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/DNN_phase1_test/tresholds.pkl", "rb")
trs = pkl.load(trs_file)
trs10 = trs['fpr 10'] 
trs5 = trs['fpr 5']   
trs1 = trs['fpr 1']   
trs01 = trs['fpr 01']   
print(trs10, trs1, trs01)

trs_file_p2 = open("/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/DNN_phase2_test/tresholds.pkl", "rb")
trs_p2 = pkl.load(trs_file_p2)
trs10_p2 = trs_p2['fpr 10']
trs5_p2 = trs_p2['fpr 5']   
trs1_p2 = trs_p2['fpr 1']   
trs01_p2 = trs_p2['fpr 01'] 


folderIn= "/eos/home-a/acagnott/DarkMatter/topcandidate_file/"

inputfiles = ["tDM_mPhi1000_mChi1_Skim_Skim.root", 
              "QCD_HT1000_Skim.root",
              "TT_Mtt_700to1000_Skim_Skim.root"]#

variables = {d: {'n_cluster': [], 'ratio_clustovrtrs_clust': [], 'best_score': []} 
             for d in inputfiles}
#inputfile_bkg = "QCD_HT1000_Skim.root"#
cluster_perevent ={d: [] for d in inputfiles}
for infile in inputfiles:   
    inputfile = ROOT.TFile.Open(folderIn+infile)    #<---------------  InputFile
    tree = InputTree(inputfile.Get("Events"))
    nevents = tree.GetEntries()
    cluster_overtrs_ratio_  = []
    cluster_tot_ = []
    cluster_up_ = []
    cluster_best_score_ = []
    for i in range(nevents):
        event = Event(tree, i)
        jets = Collection(event,"Jet")
        fatjets = Collection(event,"FatJet")
        top = Collection(event, "Top")
        goodjets, goodfatjets = presel(jets, fatjets)
        ngoodjets, ngoodfatjets = len(goodjets), len(goodfatjets)
        if len(top)>0:
            top_list_fpr10 = get_top_over_trs(top, trs10)
            if len(top_list_fpr10)>0:
                out = top_cluster_excl(top, trs5)
                cluster_perevent[infile].append(len(out['n_cluster']))
                cluster_overtrs_ratio_.append(out['n_cluster_over_trs']/out['n_cluster'])
                cluster_tot_.append(out['n_cluster'])
                cluster_best_score_.append(out['best_score'])
                cluster_up_.append(out['n_up'])
    variables[infile]['n_cluster'] = [item for sublist in cluster_tot_ for item in sublist]
    variables[infile]['ratio_clustovrtrs_clust'] = [item for sublist in cluster_overtrs_ratio_ for item in sublist]
    variables[infile]['best_score'] = [item for sublist in cluster_best_score_ for item in sublist]
for infile in inputfiles:
    print(infile+ ' ' + str(np.mean(cluster_perevent[infile])))


with open("/eos/home-a/acagnott/DarkMatter/cluster_studies/variables.pkl", "wb") as file: 
    pkl.dump(variables, file)
