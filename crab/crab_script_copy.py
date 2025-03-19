#!/usr/bin/env python3
import os
import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopEvaluate_MultiScore_v2 import *


from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp import *

p=PostProcessor('.', inputFiles(), '', modules=[GenPart_MomFirstCp(flavour = '-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'), nanoprepro(), nanoTopcand(isMC = True), nanoTopevaluate_MultiScore(model = 'MC')], 
                provenance=True, fwkJobReport=True, histFileName='hist.root', histDirName='plots', outputbranchsel='keep_and_drop.txt', postfix = '_PROVA', maxEntries = 100000)
p.run()
print('DONE')



