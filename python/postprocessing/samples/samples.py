import ROOT
import os
#import json_reader as jr

path = os.path.dirname(os.path.abspath(__file__))

class sample:
    def __init__(self, color, style, fill, leglabel, label):
        self.color = color
        self.style = style
        self.fill = fill
        self.leglabel = leglabel
        self.label = label

#da controllare i tag aggiungere la QCD

tag_2016 = 'RunIISummer16NanoAODv7-PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8'
tag_2017 = 'RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_102X_mc2017_realistic_v8'
tag2_2017 = 'RunIIFall17NanoAODv7-PU2017_12Apr2018_Nano02Apr2020_new_pmx_102X_mc2017_realistic_v8'
tag_2018 = 'RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21'

################################ WJets ################################
altXSUp=0
kFactorsQCD={
    "WJetsHT100to200" : 1.21,
    "WJetsHT200to400" : 1.21,
    "WJetsHT400to600" : 1.21,
    "WJetsHT600to800" : 1.21,
    "WJetsHT800to1200" : 1.21,
    "WJetsHT1200to2500" : 1.21,
    "WJetsHT2500toInf" : 1.21
}

###############################################################################################################################
##########################################                                           ##########################################
##########################################                    2018                   ##########################################
##########################################                                           ##########################################
###############################################################################################################################

################################ QCD ################################
QCDHT_100to200_2018         = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_100to200_2018")
QCDHT_100to200_2018.sigma   = 27990000 #23590000 #pb
QCDHT_100to200_2018.year    = 2018
QCDHT_100to200_2018.dataset = '/QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
QCDHT_100to200_2018.process = 'QCD_2018'
QCDHT_100to200_2018.unix_code = 21000

QCDHT_200to300_2018         = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_200to300_2018")
QCDHT_200to300_2018.sigma   = 1712000#1555000 #pb
QCDHT_200to300_2018.year    = 2018
QCDHT_200to300_2018.dataset = '/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
QCDHT_200to300_2018.process = 'QCD_2018'
QCDHT_200to300_2018.unix_code = 21001

QCDHT_300to500_2018         = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_300to500_2018")
QCDHT_300to500_2018.sigma   = 347700 #324500 #pb
QCDHT_300to500_2018.year    = 2018
QCDHT_300to500_2018.dataset = '/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
QCDHT_300to500_2018.process = 'QCD_2018'
QCDHT_300to500_2018.unix_code = 21002
# QCDHT_300to500_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/QCD_HT300to500_2018_Skim.root"

QCDHT_500to700_2018         = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_500to700_2018")
QCDHT_500to700_2018.sigma   = 32100 #30310 #pb
QCDHT_500to700_2018.year    = 2018
QCDHT_500to700_2018.dataset = '/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
QCDHT_500to700_2018.process = 'QCD_2018'
QCDHT_500to700_2018.unix_code = 21003
# QCDHT_500to700_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/QCD_HT500to700_2018_Skim.root"

QCDHT_700to1000_2018         = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_700to1000_2018")
QCDHT_700to1000_2018.sigma   = 6832 #6444 #pb
QCDHT_700to1000_2018.year    = 2018
QCDHT_700to1000_2018.dataset = '/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
QCDHT_700to1000_2018.process = 'QCD_2018'
QCDHT_700to1000_2018.unix_code = 21004
# QCDHT_700to1000_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/QCD_HT700to1000_2018_Skim.root"

QCDHT_1000to1500_2018         = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_1000to1500_2018")
QCDHT_1000to1500_2018.sigma   = 1207 #1127 #pb
QCDHT_1000to1500_2018.year    = 2018
QCDHT_1000to1500_2018.dataset = '/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
QCDHT_1000to1500_2018.process = 'QCD_2018'
QCDHT_1000to1500_2018.unix_code = 21005
# QCDHT_1000to1500_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/QCD_HT1000_Skim.root"

QCDHT_1500to2000_2018         = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_1500to2000_2018")
QCDHT_1500to2000_2018.sigma   = 119.9 #109.8 #pb
QCDHT_1500to2000_2018.year    = 2018
QCDHT_1500to2000_2018.dataset = '/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
QCDHT_1500to2000_2018.process = 'QCD_2018'
QCDHT_1500to2000_2018.unix_code = 21006
# QCDHT_1500to2000_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/QCD-HT1500to2000_2018_Skim.root"

QCDHT_2000toInf_2018         = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_2000toInf_2018")
QCDHT_2000toInf_2018.sigma   = 25.24 #21.98 #pb   #####
QCDHT_2000toInf_2018.year    = 2018
QCDHT_2000toInf_2018.dataset = '/QCD_HT2000toInf_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
QCDHT_2000toInf_2018.process = 'QCD_2018'
QCDHT_2000toInf_2018.unix_code = 21007
# QCDHT_2000toInf_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/QCD-HT2000toInf_2018_Skim.root"

