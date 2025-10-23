import ROOT  
import json
from PhysicsTools.NanoAODTools.postprocessing.get_file_fromdas import *
import numpy as np
# from ROOT.EColor import kP8AzurekP8Pink, kP8Red, kP8Green, kP8Blue, kP8Cyan, kP8Orange, kP8Grey

class sample:
    def __init__(self, color, style, fill, leglabel, label):
        self.color = color
        self.style = style
        self.fill = fill
        self.leglabel = leglabel
        self.label = label

# ci = ROOT.TColor.GetFreeColorIndex()
# color_azure = ROOT.TColor(ci, 0.53, 0.78, 0.87)
# QCD_HT70to100_2022.SetFillColor(ci) 
# color_azure = ROOT.TColor(azure_idx, 0.53 ,0.78, 0.87)
QCD_HT70to100_2022   = sample(ROOT.kAzure -4, 1, 1001, 'QCD_HT70to100_2022', 'QCD_HT70to100_2022')
QCD_HT70to100_2022.dataset = '/QCD-4Jets_HT-40to100_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT70to100_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER'
QCD_HT100to200_2022  = sample(ROOT.kAzure -4, 1, 1001, 'QCD_HT100to200_2022', 'QCD_HT100to200_2022')
QCD_HT100to200_2022.dataset = '/QCD-4Jets_HT-100to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT100to200_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER'
QCD_HT200to400_2022  = sample(ROOT.kAzure -4, 1, 1001, 'QCD_HT200to400_2022', 'QCD_HT200to400_2022')
QCD_HT200to400_2022.dataset = '/QCD-4Jets_HT-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT200to400_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER'
QCD_HT400to600_2022  = sample(ROOT.kAzure -4, 1, 1001, 'QCD_HT400to600_2022', 'QCD_HT400to600_2022')
QCD_HT400to600_2022.dataset = '/QCD-4Jets_HT-400to600_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT400to600_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER'
QCD_HT600to800_2022  = sample(ROOT.kAzure -4, 1, 1001, 'QCD_HT600to800_2022', 'QCD_HT600to800_2022')
QCD_HT600to800_2022.dataset = '/QCD-4Jets_HT-600to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT600to800_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER'
QCD_HT800to1000_2022 = sample(ROOT.kAzure -4, 1, 1001, 'QCD_HT800to1000_2022', 'QCD_HT800to1000_2022')
QCD_HT800to1000_2022.dataset = '/QCD-4Jets_HT-800to1000_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT800to1000_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER'
QCD_HT1000to1200_2022 = sample(ROOT.kAzure -4, 1, 1001, 'QCD_HT1000to1200_2022', 'QCD_HT1000to1200_2022')
QCD_HT1000to1200_2022.dataset = '/QCD-4Jets_HT-1000to1200_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT1000to1200_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER'
QCD_HT1200to1500_2022 = sample(ROOT.kAzure -4, 1, 1001, 'QCD_HT1200to1500_2022', 'QCD_HT1200to1500_2022')
QCD_HT1200to1500_2022.dataset = '/QCD-4Jets_HT-1200to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT1200to1500_2022_v2-0fa328e40e38f44cd311b92489b92b5b/USER'
QCD_HT1500to2000_2022 = sample(ROOT.kAzure -4, 1, 1001, 'QCD_HT1500to2000_2022', 'QCD_HT1500to2000_2022')
QCD_HT1500to2000_2022.dataset = '/QCD-4Jets_HT-1500to2000_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT1500to2000_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER'
QCD_HT2000_2022 = sample(ROOT.kAzure -4, 1, 1001, 'QCD_HT2000_2022', 'QCD_HT2000_2022')
QCD_HT2000_2022.dataset = '/QCD-4Jets_HT-2000_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-QCD_HT2000_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER'






