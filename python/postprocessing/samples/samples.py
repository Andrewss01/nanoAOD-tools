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

###############################################################################################################################
##########################################                                           ##########################################
##########################################                    2018                   ##########################################
##########################################                                           ##########################################
###############################################################################################################################

################################ QCD ################################
QCDHT_100to200_2018         = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_100to200_2018")
QCDHT_100to200_2018.sigma   = 23590000 #pb
QCDHT_100to200_2018.year    = 2018
QCDHT_100to200_2018.dataset = '/QCD_HT100to200_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
QCDHT_100to200_2018.process = 'QCD_2018'
QCDHT_100to200_2018.unix_code = 21000

QCDHT_200to300_2018         = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_200to300_2018")
QCDHT_200to300_2018.sigma   = 1555000#pb
QCDHT_200to300_2018.year    = 2018
QCDHT_200to300_2018.dataset = '/QCD_HT200to300_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
QCDHT_200to300_2018.process = 'QCD_2018'
QCDHT_200to300_2018.unix_code = 21001

QCDHT_300to500_2018         = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_300to500_2018")
QCDHT_300to500_2018.sigma   = 324500 #pb
QCDHT_300to500_2018.year    = 2018
QCDHT_300to500_2018.dataset = '/QCD_HT300to500_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
QCDHT_300to500_2018.process = 'QCD_2018'
QCDHT_300to500_2018.unix_code = 21002
# QCDHT_300to500_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/QCD_HT300to500_2018_Skim.root"

QCDHT_500to700_2018         = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_500to700_2018")
QCDHT_500to700_2018.sigma   = 30310 #pb
QCDHT_500to700_2018.year    = 2018
QCDHT_500to700_2018.dataset = '/QCD_HT500to700_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
QCDHT_500to700_2018.process = 'QCD_2018'
QCDHT_500to700_2018.unix_code = 21003
# QCDHT_500to700_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/QCD_HT500to700_2018_Skim.root"

QCDHT_700to1000_2018         = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_700to1000_2018")
QCDHT_700to1000_2018.sigma   = 6444 #pb
QCDHT_700to1000_2018.year    = 2018
QCDHT_700to1000_2018.dataset = '/QCD_HT700to1000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
QCDHT_700to1000_2018.process = 'QCD_2018'
QCDHT_700to1000_2018.unix_code = 21004
# QCDHT_700to1000_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/QCD_HT700to1000_2018_Skim.root"

QCDHT_1000to1500_2018         = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_1000to1500_2018")
QCDHT_1000to1500_2018.sigma   = 1127 #pb
QCDHT_1000to1500_2018.year    = 2018
QCDHT_1000to1500_2018.dataset = '/QCD_HT1000to1500_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
QCDHT_1000to1500_2018.process = 'QCD_2018'
QCDHT_1000to1500_2018.unix_code = 21005
# QCDHT_1000to1500_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/QCD_HT1000_Skim.root"

QCDHT_1500to2000_2018         = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_1500to2000_2018")
QCDHT_1500to2000_2018.sigma   = 109.8 #pb
QCDHT_1500to2000_2018.year    = 2018
QCDHT_1500to2000_2018.dataset = '/QCD_HT1500to2000_TuneCP5_PSWeights_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
QCDHT_1500to2000_2018.process = 'QCD_2018'
QCDHT_1500to2000_2018.unix_code = 21006
# QCDHT_1500to2000_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/QCD-HT1500to2000_2018_Skim.root"

QCDHT_2000toInf_2018         = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_2000toInf_2018")
QCDHT_2000toInf_2018.sigma   = 21.98 #pb   #####
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
TT_hadr_2018.sigma   = 687.1 #pb
TT_hadr_2018.year    = 2018
TT_hadr_2018.dataset = '/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
TT_hadr_2018.process = 'TT_2018'
TT_hadr_2018.unix_code = 21101
# TT_hadr_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/TT_Hadr_2018_Skim.root"

TT_Mtt700to1000_2018         = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_Mtt700to1000_2018")
TT_Mtt700to1000_2018.sigma   = 66.85 #pb
TT_Mtt700to1000_2018.year    = 2018
TT_Mtt700to1000_2018.dataset = '/TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
TT_Mtt700to1000_2018.process = 'TT_2018'
TT_Mtt700to1000_2018.unix_code = 21102
# TT_Mtt700to1000_2018.local_path= "/eos/home-a/acagnott/DarkMatter/topcandidate_file/TT_Mtt-700to1000_2018_Skim.root"