QCD_2018 = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_2018")
QCD_2018.year = 2018
QCD_2018.components = [QCDHT_100to200_2018, QCDHT_200to300_2018,
                       QCDHT_300to500_2018, QCDHT_500to700_2018, 
                       QCDHT_700to1000_2018, QCDHT_1000to1500_2018, 
                       QCDHT_1500to2000_2018, QCDHT_2000toInf_2018]

#QCD_2018.components = [QCDHT_300to500_2018, QCDHT_500to700_2018, QCDHT_1000to1500_2018, QCDHT_1500to2000_2018, QCDHT_2000toInf_2018]

################################ TTbar ################################

TT_hadr_2018         = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_hadr_2018")
TT_hadr_2018.sigma   = 380.94 #687.1 #pb
TT_hadr_2018.year    = 2018
TT_hadr_2018.dataset = '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
TT_hadr_2018.process = 'TT_2018'
TT_hadr_2018.unix_code = 21101
# TT_hadr_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/TT_Hadr_2018_Skim.root"

TT_Mtt700to1000_2018         = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_Mtt700to1000_2018")
TT_Mtt700to1000_2018.sigma   = 80.5 #pb
TT_Mtt700to1000_2018.year    = 2018
TT_Mtt700to1000_2018.dataset = '/TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
TT_Mtt700to1000_2018.process = 'TT_2018'
TT_Mtt700to1000_2018.unix_code = 21102
# TT_Mtt700to1000_2018.local_path= "/eos/home-a/acagnott/DarkMatter/topcandidate_file/TT_Mtt-700to1000_2018_Skim.root"

TT_Mtt1000toInf_2018         = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_Mtt1000toInf_2018")
TT_Mtt1000toInf_2018.sigma   = 21.3 #pb
TT_Mtt1000toInf_2018.year    = 2018
TT_Mtt1000toInf_2018.dataset = '/TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
TT_Mtt1000toInf_2018.process = 'TT_2018'
TT_Mtt1000toInf_2018.unix_code = 21103
# TT_Mtt1000toInf_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/TT_Mtt-1000toInf_2018_Skim.root"

TT_semilep_2018         = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_semilep_2018")
TT_semilep_2018.sigma   = 364.51 #pb
TT_semilep_2018.year    = 2018
TT_semilep_2018.dataset = '/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
TT_semilep_2018.process = 'TT_2018'
TT_semilep_2018.unix_code = 21104
# TT_semilep_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/TT_SemiLep_2018_Skim.root"

TT_2018             = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_2018")
TT_2018.year        = 2018
TT_2018.components  = [TT_hadr_2018, TT_semilep_2018, TT_Mtt1000toInf_2018, TT_Mtt700to1000_2018]

################################ ZJetsToNuNu ################################
ZJetsToNuNu_HT100to200_2018         = sample(ROOT.kAzure+6, 1, 1001, "ZJets HT-100To200", "ZJetsToNuNu_HT100to200_2018")
ZJetsToNuNu_HT100to200_2018.sigma   = 280.35 * 1.37 #267.0	 #pb 
ZJetsToNuNu_HT100to200_2018.year    = 2018
ZJetsToNuNu_HT100to200_2018.dataset = '/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
ZJetsToNuNu_HT100to200_2018.process = 'ZJetsToNuNu_2018'
ZJetsToNuNu_HT100to200_2018.unix_code = 21200
# ZJetsToNuNu_HT100to200_2018.local_path = '/eos/home-a/acagnott/DarkMatter/topcandidate_file/ZJetsToNuNu_HT100to200_2018_Skim.root'

ZJetsToNuNu_HT200to400_2018         = sample(ROOT.kAzure+6, 1, 1001, "ZJets HT-200To400", "ZJetsToNuNu_HT200to400_2018")
ZJetsToNuNu_HT200to400_2018.sigma   = 77.67*1.52 #73.08 #pb
ZJetsToNuNu_HT200to400_2018.year    = 2018
ZJetsToNuNu_HT200to400_2018.dataset = '/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
ZJetsToNuNu_HT200to400_2018.process = 'ZJetsToNuNu_2018'
ZJetsToNuNu_HT200to400_2018.unix_code = 21201
# ZJetsToNuNu_HT200to400_2018.local_path = '/eos/home-a/acagnott/DarkMatter/topcandidate_file/ZJetsToNuNu_HT200to400_2018_Skim.root'

ZJetsToNuNu_HT400to600_2018         = sample(ROOT.kAzure+6, 1, 1001, "ZJetsToNuNu HT-400To600", "ZJetsToNuNu_HT400to600_2018")
ZJetsToNuNu_HT400to600_2018.sigma   = 10.73*1.37 #9.904	 #pb
ZJetsToNuNu_HT400to600_2018.year    = 2018
ZJetsToNuNu_HT400to600_2018.dataset = '/ZJetsToNuNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
ZJetsToNuNu_HT400to600_2018.process = 'ZJetsToNuNu_2018'
ZJetsToNuNu_HT400to600_2018.unix_code = 21202
# ZJetsToNuNu_HT400to600_2018.local_path = '/eos/home-a/acagnott/DarkMatter/topcandidate_file/ZJetsToNuNu_HT400to600_2018_Skim.root'

