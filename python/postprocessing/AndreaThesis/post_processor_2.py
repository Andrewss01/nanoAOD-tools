import ROOT

# from modules.ExampleModule import ExampleAnalysis
import sys
#sys.path.append('/afs/cern.ch/user/a/apuglia/CMSSW_14_1_7/src/')
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2 import *
from ML.NanoTopCandidate_PF_SV import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopEvaluate_MultiScore_v3 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopEvaluate_MultiScore_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import * 
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.ExampleModule import *
#from modules.selection import *
# from PhysicsTools.NanoAODTools.postprocessing.ML.NanoTopCandidate import *
from ML.idx_PFC_SV import *
from ML.deltaR_PF_SV import * 
import os
import sys
path  ='/eos/user/a/apuglia/thesis/Datasets/'
#files=["Datasets/ZJ_2.root"]
#files = ['Datasets/ZJ_1.root']
files = [path + 'TT.root']

#files_toselect = ['ZJ_1_Skim.root']
#files_toselect = ['ZJ_2_Skim.root']
#files_toselect =  ['Datasets/TT_Skim.root']

#files_toeval = ['Datasets/ZJ_1_Skim.root']

#files_toeval = ['Datasets/ZJ_2_Skim.root']
#files_toeval = ['Datasets/TT_Skim_10k.root']
#files_toeval = ["root://xrootd-cms.infn.it//store/mc/Run3Winter22NanoAOD/TTToSemiLeptonic_TuneCP5_13p6TeV-powheg-pythia8/NANOAODSIM/FlatPU0to70_pilot_122X_mcRun3_2021_realistic_v9-v1/30000/98dec374-b9cb-4725-9838-422a5968c486.root"]
evaluate= False
create_file_select = True
select =  False

create_histo  = False



# fnames = [sys.argv[1]]
# label = sys.argv[4]

fnames = ["/eos/user/o/oiorio/tDM/PFNano/nano_mcRun3_ttsl1.root"]
# Idx_PF()
#deltaR_PF(), nanoprepro(), nanoTopcand(isMC = True)
# #Il primo prende il file, fa lo Skim e poi lo valuta con il modello che scegli in input
if create_file_select:
    p=PostProcessor("/eos/user/a/apuglia/thesis/Datasets/",fnames,branchsel=None,modules=[GenPart_MomFirstCp(flavour = '-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'), Idx_PFC_SV(), deltaR_PF_SV(),
                                                                                         collectionMerger(input = ['PFCands'], output = "PFCands", sortkey=lambda x: x.pt, reverse = True, selector = None, maxObjects = None),
                                                                                         collectionMerger(input = ['SV'], output = "SV", sortkey=lambda x: x.ntracks, reverse = True, selector = None, maxObjects = None), nanoprepro(), nanoTopcand_PFC_SV()]
                    ,histFileName="histOut.root",histDirName="plots", postfix = '_debug', outputbranchsel="%s/src/PhysicsTools/NanoAODTools/scripts/keep_and_drop_jets_pf_sv.txt" % os.environ["CMSSW_BASE"], maxEntries = 10)
    p.run()
    
# if create_histo:
#     p = PostProcessor("/eos/user/a/apuglia/thesis/Datasets/", files , branchsel = None, modules = [GenPart_MomFirstCp(flavour = '-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'), nanoprepro(), nanoTopcand(), ExampleAnalysis()], 
#                       histFileName='histOut.root', histDirName = 'plots', postfix = '_prova', maxEntries = 1000,  noOut=True)
# if select:
#     p=PostProcessor("/eos/user/a/apuglia/SWAN_projects/thesis/CMSSW_14_1_7/src/Datasets/",files_toselect,branchsel=None,histFileName="histOut.root",histDirName="plots",  postfix = '_CutPt', outputbranchsel=os.path.abspath('PhysicsTools/NanoAODTools/scripts/keep_and_drop.txt'), maxEntries = 1000)
#     p.run()
    
# if evaluate: 
#     p=PostProcessor(".",files_toeval,branchsel=None,modules=[nanoTopevaluate_MultiScore(model = 'MC')]
#                     ,histFileName="histOut.root",histDirName="plots", postfix = '_ScoresMS', 
# outputbranchsel=os.path.abspath('PhysicsTools/NanoAODTools/scripts/keep_and_drop.txt'), maxEntries = 10000)
#     p.run()

# # 1  è associato al modello TT
# # 2 è associato a TTvs ZJ no bkg

#file = ROOT.TFile.Open("root://xrootd-cms.infn.it//store/mc/Run3Winter22NanoAOD/TTToSemiLeptonic_TuneCP5_13p6TeV-powheg-pythia8/NANOAODSIM/FlatPU0to70_pilot_122X_mcRun3_2021_realistic_v9-v1/30000/98dec374-b9cb-4725-9838-422a5968c486.root", "READ")
# file = ROOT.TFile.Open('Datasets/TT_Skim_10k.root', 'read')
# tree = file.Get('Events')
# tree.Print('FatJet_particleNet*')