TTZprimetoTT_3000_2022 = sample(ROOT.kAzure +7, 1, 1001, 'TTZprimetoTT_3000_2022', 'TTZprimetoTT_3000_2022')
TTZprimetoTT_3000_2022.dataset = '/TTZprimetoTT_M-3000_Width4_TuneCP5_13p6TeV_madgraph-pythia8/fsalerno-TTZprimetoTT_M_3000_W_4_2022-0fa328e40e38f44cd311b92489b92b5b/USER'
TT_inclusive_2022 = sample(ROOT.kViolet-6, 1, 1001, 'TT_inclusive_2022', 'TT_inclusive_2022')
TT_inclusive_2022.dataset = '/TT_TuneCP5_13p6TeV_powheg-pythia8/fsalerno-TT_inclusive_2022-0fa328e40e38f44cd311b92489b92b5b/USER'
TT_hadr_2022 = sample(ROOT.kTeal -5, 1, 1001, 'TT_hadronic_2022', 'TT_hadronic_2022')
TT_hadr_2022.dataset = '/TTto4Q_TuneCP5CR1_13p6TeV_powheg-pythia8/fsalerno-TT_hadronic_2022-0fa328e40e38f44cd311b92489b92b5b/USER'
TT_semilep_2022 = sample(ROOT.kTeal -5, 1, 1001, 'TT_semilep_2022', 'TT_semilep_2022')
TT_semilep_2022.dataset = '/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/fsalerno-TT_semilep_2022-0fa328e40e38f44cd311b92489b92b5b/USER'
TT_dilep_2022  = sample(ROOT.kMagenta -6,1,1001,'TT_dilep_2022','TT_dilep_2022')
TT_dilep_2022.dataset = '/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/apuglia-TTto2L2Nu_2022_v2-0fa328e40e38f44cd311b92489b92b5b/USER'


ZJetsto2Nu_HT100to200_2022 = sample(ROOT.kAzure, 1, 1001, 'ZJetsto2Nu_HT100to200_2022', 'ZJetsto2Nu_HT100to200_2022')
ZJetsto2Nu_HT100to200_2022.dataset = '/Zto2Nu-4Jets_HT-100to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-ZJetsto2Nu_HT100to200_2022_v2-0fa328e40e38f44cd311b92489b92b5b/USER'
ZJetsto2Nu_HT200to400_2022 = sample(ROOT.kAzure, 1, 1001, 'ZJetsto2Nu_HT200to400_2022', 'ZJetsto2Nu_HT200to400_2022')
ZJetsto2Nu_HT200to400_2022.dataset = '/Zto2Nu-4Jets_HT-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-ZJetsto2Nu_HT200to400_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER'
ZJetsto2Nu_HT1500to2500_2022 = sample(ROOT.kAzure, 1, 1001, 'ZJetsto2Nu_HT1500to2500_2022', 'ZJetsto2Nu_HT1500to2500_2022')
ZJetsto2Nu_HT1500to2500_2022.dataset = '/Zto2Nu-4Jets_HT-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_1500_2500_2022-0fa328e40e38f44cd311b92489b92b5b/USER'
ZJetsto2Nu_HT2500_2022 = sample(ROOT.kAzure, 1, 1001, 'ZJetsto2Nu_HT2500_2022', 'ZJetsto2Nu_HT2500_2022')
ZJetsto2Nu_HT2500_2022.dataset = '/Zto2Nu-4Jets_HT-2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_2500_inf_2022-0fa328e40e38f44cd311b92489b92b5b/USER'
ZJetsto2Nu_HT400to800_2022 = sample(ROOT.kAzure, 1, 1001, 'ZJetsto2Nu_HT400to800_2022', 'ZJetsto2Nu_HT400to800_2022')
ZJetsto2Nu_HT400to800_2022.dataset = '/Zto2Nu-4Jets_HT-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_400_800_2022-0fa328e40e38f44cd311b92489b92b5b/USER'
ZJetsto2Nu_HT800to1500_2022 = sample(ROOT.kAzure,1, 1001, 'ZJetsto2Nu_HT800to1500_2022', 'ZJetsto2Nu_HT800to1500_2022')
ZJetsto2Nu_HT800to1500_2022.dataset = '/Zto2Nu-4Jets_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/fsalerno-QCD_HT_800_1500_2022-0fa328e40e38f44cd311b92489b92b5b/USER'