ZJetsToNuNu_HT600to800_2018         = sample(ROOT.kAzure+6, 1, 1001, "ZJetsToNuNu HT-600To800", "ZJetsToNuNu_HT600to800_2018")
ZJetsToNuNu_HT600to800_2018.sigma   = 2.56*1.04 #2.413 #pb
ZJetsToNuNu_HT600to800_2018.year    = 2018
ZJetsToNuNu_HT600to800_2018.dataset = '/ZJetsToNuNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
ZJetsToNuNu_HT600to800_2018.process = 'ZJetsToNuNu_2018'
ZJetsToNuNu_HT600to800_2018.unix_code = 21203
# ZJetsToNuNu_HT600to800_2018.local_path = '/eos/home-a/acagnott/DarkMatter/topcandidate_file/ZJetsToNuNu_HT600to800_2018_Skim.root'

ZJetsToNuNu_HT800to1200_2018         = sample(ROOT.kAzure+6, 1, 1001, "ZJetsToNuNu HT-800To1200", "ZJetsToNuNu_HT800to1200_2018")
ZJetsToNuNu_HT800to1200_2018.sigma   = 1.18*1.14 #1.071 #pb
ZJetsToNuNu_HT800to1200_2018.year    = 2018
ZJetsToNuNu_HT800to1200_2018.dataset = '/ZJetsToNuNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
ZJetsToNuNu_HT800to1200_2018.process = 'ZJetsToNuNu_2018'
ZJetsToNuNu_HT800to1200_2018.unix_code = 21204
# ZJetsToNuNu_HT800to1200_2018.local_path = '/eos/home-a/acagnott/DarkMatter/topcandidate_file/ZJetsToNuNu_HT800to1200_2018_Skim.root'

ZJetsToNuNu_HT1200to2500_2018         = sample(ROOT.kAzure+6, 1, 1001, "ZJetsToNuNu HT-1200To2500", "ZJetsToNuNu_HT1200to2500_2018")
ZJetsToNuNu_HT1200to2500_2018.sigma   = 0.29*0.88 #0.2497 #pb
ZJetsToNuNu_HT1200to2500_2018.year    = 2018
ZJetsToNuNu_HT1200to2500_2018.dataset = '/ZJetsToNuNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
ZJetsToNuNu_HT1200to2500_2018.process = 'ZJetsToNuNu_2018'
ZJetsToNuNu_HT1200to2500_2018.unix_code = 21205
# ZJetsToNuNu_HT1200to2500_2018.local_path = '/eos/home-a/acagnott/DarkMatter/topcandidate_file/ZJetsToNuNu_HT1200to2500_2018_Skim.root'

ZJetsToNuNu_HT2500toInf_2018         = sample(ROOT.kAzure+6, 1, 1001, "ZJetsToNuNu HT-2500ToInf", "ZJetsToNuNu_HT2500toInf_2018")
ZJetsToNuNu_HT2500toInf_2018.sigma   = 0.007*0.88 #0.005618	 #pb
ZJetsToNuNu_HT2500toInf_2018.year    = 2018
ZJetsToNuNu_HT2500toInf_2018.dataset = '/ZJetsToNuNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
ZJetsToNuNu_HT2500toInf_2018.process = 'ZJetsToNuNu_2018'
ZJetsToNuNu_HT2500toInf_2018.unix_code = 21206
# ZJetsToNuNu_HT2500toInf_2018.local_path = '/eos/home-a/acagnott/DarkMatter/topcandidate_file/ZJetsToNuNu_HT2500toInf_2018_Skim.root'

ZJetsToNuNu_2018            = sample(ROOT.kAzure+6, 1, 1001, "ZJetsToNuNu", "ZJetsToNuNu_2018")
ZJetsToNuNu_2018.year       = 2018
ZJetsToNuNu_2018.components = [ZJetsToNuNu_HT100to200_2018, ZJetsToNuNu_HT200to400_2018, 
                               ZJetsToNuNu_HT400to600_2018, ZJetsToNuNu_HT600to800_2018, 
                               ZJetsToNuNu_HT800to1200_2018, ZJetsToNuNu_HT1200to2500_2018, 
                               ZJetsToNuNu_HT2500toInf_2018]

#ZJetsToNuNu_2018.components = [ZJetsToNuNu_HT100to200_2018, ZJetsToNuNu_HT200to400_2018, ZJetsToNuNu_HT400to600_2018, ZJetsToNuNu_HT600to800_2018, ZJetsToNuNu_HT1200to2500_2018, ZJetsToNuNu_HT2500toInf_2018]

################################ WJets ################################

WJetsHT70to100_2018         = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJetsHT70to100_2018")
WJetsHT70to100_2018.sigma   = 1353.0 * kFactorsQCD["WJetsHT100to200"] #pb
WJetsHT70to100_2018.year    = 2018
WJetsHT70to100_2018.dataset = '/WJetsToLNu_HT-70To100_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
WJetsHT70to100_2018.process = 'WJets_2018'
WJetsHT70to100_2018.unix_code = 21200

