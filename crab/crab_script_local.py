#!/usr/bin/env python3
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
# from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
# from PhysicsTools.NanoAODTools.postprocessing.modules.common.JetVetoMaps_run3 import *
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
# from PhysicsTools.NanoAODTools.postprocessing.modules.common.MCweight_writer import *
# from PhysicsTools.NanoAODTools.postprocessing.modules.common.MET_Filter import *
# from PhysicsTools.NanoAODTools.postprocessing.modules.common.preselection import *
# from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *
# from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp import *
# from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2 import *
# from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2 import *
# from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopEvaluate_MultiScore_v2 import *
# from PhysicsTools.NanoAODTools.postprocessing.modules.common.SampleIdx import *
# from PhysicsTools.NanoAODTools.postprocessing.modules.common.globalvar import *
# from PhysicsTools.NanoAODTools.postprocessing.modules.common.lumiMask import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.CMSJMECalculatorsFatJet_module import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.CMSJMECalculatorsMET_module import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.CMSJMECalculatorsJet_module import *


# metCorrector = createJMECorrector(isMC=False, dataYear="2022", runPeriod='C', jesUncert='All', redojec=True,jetType = 'AK4PFPuppi')
# fatJetCorrector = createJMECorrector(isMC=False, dataYear="2022", runPeriod='C', jesUncert='All', redojec=True, jetType = 'AK8PFPuppi')
# metCorrector_tot = createJMECorrector(isMC=False, dataYear="2022", runPeriod='C', jesUncert='Total', redojec=True,jetType = 'AK4PFPuppi')
# fatJetCorrector_tot = createJMECorrector(isMC=False, dataYear="2022", runPeriod='C', jesUncert='Total', redojec=True, jetType = 'AK8PFPuppi')
p=PostProcessor('.', ["root://cms-xrd-global.cern.ch//store/mc/Run3Summer22NanoAODv12/QCD-4Jets_HT-1000to1200_TuneCP5_13p6TeV_madgraphMLM-pythia8/NANOAODSIM/JMENano12p5_132X_mcRun3_2022_realistic_v3-v2/60000/b9d48100-f36a-4422-b17c-6605da590baa.root"], 
                '', modules=[CMSJMECalculatorsFatJet()],
                # '', modules=[CMSJMECalculatorsJet()],
                # '', modules=[CMSJMECalculatorsMET()],
                provenance=True, fwkJobReport=True, haddFileName='tree_hadd.root' , histFileName='hist.root', histDirName='plots',
                outputbranchsel='../scripts/keep_and_drop.txt', maxEntries=10)
p.run()
print('DONE')