TT_Mtt1000toInf_2018         = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_Mtt1000toInf_2018")
TT_Mtt1000toInf_2018.sigma   = 16.42 #pb
TT_Mtt1000toInf_2018.year    = 2018
TT_Mtt1000toInf_2018.dataset = '/TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
TT_Mtt1000toInf_2018.process = 'TT_2018'
TT_Mtt1000toInf_2018.unix_code = 21103
# TT_Mtt1000toInf_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/TT_Mtt-1000toInf_2018_Skim.root"

TT_semilep_2018         = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_semilep_2018")
TT_semilep_2018.sigma   = 687.1 #pb
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
ZJetsToNuNu_HT100to200_2018.sigma   = 267.0	 #pb
ZJetsToNuNu_HT100to200_2018.year    = 2018
ZJetsToNuNu_HT100to200_2018.dataset = '/ZJetsToNuNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
ZJetsToNuNu_HT100to200_2018.process = 'ZJetsToNuNu_2018'
ZJetsToNuNu_HT100to200_2018.unix_code = 21200
# ZJetsToNuNu_HT100to200_2018.local_path = '/eos/home-a/acagnott/DarkMatter/topcandidate_file/ZJetsToNuNu_HT100to200_2018_Skim.root'

ZJetsToNuNu_HT200to400_2018         = sample(ROOT.kAzure+6, 1, 1001, "ZJets HT-200To400", "ZJetsToNuNu_HT200to400_2018")
ZJetsToNuNu_HT200to400_2018.sigma   =  73.08 #pb
ZJetsToNuNu_HT200to400_2018.year    = 2018
ZJetsToNuNu_HT200to400_2018.dataset = '/ZJetsToNuNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
ZJetsToNuNu_HT200to400_2018.process = 'ZJetsToNuNu_2018'
ZJetsToNuNu_HT200to400_2018.unix_code = 21201
# ZJetsToNuNu_HT200to400_2018.local_path = '/eos/home-a/acagnott/DarkMatter/topcandidate_file/ZJetsToNuNu_HT200to400_2018_Skim.root'

ZJetsToNuNu_HT400to600_2018         = sample(ROOT.kAzure+6, 1, 1001, "ZJetsToNuNu HT-400To600", "ZJetsToNuNu_HT400to600_2018")
ZJetsToNuNu_HT400to600_2018.sigma   = 9.904	 #pb
ZJetsToNuNu_HT400to600_2018.year    = 2018
ZJetsToNuNu_HT400to600_2018.dataset = '/ZJetsToNuNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
ZJetsToNuNu_HT400to600_2018.process = 'ZJetsToNuNu_2018'
ZJetsToNuNu_HT400to600_2018.unix_code = 21202
# ZJetsToNuNu_HT400to600_2018.local_path = '/eos/home-a/acagnott/DarkMatter/topcandidate_file/ZJetsToNuNu_HT400to600_2018_Skim.root'

ZJetsToNuNu_HT600to800_2018         = sample(ROOT.kAzure+6, 1, 1001, "ZJetsToNuNu HT-600To800", "ZJetsToNuNu_HT600to800_2018")
ZJetsToNuNu_HT600to800_2018.sigma   = 2.413 #pb
ZJetsToNuNu_HT600to800_2018.year    = 2018
ZJetsToNuNu_HT600to800_2018.dataset = '/ZJetsToNuNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
ZJetsToNuNu_HT600to800_2018.process = 'ZJetsToNuNu_2018'
ZJetsToNuNu_HT600to800_2018.unix_code = 21203
# ZJetsToNuNu_HT600to800_2018.local_path = '/eos/home-a/acagnott/DarkMatter/topcandidate_file/ZJetsToNuNu_HT600to800_2018_Skim.root'

ZJetsToNuNu_HT800to1200_2018         = sample(ROOT.kAzure+6, 1, 1001, "ZJetsToNuNu HT-800To1200", "ZJetsToNuNu_HT800to1200_2018")
ZJetsToNuNu_HT800to1200_2018.sigma   = 1.071 #pb
ZJetsToNuNu_HT800to1200_2018.year    = 2018
ZJetsToNuNu_HT800to1200_2018.dataset = '/ZJetsToNuNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
ZJetsToNuNu_HT800to1200_2018.process = 'ZJetsToNuNu_2018'
ZJetsToNuNu_HT800to1200_2018.unix_code = 21204
# ZJetsToNuNu_HT800to1200_2018.local_path = '/eos/home-a/acagnott/DarkMatter/topcandidate_file/ZJetsToNuNu_HT800to1200_2018_Skim.root'

