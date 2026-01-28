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
from modules.preselection_PF import *
# from modules.nanoTopEvaluate_MultiScore_v3 import *

# fnames = [sys.argv[1]]
# # print(fnames)
# path = sys.argv[2]
# label = sys.argv[3]



fnames=["root://cms-xrd-global.cern.ch//store/user/apuglia/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/TT_semilep_2022_v1/251103_093221/0000/nano_mcRun3_1-1.root"]
path = '/eos/user/a/apuglia/'
label = 'prova'
#preselction()
p=PostProcessor(path,fnames,branchsel=None,modules=[MCweight_writer(), GenPart_MomFirstCp(flavour = '-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'),Idx_PFC_SV()],
                postfix = '_Skim',  histFileName=path+"histOut_"+label+".root", histDirName="plots", haddFileName = path +label+'.root', maxEntries = 100)

#  deltaR_PF_SV(),
#                                                     collectionMerger(input = ['PFCands'], output = "PFCands", sortkey=lambda x: x.pt, reverse = True, selector = None, maxObjects = None),
#                                                     collectionMerger(input = ['SV'], output = "SV", sortkey=lambda x: x.ntracks, reverse = True, selector = None, maxObjects = None), nanoprepro(), nanoTopcand_PFC_SV()],
#                                                     postfix = '_Skim', outputbranchsel="%s/src/PhysicsTools/NanoAODTools/scripts/keep_and_drop_large.txt" % os.environ["CMSSW_BASE"], histFileName=path+"histOut_"+label+".root", histDirName="plots", haddFileName = path +label+'.root')
p.run()

