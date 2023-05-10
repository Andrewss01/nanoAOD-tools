import ROOT
import numpy as np
import ROOT
import pickle as pkl
import matplotlib.pyplot as plt
import mplhep as hep
hep.style.use(hep.style.CMS)
import awkward as ak
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import os
from samples.samples import *
from coffea.analysis_tools import Weights


datasets = [QCD_2018, ZJetsToNuNu_2018, TT_2018,
            TprimeToTZ_1800_2018, TprimeToTZ_1000_2018, TprimeToTZ_700_2018]

folder_files = "../../crab/macros/files/"
lumi = 59.7*1000

def files_string(dat):
    folder_files = "../../crab/macros/files/"
    infile_string = open(folder_files+dat.label+".txt")
    strings = infile_string.readlines()
    for s in strings: s.replace('\n', '')
    return strings
    
def load_files(dat, strings):
    rfiles = []
    wes = []
    for s in strings:
        rfiles.append(NanoEventsFactory.from_root(
            s,
            schemaclass=NanoAODSchema.v6).events())
        infile = ROOT.TFile.Open(s)
        h_genweight = ROOT.TH1F(infile.Get("plots/h_genweight"))
        w=(dat.sigma*lumi/h_genweight)
        weights = Weights(len(rfiles[-1]))

        weights.add("genWeight", rfiles[-1].genWeight*w)
        wes.append(weights)
    return rfiles, wes

trees_bkg = {d: {s: 0 for s in d.components } for d in datasets if hasattr(d,"components")}
w_bkg = {d: {s: 0 for s in d.components } for d in datasets if hasattr(d,"components")}
trees_sgn = {d: 0 for d in datasets if not hasattr(d, "components")}
w_sgn = {d: 0 for d in datasets if not hasattr(d, "components")}

for d in datasets:
    print("Loading files for : ", d.label)
    if hasattr(d, "components"):
        for s in d.components:
            print(".... loading files for : ", s.label)
            strings = files_string(s)
            trees_bkg[d][s],  w_bkg[d][s] = load_files(s, strings)
            print("# files for "+s.label+" : ", len(trees_bkg[d][s]))

print(trees_bkg, w_bkg)
print(trees_bkg['QCD_2018']['QCDHT_700to1000_2018'][0].MinDelta.phi)
