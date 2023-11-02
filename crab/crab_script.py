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
from PhysicsTools.NanoAODTools.postprocessing.modules.common.SampleIdx import *
p=PostProcessor('.', ["root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1/260000/AA06967A-EC11-1C40-9600-91B3551483DB.root"], '', modules=[MCweight_writer(), preselection(), SampleIdx(21200), GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'),nanoprepro(),nanoTopcand(isMC=1), globalvar(), nanoTopevaluate()], provenance=True, fwkJobReport=True, histFileName='hist.root', histDirName='plots', outputbranchsel='../scripts/keep_and_drop.txt', maxEntries = 100)
p.run()
print('DONE')