WJetsHT100to200_2018         = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJetsHT100to200_2018")
WJetsHT100to200_2018.sigma   = 1345 * kFactorsQCD["WJetsHT100to200"] #pb
WJetsHT100to200_2018.year    = 2018
WJetsHT100to200_2018.dataset = '/WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
WJetsHT100to200_2018.process = 'WJets_2018'
WJetsHT100to200_2018.unix_code = 21201

WJetsHT200to400_2018         = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJetsHT200to400_2018")
WJetsHT200to400_2018.sigma   = 359.7 * kFactorsQCD["WJetsHT200to400"] #pb
WJetsHT200to400_2018.year    = 2018
WJetsHT200to400_2018.dataset = '/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
WJetsHT200to400_2018.process = 'WJets_2018'
WJetsHT200to400_2018.unix_code = 21202

WJetsHT400to600_2018         = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJetsHT400to600_2018")
WJetsHT400to600_2018.sigma   = 48.91 * kFactorsQCD["WJetsHT400to600"] #pb
WJetsHT400to600_2018.year    = 2018
WJetsHT400to600_2018.dataset = '/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1_ext1-v2/NANOAODSIM'
WJetsHT400to600_2018.process = 'WJets_2018' 
WJetsHT400to600_2018.unix_code = 21203

WJetsHT600to800_2018         = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJetsHT600to800_2018")
WJetsHT600to800_2018.sigma   = 12.05 * kFactorsQCD["WJetsHT600to800"] #pb
WJetsHT600to800_2018.year    = 2018
WJetsHT600to800_2018.dataset = '/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1_ext1-v2/NANOAODSIM'
WJetsHT600to800_2018.process = 'WJets_2018'
WJetsHT600to800_2018.unix_code = 21204

WJetsHT800to1200_2018         = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJetsHT800to1200_2018")
WJetsHT800to1200_2018.sigma   = 5.501 * kFactorsQCD["WJetsHT800to1200"] #pb
WJetsHT800to1200_2018.year    = 2018
WJetsHT800to1200_2018.dataset = '/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1_ext1-v2/NANOAODSIM'
WJetsHT800to1200_2018.process = 'WJets_2018' 
WJetsHT800to1200_2018.unix_code = 21205

WJetsHT1200to2500_2018         = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJetsHT1200to2500_2018")
WJetsHT1200to2500_2018.sigma   = 1.329 * kFactorsQCD["WJetsHT1200to2500"] #pb
WJetsHT1200to2500_2018.year    = 2018
WJetsHT1200to2500_2018.dataset = '/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1_ext1-v2/NANOAODSIM'
WJetsHT1200to2500_2018.process = 'WJets_2018' 
WJetsHT1200to2500_2018.unix_code = 21206

WJetsHT2500toInf_2018         = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJetsHT2500toInf_2018")
WJetsHT2500toInf_2018.sigma   = 0.03216 * kFactorsQCD["WJetsHT2500toInf"] #pb
WJetsHT2500toInf_2018.year    = 2018
WJetsHT2500toInf_2018.dataset = '/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM'
WJetsHT2500toInf_2018.process = 'WJets_2018'
WJetsHT2500toInf_2018.unix_code = 21207

WJets_2018 = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJets_2018")
WJets_2018.year = 2018
WJets_2018.components = [WJetsHT70to100_2018, 
                         WJetsHT100to200_2018, WJetsHT200to400_2018, 
                         WJetsHT400to600_2018, WJetsHT600to800_2018, 
                         WJetsHT800to1200_2018, WJetsHT1200to2500_2018, 
                         WJetsHT2500toInf_2018]

################################ Signal tDM ################################

tDM_mPhi1000_mChi1_2018 = sample(ROOT.kGreen+2, 1, 1001, "DM (m_{#Phi}=1000)", "tDM_mPhi1000_mChi1_2018")
tDM_mPhi1000_mChi1_2018.sigma = 24.99 *0.00001 #*100    #pb  aggiunto*100 per i plot
tDM_mPhi1000_mChi1_2018.year = 2018
tDM_mPhi1000_mChi1_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/tDM_mPhi1000_mChi1_Skim.root"
tDM_mPhi1000_mChi1_2018.unix_code = 22100

tDM_mPhi500_mChi1_2018 = sample(ROOT.kGreen+1, 1, 1001, "DM (m_{#Phi}=500)", "tDM_mPhi500_mChi1_2018")
tDM_mPhi500_mChi1_2018.year = 2018
tDM_mPhi500_mChi1_2018.sigma = 43.85 *0.0001  #pb
tDM_mPhi500_mChi1_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/tDM_mPhi500_mChi1_Skim.root"
tDM_mPhi500_mChi1_2018.unix_code = 22101

tDM_mPhi50_mChi1_2018= sample(ROOT.kGreen, 1, 1001, "DM (m_{#Phi}=50)", "tDM_mPhi50_mChi1_2018")
tDM_mPhi50_mChi1_2018.year = 2018
tDM_mPhi50_mChi1_2018.sigma = 0.7  #pb
tDM_mPhi50_mChi1_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/tDM_mPhi50_mChi1_Skim.root"
tDM_mPhi50_mChi1_2018.unix_code = 22102

