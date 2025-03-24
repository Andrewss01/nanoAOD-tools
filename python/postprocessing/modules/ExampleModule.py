import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import numpy as np

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



#mette ogni top nell'intervallo di pt giusto
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
        self.writeHistFile=True
        
        
        
        

    def beginJob(self,histFile=None,histDirName=None):
        Module.beginJob(self,histFile, histDirName)
        n_points= 21
        self.g_resolved = ROOT.TGraphErrors(n_points)
        self.g_mixed = ROOT.TGraphErrors(n_points)
        self.addObject(self.g_resolved)
        self.addObject(self.g_mixed)
        
        
        
       

    def analyze(self, event):
        top_resolved = Collection(event, 'TopResolved')
        top_mixed = Collection(event, 'TopMixed')
        top_resolved_pt = []
        top_mixed_pt = []
        n_tops_resolved = np.zeros(21)
        n_tops_mixed = np.zeros(21)
        
        
        for top in top_resolved:
            if top.truth == 1: 
                top_resolved_pt.append(top.pt)
                #print(top.pt)
        for top in top_mixed:
            if top.truth == 1:
                top_mixed_pt.append(top.pt)
        
        pt_value, pt_error = pt_values()
        
        if len(top_resolved_pt) !=0:
            for pt in top_resolved_pt:
                n_tops_resolved = N_tops(pt, n_tops_resolved)
                
            n_tops_resolved_error = np.sqrt(n_tops_resolved)
            #resolved_max_pt= max(top_resolved_pt)
            #n_tops_resolved = N_tops(resolved_max_pt, n_tops)
            #n_tops_resolved_error = np.sqrt(n_tops_resolved)
            
            for i in range(len(pt_value)):
                self.g_resolved.SetPoint(i,pt_value[i],n_tops_resolved[i])
                self.g_resolved.SetPointError(i, pt_error[i],n_tops_resolved_error[i])
            
            self.g_resolved.SetMarkerStyle(4)
            self.g_resolved.SetMarkerColor(2)
            self.g_resolved.SetLineColor(2)
            #self.g_resolved.Scale(1.0/self.g_resolved.Integral())
            self.g_resolved.SetName('grafico_1') 

            
        #n_tops_mixed = np.zeros(21)
        if len(top_mixed_pt) !=0:
            for pt in top_mixed_pt:
                n_tops_mixed = N_tops(pt, n_tops_mixed)
            n_tops_mixed_error = np.sqrt(n_tops_mixed)
            #tops_mixed = max(top_mixed_pt)
            #n_tops_mixed = N_tops(tops_mixed, n_tops)
            #n_tops_mixed_error = np.sqrt(n_tops_mixed) 
            
            for i in range(len(pt_value)):
                self.g_mixed.SetPoint(i, pt_value[i], n_tops_mixed[i])
                self.g_mixed.SetPointError(i, pt_error[i], n_tops_mixed_error[i])
            
            self.g_mixed.SetMarkerStyle(4)
            self.g_mixed.SetMarkerColor(3)
            self.g_mixed.SetLineColor(3)
    #        self.g_mixed.Scale(1.0/self.g_resolved.Integral())
            self.g_mixed.SetName('grafico_2')
        
        
        
            

        return True
    
    


#preselection="Jet_pt[0] > 250"
