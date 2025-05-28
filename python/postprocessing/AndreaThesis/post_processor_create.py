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

fnames = sys.argv[1].split(',')
# print(fnames)
path = sys.argv[2]
cluster_label = sys.argv[3]

p=PostProcessor(path,fnames,branchsel=None,modules=[MCweight_writer(), preselection(), GenPart_MomFirstCp(flavour = '-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'),Idx_PFC_SV(), deltaR_PF_SV(),
                                                    collectionMerger(input = ['PFCands'], output = "PFCands", sortkey=lambda x: x.pt, reverse = True, selector = None, maxObjects = None),
                                                    collectionMerger(input = ['SV'], output = "SV", sortkey=lambda x: x.ntracks, reverse = True, selector = None, maxObjects = None), nanoprepro(), nanoTopcand_PFC_SV()],
                                                    postfix = '_Skim', outputbranchsel="%s/src/PhysicsTools/NanoAODTools/scripts/keep_and_drop_jets_pf_sv.txt" % os.environ["CMSSW_BASE"], histFileName=path+"/histOut_"+cluster_label+".root", histDirName="plots", haddFileName = path +'/'+cluster_label+'.root', maxEntries = 10000)
p.run()