################################ Signal Tprime ################################

TprimeToTZ_1800_2018         = sample(ROOT.kGreen+4, 1, 1001, "T#rightarrow tZ M1800GeV", "TprimeToTZ_1800_2018")
TprimeToTZ_1800_2018.sigma   = 0.00045 #pb
TprimeToTZ_1800_2018.year    = 2018
TprimeToTZ_1800_2018.dataset = '/TprimeBToTZ_M-1800_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM'
TprimeToTZ_1800_2018.unix_code = 22000
# TprimeToTZ_1800_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/"+TprimeToTZ_1800_2018.label +"_Skim.root"

TprimeToTZ_1000_2018         = sample(ROOT.kGreen+2, 1, 1001, "T#rightarrow TZ M1000GeV", "TprimeToTZ_1000_2018")
TprimeToTZ_1000_2018.sigma   = 0.01362 #pb
TprimeToTZ_1000_2018.year    = 2018
TprimeToTZ_1000_2018.dataset = '/TprimeBToTZ_M-1000_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM'
TprimeToTZ_1000_2018.unix_code = 22001
# TprimeToTZ_1000_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/"+TprimeToTZ_1000_2018.label +"_Skim.root"

TprimeToTZ_700_2018         = sample(ROOT.kGreen, 1, 1001, "T#rightarrow tZ M700GeV", "TprimeToTZ_700_2018")
TprimeToTZ_700_2018.sigma   = 0.07804 #pb
TprimeToTZ_700_2018.year    = 2018
TprimeToTZ_700_2018.dataset = '/TprimeBToTZ_M-700_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/RunIISummer19UL18NanoAODv2-106X_upgrade2018_realistic_v15_L1v1-v1/NANOAODSIM'
TprimeToTZ_700_2018.unix_code = 22002
# TprimeToTZ_700_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/"+TprimeToTZ_700_2018.label +"_Skim.root"


###############################################################################################################################
##########################################                                           ##########################################
##########################################                    2022                   ##########################################
##########################################                                           ##########################################
###############################################################################################################################

################################ QCD ################################
QCD_Pt_300to470_2022 = sample(ROOT.kAzure-5, 1, 1001, "QCD", "QCD_Pt_300to470_2022")
QCD_Pt_300to470_2022.sigma = 7589.0#pb
QCD_Pt_300to470_2022.year = 2022
QCD_Pt_300to470_2022.dataset ="/QCD_PT-300to470_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1_ext1-v1/NANOAODSIM"
QCD_Pt_300to470_2022.process = 'QCD_2022'
QCD_Pt_300to470_2022.unix_code = 31000

QCD_Pt_470to600_2022 = sample(ROOT.kAzure-5, 1, 1001, "QCD", "QCD_Pt_470to600_2022")
QCD_Pt_470to600_2022.sigma = 626.4#pb
QCD_Pt_470to600_2022.year = 2022
QCD_Pt_470to600_2022.dataset = "/QCD_PT-470to600_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1_ext1-v1/NANOAODSIM"
QCD_Pt_470to600_2022.process = 'QCD_2022'
QCD_Pt_470to600_2022.unix_code = 31001

QCD_Pt_1000to1400_2022 = sample(ROOT.kAzure-5, 1, 1001, "QCD", "QCD_Pt_1000to1400_2022")
QCD_Pt_1000to1400_2022.sigma = 8.92	 #pb
QCD_Pt_1000to1400_2022.year = 2022
QCD_Pt_1000to1400_2022.dataset = "/QCD_PT-1000to1400_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1_ext1-v1/NANOAODSIM"
QCD_Pt_1000to1400_2022.process = 'QCD_2022'
QCD_Pt_1000to1400_2022.unix_code = 31002

QCD_Pt_1800to2400_2022 = sample(ROOT.kAzure-5, 1, 1001, "QCD", "QCD_Pt_1800to2400_2022")
QCD_Pt_1800to2400_2022.sigma = 0.1148 #pb
QCD_Pt_1800to2400_2022.year = 2022
QCD_Pt_1800to2400_2022.dataset = "/QCD_PT-1800to2400_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1_ext1-v1/NANOAODSIM"
QCD_Pt_1800to2400_2022.process = "QCD_2022"
QCD_Pt_1800to2400_2022.unix_code = 31003

QCD_Pt_2400to3200_2022 = sample(ROOT.kAzure-5, 1, 1001, "QCD", "QCD_Pt_2400to3200_2022")
QCD_Pt_2400to3200_2022.sigma = 0.007542	 #pb
QCD_Pt_2400to3200_2022.year = 2022
QCD_Pt_2400to3200_2022.dataset = "/QCD_PT-2400to3200_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1_ext1-v1/NANOAODSIM"
QCD_Pt_2400to3200_2022.process = "QCD_2022"
QCD_Pt_2400to3200_2022.unix_code = 31004

