import ROOT
from ROOT import TLorentzVector
import pickle as pkl
#from PhysicsTools.NanoAODTools.postprocessing.tools import *
trs_file = open("/eos/user/a/apuglia/SWAN_projects/thesis/CMSSW_14_1_7/src/training_dataset/trainingset_TTvsZJ_noTTbkg.pkl", "rb")
trs = pkl.load(trs_file)
from math import hypot
import numpy as np


class Jet:
    def __init__(self, pt, eta, phi, mass):
        self._pt = pt
        self._eta = eta
        self._phi = phi
        self._mass = mass
        self._p4 = TLorentzVector()
        self._p4.SetPtEtaPhiM(pt, eta, phi, mass)
        
    def pt(self):
        return self._pt
        
    def eta(self): #delta eta con il fat jet
        return self._eta
        
    def phi(self): #delta phi con il fat jet
        return self._phi
    
    def mass(self):
        return self._mass 
    
    def p4(self):
        return self._p4
    
class FatJet:
    def __init__(self, pt, eta, phi, mass):
        self._pt = pt
        self._eta = eta
        self._phi = phi
        self._mass = mass
        self._p4 = TLorentzVector()
        self._p4.SetPtEtaPhiM(pt,eta,phi,mass)
        
    def pt(self):
        return self._pt
        
    def eta(self): #delta eta con il fat jet
        return self._eta
        
    def phi(self): #delta phi con il fat jet
        return self._phi
    
    def mass(self):
        return self._mass
    
    def p4(self):
        """Restituisce il TLorentzVector"""
        return self._p4
    

def deltaR(jet):
    # catch if called with objects
    #if eta2 == None:
        #return deltaR(eta1.eta, eta1.phi, phi1.eta, phi1.phi)
    # otherwise
    return hypot(jet.eta(),jet.phi())

def top2j1fj(fj, j0, j1):
    #print(hypot(j0.eta,j0.phi))
    dr0 = hypot(j0.eta(), j0.phi()) < 0.8 #perchè sono già definiti come Delta Eta e delta Phi rispetto al fat jet
    dr1 = hypot(j1.eta(), j1.phi()) <0.8
    if dr0*dr1:
        p4 = fj.p4()
    elif dr0:
        p4 = fj.p4()+j1.p4()
    elif dr1:
        p4 = fj.p4()+j0.p4()
    else:
        p4 = fj.p4()+j0.p4()+j1.p4()
    #print(p4, p4.M())
    return p4

def top3j1fj(fj, j0, j1, j2):
    #print(hypot(j0.eta,j0.phi))
    dr0 = hypot(j0.eta(), j0.phi())<0.8
    dr1 = hypot(j1.eta(), j1.phi())<0.8
    dr2 = hypot(j2.eta(), j2.phi())<0.8
    if dr0*dr1*dr2:
        p4 = fj.p4()
    elif dr0*dr1:
        p4 = fj.p4()+j2.p4()
    elif dr0*dr2:
        p4 = fj.p4()+j1.p4()
    elif dr1*dr2:
        p4 = fj.p4()+j0.p4()
    elif dr0:
        p4 = fj.p4()+j1.p4()+j2.p4()
    elif dr1:
        p4 = fj.p4()+j0.p4()+j2.p4()
    elif dr2:
        p4 = fj.p4()+j0.p4()+j1.p4()
    else:
        p4 = (j0.p4()+j1.p4()+j2.p4()) #None      ###<--------------------to exclude 3j1fj not overlapping
    #print(p4, p4.M())
    return p4



def pt_top(j0, j1, j2, fj):
    
    if fj == None:
       
        top = j0.p4() + j1.p4() + j2.p4()
    elif j2 ==None:
        top = top2j1fj(fj, j0, j1)
    else:
        top = top3j1fj(fj, j0, j1, j2)
    return top

categories = ['3j0fj', '3j1fj', '2j1fj']

for d in trs:
    print(d)
    for c in categories:
        idx_drop_pt_selection = []
        for i in range(len(trs[d][c][2])):
            j0 = Jet(pt = trs[d][c][0][i,0,5],eta=  trs[d][c][0][i,0,7], phi=trs[d][c][0][i,0,6], mass = trs[d][c][0][i,0,3])
            j1 = Jet(pt = trs[d][c][0][i,1,5],eta= trs[d][c][0][i,1,7],phi= trs[d][c][0][i,1,6],mass= trs[d][c][0][i,1,3])
            j2 = Jet(pt = trs[d][c][0][i,2,5],eta= trs[d][c][0][i,2,7],phi= trs[d][c][0][i,2,6],mass= trs[d][c][0][i,2,3])
            fj = FatJet(pt = trs[d][c][1][i,11],eta= trs[d][c][1][i,8],phi= trs[d][c][1][i,10],mass= trs[d][c][1][i,9])
            if j2.pt() == 0:
                #print(j0.eta, j0.phi)
                top_p4 = pt_top(j0 = j0,j1 = j1, j2 = None, fj = fj)
                
            elif fj.pt() == 0:
                top_p4 = pt_top(j0 = j0, j1 = j1, j2 = j2, fj = None)
            else:
                top_p4 = pt_top(j0=j0, j1=j1, j2=j2, fj=fj)
            #print(top_p4)
            if top_p4.Pt() > 500 or top_p4.Pt() <350:
                idx_drop_pt_selection.append(i)
                
        trs[d][c][0] = np.delete(trs[d][c][0], idx_drop_pt_selection, axis=0)    
        trs[d][c][1] = np.delete(trs[d][c][1], idx_drop_pt_selection, axis=0)
        trs[d][c][2] = np.delete(trs[d][c][2], idx_drop_pt_selection, axis=0)
        trs[d][c][3] = np.delete(trs[d][c][3], idx_drop_pt_selection, axis=0)
        


                
                
     
       