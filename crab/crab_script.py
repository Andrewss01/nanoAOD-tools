#!/usr/bin/env python3
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.modules.common.MCweight_writer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.preselection import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopevaluate import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.globalvar import *
p=PostProcessor('.', inputFiles(), '', modules=[preselection(),nanoTopcand(isMC=0), nanoTopevaluate(), globalvar()], provenance=True, fwkJobReport=True, haddFileName='tree_hadd.root', outputbranchsel='keep_and_drop.txt')
p.run()
print('DONE')