WtoLNu_HT120to200_2022 = sample(ROOT.kRed -6,1, 1001, 'WtoLNu_HT120to200_2022', 'WtoLNu_HT120to200_2022')
WtoLNu_HT120to200_2022.dataset = '/WtoLNu-4Jets_MLNu-120to200_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-WtoLNu-4Jets_MLNu-120to200_v2-0fa328e40e38f44cd311b92489b92b5b/USER'
WtoLNu_HT200to400_2022 = sample(ROOT.kRed -6,1,1001, 'WtoLNu_HT200to400_2022','WtoLNu_HT200to400_2022' )
WtoLNu_HT200to400_2022.dataset = '/WtoLNu-4Jets_MLNu-200to400_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-WtoLNu-4Jets_MLNu-200to400_v2-0fa328e40e38f44cd311b92489b92b5b/USER'
WtoLNu_HT400to800_2022 = sample(ROOT.kRed -6, 1, 1001, 'WtoLNu_HT400to800_2022', 'WtoLNu_HT400to800_2022')
WtoLNu_HT400to800_2022.dataset = '/WtoLNu-4Jets_MLNu-400to800_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-WtoLNu-4Jets_MLNu-400to800_v2-0fa328e40e38f44cd311b92489b92b5b/USER'
WtoLNu_HT800to1500_2022 = sample(ROOT.kRed -6, 1, 1001, 'WtoLNu_HT800to1500_2022', 'WtoLNu_HT800to1500_2022')
WtoLNu_HT800to1500_2022.dataset = '/WtoLNu-4Jets_MLNu-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-WtoLNu-4Jets_MLNu-800to1500_v1-0fa328e40e38f44cd311b92489b92b5b/USER'
WtoLNu_HT1500to2500_2022 = sample(ROOT.kRed -6, 1, 1001, 'WtoLNu_HT1500to2500_2022', 'WtoLNu_HT1500to2500_2022')
WtoLNu_HT1500to2500_2022.dataset = '/WtoLNu-4Jets_MLNu-1500to2500_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-WtoLNu-4Jets_MLNu-1500to2500_v1-0fa328e40e38f44cd311b92489b92b5b/USER'
WtoLNu_HT2500to4000_2022 = sample(ROOT.kRed -6, 1, 1001, 'WtoLNu_HT2500to4000_2022', 'WtoLNu_HT2500to4000_2022')
WtoLNu_HT2500to4000_2022.dataset = '/WtoLNu-4Jets_MLNu-2500to4000_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-WtoLNu-4Jets_MLNu-2500to4000_v1-0fa328e40e38f44cd311b92489b92b5b/USER'
WtoLNu_HT4000to6000_2022 = sample(ROOT.kRed -6, 1, 1001, 'WtoLNu_HT4000to6000_2022', 'WtoLNu_HT4000to6000_2022')
WtoLNu_HT4000to6000_2022.dataset = '/WtoLNu-4Jets_MLNu-4000to6000_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-WtoLNu-4Jets_MLNu-4000to6000_v1-0fa328e40e38f44cd311b92489b92b5b/USER'
WtoLNu_HT6000_2022 = sample(ROOT.kRed -6, 1, 1001, 'WtoLNu_HT6000_2022', 'WtoLNu_HT6000_2022')
WtoLNu_HT6000_2022.dataset = '/WtoLNu-4Jets_MLNu-6000_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-WtoLNu-4Jets_MLNu-6000_v1-0fa328e40e38f44cd311b92489b92b5b/USER'


