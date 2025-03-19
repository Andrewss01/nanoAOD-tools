import ROOT

from modules.ExampleModule import ExampleAnalysis

from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopEvaluate_MultiScore_v3 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopEvaluate_MultiScore_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp import *
from modules.selection import *

#files=["Datasets/ZJ_2.root"]
#files = ['Datasets/ZJ_1.root']
#files = ['Datasets/TT.root']

#files_toselect = ['ZJ_1_Skim.root']
#files_toselect = ['ZJ_2_Skim.root']
#files_toselect =  ['Datasets/TT_Skim.root']

#files_toeval = ['Datasets/ZJ_1_Skim.root']

#files_toeval = ['Datasets/ZJ_2_Skim.root']
files_toeval = ['Datasets/TT_Skim_10k.root']
#files_toeval = ["root://xrootd-cms.infn.it//store/mc/Run3Winter22NanoAOD/TTToSemiLeptonic_TuneCP5_13p6TeV-powheg-pythia8/NANOAODSIM/FlatPU0to70_pilot_122X_mcRun3_2021_realistic_v9-v1/30000/98dec374-b9cb-4725-9838-422a5968c486.root"]
evaluate= True
create_file_select = False
select =  False

# #Il primo prende il file, fa lo Skim e poi lo valuta con il modello che scegli in input
if create_file_select:
    p=PostProcessor(".",files,branchsel=None,modules=[GenPart_MomFirstCp(flavour = '-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'), nanoprepro(), nanoTopcand(isMC = True), Selection()]
                    ,histFileName="histOut.root",histDirName="plots", postfix = '_Skim', outputbranchsel=os.path.abspath('PhysicsTools/NanoAODTools/scripts/keep_and_drop.txt'))
    p.run()
    
if select:
    p=PostProcessor(".",files_toselect,branchsel=None,histFileName="histOut.root",histDirName="plots",  postfix = '_CutPt', outputbranchsel=os.path.abspath('PhysicsTools/NanoAODTools/scripts/keep_and_drop.txt'), maxEntries = 10000)
    p.run()
    
if evaluate: 
    p=PostProcessor(".",files_toeval,branchsel=None,modules=[nanoTopevaluate_MultiScore(model = 'MC')]
                    ,histFileName="histOut.root",histDirName="plots", postfix = '_ScoresMS', 
outputbranchsel=os.path.abspath('PhysicsTools/NanoAODTools/scripts/keep_and_drop.txt'), maxEntries = 10000)
    p.run()

# # 1  è associato al modello TT
# # 2 è associato a TTvs ZJ no bkg

#file = ROOT.TFile.Open("root://xrootd-cms.infn.it//store/mc/Run3Winter22NanoAOD/TTToSemiLeptonic_TuneCP5_13p6TeV-powheg-pythia8/NANOAODSIM/FlatPU0to70_pilot_122X_mcRun3_2021_realistic_v9-v1/30000/98dec374-b9cb-4725-9838-422a5968c486.root", "READ")
# file = ROOT.TFile.Open('Datasets/TT_Skim_10k.root', 'read')
# tree = file.Get('Events')
# tree.Print('FatJet_particleNet*')