ZJetsToNuNu_HT1200to2500_2018         = sample(ROOT.kAzure+6, 1, 1001, "ZJetsToNuNu HT-1200To2500", "ZJetsToNuNu_HT1200to2500_2018")
ZJetsToNuNu_HT1200to2500_2018.sigma   = 0.2497 #pb
ZJetsToNuNu_HT1200to2500_2018.year    = 2018
ZJetsToNuNu_HT1200to2500_2018.dataset = '/ZJetsToNuNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
ZJetsToNuNu_HT1200to2500_2018.process = 'ZJetsToNuNu_2018'
ZJetsToNuNu_HT1200to2500_2018.unix_code = 21205
# ZJetsToNuNu_HT1200to2500_2018.local_path = '/eos/home-a/acagnott/DarkMatter/topcandidate_file/ZJetsToNuNu_HT1200to2500_2018_Skim.root'

ZJetsToNuNu_HT2500toInf_2018         = sample(ROOT.kAzure+6, 1, 1001, "ZJetsToNuNu HT-2500ToInf", "ZJetsToNuNu_HT2500toInf_2018")
ZJetsToNuNu_HT2500toInf_2018.sigma   = 0.005618	 #pb
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
WJetsHT70to100_2018.sigma   = 1292 #pb
WJetsHT70to100_2018.year    = 2018
WJetsHT70to100_2018.dataset = '/WJetsToLNu_HT-70To100_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
WJetsHT70to100_2018.process = 'WJets_2018'
WJetsHT70to100_2018.unix_code = 21200

WJetsHT100to200_2018         = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJetsHT100to200_2018")
WJetsHT100to200_2018.sigma   = 1395 #pb
WJetsHT100to200_2018.year    = 2018
WJetsHT100to200_2018.dataset = '/WJetsToLNu_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
WJetsHT100to200_2018.process = 'WJets_2018'
WJetsHT100to200_2018.unix_code = 21201

WJetsHT200to400_2018         = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJetsHT200to400_2018")
WJetsHT200to400_2018.sigma   = 407.9 #pb
WJetsHT200to400_2018.year    = 2018
WJetsHT200to400_2018.dataset = '/WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM'
WJetsHT200to400_2018.process = 'WJets_2018'
WJetsHT200to400_2018.unix_code = 21202

WJetsHT400to600_2018         = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJetsHT400to600_2018")
WJetsHT400to600_2018.sigma   = 57.48 #pb
WJetsHT400to600_2018.year    = 2018
WJetsHT400to600_2018.dataset = '/WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1_ext1-v2/NANOAODSIM'
WJetsHT400to600_2018.process = 'WJets_2018' 
WJetsHT400to600_2018.unix_code = 21203

WJetsHT600to800_2018         = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJetsHT600to800_2018")
WJetsHT600to800_2018.sigma   = 12.87 #pb
WJetsHT600to800_2018.year    = 2018
WJetsHT600to800_2018.dataset = '/WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1_ext1-v2/NANOAODSIM'
WJetsHT600to800_2018.process = 'WJets_2018'
WJetsHT600to800_2018.unix_code = 21204

WJetsHT800to1200_2018         = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJetsHT800to1200_2018")
WJetsHT800to1200_2018.sigma   = 5.366 #pb
WJetsHT800to1200_2018.year    = 2018
WJetsHT800to1200_2018.dataset = '/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1_ext1-v2/NANOAODSIM'
WJetsHT800to1200_2018.process = 'WJets_2018' 
WJetsHT800to1200_2018.unix_code = 21205

WJetsHT1200to2500_2018         = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJetsHT1200to2500_2018")
WJetsHT1200to2500_2018.sigma   = 1.074 #pb
WJetsHT1200to2500_2018.year    = 2018
WJetsHT1200to2500_2018.dataset = '/WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1_ext1-v2/NANOAODSIM'
WJetsHT1200to2500_2018.process = 'WJets_2018' 
WJetsHT1200to2500_2018.unix_code = 21206

