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
# fnames = ['/eos/user/o/oiorio/tDM/PFNano/nano_mcRun3_ttsl1.root']

fnames = [sys.argv[1]]
path = sys.argv[4]
# path = '/eos/user/a/apuglia/thesis/Dataset/post_processor_21_05_2025/'
# fnames = ['/eos/user/a/apuglia/thesis/Datasets/ZJ_1.root', '/eos/user/a/apuglia/thesis/Datasets/TT.root']
p=PostProcessor(path,fnames,branchsel=None,modules=[MCweight_writer(), GenPart_MomFirstCp(flavour = '-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'),Idx_PFC_SV(), deltaR_PF_SV(),
                                                    collectionMerger(input = ['PFCands'], output = "PFCands", sortkey=lambda x: x.pt, reverse = True, selector = None, maxObjects = None),
                                                    collectionMerger(input = ['SV'], output = "SV", sortkey=lambda x: x.ntracks, reverse = True, selector = None, maxObjects = None), nanoprepro(), nanoTopcand_PFC_SV()],
                                                    postfix = '_Skim', outputbranchsel="%s/src/PhysicsTools/NanoAODTools/scripts/keep_and_drop_jets_pf_sv.txt" % os.environ["CMSSW_BASE"], histFileName=path+"histOut_"+label+".root", histDirName="plots")
p.run()


