from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from CMSJMECalculators import loadJMESystematicsCalculators
from CMSJMECalculators.utils import (
    toRVecFloat,
    getJetMETArgs,
    getFatJetArgs,
    configureCalc,
    configureFatJetCalc,
)
from CMSJMECalculators import config as calcConfig
from CMSJMECalculators.jetdatabasecache import JetDatabaseCache



class CMSJMECalculatorsJet(Module):
    def __init__(self):
        self.jecDBCache = JetDatabaseCache("JECDatabase", repository="cms-jet/JECDatabase", cachedir="./", mayWrite=True)
        self.jrDBCache = JetDatabaseCache("JRDatabase", repository="cms-jet/JRDatabase", cachedir="./", mayWrite=True)
        pass

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        # self.out = wrappedOutputTree
        # self.out.branch("EventMass", "F")
        pass

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        config = calcConfig.JetVariations()
        configureCalc(config, jetType="AK4PFPuppi", jerTag="JR_Winter22Run3_V1_MC", splitJER=False,
                jecTag="Summer22_22Sep2023_V2_MC", levels=["L1FastJet", "L2Relative", "L3Absolute"],
                uncSources=["Total", "AbsoluteStat", "AbsoluteScale"],
                jecDBCache=self.jecDBCache, jrDBCache=self.jrDBCache)
        loadJMESystematicsCalculators()
        jer = config.create()


        res = jer.produce(*getJetMETArgs(event._tree, isMC=True, forMET=False))
        print(jer.available())
        for i in range(jer.available().size()):
            print(res.pt(i))
        
        # res = jer.produce( toRVecFloat(event.Jet_pt),
        # toRVecFloat(event.Jet_eta),
        # toRVecFloat(event.Jet_phi),
        # toRVecFloat(event.Jet_mass),
        # toRVecFloat(event.Jet_rawFactor),
        # toRVecFloat(event.Jet_area))

        return True


# DATA ["L1FastJet", "L2Relative", "L3Absolute", "L2L3Residual"], UncSources = "Total"

# Summer22EEPrompt22_JRV1_MC, Summer22EE_22Sep2023_V2_MC
# JR_Winter22Run3_V1_MC, Summer22_22Sep2023_V2_MC