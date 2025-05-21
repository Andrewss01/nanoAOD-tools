import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from modules.nanoTopEvaluate_MultiScore_v4 import *
import sys
from modules.preselection_PF import *

fnames = [sys.argv[1]]
path = sys.argv[2]

p=PostProcessor(path,fnames,branchsel=None,modules=[ preselection(), nanoTopevaluate_MultiScore()], postfix = '_Scores_Selected', 
                outputbranchsel="%s/src/PhysicsTools/NanoAODTools/scripts/keep_and_drop_jets.txt" % os.environ["CMSSW_BASE"])
p.run()