QCD_Pt_3200_2022 = sample(ROOT.kAzure-5, 1, 1001, "QCD", "QCD_Pt_3200_2022")
QCD_Pt_3200_2022.sigma = 0.0002331 #pb
QCD_Pt_3200_2022.year = 2022
QCD_Pt_3200_2022.dataset = "/QCD_PT-3200_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1_ext1-v1/NANOAODSIM"
QCD_Pt_3200_2022.process = "QCD_2022"
QCD_Pt_3200_2022.unix_code = 31005

QCD_2022 = sample(ROOT.kAzure-5, 1, 1001, "QCD", "QCD_2022")
QCD_2022.year = 2018
QCD_2022.components = [ QCD_Pt_300to470_2022, QCD_Pt_470to600_2022,  QCD_Pt_1000to1400_2022, QCD_Pt_1800to2400_2022, QCD_Pt_2400to3200_2022, QCD_Pt_3200_2022 ]

################################ TTbar ################################
TT_semilep_2022 = sample(ROOT.kViolet-4, 1, 1001, "t#bar{t}", "TT_semilep_2022")
TT_semilep_2022.sigma = 762.1 #pb
TT_semilep_2022.year = 2022
TT_semilep_2022.dataset = "/TTtoLNu2Q_TuneCP5CR1_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM"
TT_semilep_2022.process = 'TT_2022'
TT_semilep_2022.unix_code = 31100

TT_hadr_2022 = sample(ROOT.kViolet-4, 1, 1001, "t#bar{t}", "TT_hadr_2022")
TT_hadr_2022.sigma = 762.1
TT_hadr_2022.year = 2022
TT_hadr_2022.dataset = "/TTto4Q_TuneCP5CR2_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM"
TT_hadr_2022.precess = 'TT_2022'
TT_hadr_2022.unix_code = 31101

TT_2022 = sample(ROOT.kViolet-4, 1, 1001, "t#bar{t}", "TT_2022")
TT_2022.year = 2022
TT_2022.components = [TT_semilep_2022, TT_hadr_2022]

# ROOT.kSpring+3 per ZJetsToNuNu

########################### DATA 2016 ############################################
DataHTH_2016           = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTH_2016")  #8.6fb
DataHTH_2016.runP      = 'H'
DataHTH_2016.year      = 2016
DataHTH_2016.dataset   = '/MET/Run2016H-UL2016_MiniAODv2_NanoAODv9-v1/NANOAOD'
# DataHTH_2016.unix_code = 

########################### DATA 2018 ############################################
DataMETA_2018           = sample(ROOT.kBlack, 1, 1001, "Data", "DataMETA_2018")
DataMETA_2018.runP      = 'A'
DataMETA_2018.year      = 2018
DataMETA_2018.dataset   = '/MET/Run2018A-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD' #'/MET/Run2018A-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD'
DataMETA_2018.process   = "DataMET_2018"
DataMETA_2018.unix_code = 20000
DataMETB_2018           = sample(ROOT.kBlack, 1, 1001, "Data", "DataMETB_2018")
DataMETB_2018.runP      = 'B'
DataMETB_2018.year      = 2018
DataMETB_2018.dataset   = '/MET/Run2018B-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD' #'/MET/Run2018B-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD'
DataMETB_2018.process   = "DataMET_2018"
DataMETB_2018.unix_code = 20001
DataMETC_2018           = sample(ROOT.kBlack, 1, 1001, "Data", "DataMETC_2018")
DataMETC_2018.runP      = 'C'
DataMETC_2018.year      = 2018
DataMETC_2018.dataset   = '/MET/Run2018C-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD'#'/MET/Run2018C-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD'
DataMETC_2018.process   = "DataMET_2018"
DataMETC_2018.unix_code = 20002
DataMETD_2018           = sample(ROOT.kBlack, 1, 1001, "Data", "DataMETD_2018")
DataMETD_2018.runP      = 'D'
DataMETD_2018.year      = 2018
DataMETD_2018.dataset   = '/MET/Run2018D-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD'#'/MET/Run2018D-UL2018_MiniAODv2_NanoAODv9-v1/NANOAOD'
DataMETD_2018.process   = "DataMET_2018"
DataMETD_2018.unix_code = 20003

DataMET_2018            = sample(ROOT.kBlack, 1, 1001, "Data", "DataMET_2018")
DataMET_2018.year       = 2018
DataMET_2018.components = [DataMETA_2018, DataMETB_2018, 
                          DataMETC_2018, DataMETD_2018
                          ]

