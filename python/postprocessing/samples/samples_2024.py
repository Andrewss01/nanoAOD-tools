import ROOT
import os 

path = os.path.dirname(os.path.abspath(__file__))

class sample:
    def __init__(self, color, style, fill, leglabel, label ):
        self.color = color
        self.style = style
        self.fill = fill
        self.leglabel = leglabel
        self.label = label


########################################################################################
###################################2024#################################################
########################################################################################


#================================================================================
#================================TTbar===========================================
#================================================================================

TT_Semilep_2024 = sample(ROOT.kOrange,1,1001,"t#bar{t}","TT_Semilep_2024")
TT_Semilep_2024.sigma  = 404#pb
TT_Semilep_2024.year = 2024
TT_Semilep_2024.dataset = "/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/RunIII2024Summer24NanoAODv15-150X_mcRun3_2024_realistic_v2-v2/NANOAODSIM"
TT_Semilep_2024.process = "TTbar_semilep_2024" 
TT_Semilep_2024.unix_code = 31100
TT_Semilep_2024.EE = 0

TT_Dileptonic_2024 = sample(ROOT.kOrange,1,1001,"t#bar{t}","TT_Dilep_2024")
TT_Dileptonic_2024.sigma = 96.6  #pb
TT_Dileptonic_2024.year = 2024
TT_Dileptonic_2024.dataset = "/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/RunIII2024Summer24NanoAODv15-150X_mcRun3_2024_realistic_v2-v3/NANOAODSIM"
TT_Dileptonic_2024.process = "TT_Dileptonic_2024"
TT_Dileptonic_2024.unix_code = 31101
TT_Dileptonic_2024.EE = 0

TT_bar_2024 = sample (ROOT.kGreen-3,1,1001,"t#bar{t}","TT_bar_2024")
TT_bar_2024.year = 2024
TT_bar_2024.components = [TT_Semilep_2024,TT_Dileptonic_2024]

#===============================================================================
#==============================Signal 4Fs=======================================
#===============================================================================
#

tWb_Signal_4FS_T = sample(ROOT.kRed,1,1002,"ST_{bb}","TBbarQ")
tWb_Signal_4FS_T.sigma = 146.1 #pb
tWb_Signal_4FS_T.year = 2024
tWb_Signal_4FS_T.dataset = "/TBbarQtoLNu-t-channel-4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8/RunIII2024Summer24NanoAODv15-150X_mcRun3_2024_realistic_v2-v2/NANOAODSIM"
tWb_Signal_4FS_T.process = "TBbarQ"
tWb_Signal_4FS_T.unix_code = 31102 
tWb_Signal_4FS_T.EE = 0
#

#tWb_Signal_4FS_T_1 = sample(ROOT.kRed,1,1002,"t#bar{b}_4Fs","TBbarQ")
tWb_Signal_4FS_T_1 = sample(ROOT.kRed,1,1002,"ST_{bb}","TBbarQ")
tWb_Signal_4FS_T_1.sigma = 146.1 #pb
tWb_Signal_4FS_T_1.year = 2024
tWb_Signal_4FS_T_1.dataset = "/TBbarQtoLNu-t-channel-4FS_TuneCP5Up_13p6TeV_powheg-madspin-pythia8/RunIII2024Summer24NanoAODv15-150X_mcRun3_2024_realistic_v2-v2/NANOAODSIM"
tWb_Signal_4FS_T_1.process = "TBbarQ"
tWb_Signal_4FS_T_1.unix_code = 31102
tWb_Signal_4FS_T_1.EE = 0 


tWb_Signal_4FS_T_bar = sample(ROOT.kRed,1,1002,"ST_{bb}","TbarBQ")
tWb_Signal_4FS_T_bar.sigma = 88.15 #pb 
tWb_Signal_4FS_T_bar.year = 2024
tWb_Signal_4FS_T_bar.dataset = "/TbarBQtoLNu-t-channel-4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8/RunIII2024Summer24NanoAODv15-150X_mcRun3_2024_realistic_v2-v2/NANOAODSIM"
tWb_Signal_4FS_T_bar.process = "TbarBQ"
tWb_Signal_4FS_T_bar.unix_code = 31102
tWb_Signal_4FS_T_bar.EE = 0 

tWb_Signal_4FS_T_bar_1 = sample(ROOT.kRed,1,1002,"ST_{bb}","TbarBQ")
tWb_Signal_4FS_T_bar_1.sigma = 88.15 #pb
tWb_Signal_4FS_T_bar_1.year = 2024
tWb_Signal_4FS_T_bar_1.dataset = "/TbarBQtoLNu-t-channel-4FS_TuneCP5_13p6TeV_powheg-madspin-pythia8/RunIII2024Summer24NanoAODv15-BTVNanoV15_150X_mcRun3_2024_realistic_v2-v1/NANOAODSIM"
tWb_Signal_4FS_T_bar_1.process = "TbarBQ"
tWb_Signal_4FS_T_bar_1.unix_code = 31102
tWb_Signal_4FS_T_bar_1.EE = 0



