import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from modules.nanoTopEvaluate_MultiScore_v3 import *
import sys
from modules.preselection_PF import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.MCweight_writer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2 import *
from modules.NanoTopCandidate_PF_SV import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import * 
from modules.idx_PFC_SV import *
from modules.deltaR_PF_SV import * 
from PhysicsTools.NanoAODTools.postprocessing.modules.common.MCweight_writer import *


# path = '/eos/user/a/apuglia/Thesis/Data/MuonRun3C27Jun2023/' 
# fnames = ['root://cms-xrd-global.cern.ch//store/user/apuglia/Muon/DataMuon_v1/250519_082700/0000/nano_data2022CDE_1-10.root', 
# 'root://cms-xrd-global.cern.ch///store/user/apuglia/Muon/DataMuon_v1/250519_082700/0000/nano_data2022CDE_1-11.root', 
# 'root://cms-xrd-global.cern.ch///store/user/apuglia/Muon/DataMuon_v1/250519_082700/0000/nano_data2022CDE_1-12.root']

fnames = [sys.argv[1]]
# fnames =['root://cms-xrd-global.cern.ch//store/user/apuglia/Muson/DataMuon_v1/250519_082700/0000/nano_data2022CDE_25.root']
# print(fnames)
path = sys.argv[2]
# path = '/eos/user/a/apuglia/'
p=PostProcessor(path,fnames,branchsel=None,modules=[ preselection(),Idx_PFC_SV(), deltaR_PF_SV(),
                                                    collectionMerger(input = ['PFCands'], output = "PFCands", sortkey=lambda x: x.pt, reverse = True, selector = None, maxObjects = None),
                                                    collectionMerger(input = ['SV'], output = "SV", sortkey=lambda x: x.ntracks, reverse = True, selector = None, maxObjects = None), nanoTopcand_PFC_SV(isMC = 0), nanoTopevaluate_MultiClass()], postfix = '_cnn_model_sel_one_muon', 
                  outputbranchsel="%s/src/PhysicsTools/NanoAODTools/scripts/keep_and_drop_large.txt" % os.environ["CMSSW_BASE"])
p.run()
