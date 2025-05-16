import ROOT  
import json
from PhysicsTools.NanoAODTools.postprocessing.get_file_fromdas import *
import numpy as np
class sample:
    def __init__(self, color, style, fill, leglabel, label):
        self.color = color
        self.style = style
        self.fill = fill
        self.leglabel = leglabel
        self.label = label


QCD_HT400to600_2022 = sample(ROOT.kGray, 1, 1001, 'QCD_HT400to600_2022', 'QCD_HT400to600_2022')
QCD_HT400to600_2022.dataset = '/QCD-4Jets_HT-400to600_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_400_600_2022-0fa328e40e38f44cd311b92489b92b5b/USER'
QCD_HT600to800_2022 = sample(ROOT.kGray, 1, 1001, 'QCD_HT600to800_2022', 'QCD_HT600to800_2022')
QCD_HT600to800_2022.dataset = '/QCD-4Jets_HT-600to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_600_800_2022-0fa328e40e38f44cd311b92489b92b5b/USER'
QCD_HT800to1000_2022 = sample(ROOT.kGray, 1, 1001, 'QCD_HT800to1000_2022', 'QCD_HT800to1000_2022')
QCD_HT800to1000_2022.dataset = '/QCD-4Jets_HT-800to1000_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_800_1000_2022-0fa328e40e38f44cd311b92489b92b5b/USER'
QCD_HT1000to1200_2022 = sample(ROOT.kGray, 1, 1001, 'QCD_HT1000to1200_2022', 'QCD_HT1000to1200_2022')
QCD_HT1000to1200_2022.dataset = '/QCD-4Jets_HT-1000to1200_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_1000_1200_2022-0fa328e40e38f44cd311b92489b92b5b/USER'
QCD_HT1200to1500_2022 = sample(ROOT.kGray, 1, 1001, 'QCD_HT1200to1500_2022', 'QCD_HT1200to1500_2022')
QCD_HT1200to1500_2022.dataset = '/QCD-4Jets_HT-1200to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_1200_1500_2022-0fa328e40e38f44cd311b92489b92b5b/USER'
QCD_HT1500to2000_2022 = sample(ROOT.kGray, 1, 1001, 'QCD_HT1500to2000_2022', 'QCD_HT1500to2000_2022')
QCD_HT1500to2000_2022.dataset = '/QCD-4Jets_HT-1500to2000_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_1500_2000_2022-0fa328e40e38f44cd311b92489b92b5b/USER'
QCD_HT2000_2022       = sample(ROOT.kGray, 1, 1001, 'QCD_HT2000_2022',       'QCD_HT2000_2022')
QCD_HT2000_2022.dataset = '/QCD-4Jets_HT-2000_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_2000_inf_2022-0fa328e40e38f44cd311b92489b92b5b/USER'

TTZprimetoTT_3000_2022 = sample(ROOT.kGreen, 1, 1001, 'TTZprimetoTT_3000_2022', 'TTZprimetoTT_3000_2022')
TTZprimetoTT_3000_2022.dataset = '/TTZprimetoTT_M-3000_Width4_TuneCP5_13p6TeV_madgraph-pythia8/fsalerno-TTZprimetoTT_M_3000_W_4_2022-0fa328e40e38f44cd311b92489b92b5b/USER'
TT_inclusive_2022 = sample(ROOT.kRed, 1, 1001, 'TT_inclusive_2022', 'TT_inclusive_2022')
TT_inclusive_2022.dataset = '/TT_TuneCP5_13p6TeV_powheg-pythia8/fsalerno-PFNanoAOD_TT_inclusive_2022-0fa328e40e38f44cd311b92489b92b5b/USER'
TT_hadronic_2022 = sample(ROOT.kRed, 1, 1001, 'TT_hadronic_2022', 'TT_hadronic_2022')
TT_hadronic_2022.dataset = '/TTto4Q_TuneCP5CR1_13p6TeV_powheg-pythia8/fsalerno-TT_hadronic_2022-0fa328e40e38f44cd311b92489b92b5b/USER'
TT_semilep_2022 = sample(ROOT.kRed, 1, 1001, 'TT_semilep_2022', 'TT_semilep_2022')
TT_semilep_2022.dataset = '/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/fsalerno-TT_semilep_2022-0fa328e40e38f44cd311b92489b92b5b/USER'

ZJetsto2Nu_HT1500to2500_2022 = sample(ROOT.kAzure, 1, 10001, 'ZJetsto2Nu_HT1500to2500_2022', 'ZJetsto2Nu_HT1500to2500_2022')
ZJetsto2Nu_HT1500to2500_2022.dataset = '/Zto2Nu-4Jets_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_1500_2500_2022-0fa328e40e38f44cd311b92489b92b5b/USER'
ZJetsto2Nu_HT2500_2022 = sample(ROOT.kAzure, 1, 1001, 'ZJetsto2Nu_HT2500_2022', 'ZJetsto2Nu_HT2500_2022')
ZJetsto2Nu_HT2500_2022.dataset = '/Zto2Nu-4Jets_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_2500_inf_2022-0fa328e40e38f44cd311b92489b92b5b/USER'
ZJetsto2Nu_HT400to800_2022 = sample(ROOT.kAzure, 1, 1001, 'ZJetsto2Nu_400to800_2022', 'ZJetsto2Nu_400to800_2022')
ZJetsto2Nu_HT400to800_2022.dataset = '/Zto2Nu-4Jets_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_400_800_2022-0fa328e40e38f44cd311b92489b92b5b/USER'
ZJetsto2Nu_HT800to1500_2022 = sample(ROOT.kAzure,1, 1001, 'ZJetsto2Nu_800to1500_2022', 'ZJetsto2Nu_800to1500_2022')
ZJetsto2Nu_HT800to1500_2022.dataset = '/Zto2Nu-4Jets_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_800_1500_2022-0fa328e40e38f44cd311b92489b92b5b/USER'



file_to_save = '/afs/cern.ch/user/a/apuglia/CMSSW_14_1_7/src/PhysicsTools/NanoAODTools/python/postprocessing/samples/data_MC_2022.json' #cartella in cui vengono salvati i datasrt



files = [QCD_HT400to600_2022, QCD_HT600to800_2022, QCD_HT800to1000_2022, QCD_HT1000to1200_2022, QCD_HT1200to1500_2022, QCD_HT1500to2000_2022, QCD_HT2000_2022,
        TTZprimetoTT_3000_2022, TT_inclusive_2022, TT_hadronic_2022, TT_semilep_2022, 
        ZJetsto2Nu_HT400to800_2022, ZJetsto2Nu_HT800to1500_2022, ZJetsto2Nu_HT1500to2500_2022, ZJetsto2Nu_HT2500_2022]



with open(file_to_save) as data_file:
    dataset = json.load(data_file)


for d in files: 
    if hasattr(d,'dataset'):
        if d.label not in dataset.keys():

            dataset[d.label] = {}  
            list_strings = []

            files_string = get_files_string(d)
            list_num = list(np.zeros(len(files_string)))
            for i, file in enumerate(files_string):
                if file != '':
                    file = 'root://cms-xrd-global.cern.ch//' + file
                    list_strings.append(file)
                    # rfile = ROOT.TFile.Open(file, 'READ')
                    # tree  = rfile.Get('Events')
                    # list_num.append(tree.GetEntries())

            dataset[d.label]['strings'] = list_strings
            dataset[d.label]['num'] = list_num

with open(file_to_save, 'w') as data_file:
    json.dump(dataset, data_file, indent = 4)


        

