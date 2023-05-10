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

################################ TTbar ################################

TT_Mtt700to1000_2018 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_Mtt700to1000_2018")
TT_Mtt700to1000_2018.sigma = 80.5 #pb
TT_Mtt700to1000_2018.year = 2018
TT_Mtt700to1000_2018.dataset = "/TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8/"+tag_2018+"-v1/NANOAODSIM"
TT_Mtt700to1000_2018.local_path= "/eos/home-a/acagnott/DarkMatter/topcandidate_file/TT_Mtt-700to1000_2018_Skim.root"
TT_Mtt700to1000_2018.process = 'TT_2018'

TT_Mtt1000toInf_2018 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_Mtt1000toInf_2018")
TT_Mtt1000toInf_2018.sigma = 21.3 #pb
TT_Mtt1000toInf_2018.year = 2018
TT_Mtt1000toInf_2018.dataset = "/TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8/"+tag_2018+"-v1/NANOAODSIM"
TT_Mtt1000toInf_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/TT_Mtt-1000toInf_2018_Skim.root"
TT_Mtt1000toInf_2018.process = 'TT_2018'

TT_semilep_2018 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_semilep_2018")
TT_semilep_2018.sigma = 831.76*0.438 #pb
TT_semilep_2018.year = 2018
TT_semilep_2018.dataset = "/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/" + tag_2018 + "-v1/NANOAODSIM"
TT_semilep_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/TT_SemiLep_2018_Skim.root"
TT_semilep_2018.process = 'TT_2018'

TT_hadr_2018 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_hadr_2018")
TT_hadr_2018.sigma = 831.76*((1-0.324)**2) #pb
TT_hadr_2018.year = 2018
TT_hadr_2018.dataset = "/TTToHadronic_TuneCP5_13TeV-powheg-pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM"
TT_hadr_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/TT_Hadr_2018_Skim.root"
TT_hadr_2018.process = 'TT_2018'

TT_2018 = sample(ROOT.kRed, 1, 1001, "t#bar{t}", "TT_2018")
TT_2018.year= 2018
TT_2018.components=[TT_hadr_2018, TT_semilep_2018, TT_Mtt1000toInf_2018, TT_Mtt700to1000_2018]

################################ QCD ################################
QCDHT_300to500_2018 = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_300to500_2018")
QCDHT_300to500_2018.sigma = 347700 #pb
QCDHT_300to500_2018.year = 2018
QCDHT_300to500_2018.dataset = "/QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
QCDHT_300to500_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/QCD_HT300to500_2018_Skim.root"
QCDHT_300to500_2018.process = 'QCD_2018'

QCDHT_500to700_2018 = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_500to700_2018")
QCDHT_500to700_2018.sigma = 32100 #pb
QCDHT_500to700_2018.year = 2018
QCDHT_500to700_2018.dataset = "/QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
QCDHT_500to700_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/QCD_HT500to700_2018_Skim.root"
QCDHT_500to700_2018.process = 'QCD_2018'

QCDHT_700to1000_2018 = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_700to1000_2018")
QCDHT_700to1000_2018.sigma = 6831 #pb
QCDHT_700to1000_2018.year = 2018
QCDHT_700to1000_2018.dataset = "/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
QCDHT_700to1000_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/QCD_HT700to1000_2018_Skim.root"
QCDHT_700to1000_2018.process = 'QCD_2018'

QCDHT_1000to1500_2018 = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_1000to1500_2018")
QCDHT_1000to1500_2018.sigma = 1207 #pb
QCDHT_1000to1500_2018.year = 2018
QCDHT_1000to1500_2018.dataset = "/QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
QCDHT_1000to1500_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/QCD_HT1000_Skim.root"
QCDHT_1000to1500_2018.process = 'QCD_2018'

QCDHT_1500to2000_2018 = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_1500to2000_2018")
QCDHT_1500to2000_2018.sigma = 119.9 #pb
QCDHT_1500to2000_2018.year = 2018
QCDHT_1500to2000_2018.dataset = "/QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
QCDHT_1500to2000_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/QCD-HT1500to2000_2018_Skim.root"
QCDHT_1500to2000_2018.process = 'QCD_2018'

