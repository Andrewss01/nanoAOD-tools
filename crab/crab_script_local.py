#!/usr/bin/env python3
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.JetVetoMaps_run3 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.BTagSF import *
from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis
from PhysicsTools.NanoAODTools.postprocessing.modules.common.MCweight_writer import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.MET_Filter import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.preselection import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PUreweight import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopEvaluate_MultiScore_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.SampleIdx import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.globalvar import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.lumiMask import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.CMSJMECalculators_module import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.CMSJMECalculatorsHelper import *
from CMSJMECalculators import loadJMESystematicsCalculators
from CMSJMECalculators.utils import (
    toRVecFloat,
    toRVecInt,
    getJetMETArgs,
    getFatJetArgs,
)
from CMSJMECalculators import config as calcConfigs
loadJMESystematicsCalculators()

p=PostProcessor('.', ["root://cms-xrd-global.cern.ch//store/data/Run2022F/JetMET/NANOAOD/22Sep2023-v2/80000/44dedf5c-9f05-4e8a-9587-110d35a868a3.root"], 
                '', modules=[JetVetoMaps_run3(2022, '2022_Summer22'), #metCorrector(), fatJetCorrector(), metCorrector_tot(), fatJetCorrector_tot(), 

                # MC

                # PUreweight(2022, '2022_Summer22'),
                # BTagSF(2022, '2022_Summer22'), 
                # JetVetoMaps_run3(2022, '2022_Summer22'), 
                # CMSJMECalculators(configcreate(isMC=True, year=2022, EE=False, runPeriod=".", jetType="AK4PFPuppi", forMET=False, doJer=False), 
                #     jetType="AK4PFPuppi", isMC=True, forMET=False, PuppiMET=False, addHEM2018Issue=False, NanoAODv=12),
                # CMSJMECalculators(configcreate(isMC=True, year=2022, EE=False, runPeriod=".", jetType="AK8PFPuppi", forMET=False, doJer=False), 
                #     jetType="AK8PFPuppi", isMC=True, forMET=False, PuppiMET=False, addHEM2018Issue=False, NanoAODv=12), 
                # CMSJMECalculators(configcreate(isMC=True, year=2022, EE=False, runPeriod=".", jetType="AK4PFPuppi", forMET=True, doJer=False), 
                #     jetType="AK4PFPuppi", isMC=True, forMET=True, PuppiMET=True, addHEM2018Issue=False, NanoAODv=12), 
                
                # Data
                
                CMSJMECalculators(configcreate(isMC=False, year=2022, EE=True, runPeriod="F", jetType="AK4PFPuppi", forMET=False, doJer=False), 
                    jetType="AK4PFPuppi", isMC=False, forMET=False, PuppiMET=False, addHEM2018Issue=False, NanoAODv=12),
                CMSJMECalculators(configcreate(isMC=False, year=2022, EE=True, runPeriod="F", jetType="AK8PFPuppi", forMET=False, doJer=False), 
                    jetType="AK8PFPuppi", isMC=False, forMET=False, PuppiMET=False, addHEM2018Issue=False, NanoAODv=12), 
                CMSJMECalculators(configcreate(isMC=False, year=2022, EE=True, runPeriod="F", jetType="AK4PFPuppi", forMET=True, doJer=False), 
                    jetType="AK4PFPuppi", isMC=False, forMET=True, PuppiMET=True, addHEM2018Issue=False, NanoAODv=12), 
              
                ],
                provenance=True, fwkJobReport=True, haddFileName='tree_hadd.root' , histFileName='hist.root', histDirName='plots',
                outputbranchsel='../scripts/keep_and_drop.txt', maxEntries=10)
p.run()
print('DONE')
# root://cms-xrd-global.cern.ch//store/mc/Run3Summer22NanoAODv12/QCD-4Jets_HT-1000to1200_TuneCP5_13p6TeV_madgraphMLM-pythia8/NANOAODSIM/JMENano12p5_132X_mcRun3_2022_realistic_v3-v2/60000/b9d48100-f36a-4422-b17c-6605da590baa.root
# root://cms-xrd-global.cern.ch//store/data/Run2022C/JetMET/NANOAOD/22Sep2023-v1/40000/ba932d98-89fb-4481-bc84-0c1d19f11249.root