DataSingleMuA_2018           = sample(ROOT.kBlack, 1, 1001, "Data", "DataSingleMuA_2018")
DataSingleMuA_2018.runP      = 'A'
DataSingleMuA_2018.year      = 2018
DataSingleMuA_2018.dataset   = '/SingleMuon/Run2018A-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD'
DataSingleMuA_2018.process   = "DataSingleMu_2018"
DataSingleMuA_2018.unix_code = 20100
DataSingleMuB_2018           = sample(ROOT.kBlack, 1, 1001, "Data", "DataSingleMuB_2018")
DataSingleMuB_2018.runP      = 'B'
DataSingleMuB_2018.year      = 2018
DataSingleMuB_2018.dataset   = '/SingleMuon/Run2018B-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD'
DataSingleMuB_2018.process   = "DataSingleMu_2018"
DataSingleMuB_2018.unix_code = 20101
DataSingleMuC_2018           = sample(ROOT.kBlack, 1, 1001, "Data", "DataSingleMuC_2018")
DataSingleMuC_2018.runP      = 'C'
DataSingleMuC_2018.year      = 2018
DataSingleMuC_2018.dataset   = '/SingleMuon/Run2018C-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD'
DataSingleMuC_2018.process   = "DataSingleMu_2018"
DataSingleMuC_2018.unix_code = 20102
DataSingleMuD_2018           = sample(ROOT.kBlack, 1, 1001, "Data", "DataSingleMuD_2018")
DataSingleMuD_2018.runP      = 'D'
DataSingleMuD_2018.year      = 2018
DataSingleMuD_2018.dataset   = '/SingleMuon/Run2018D-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD'
DataSingleMuD_2018.process   = "DataSingleMu_2018"
DataSingleMuD_2018.unix_code = 20103

DataSingleMu_2018            = sample(ROOT.kBlack, 1, 1001, "Data", "DataSingleMu_2018")
DataSingleMu_2018.year       = 2018
DataSingleMu_2018.components = [DataSingleMuA_2018, DataSingleMuB_2018, 
                                DataSingleMuC_2018, DataSingleMuD_2018
                               ]


# DataMETA_2018          = sample(ROOT.kBlack, 1, 1001, "Data", "DataMETA_2018")
# DataMETA_2018.runP     = 'A'
# DataMETA_2018.year     = 2018
# DataMETA_2018.dataset  = '/MET/Run2018A-02Apr2020-v1/NANOAOD' #ReRECO 2018 A

########################### DATA 2022 ############################################
DataJetMETC_2022 = sample(ROOT.kBlack, 1, 1001, "Data", "DataJetMETC_2022")
DataJetMETC_2022.runP = 'C'
DataJetMETC_2022.year = 2022
DataJetMETC_2022.dataset = '/JetMET/Run2022C-ReRecoNanoAODv11-v1/NANOAOD'
DataJetMETC_2022.unix_code = 30000
DataJetMETD_2022 = sample(ROOT.kBlack, 1, 1001, "Data", "DataJetMETD_2022")
DataJetMETD_2022.runP = 'D'
DataJetMETD_2022.year = 2022
DataJetMETD_2022.dataset = '/JetMET/Run2022D-ReRecoNanoAODv11-v1/NANOAOD'
DataJetMETD_2022.unix_code = 30001
DataJetMETE_2022 = sample(ROOT.kBlack, 1, 1001, "Data", "DataJetMETE_2022")
DataJetMETE_2022.runP = 'E'
DataJetMETE_2022.year = 2022
DataJetMETE_2022.dataset = '/JetMET/Run2022E-ReRecoNanoAODv11-v1/NANOAOD'
DataJetMETE_2022.unix_code = 30002
DataJetMETF_2022 = sample(ROOT.kBlack, 1, 1001, "Data", "DataJetMETF_2022")
DataJetMETF_2022.runP = 'F'
DataJetMETF_2022.year = 2022
DataJetMETF_2022.dataset = '/JetMET/Run2022F-PromptNanoAODv11_v1-v2/NANOAOD'
DataJetMETF_2022.unix_code = 30003
DataJetMETG_2022 = sample(ROOT.kBlack, 1, 1001, "Data", "DataJetMETG_2022")
DataJetMETG_2022.runP = 'G'
DataJetMETG_2022.year = 2022
DataJetMETG_2022.dataset = '/JetMET/Run2022G-PromptNanoAODv11_v1-v2/NANOAOD'
DataJetMETG_2022.unix_code = 30004
DataJetMET_2022 = sample(ROOT.kBlack, 1, 1001, "Data", "DataJetMET_2022")
DataJetMET_2022.year = 2022
DataJetMET_2022.components = [DataJetMETC_2022, DataJetMETD_2022, DataJetMETE_2022, DataJetMETF_2022, DataJetMETG_2022]

############### code meanings ################
# XXXXX  5 digits for each sample
# 1st digit: 0 for 2016, 1 for 2017, 2 for 2018, 3 for 2022, 4 for 2023
# 2nd digit: 0 for data, 1 for MC bkg, 2 for MC signal
# 3rd digit: for the process (QCD = 0, TT = 1, ZJets = 2, WJets = 3, 
#                             Tprime = 0, tDM = 1, 
#                             Data_MET = 0, Data_SingleMu = 1,...)
# 3rd digit and 4th digit: 2 digits identifies the sample 

# example: QCDHT_100to200_2018 == 21000, QCDHT_200to300_2018 == 21001
#          DATAHTA_2018 == 20600, DATAHTB_2018 == 20601, DATAHTC_2018 == 20602, DATAHTD_2018 == 20603  
### non diamo un codice ai sample con le components --> da capire se serve aggiungerlo