QCDHT_2000toInf_2018 = sample(ROOT.kGray, 1, 1001, "QCD", "QCDHT_2000toInf_2018")
QCDHT_2000toInf_2018.sigma = 25.24 #pb   #####
QCDHT_2000toInf_2018.year = 2018
QCDHT_2000toInf_2018.dataset = "/QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8/"+tag_2018+"-v1/NANOAODSIM"
QCDHT_2000toInf_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/QCD-HT2000toInf_2018_Skim.root"
QCDHT_2000toInf_2018.process = 'QCD_2018'

QCD_2018 = sample(ROOT.kGray, 1, 1001, "QCD", "QCD_2018")
QCD_2018.year = 2018
QCD_2018.components = [QCDHT_300to500_2018, QCDHT_500to700_2018, QCDHT_700to1000_2018, QCDHT_1000to1500_2018, QCDHT_1500to2000_2018, QCDHT_2000toInf_2018]
#QCD_2018.components = [QCDHT_300to500_2018, QCDHT_500to700_2018, QCDHT_1000to1500_2018, QCDHT_1500to2000_2018, QCDHT_2000toInf_2018]

################################ ZJetsToNuNu ################################
ZJetsToNuNu_HT100to200_2018 = sample(ROOT.kAzure+6, 1, 1001, "ZJets HT-100To200", "ZJetsToNuNu_HT100to200_2018")
ZJetsToNuNu_HT100to200_2018.sigma = 280.35*1.37 #pb
ZJetsToNuNu_HT100to200_2018.year = 2018
ZJetsToNuNu_HT100to200_2018.dataset = '/ZJetsToNuNu_HT-100To200_13TeV-madgraph/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM'
ZJetsToNuNu_HT100to200_2018.local_path = '/eos/home-a/acagnott/DarkMatter/topcandidate_file/ZJetsToNuNu_HT100to200_2018_Skim.root'
ZJetsToNuNu_HT100to200_2018.process = 'ZJetsToNuNu_2018'

ZJetsToNuNu_HT200to400_2018 = sample(ROOT.kAzure+6, 1, 1001, "ZJets HT-200To400", "ZJetsToNuNu_HT200to400_2018")
ZJetsToNuNu_HT200to400_2018.sigma =  77.67*1.52 #pb
ZJetsToNuNu_HT200to400_2018.year = 2018
ZJetsToNuNu_HT200to400_2018.dataset = '/ZJetsToNuNu_HT-200To400_13TeV-madgraph/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM'
ZJetsToNuNu_HT200to400_2018.local_path = '/eos/home-a/acagnott/DarkMatter/topcandidate_file/ZJetsToNuNu_HT200to400_2018_Skim.root'
ZJetsToNuNu_HT200to400_2018.process = 'ZJetsToNuNu_2018'

ZJetsToNuNu_HT400to600_2018 = sample(ROOT.kAzure+6, 1, 1001, "ZJetsToNuNu HT-400To600", "ZJetsToNuNu_HT400to600_2018")
ZJetsToNuNu_HT400to600_2018.sigma = 10.73*1.37 #pb
ZJetsToNuNu_HT400to600_2018.year = 2018
ZJetsToNuNu_HT400to600_2018.dataset = '/ZJetsToNuNu_HT-400To600_TuneCP5_13TeV-madgraph/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM'
ZJetsToNuNu_HT400to600_2018.local_path = '/eos/home-a/acagnott/DarkMatter/topcandidate_file/ZJetsToNuNu_HT400to600_2018_Skim.root'
ZJetsToNuNu_HT400to600_2018.process = 'ZJetsToNuNu_2018'

ZJetsToNuNu_HT600to800_2018 = sample(ROOT.kAzure+6, 1, 1001, "ZJetsToNuNu HT-600To800", "ZJetsToNuNu_HT600to800_2018")
ZJetsToNuNu_HT600to800_2018.sigma = 2.56*1.04 #pb
ZJetsToNuNu_HT600to800_2018.year = 2018
ZJetsToNuNu_HT600to800_2018.dataset = '/ZJetsToNuNu_HT-600To800_13TeV-madgraph/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM'
ZJetsToNuNu_HT600to800_2018.local_path = '/eos/home-a/acagnott/DarkMatter/topcandidate_file/ZJetsToNuNu_HT600to800_2018_Skim.root'
ZJetsToNuNu_HT600to800_2018.process = 'ZJetsToNuNu_2018'

