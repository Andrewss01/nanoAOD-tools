import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from modules.nanoTopEvaluate_MultiScore_v3 import *
import sys
from modules.preselection_PF import *

fnames = [sys.argv[1]]
path = sys.argv[2]

#preselection()
p=PostProcessor(path,fnames,branchsel=None,modules=[  preselection(), nanoTopevaluate_MultiClass()], postfix = '_cnn_model_sel', 
                outputbranchsel="%s/src/PhysicsTools/NanoAODTools/scripts/keep_and_drop_large.txt" % os.environ["CMSSW_BASE"])
p.run()
