import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2 import *
from PhysicsTools.NanoAODTools.python.postprocessing.AndreaThesis.ML.training_steps.NanoTopCandidate_PF_SV import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import * 
from PhysicsTools.NanoAODTools.python.postprocessing.AndreaThesis.ML.training_steps.idx_PFC_SV import *
from ML.deltaR_PF_SV import * 
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopEvaluate_MultiScore_v3 import *
import sys
# fnames = ['/eos/user/o/oiorio/tDM/PFNano/nano_mcRun3_ttsl1.root']

fnames = [sys.argv[1]]
label = sys.argv[4]
to_do = sys.argv[5]

if to_do == 'dataset':
    p=PostProcessor("/eos/user/a/apuglia/thesis/Datasets/",fnames,branchsel=None,modules=[GenPart_MomFirstCp(flavour = '-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'), Idx_PFC_SV(), deltaR_PF_SV(),
                                                                                            collectionMerger(input = ['PFCands'], output = "PFCands", sortkey=lambda x: x.pt, reverse = True, selector = None, maxObjects = None),
                                                                                            collectionMerger(input = ['SV'], output = "SV", sortkey=lambda x: x.ntracks, reverse = True, selector = None, maxObjects = None), nanoprepro(), nanoTopcand_PFC_SV()]
                        ,histFileName="histOut"+label+".root",histDirName="plots", postfix = '_Skim', outputbranchsel="%s/src/PhysicsTools/NanoAODTools/scripts/keep_and_drop_jets_pf_sv.txt" % os.environ["CMSSW_BASE"])
    p.run()

elif to_do == 'evaluate': 
    p=PostProcessor("/eos/user/a/apuglia/thesis/Datasets/Dataset_26_04_2025_Scores/",fnames,branchsel=None,modules=[nanoTopevaluate_MultiClass()]
                        ,histFileName="histOut"+label+".root",histDirName="plots", postfix = '_Scores', outputbranchsel="%s/src/PhysicsTools/NanoAODTools/scripts/keep_and_drop_jets_pf_sv.txt" % os.environ["CMSSW_BASE"])
    p.run()
 