sample_dict = {

    ################################## RUN II
    'DataHTH_2016': DataHTH_2016,
    # Data MET 2018   
    'DataMET_2018': DataMET_2018, 'DataMETA_2018': DataMETA_2018, 'DataMETB_2018': DataMETB_2018,
    'DataMETC_2018': DataMETC_2018, 'DataMETD_2018': DataMETD_2018, 
    # 'DataMETA_2018': DataMETA_2018,
    # Data Single Muon 2018
    'DataSingleMu_2018':DataSingleMu_2018, 'DataSingleMuA_2018':DataSingleMuA_2018, 'DataSingleMuB_2018':DataSingleMuB_2018, 
    'DataSingleMuC_2018':DataSingleMuC_2018, 'DataSingleMuD_2018':DataSingleMuD_2018,
    # BKGs 2018
    'QCDHT_100to200_2018':QCDHT_100to200_2018, 'QCDHT_200to300_2018':QCDHT_200to300_2018, 
    'QCDHT_300to500_2018':QCDHT_300to500_2018, 'QCDHT_500to700_2018':QCDHT_500to700_2018, 
    'QCDHT_700to1000_2018':QCDHT_700to1000_2018, 'QCDHT_1000to1500_2018':QCDHT_1000to1500_2018, 
    'QCDHT_1500to2000_2018':QCDHT_1500to2000_2018, 'QCDHT_2000toInf_2018':QCDHT_2000toInf_2018, 
    'QCD_2018':QCD_2018,
    'TT_Mtt700to1000_2018':TT_Mtt700to1000_2018, 'TT_Mtt1000toInf_2018':TT_Mtt1000toInf_2018, 
    'TT_semilep_2018':TT_semilep_2018, 'TT_hadr_2018':TT_hadr_2018,
    'TT_2018':TT_2018,
    'ZJetsToNuNu_HT100to200_2018':ZJetsToNuNu_HT100to200_2018, 'ZJetsToNuNu_HT200to400_2018':ZJetsToNuNu_HT200to400_2018, 
    'ZJetsToNuNu_HT400to600_2018':ZJetsToNuNu_HT400to600_2018, 'ZJetsToNuNu_HT600to800_2018':ZJetsToNuNu_HT600to800_2018, 
    'ZJetsToNuNu_HT800to1200_2018':ZJetsToNuNu_HT800to1200_2018, 'ZJetsToNuNu_HT1200to2500_2018':ZJetsToNuNu_HT1200to2500_2018, 
    'ZJetsToNuNu_HT2500toInf_2018':ZJetsToNuNu_HT2500toInf_2018, 
    'ZJetsToNuNu_2018':ZJetsToNuNu_2018,
    'WJetsHT70to100_2018':WJetsHT70to100_2018,'WJetsHT100to200_2018':WJetsHT100to200_2018,
    'WJetsHT200to400_2018':WJetsHT200to400_2018,'WJetsHT400to600_2018':WJetsHT400to600_2018,
    'WJetsHT600to800_2018':WJetsHT600to800_2018,'WJetsHT800to1200_2018':WJetsHT800to1200_2018,
    'WJetsHT1200to2500_2018':WJetsHT1200to2500_2018,'WJetsHT2500toInf_2018':WJetsHT2500toInf_2018,
    'WJets_2018':WJets_2018,    
    # signals 2018
    'TprimeToTZ_1800_2018' : TprimeToTZ_1800_2018, 
    'TprimeToTZ_1000_2018' : TprimeToTZ_1000_2018, 
    'TprimeToTZ_700_2018' : TprimeToTZ_700_2018,
    'tDM_mPhi50_mChi1_2018' : tDM_mPhi50_mChi1_2018, 'tDM_mPhi500_mChi1_2018' : tDM_mPhi500_mChi1_2018, 'tDM_mPhi1000_mChi1_2018' : tDM_mPhi1000_mChi1_2018,
    
    
    ############################### RUN III
    ############ QCD
    'QCD_2022' : QCD_2022, 'QCD_Pt_300to470_2022' : QCD_Pt_300to470_2022, 'QCD_Pt_470to600_2022' : QCD_Pt_470to600_2022,  
    'QCD_Pt_1000to1400_2022' : QCD_Pt_1000to1400_2022, 'QCD_Pt_1800to2400_2022' : QCD_Pt_1800to2400_2022, 'QCD_Pt_2400to3200_2022' : QCD_Pt_2400to3200_2022, 'QCD_Pt_3200_2022' : QCD_Pt_3200_2022,
    ########### TT
    'TT_2022': TT_2022, 'TT_semilep_2022' : TT_semilep_2022, 'TT_hadr_2022' : TT_hadr_2022,
    ############################################# DATA 
    'DataJetMET_2022': DataJetMET_2022, 'DataJetMETC_2022':DataJetMETC_2022, 'DataJetMETD_2022':DataJetMETD_2022, 
    'DataJetMETE_2022':DataJetMETE_2022, 'DataJetMETF_2022':DataJetMETF_2022, 'DataJetMETG_2022':DataJetMETG_2022
    }