#
tWb_Signal_4FS = sample(ROOT.kRed,1,1002,"tWb_Signal","tWb_Signal_4FS")
tWb_Signal_4FS.year = 2024
tWb_Signal_4FS.components = [tWb_Signal_4FS_T,tWb_Signal_4FS_T_bar]
#


#===================================================================================
#================================W+jets=============================================
#===================================================================================


W_to_2Jets_Ele = sample(ROOT.kGreen,1,1003,"W+Jets","W_to_2Jets_Ele") 
W_to_2Jets_Ele.sigma = 6800 #pb
W_to_2Jets_Ele.year = 2024
W_to_2Jets_Ele.dataset = "/WtoENu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/RunIII2024Summer24NanoAODv15-150X_mcRun3_2024_realistic_v2-v3/NANOAODSIM"
W_to_2Jets_Ele.process = "W+Jets"
W_to_2Jets_Ele.unix_code = 31103
W_to_2Jets_Ele.EE = 0


W_to_2Jets_Mu = sample(ROOT.kGreen,1,1003,"W+Jets","W_to_2Jets_Mu")
W_to_2Jets_Mu.sigma =  6800 #pb
W_to_2Jets_Mu.year = 2024
W_to_2Jets_Mu.dataset = "/WtoMuNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/RunIII2024Summer24NanoAODv15-150X_mcRun3_2024_realistic_v2-v3/NANOAODSIM"
W_to_2Jets_Mu.process = "W+Jets"
W_to_2Jets_Mu.unix_code = 31103
W_to_2Jets_Mu.EE = 0



W_to_Jets = sample(ROOT.kGreen,1,1003,"W+Jets","W_to_Jets")
W_to_Jets.year = 2024
W_to_Jets.components = [W_to_2Jets_Mu,W_to_2Jets_Ele]



#==============================================================================
#=========================W and Top============================================
#==============================================================================


Top_W_minus_Lepton_2Q = sample(ROOT.kYellow,1,1004,"tW","Top_W_minus_Lepton_2Q")
Top_W_minus_Lepton_2Q.sigma = 13#pb
Top_W_minus_Lepton_2Q.year = 2024
Top_W_minus_Lepton_2Q.dataset = "/TWminustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/RunIII2024Summer24NanoAODv15-150X_mcRun3_2024_realistic_v2-v2/NANOAODSIM"
Top_W_minus_Lepton_2Q.process = "tW"
Top_W_minus_Lepton_2Q.unix_code = 31104
Top_W_minus_Lepton_2Q.EE = 0


Top_W_minus_2Lepton = sample(ROOT.kYellow,1,1004,"tW","Top_W_minus_2Lepton")
Top_W_minus_2Lepton.sigma = 3.37 #pb
Top_W_minus_2Lepton.year = 2024
Top_W_minus_2Lepton.dataset = "/TWminusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/RunIII2024Summer24NanoAODv15-150X_mcRun3_2024_realistic_v2-v2/NANOAODSIM"
Top_W_minus_2Lepton.process = "tW"
Top_W_minus_2Lepton.unix_code = 31104
Top_W_minus_2Lepton.EE = 0


Top_W_plus_Lepton_2Q = sample(ROOT.kYellow,1,1004,"tW","Top_W_plus_Lepton_2Q")
Top_W_plus_Lepton_2Q.sigma = 13 #pb
Top_W_plus_Lepton_2Q.year = 2024
Top_W_plus_Lepton_2Q.dataset = "/TbarWplustoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/RunIII2024Summer24NanoAODv15-150X_mcRun3_2024_realistic_v2-v2/NANOAODSIM"
Top_W_plus_Lepton_2Q.process = "tW"
Top_W_plus_Lepton_2Q.unix_code = 31104
Top_W_plus_Lepton_2Q.EE = 0

Top_W_plus_2Lepton = sample(ROOT.kYellow,1,1004,"tW","Top_W_plus_2Lepton")
Top_W_plus_2Lepton.sigma = 3.37 #pb
Top_W_plus_2Lepton.year = 2024
Top_W_plus_2Lepton.dataset = "/TbarWplusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/RunIII2024Summer24NanoAODv15-150X_mcRun3_2024_realistic_v2-v2/NANOAODSIM"
Top_W_plus_2Lepton.process = "tW"
Top_W_plus_2Lepton.unix_code = 31104
Top_W_plus_2Lepton.EE = 0



tW = sample(ROOT.kRed,1,1004,"tW","tW")
tW.year = 2024
tW.components = [Top_W_minus_Lepton_2Q,Top_W_minus_2Lepton,Top_W_plus_Lepton_2Q,Top_W_plus_2Lepton]



#Dictionary

sample_dict = {
    "TT_Semilep_2024" : TT_Semilep_2024,
    "TT_Dileptonic_2024" : TT_Dileptonic_2024,
    "tWb_Signal_4FS_T" : tWb_Signal_4FS_T,
    "tWb_Signal_4FS_T_bar" : tWb_Signal_4FS_T_bar,
    "Top_W_minus_Lepton_2Q" : Top_W_minus_Lepton_2Q,
    "Top_W_minus_2Lepton" : Top_W_minus_2Lepton,
    "W_to_2Jets_Mu"  : W_to_2Jets_Mu,
    "W_to_2Jets_Ele" : W_to_2Jets_Ele

}