ZJetsToNuNu_HT800to1200_2018 = sample(ROOT.kAzure+6, 1, 1001, "ZJetsToNuNu HT-800To1200", "ZJetsToNuNu_HT800to1200_2018")
ZJetsToNuNu_HT800to1200_2018.sigma = 1.18*1.14 #pb
ZJetsToNuNu_HT800to1200_2018.year = 2018
ZJetsToNuNu_HT800to1200_2018.dataset = '/ZJetsToNuNu_HT-800To1200_13TeV-madgraph/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM'
ZJetsToNuNu_HT800to1200_2018.local_path = '/eos/home-a/acagnott/DarkMatter/topcandidate_file/ZJetsToNuNu_HT800to1200_2018_Skim.root'
ZJetsToNuNu_HT800to1200_2018.process = 'ZJetsToNuNu_2018'

ZJetsToNuNu_HT1200to2500_2018 = sample(ROOT.kAzure+6, 1, 1001, "ZJetsToNuNu HT-1200To2500", "ZJetsToNuNu_HT1200to2500_2018")
ZJetsToNuNu_HT1200to2500_2018.sigma = 0.29*0.88 #pb
ZJetsToNuNu_HT1200to2500_2018.year = 2018
ZJetsToNuNu_HT1200to2500_2018.dataset = '/ZJetsToNuNu_HT-1200To2500_13TeV-madgraph/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM'
ZJetsToNuNu_HT1200to2500_2018.local_path = '/eos/home-a/acagnott/DarkMatter/topcandidate_file/ZJetsToNuNu_HT1200to2500_2018_Skim.root'
ZJetsToNuNu_HT1200to2500_2018.process = 'ZJetsToNuNu_2018'

ZJetsToNuNu_HT2500toInf_2018 = sample(ROOT.kAzure+6, 1, 1001, "ZJetsToNuNu HT-2500ToInf", "ZJetsToNuNu_HT2500toInf_2018")
ZJetsToNuNu_HT2500toInf_2018.sigma = 0.007*0.88 #pb
ZJetsToNuNu_HT2500toInf_2018.year = 2018
ZJetsToNuNu_HT2500toInf_2018.dataset = '/ZJetsToNuNu_HT-2500ToInf_13TeV-madgraph/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM'
ZJetsToNuNu_HT2500toInf_2018.local_path = '/eos/home-a/acagnott/DarkMatter/topcandidate_file/ZJetsToNuNu_HT2500toInf_2018_Skim.root'
ZJetsToNuNu_HT2500toInf_2018.process = 'ZJetsToNuNu_2018'

ZJetsToNuNu_2018 = sample(ROOT.kAzure+6, 1, 1001, "ZJetsToNuNu", "ZJetsToNuNu_2018")
ZJetsToNuNu_2018.year = 2018
ZJetsToNuNu_2018.components = [ZJetsToNuNu_HT100to200_2018, ZJetsToNuNu_HT200to400_2018, ZJetsToNuNu_HT400to600_2018, ZJetsToNuNu_HT600to800_2018, ZJetsToNuNu_HT800to1200_2018, ZJetsToNuNu_HT1200to2500_2018, ZJetsToNuNu_HT2500toInf_2018]
#ZJetsToNuNu_2018.components = [ZJetsToNuNu_HT100to200_2018, ZJetsToNuNu_HT200to400_2018, ZJetsToNuNu_HT400to600_2018, ZJetsToNuNu_HT600to800_2018, ZJetsToNuNu_HT1200to2500_2018, ZJetsToNuNu_HT2500toInf_2018]

################################ Signal tDM ################################

tDM_mPhi1000_mChi1_2018 = sample(ROOT.kGreen+2, 1, 1001, "DM (m_{#Phi}=1000)", "tDM_mPhi1000_mChi1_2018")
tDM_mPhi1000_mChi1_2018.sigma = 24.99 *0.00001 #*100    #pb  aggiunto*100 per i plot
tDM_mPhi1000_mChi1_2018.year = 2018
tDM_mPhi1000_mChi1_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/tDM_mPhi1000_mChi1_Skim.root"

tDM_mPhi500_mChi1_2018 = sample(ROOT.kGreen+1, 1, 1001, "DM (m_{#Phi}=500)", "tDM_mPhi500_mChi1_2018")
tDM_mPhi500_mChi1_2018.year = 2018
tDM_mPhi500_mChi1_2018.sigma = 43.85 *0.0001  #pb
tDM_mPhi500_mChi1_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/tDM_mPhi500_mChi1_Skim.root"

