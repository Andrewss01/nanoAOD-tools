import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import numpy as np

from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2 import *

#Crea gli intervalli di pt a intervalli di 50 e per ognuno prende il valore medio 
#come punto centrale 
def pt_values(start= 0,stop=1050, step= 50):
    pt_range = range(start,stop,step)
    pt_value, pt_error = [],[]
    for i in range(0, len(pt_range)):
    #print(pt_range[i])
        if i != len(pt_range)-1:
            x = (pt_range[i+1] + pt_range[i])/2
            x_error = (pt_range[i+1] - pt_range[i])/2
            #print('x mean is: ',x)
            #print('x error is: ', x_error)
            pt_value.append(x)
            pt_error.append(x_error)
        if i == len(pt_range)-1:
            pt_value.append(pt_range[i])
            pt_error.append(x_error)
    return pt_value, pt_error



#per ogni top, vede in che intervallo di pt si trova e per quell'intervallo setta il numero di top totali che hanno quel range id impulso
def N_tops(pt, n_tops):
    k = pt//50
    #print(k)
    if k >= len(n_tops)-1 :
        n_tops[len(n_tops) -1] += 1
    else: 
        n_tops[int(k)] += 1
        
    return n_tops
 

class ExampleAnalysis(Module):
    def __init__(self):
        self.writeHistFile = True
        self.n_points = 21
        self.g_resolved = ROOT.TGraphErrors(self.n_points)
        # 

    def beginJob(self, histFile = None, histDirName=None):
        Module.beginJob(self, histFile, histDirName)
        # pass
        self.addObject(self.g_resolved)
        

    def analyze(self, event):
        # electrons = Collection(event, "Electron")
        # muons = Collection(event, "Muon")
        # jets = Collection(event, "Jet")
        # eventSum = ROOT.TLorentzVector()
        top_resolved = Collection(event, 'TopResolved')
        top_resolved_pt = []
        n_tops_resolved = np.zeros(self.n_points)
        
        
        
        for top in top_resolved:
            if top.truth == 1: 
                top_resolved_pt.append(top.pt)
                #print(top.pt)
        # for top in top_mixed:
        #     if top.truth == 1:
        #         top_mixed_pt.append(top.pt)
        
        pt_value, pt_error = pt_values()
        
        if len(top_resolved_pt) !=0:
            for pt in top_resolved_pt:
                n_tops_resolved = N_tops(pt, n_tops_resolved)
                
            n_tops_resolved_error = np.sqrt(n_tops_resolved)
            #resolved_max_pt= max(top_resolved_pt)
            #n_tops_resolved = N_tops(resolved_max_pt, n_tops)
            #n_tops_resolved_error = np.sqrt(n_tops_resolved)
            
            for i in range(len(pt_value)):
                # self.g_resolved.Fill(i)
                self.g_resolved.SetPoint(i,pt_value[i],n_tops_resolved[i])
                self.g_resolved.SetPointError(i, pt_error[i],n_tops_resolved_error[i])
            
            self.g_resolved.SetMarkerStyle(4)
            self.g_resolved.SetMarkerColor(2)
            self.g_resolved.SetLineColor(2)
            #self.g_resolved.Scale(1.0/self.g_resolved.Integral())
            self.g_resolved.SetName('grafico_1') 
            
        return True
            
        #n_tops_mixed = np.zeros(21)
        # if len(top_mixed_pt) !=0:
        #     for pt in top_mixed_pt:
        #         n_tops_mixed = N_tops(pt, n_tops_mixed)
        #     n_tops_mixed_error = np.sqrt(n_tops_mixed)
            #tops_mixed = max(top_mixed_pt)
            #n_tops_mixed = N_tops(tops_mixed, n_tops)
            #n_tops_mixed_error = np.sqrt(n_tops_mixed) 
            
    #         for i in range(len(pt_value)):
    #             self.g_mixed.SetPoint(i, pt_value[i], n_tops_mixed[i])
    #             self.g_mixed.SetPointError(i, pt_error[i], n_tops_mixed_error[i])
            
    #         self.g_mixed.SetMarkerStyle(4)
    #         self.g_mixed.SetMarkerColor(3)
    #         self.g_mixed.SetLineColor(3)
    # #        self.g_mixed.Scale(1.0/self.g_resolved.Integral())
    #         self.g_mixed.SetName('grafico_2')
        
        
        
            
files = ["/eos/user/a/apuglia/thesis/Datasets/TT.root"]
p = PostProcessor(".", files, branchsel=None, modules=[GenPart_MomFirstCp(flavour = '-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24'), nanoprepro(), nanoTopcand(), ExampleAnalysis()], 
                   histFileName="histOut.root", histDirName="plots")
p.run()

      
    
    


#preselection="Jet_pt[0] > 250"
