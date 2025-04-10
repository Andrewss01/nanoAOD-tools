import ROOT
import math
import numpy as np
from array import array
#from datetime import datetime
ROOT.PyConfig.IgnoreCommandLineOptions = True
#from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
#from PhysicsTools.NanoAODTools.postprocessing.skimtree_utils import *






class Idx_PFC_SV(Module):
    def __init__(self):
        pass
        
        
    def beginJob(self):
        pass
        
        
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        
        #self.out.branch("Jet_deltaR",      "F", lenVar="nJet") 
        self.out.branch("PFCands_JetIdx"   ,       "I", lenVar="nPFCands")    #nJetPFCands"? 
        self.out.branch("PFCands_FatJetIdx",       "I", lenVar="nPFCands")
        self.out.branch("PFCands_Idx"      ,       "I", lenVar="nPFCands")

        self.out.branch("SV_JetIdx"   ,       "I", lenVar = "nSV"   ) 
        self.out.branch("SV_FatJetIdx",       "I", lenVar = "nSV"   )
        self.out.branch("SV_Idx"      ,       "I", lenVar = "nSV"   )
        



        #self.out.branch("PFCands_JetdzFromPV",     "I", lenVar="nPFCands")
        #self.out.branch("PFCands_FatJetdzFromPV",  "I", lenVar="nPFCands")
        #self.out.branch("PFCands_JetdxyFromPV",    "I", lenVar="nPFCands")
        #self.out.branch("PFCands_FatJetdxyFromPV", "I", lenVar="nPFCands")
        




    def endFile(self, inputFile, outputFile, inputTree,wrappedOutputTree):
        pass


    def analyze(self, event):
        #t0 = datetime.now()
        """process event, return True (go to next module) or False (fail, go to next event)"""        
        jets       = Collection(event,"Jet")
        Njets      = len(jets)
        fatjets  = Collection(event,"FatJet")
        PFCs       = Collection(event,"PFCands")
        NPFCs      = len(PFCs)
        jetPFCs    = Collection(event,"JetPFCands")
        fatjetPFCs = Collection(event,"FatJetPFCands")
        SVs = Collection(event, "SV")
        jetSVs = Collection(event, "JetSVs")
        fatjetSVs = Collection(event, "FatJetSVs")
        NSVs = len(SVs)

        

        '''init variables to branch'''
        PFCs_jets_idx          = np.full(NPFCs,-1)
        PFCs_fat_jets_idx      = np.full(NPFCs,-1)
        PFCs_idx               = np.full(NPFCs,-1)
        SVs_jets_idx           = np.full(NSVs ,-1)
        SVs_fat_jets_idx       = np.full(NSVs ,-1)
        SVs_idx                = np.full(NSVs ,-1)
        SVs_multiple_jets      = np.full(NSVs ,-1)
        SVs_multiple_fat_jets  = np.full(NSVs ,-1)
      



        for jPFC in jetPFCs:
            
            if PFCs_jets_idx[jPFC.pFCandsIdx] == -1:
                PFCs_jets_idx[jPFC.pFCandsIdx]=jPFC.jetIdx
            else: 
                print("errore: a questo pf cands corrisponde più di un jet")
        
        for fjPFC in fatjetPFCs:
            if PFCs_fat_jets_idx[fjPFC.pFCandsIdx] == -1:
                PFCs_fat_jets_idx[fjPFC.pFCandsIdx]=fjPFC.jetIdx
            else:
                print('errore: a questo pf cands corrisponde più di un fat jet ')

        for i in range(NPFCs):
            PFCs_idx[i]=i
        
#  if particle.JetIdx!=-1:
#                 jIdx=int(particle.JetIdx)
#                 dr_jet=deltaR(particle, jets[jIdx])
#                 #print("\nche succede?",dr_jet,"\n")
#                 is_in_jet=1
#             if particle.FatJetIdx!=-1:
#                 fjIdx=int(particle.FatJetIdx)
#                 dr_Fatjet=deltaR(particle, fjets[fjIdx])
#                 is_in_fat_jet=1
        
        for jSV in jetSVs:
            if jSV.sVIdx != -1:
                if SVs_multiple_jets[jSV.sVIdx] == -1:
                    SVs_multiple_jets[jSV.sVIdx] = jSV.jetIdx
                else:
                    jet_1_idx = int(SVs_multiple_jets[jSV.sVIdx])
                    sv_particle = SVs[jSV.sVIdx]
                    jet_1 = jets[jet_1_idx]
                    dr_1 = deltaR(sv_particle, jet_1)
                    jet_2 = jets[int(jSV.jetIdx)] 
                    dr_2 = deltaR(sv_particle, jet_2)
                    if dr_2 < dr_1:
                        SVs_multiple_jets[jSV.sVIdx] = jSV.jetIdx
            

        for fjSV in fatjetSVs:
            if fjSV.sVIdx != -1:
                if SVs_multiple_fat_jets[fjSV.sVIdx] == -1:
                    SVs_multiple_fat_jets[fjSV.sVIdx] = fjSV.jetIdx
                    
                else:
                    fatjet_1_idx = int(SVs_multiple_fat_jets[fjSV.sVIdx])
                    sv_particle = SVs[fjSV.sVIdx]
                    fatjet_1 = fatjets[int(fatjet_1_idx)]
                    dr_1 = deltaR(sv_particle, fatjet_1)
                    fatjet_2 = fatjets[fjSV.jetIdx]
                    dr_2 = deltaR(sv_particle, fatjet_2)
                    if dr_2 < dr_1: 
                        SVs_multiple_fat_jets[fjSV.sVIdx] = fjSV.jetIdx
                
        
            #PFCs_fat_jets_dz_PV[jPFC.pFCandsIdx]=fjPFC.dzFromPV
            #PFCs_fat_jets_dxy_PV[jPFC.pFCandsIdx]=fjPFC.dxyFromPV
        
        # for fjSV in fatjetSVs:
            # SVs_fat_jets_idx[fjSV.sVIdx] = fjSV.jetIdx

      

        for j in range(NSVs):
            SVs_idx[j] = j  
        
        for num_fat_jet,fat_jet_idx in enumerate(SVs_multiple_fat_jets):
            SVs_fat_jets_idx[num_fat_jet] = fat_jet_idx
        
        for num_jet, jet_idx in enumerate(SVs_multiple_jets):
            SVs_jets_idx[num_jet] = jet_idx




        self.out.fillBranch("PFCands_JetIdx"   ,    PFCs_jets_idx )
        self.out.fillBranch("PFCands_FatJetIdx", PFCs_fat_jets_idx)
        self.out.fillBranch("PFCands_Idx"      ,       PFCs_idx   )


        self.out.fillBranch("SV_JetIdx"        ,    SVs_jets_idx  ) 
        self.out.fillBranch("SV_FatJetIdx"     , SVs_fat_jets_idx )
        self.out.fillBranch("SV_Idx"           ,       SVs_idx    )
  
        #self.out.fillBranch("PFCands_JetdzFromPV", PFCs_jets_dz_PV)
        #self.out.fillBranch("PFCands_FatJetdzFromPV",  PFCs_fat_jets_dz_PV)
        #self.out.fillBranch("PFCands_JetdxyFromPV", PFCs_jets_dxy_PV)
        #self.out.fillBranch("PFCands_FatJetdxyFromPV",  PFCs_fat_jets_dxy_PV)


        #self.out.fillBranch("Top_indFatJet", ind_fatjets) 
        #self.out.fillBranch("Top_indJet", ind_jets) 
        # t1 = datetime.now()
        # print("nanprepro module time :", t1-t0) 
        return True