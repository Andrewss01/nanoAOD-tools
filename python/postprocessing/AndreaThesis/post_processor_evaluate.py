import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from modules.nanoTopEvaluate_MultiScore_v3 import *
import sys
<<<<<<< HEAD
from modules.preselection_PF import *
=======

>>>>>>> f11b9505a90d871535a21e15c5c09d8fa8f565d9

fnames = [sys.argv[1]]
path = sys.argv[2]

<<<<<<< HEAD
p=PostProcessor(path,fnames,branchsel=None,modules=[ nanoTopevaluate_MultiClass()], postfix = '_Scores_Selected', 
=======
p=PostProcessor(path,fnames,branchsel=None,modules=[nanoTopevaluate_MultiClass()], postfix = '_Scores', 
>>>>>>> f11b9505a90d871535a21e15c5c09d8fa8f565d9
                outputbranchsel="%s/src/PhysicsTools/NanoAODTools/scripts/keep_and_drop_jets_pf_sv.txt" % os.environ["CMSSW_BASE"])
p.run()
