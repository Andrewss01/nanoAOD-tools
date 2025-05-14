import ROOT

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Event, InputTree, Collection, Object
import math
from array import array
import numpy as np


file = ROOT.TFile('Datasets/nano_mcRun3_ttsl1_topcand_PF_semilelp_Skim.root', 'OPEN')
tree_p = file.Get('Events')
tree = InputTree(tree_p)


tops_resolved = []
tops_mixed =  []
pt_range = range(0, 1050, 50)
tops_mixed_0, tops_mixed_1, tops_mixed_2 = [],[],[]
for i in range(0, tree.GetEntries()):
    event = Event(tree,i)
    electrons = Collection(event,'Electron')
    muons = Collection(event, 'Muon')
    jets = Collection(event, 'Jet')
    njet = len(jets)
    fatjets = Collection(event, 'FatJet')
    HT = Object(event, 'HT')
    PV = Object(event, 'PV')
    HLT = Object(event, 'HLT')
    Flag = Object(event, 'Flag')
    met = Object(event, 'MET')
    top_mixed = Collection(event, 'TopMixed')
    top_resolved = Collection(event, 'TopResolved')
    top_resolved_pt =[]
    top_mixed_0_pt, top_mixed_1_pt, top_mixed_2_pt = [], [], []
    top_mixed_pt = []
    for top in top_resolved:
        if top.truth == 1: 
            top_resolved_pt.append(top.pt)
    for top in top_mixed:
        if top.truth == 1:
            category = top.category
            if category == 0:
                top_mixed_0_pt.append(top.pt)
            elif category ==1 : 
                top_mixed_1_pt.append(top.pt)
            else:
                top_mixed_2_pt.append(top.pt)
            top_mixed_pt.append(top.pt)
    if i == 400:
        print(top_mixed_0_pt, top_resolved_pt, top_mixed_1_pt, top_mixed_2_pt, top_mixed_pt)
        
    
    if len(top_mixed_0_pt) !=0:
        tops_mixed_0.append(max(top_mixed_0_pt))
    if len(top_resolved_pt) !=0:
        tops_resolved.append(max(top_resolved_pt))
    if len(top_mixed_1_pt)!=0:
        tops_mixed_1.append(max(top_mixed_1_pt))
    if len(top_mixed_2_pt) !=0: 
        tops_mixed_2.append(max(top_mixed_2_pt))
    if len(top_mixed_pt) != 0:
        tops_mixed.append(max(top_mixed_pt))
        
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
        
import numpy as np
n_tops_resolved = np.zeros(21)
for pt in tops_resolved:
    k = pt//50
    #print(k)
    n_tops_resolved[int(k)] +=1 

#print(n_tops_resolved)

n_tops_mixed_0 = np.zeros(21)
for pt in tops_mixed_0:
    k = pt//50 
    n_tops_mixed_0[int(k)] += 1
    
n_tops_mixed_1 = np.zeros(21)
for pt in tops_mixed_1:
    k = pt//50 
    
    n_tops_mixed_1[int(k)] += 1

n_tops_mixed_2 = np.zeros(21)
for pt in tops_mixed_2:
    k = pt//50 
   
    if k>= 21:
        n_tops_mixed_2[20] +=1 
    else:
        n_tops_mixed_2[int(k)] += 1

n_tops_mixed = np.zeros(21)
for top in tops_mixed:
    k = pt//50
    
    if k>=21:
        n_tops_mixed[20] += 1
    else:
        n_tops_mixed[int(k)] += 1

error_n_resolved = np.sqrt(n_tops_resolved)
error_n_mixed_0 = np.sqrt(n_tops_mixed_0)
error_n_mixed_1 = np.sqrt(n_tops_mixed_1)
error_n_mixed_2 = np.sqrt(n_tops_mixed_2)
error_n_mixed = np.sqrt(n_tops_mixed)

c1 = ROOT.TCanvas()
curve_resolved = ROOT.TGraphErrors(len(pt_value),array("f",pt_value), array("f",n_tops_resolved), 
                                  array("f", pt_error), array("f", error_n_resolved))
curve_mixed_0 = ROOT.TGraphErrors(len(pt_value),array("f",pt_value), array("f",n_tops_mixed_0), 
                           array("f", pt_error), array("f", error_n_mixed_0))
curve_mixed_1 = ROOT.TGraphErrors(len(pt_value),array("f",pt_value), array("f",n_tops_mixed_1), 
                           array("f", pt_error), array("f", error_n_mixed_1))
curve_mixed_2 = ROOT.TGraphErrors(len(pt_value),array("f",pt_value), array("f",n_tops_mixed_2), 
                           array("f", pt_error), array("f", error_n_mixed_2))
curve_mixed = ROOT.TGraphErrors(len(pt_value),array("f",pt_value), array("f",n_tops_mixed), 
                           array("f", pt_error), array("f", error_n_mixed))


curve_resolved.SetMarkerStyle(4)
curve_resolved.SetMarkerColor(2)
curve_resolved.SetLineColor(2)
curve_resolved.Scale(1.0/(curve_resolved.Integral()))

curve_mixed_0.SetMarkerStyle(4)
curve_mixed_0.SetMarkerColor(100)
curve_mixed_0.SetLineColor(100)

curve_mixed_1.SetMarkerStyle(4)
curve_mixed_1.SetMarkerColor(45)
curve_mixed_1.SetLineColor(45)

curve_mixed.SetMarkerStyle(4)
curve_mixed.SetMarkerColor(55)
curve_mixed.SetLineColor(55)
curve_mixed.Scale(1.0/(curve_mixed.Integral()))

curve_mixed_1.SetTitle('N top vs pt')
curve_mixed_1.GetYaxis().SetTitle('N top truth = 1')
curve_mixed_1.GetXaxis().SetTitle('pt')

#curve_mixed_1.Draw('AP')
curve_resolved.Draw('SAMEP')
#curve_mixed_0.Draw('SAMEP')
#curve_mixed_2.Draw('SAMEP')
#curve_mixed.Draw('SAMEAP')


Leg = ROOT.TLegend(0.9,0.7,0.7,0.9)
Leg.SetHeader("Legend","C")
Leg.AddEntry(curve_resolved, "resolved")
#Leg.AddEntry(curve_mixed_0, "mixed 0")
#Leg.AddEntry(curve_mixed_1, "mixed 1")
#Leg.AddEntry(curve_mixed_2, "mixed 2")
Leg.AddEntry(curve_mixed, 'mixed')
Leg.Draw()

c1.Draw()
c1.SaveAs('Canvasprova.png')
