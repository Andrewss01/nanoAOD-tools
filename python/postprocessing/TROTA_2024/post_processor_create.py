import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2 import *
from modules.NanoTopCandidate_PF_SV import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import * 
from modules.idx_PFC_SV import *
from modules.deltaR_PF_SV import * 
from PhysicsTools.NanoAODTools.postprocessing.modules.common.MCweight_writer import *
import sys
from PhysicsTools.NATModules.modules.jetId import * 
from PhysicsTools.NATModules.modules.fatjetId import *
# from modules.preselection_PF import *
# from modules.nanoTopEvaluate_MultiScore_v3 import *
    
fnames = [sys.argv[1]]
path_dataset = sys.argv[2]
label = sys.argv[3]


json = "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-24CDEReprocessingFGHIPrompt-Summer24-NanoAODv15/2025-07-17/jetid.json.gz"


print(path_dataset)
#preselction()
p=PostProcessor(path_dataset,fnames,branchsel=None,modules=[MCweight_writer(), GenPart_MomFirstCp(flavour = '-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'),Idx_PFC_SV(), 
                deltaR_PF_SV(), collectionMerger(input = ['PFCand'], output = "PFCand", sortkey=lambda x: x.pt, reverse = True, selector = None, maxObjects = None),
                collectionMerger(input = ['SV'], output = "SV", sortkey=lambda x: x.ntracks, reverse = True, selector = None, maxObjects = None), nanoprepro(), jetId(json, jetType="AK4PUPPI"),  fatjetId(json, jetType="AK8PUPPI"), 
                nanoTopcand_PFC_SV()], 
                postfix = '_Skim',histFileName=path_dataset+"histOut_"+label+".root", histDirName="plots", haddFileName = path_dataset +label+'.root', maxEntries = 100)

# 



#                                                     postfix = '_Skim', outputbranchsel="%s/src/PhysicsTools/NanoAODTools/scripts/keep_and_drop_large.txt" % os.environ["CMSSW_BASE"], histFileName=path+"histOut_"+label+".root", histDirName="plots", haddFileName = path +label+'.root')
p.run()