WJetsHT2500toInf_2018         = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJetsHT2500toInf_2018")
WJetsHT2500toInf_2018.sigma   = 0.008001 #pb
WJetsHT2500toInf_2018.year    = 2018
WJetsHT2500toInf_2018.dataset = '/WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM'
WJetsHT2500toInf_2018.process = 'WJets_2018'
WJetsHT2500toInf_2018.unix_code = 21207

WJets_2018 = sample(ROOT.kGreen-3, 1, 1001, "W + Jets", "WJets_2018")
WJets_2018.year = 2018
WJets_2018.components = [#WJetsHT70to100_2018, 
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

QCD_Pt_470to600_2022 = sample(ROOT.kAzure-5, 1, 1001, "QCD", "QCD_Pt_470to600_2022")
QCD_Pt_470to600_2022.sigma = 626.4#pb
QCD_Pt_470to600_2022.year = 2022
QCD_Pt_470to600_2022.dataset = "/QCD_PT-470to600_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1_ext1-v1/NANOAODSIM"
QCD_Pt_470to600_2022.process = 'QCD_2022'

QCD_Pt_1000to1400_2022 = sample(ROOT.kAzure-5, 1, 1001, "QCD", "QCD_Pt_1000to1400_2022")
QCD_Pt_1000to1400_2022.sigma = 8.92	 #pb
QCD_Pt_1000to1400_2022.year = 2022
QCD_Pt_1000to1400_2022.dataset = "/QCD_PT-1000to1400_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1_ext1-v1/NANOAODSIM"
QCD_Pt_1000to1400_2022.process = 'QCD_2022'

QCD_Pt_1800to2400_2022 = sample(ROOT.kAzure-5, 1, 1001, "QCD", "QCD_Pt_1800to2400_2022")
QCD_Pt_1800to2400_2022.sigma = 0.1148 #pb
QCD_Pt_1800to2400_2022.year = 2022
QCD_Pt_1800to2400_2022.dataset = "/QCD_PT-1800to2400_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1_ext1-v1/NANOAODSIM"
QCD_Pt_1800to2400_2022.process = "QCD_2022"

QCD_Pt_2400to3200_2022 = sample(ROOT.kAzure-5, 1, 1001, "QCD", "QCD_Pt_2400to3200_2022")
QCD_Pt_2400to3200_2022.sigma = 0.007542	 #pb
QCD_Pt_2400to3200_2022.year = 2022
QCD_Pt_2400to3200_2022.dataset = "/QCD_PT-2400to3200_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1_ext1-v1/NANOAODSIM"
QCD_Pt_2400to3200_2022.process = "QCD_2022"

QCD_Pt_3200_2022 = sample(ROOT.kAzure-5, 1, 1001, "QCD", "QCD_Pt_3200_2022")
QCD_Pt_3200_2022.sigma = 0.0002331 #pb
QCD_Pt_3200_2022.year = 2022
QCD_Pt_3200_2022.dataset = "/QCD_PT-3200_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1_ext1-v1/NANOAODSIM"
QCD_Pt_3200_2022.process = "QCD_2022"

QCD_2022 = sample(ROOT.kAzure-5, 1, 1001, "QCD", "QCD_2022")
QCD_2022.year = 2018
QCD_2022.components = [ QCD_Pt_300to470_2022, QCD_Pt_470to600_2022,  QCD_Pt_1000to1400_2022, QCD_Pt_1800to2400_2022, QCD_Pt_2400to3200_2022, QCD_Pt_3200_2022 ]

################################ TTbar ################################
TT_semilep_2022 = sample(ROOT.kViolet-4, 1, 1001, "t#bar{t}", "TT_semilep_2022")
TT_semilep_2022.sigma = 762.1 #pb
TT_semilep_2022.year = 2022
TT_semilep_2022.dataset = "/TTtoLNu2Q_TuneCP5CR1_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM"
TT_semilep_2022.process = 'TT_2022'

TT_hadr_2022 = sample(ROOT.kViolet-4, 1, 1001, "t#bar{t}", "TT_hadr_2022")
TT_hadr_2022.sigma = 762.1
TT_hadr_2022.year = 2022
TT_hadr_2022.dataset = "/TTto4Q_TuneCP5CR2_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM"
TT_hadr_2022.precess = 'TT_2022'

TT_2022 = sample(ROOT.kViolet-4, 1, 1001, "t#bar{t}", "TT_2022")
TT_2022.year = 2022
TT_2022.components = [TT_semilep_2022, TT_hadr_2022]

# ROOT.kSpring+3 per ZJetsToNuNu

########################### DATA 2018 ############################################
DataHTA_2018         = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTA_2018")
DataHTA_2018.runP    = 'A'
DataHTA_2018.year    = 2018
DataHTA_2018.dataset = '/MET/Run2018A-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD'

DataHTB_2018         = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTB_2018")
DataHTB_2018.runP    = 'B'
DataHTB_2018.year    = 2018
DataHTB_2018.dataset = '/MET/Run2018B-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD'
DataHTC_2018         = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTC_2018")
DataHTC_2018.runP    = 'C'
DataHTC_2018.year    = 2018
DataHTC_2018.dataset = '/MET/Run2018C-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD'
DataHTD_2018         = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTD_2018")
DataHTD_2018.runP    = 'D'
DataHTD_2018.year    = 2018
DataHTD_2018.dataset = '/MET/Run2018D-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD'
DataHT_2018            = sample(ROOT.kBlack, 1, 1001, "Data", "DataHT_2018")
DataHT_2018.year       = 2018
DataHT_2018.components = [DataHTA_2018, DataHTB_2018, 
                          DataHTC_2018#, DataHTD_2018
                          ]

########################### DATA 2022 ############################################
DataHTC_2022 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTC_2022")
DataHTC_2022.runP = 'C'
DataHTC_2022.year = 2022
DataHTC_2022.dataset = '/JetMET/Run2022C-ReRecoNanoAODv11-v1/NANOAOD'

DataHTD_2022 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTD_2022")
DataHTD_2022.runP = 'D'
DataHTD_2022.year = 2022
DataHTD_2022.dataset = '/JetMET/Run2022D-ReRecoNanoAODv11-v1/NANOAOD'

DataHTE_2022 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTE_2022")
DataHTE_2022.runP = 'E'
DataHTE_2022.year = 2022
DataHTE_2022.dataset = '/JetMET/Run2022E-ReRecoNanoAODv11-v1/NANOAOD'

DataHTF_2022 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTF_2022")
DataHTF_2022.runP = 'F'
DataHTF_2022.year = 2022
DataHTF_2022.dataset = '/JetMET/Run2022F-PromptNanoAODv11_v1-v2/NANOAOD'
  
DataHTG_2022 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHTG_2022")
DataHTG_2022.runP = 'G'
DataHTG_2022.year = 2022
DataHTG_2022.dataset = '/JetMET/Run2022G-PromptNanoAODv11_v1-v2/NANOAOD'

DataHT_2022 = sample(ROOT.kBlack, 1, 1001, "Data", "DataHT_2022")
DataHT_2022.year = 2022
DataHT_2022.components = [DataHTC_2022, DataHTD_2022, DataHTE_2022, DataHTF_2022, DataHTG_2022]

############### code meanings ################
# XXXXX  5 digits for each sample
# 1st digit: 0 for 2016, 1 for 2017, 2 for 2018, 3 for 2022, 4 for 2023
# 2nd digit: 0 for data, 1 for MC bkg, 2 for MC signal
# 3rd digit: for the process (QCD = 0, TT = 1, ZJets = 2, WJets = 3, 
#                             Tprime = 0, tDM = 1, 
#                             Data_MET = 0, Data_XX = 1,...)
# 3rd digit and 4th digit: 2 digits identifies the sample 

# example: QCDHT_100to200_2018 == 21000, QCDHT_200to300_2018 == 21001
#          DATAHTA_2018 == 20600, DATAHTB_2018 == 20601, DATAHTC_2018 == 20602, DATAHTD_2018 == 20603  
### non diamo un codice ai sample con le components --> da capire se serve aggiungerlo


sample_dict = {

    ################################## RUN II
    # Data MET 2018   
    'DataHT_2018': DataHT_2018, 'DataHTA_2018': DataHTA_2018, 'DataHTB_2018': DataHTB_2018, 
    'DataHTC_2018': DataHTC_2018, #'DataHTD_2018': DataHTD_2018,
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
    'DataHT_2022': DataHT_2022, 'DataHTC_2022':DataHTC_2022, 'DataHTD_2022':DataHTD_2022, 'DataHTE_2022':DataHTE_2022, 'DataHTF_2022':DataHTF_2022, 'DataHTG_2022':DataHTG_2022
    }
