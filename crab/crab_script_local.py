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


# from PhysicsTools.NanoAODTools.postprocessing.modules.jme.CMSJMECalculatorsFatJet_module import *
# from PhysicsTools.NanoAODTools.postprocessing.modules.jme.CMSJMECalculatorsMET_module import *
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.CMSJMECalculatorsJet_module import *
from CMSJMECalculators import loadJMESystematicsCalculators
from CMSJMECalculators.utils import (
    toRVecFloat,
    toRVecInt,
    getJetMETArgs,
    getFatJetArgs,
)
from CMSJMECalculators import config as calcConfigs

loadJMESystematicsCalculators()

def jetvarcalcMC():
    configCls = calcConfigs.JetVariations
    tagfile = "2022_Prompt"
    jsonFile = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/JME/"+tagfile+"/jet_jerc.json.gz"
    jetType = "AK4PFPuppi"
    config = configCls(jsonFile, jetType)
    # config.jecTag = "Summer22_22Sep2023_V2_MC"
    # config.jerTag = "Summer22_22Sep2023_V2_MC"
    config.jecTag = "Winter22Run3_V2_MC"
    config.jerTag = "JR_Winter22Run3_V1_MC"
    config.jecLevel = "L1L2L3Res"
    config.jesUncertainties = ["Total"]#, "AbsoluteStat", "AbsoluteScale"]
    config.splitJER = False
    # loadJMESystematicsCalculators()
    return config.create()
def METvarcalcMC():
    configCls = calcConfigs.METVariations
    tagfile = "2022_Prompt"
    jsonFile = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/JME/"+tagfile+"/jet_jerc.json.gz"
    jetType = "AK4PFPuppi"
    config = configCls(jsonFile, jetType)
    # config.jecTag = "Summer22_22Sep2023_V2_MC"
    # config.jerTag = "Summer22_22Sep2023_V2_MC"
    config.jecTag = "Winter22Run3_V2_MC"
    config.jerTag = "JR_Winter22Run3_V1_MC"
    config.jecLevel = "L1L2L3Res"
    config.jesUncertainties = ["Total"]#, "AbsoluteStat", "AbsoluteScale"]
    config.splitJER = False
    # loadJMESystematicsCalculators()
    return config.create()

def fatjetvarcalcMC():
    configCls = calcConfigs.FatJetVariations
    tagfile = "2022_Prompt"
    jsonFile = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/JME/"+tagfile+"/fatJet_jerc.json.gz"
    jetType = "AK8PFPuppi"
    config = configCls(jsonFile, jetType)
    config.jecTag = "Winter22Run3_V2_MC"
    config.jerTag = "JR_Winter22Run3_V1_MC"
    config.splitJER = False
    config.jecLevel = "L1L2L3Res"
    config.jesUncertainties = ["Total"]
    config.jsonFileSubjet = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/JME/"+tagfile+"/jet_jerc.json.gz"
    config.jetAlgoSubjet = "AK4PFPuppi"
    config.jecTagSubjet = "Winter22Run3_V2_MC"
    config.jecLevelSubjet = "L1L2L3Res"
    # loadJMESystematicsCalculators()
    return config.create()

# metCorrector = createJMECorrector(isMC=True, dataYear="2022", jesUncert='All', redojec=True,jetType = 'AK4PFPuppi')
# fatJetCorrector = createJMECorrector(isMC=True, dataYear="2022", jesUncert='All', redojec=True,jetType = 'AK8PFPuppi')
# metCorrector_tot = createJMECorrector(isMC=True, dataYear="2022", jesUncert='Total', redojec=True, jetType = 'AK4PFPuppi')
# fatJetCorrector_tot = createJMECorrector(isMC=True, dataYear="2022", jesUncert='Total', redojec=True,jetType = 'AK8PFPuppi')
p=PostProcessor('.', ["root://cms-xrd-global.cern.ch//store/mc/Run3Summer22NanoAODv12/QCD-4Jets_HT-1000to1200_TuneCP5_13p6TeV_madgraphMLM-pythia8/NANOAODSIM/JMENano12p5_132X_mcRun3_2022_realistic_v3-v2/60000/b9d48100-f36a-4422-b17c-6605da590baa.root"], 
                '', modules=[JetVetoMaps_run3(2022, '2022_Summer22'), #metCorrector(), fatJetCorrector(), metCorrector_tot(), fatJetCorrector_tot(), 
                # PUreweight(2022, '2022_Summer22'),
                
                #BTagSF(2022, '2022_Summer22'), 
                
                # JetVetoMaps_run3(2022, '2022_Summer22'), 
                CMSJMECalculatorsJet(jetvarcalcMC(), jetType="AK4Puppi", isMC=True, forMET=False, PuppiMET=False, addHEM2018Issue=False, NanoAODv=12), 
                # CMSJMECalculatorsJet(fatjetvarcalcMC(), jetType="AK8Puppi", isMC=True, forMET=False, PuppiMET=False, addHEM2018Issue=False, NanoAODv=12),
                # CMSJMECalculatorsJet(METvarcalcMC(), jetType="AK4Puppi", isMC=True, forMET=True, PuppiMET=True, addHEM2018Issue=False, NanoAODv=12),
                ],
                provenance=True, fwkJobReport=True, haddFileName='tree_hadd.root' , histFileName='hist.root', histDirName='plots',
                outputbranchsel='../scripts/keep_and_drop.txt', maxEntries=10)
p.run()
print('DONE')
# ["MCweight_writer(), preselection(), GenPart_MomFirstCp(flavour='-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'), nanoprepro(),nanoTopcand(isMC=1), globalvar(), nanoTopevaluate()]