WtoLNu_4Jets_2022 = sample(ROOT.kRed -7 ,1,1001,'WtoLNu_4Jets_2022', 'WtoLNu_4Jets_2022')
WtoLNu_4Jets_2022.dataset = '/WtoLNu-4Jets_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-WtoLNu_4Jets_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER'

WtoLNu_4Jets_2J_2022 = sample(ROOT.kRed -7,1,1001,'WtoLNu_4Jets_2J_2022', 'WtoLNu_4Jets_2J_2022')
WtoLNu_4Jets_2J_2022.dataset = '/WtoLNu-4Jets_2J_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-WtoLNu_4Jets_2J_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER'

WtoLNu_4Jets_3J_2022 = sample(ROOT.kRed -7 ,1,1001,'WtoLNu_4Jets_3J_2022', 'WtoLNu_4Jets_3J_2022')
WtoLNu_4Jets_3J_2022.dataset = '/WtoLNu-4Jets_3J_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-WtoLNu_4Jets_3J_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER'

WtoLNu_4Jets_4J_2022 = sample(ROOT.kRed -7 ,1,1001,'WtoLNu_4Jets_4J_2022', 'WtoLNu_4Jets_4J_2022')
WtoLNu_4Jets_4J_2022.dataset = '/WtoLNu-4Jets_4J_TuneCP5_13p6TeV_madgraphMLM-pythia8/apuglia-WtoLNu_4Jets_2022-0fa328e40e38f44cd311b92489b92b5b/USER'

# file_to_save = '/afs/cern.ch/user/a/apuglia/CMSSW_14_1_7/src/PhysicsTools/NanoAODTools/python/postprocessing/samples/data_MC_2022.json' #cartella in cui vengono salvati i datasrt


TWminus_1L_2022 = sample(ROOT.kBlue -6 ,1, 1001, 'TWminus_1L_2022', 'TWminus_1L_2022')
TWminus_1L_2022.dataset = '/TWminus_DR_AtLeastOneLepton_TuneCP5_13p6TeV_powheg-pythia8/apuglia-TWminus_1L_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER'

TbarWplus_1L_2022 = sample(ROOT.kBlue -6,1,1001,'TbarWplus_1L_2022', 'TbarWplus_1L_2022')
TbarWplus_1L_2022.dataset = '/TbarWplus_DR_AtLeastOneLepton_TuneCP5_13p6TeV_powheg-pythia8/apuglia-TbarWplus_1L_2022_v1-0fa328e40e38f44cd311b92489b92b5b/USER'
# files = [QCD_HT400to600_2022, QCD_HT600to800_2022, QCD_HT800to1000_2022, QCD_HT1000to1200_2022, QCD_HT1200to1500_2022, QCD_HT1500to2000_2022, QCD_HT2000_2022,
#         TTZprimetoTT_3000_2022, TT_inclusive_2022, TT_hadronic_2022, TT_semilep_2022, 
#         ZJetsto2Nu_HT400to800_2022, ZJetsto2Nu_HT800to1500_2022, ZJetsto2Nu_HT1500to2500_2022, ZJetsto2Nu_HT2500_2022]



# with open(file_to_save) as data_file:
#     dataset = json.load(data_file)


# for d in files: 
#     if hasattr(d,'dataset'):
#         if d.label not in dataset.keys():

#             dataset[d.label] = {}  
#             list_strings = []

#             files_string = get_files_string(d)
#             list_num = list(np.zeros(len(files_string)))
#             for i, file in enumerate(files_string):
#                 if file != '':
#                     file = 'root://cms-xrd-global.cern.ch//' + file
#                     list_strings.append(file)
#                     # rfile = ROOT.TFile.Open(file, 'READ')
#                     # tree  = rfile.Get('Events')
#                     # list_num.append(tree.GetEntries())

#             dataset[d.label]['strings'] = list_strings
#             dataset[d.label]['num'] = list_num

# with open(file_to_save, 'w') as data_file:
#     json.dump(dataset, data_file, indent = 4)


        

