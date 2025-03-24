
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import numpy as np


class Selection(Module):
    def __init__(self, pt_start=350, pt_stop =500):
        self.pt_start = pt_start
        self.pt_stop = pt_stop

    def beginJob(self):
        pass
    
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        #"branches Top candidate high pt selected pt"
        self.out.branch('TopMixed_Cut', 'I', lenVar= 'nTopMixed')
        ###self.out.branch("nTopResolved", "I")
        ##self.out.branch("TopResolved_idxJet0", "I", lenVar="nTopResolved")
        #self.out.branch("TopResolved_idxJet1", "I", lenVar="nTopResolved")
        #self.out.branch("TopResolved_idxJet2", "I", lenVar="nTopResolved")
        #self.out.branch("TopResolved_pt", "F", lenVar="nTopResolved")
        #self.out.branch("TopResolved_eta", "F", lenVar="nTopResolved")
        #self.out.branch("TopResolved_phi", "F", lenVar="nTopResolved")
        #self.out.branch("TopResolved_mass", "F", lenVar="nTopResolved")
        #self.out.branch("TopResolved_truth", "F", lenVar="nTopResolved")

    def analyze(self, event):
        #top_resolved = Collection(event, 'TopResolved')
        topmixed = Collection(event, 'TopMixed')
        
     
        iscut = []
        #top_pt = top_mixed.pt()
        
        topmixedcut = list(filter(lambda x : x.pt <= self.pt_stop and x.pt >= self.pt_start, topmixed))
        
        for top in topmixed:
            if top in topmixedcut:
                iscut.append(1)
            else:
                iscut.append(0)
        #iscut = [int(i) for i in topmixedcut if i == True]
        
     
        self.out.fillBranch('TopMixed_Cut', iscut)
 

        return True
    