tDM_mPhi50_mChi1_2018= sample(ROOT.kGreen, 1, 1001, "DM (m_{#Phi}=50)", "tDM_mPhi50_mChi1_2018")
tDM_mPhi50_mChi1_2018.year = 2018
tDM_mPhi50_mChi1_2018.sigma = 0.7  #pb
tDM_mPhi50_mChi1_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/tDM_mPhi50_mChi1_Skim.root"

################################ Signal Tprime ################################

TprimeToTZ_1800_2018 = sample(ROOT.kGreen+4, 1, 1001, "T#rightarrow tZ M1800GeV", "TprimeToTZ_1800_2018")
TprimeToTZ_1800_2018.sigma = 0.00045 #pb
TprimeToTZ_1800_2018.year = 2018
TprimeToTZ_1800_2018.dataset = '/TprimeBToTZ_M-1800_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM'
TprimeToTZ_1800_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/"+TprimeToTZ_1800_2018.label +"_Skim.root"

TprimeToTZ_1000_2018 = sample(ROOT.kGreen+2, 1, 1001, "T#rightarrow TZ M1000GeV", "TprimeToTZ_1000_2018")
TprimeToTZ_1000_2018.sigma = 0.01362 #pb
TprimeToTZ_1000_2018.year = 2018
TprimeToTZ_1000_2018.dataset = '/TprimeBToTZ_M-1000_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/NANOAODSIM'
TprimeToTZ_1000_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/"+TprimeToTZ_1000_2018.label +"_Skim.root"

TprimeToTZ_700_2018 = sample(ROOT.kGreen, 1, 1001, "T#rightarrow tZ M700GeV", "TprimeToTZ_700_2018")
TprimeToTZ_700_2018.sigma = 0.07804 #pb
TprimeToTZ_700_2018.year = 2018
TprimeToTZ_700_2018.dataset = '/TprimeBToTZ_M-700_LH_TuneCP5_PSweights_13TeV-madgraph_pythia8/RunIIAutumn18NanoAODv7-Nano02Apr2020_102X_upgrade2018_realistic_v21_ext1-v1/NANOAODSIM'
TprimeToTZ_700_2018.local_path = "/eos/home-a/acagnott/DarkMatter/topcandidate_file/"+TprimeToTZ_700_2018.label +"_Skim.root"

sample_dict = {
    'TT_Mtt700to1000_2018':TT_Mtt700to1000_2018, 'TT_Mtt1000toInf_2018':TT_Mtt1000toInf_2018, 'TT_semilep_2018':TT_semilep_2018, 'TT_hadr_2018':TT_hadr_2018,'TT_2018':TT_2018,
    'QCDHT_300to500_2018':QCDHT_300to500_2018, 'QCDHT_500to700_2018':QCDHT_500to700_2018, 'QCDHT_700to1000_2018':QCDHT_700to1000_2018, 
    'QCDHT_1000to1500_2018':QCDHT_1000to1500_2018, 'QCDHT_1500to2000_2018':QCDHT_1500to2000_2018, 'QCDHT_2000toInf_2018':QCDHT_2000toInf_2018, 'QCD_2018':QCD_2018, 
    'ZJetsToNuNu_HT100to200_2018':ZJetsToNuNu_HT100to200_2018, 'ZJetsToNuNu_HT200to400_2018':ZJetsToNuNu_HT200to400_2018, 
    'ZJetsToNuNu_HT400to600_2018':ZJetsToNuNu_HT400to600_2018, 'ZJetsToNuNu_HT600to800_2018':ZJetsToNuNu_HT600to800_2018, 
    'ZJetsToNuNu_HT800to1200_2018':ZJetsToNuNu_HT800to1200_2018, 'ZJetsToNuNu_HT1200to2500_2018':ZJetsToNuNu_HT1200to2500_2018, 
    'ZJetsToNuNu_HT2500toInf_2018':ZJetsToNuNu_HT2500toInf_2018, 'ZJetsToNuNu_2018':ZJetsToNuNu_2018,
    'tDM_mPhi50_mChi1_2018' : tDM_mPhi50_mChi1_2018, 'tDM_mPhi500_mChi1_2018' : tDM_mPhi500_mChi1_2018,'tDM_mPhi1000_mChi1_2018' : tDM_mPhi1000_mChi1_2018,
    'TprimeToTZ_1800_2018' : TprimeToTZ_1800_2018, 'TprimeToTZ_1000_2018' : TprimeToTZ_1000_2018, 'TprimeToTZ_700_2018' : TprimeToTZ_700_2018
    }
