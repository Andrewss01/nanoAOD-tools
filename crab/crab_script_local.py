#!/usr/bin/env python3
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.modules.common.MCweight_writer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.MET_Filter import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.preselection import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopEvaluate_MultiScore import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.SampleIdx import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.globalvar import *
p=PostProcessor('.', ["root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL18NanoAODv9/WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1_ext1-v2/40000/B39B1386-2DC2-3B46-98BB-D9C4E176E402.root"], 
                '', modules=[MCweight_writer(), MET_Filter(year = 2018), preselection(), puAutoWeight_2018(), SampleIdx(21007), GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'),nanoprepro(),nanoTopcand(isMC=1), globalvar(), nanoTopevaluate_MultiScore()], 
                provenance=True, fwkJobReport=True, haddFileName='tree_hadd.root',histFileName='hist.root', histDirName='plots', 
                outputbranchsel='../scripts/keep_and_drop.txt', maxEntries = 100)
p.run()
print('DONE')
