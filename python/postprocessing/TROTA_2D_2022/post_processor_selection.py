import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from modules.nanoTopEvaluate_MultiScore_v3 import *
import sys
from modules.selection_best_top import *

fnames = [sys.argv[1]]
path = sys.argv[2]

#preselection()
p=PostProcessor(path,fnames,branchsel=None,modules=[ preselection()], postfix = '_best_score_top',
                outputbranchsel="%s/src/PhysicsTools/NanoAODTools/scripts/keep_and_drop_large.txt" % os.environ["CMSSW_BASE"])
p.run()