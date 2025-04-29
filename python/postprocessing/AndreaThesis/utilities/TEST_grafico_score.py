import ROOT
import pickle
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Event, InputTree, Collection, Object

file = ROOT.TFile('TT_Skim_CutPt_Scores.root', 'OPEN')
tree_p = file.Get('Events')
tree = InputTree(tree_p)
#chain = ROOT.TChain('Events')
#chain.Add('nano_mcRun3_ttsl1_topcand_PF_semilelp_Skim.root')
#tree = InputTree(chain)
#chain.Print("TopMixed_*")


top_resolved_1, top_resolved_0 = [], []
top_mixed_1, top_mixed_0 = [], []
top_mixed_n_quark = []
#print(tree.GetEntries())
for i in range(0, tree.GetEntries()):
    event = Event(tree,i)
    top_mixed = Collection(event, 'TopMixed')
    top_resolved = Collection(event, 'TopResolved')
    
    #for top_r in top_resolved:
    #    if top_r.truth == 1: 
    #        top_resolved_1.append(top_r.TopScore)   #Prendo tutti i top resolved truth e metto il suo score nella lista 
    #    elif top_r.truth == 0:
    #        top_resolved_0.append(top_r.TopScore)   #Top falsi prendo lo score
    for top_m in top_mixed:
        if top_m.truth == 1:
            top_mixed_1.append(top_m.TopScore)
        elif top_m.truth == 0:
            top_mixed_0.append(top_m.TopScore)
            top_mixed_n_quark.append(top_m.nquark)
    
            
#histo_1_resolved = ROOT.TH1F('top resolved true', 'top resolved true', 30, 0,1)
#histo_0_resolved = ROOT.TH1F('top resolved false', 'top resolved false', 30, 0,1)

#for top1,top0 in zip(top_resolved_1, top_resolved_0):
#    histo_1_resolved.Fill(top1)
#    histo_0_resolved.Fill(top0)

histo_t1_mixed = ROOT.TH1F('top mixed true', 'top mixed true', 30, 0,1)
histo_t0_mixed = ROOT.TH1F('top mixed false', 'top mixed false', 30, 0,1)
histo_t0_0quark = ROOT.TH1F('top mixed false - 0 quark', 'top mixed false - 0 quark', 30, 0, 1)
histo_t0_1quark = ROOT.TH1F('top mixed false - 1 quark', 'top mixed false - 1 quark', 30, 0, 1)
histo_t0_2quark = ROOT.TH1F('top mixed false - 2 quark', 'top mixed false - 2 quark', 30, 0, 1)

for top1,top2 in zip(top_mixed_1, top_mixed_0):
    histo_t1_mixed.Fill(top1)
    histo_t0_mixed.Fill(top2)


print('len mixed truth 1', len(top_mixed_1))
print('len mixed truth 0', len(top_mixed_0))
for i in range(len(top_mixed_0)):
    if top_mixed_n_quark[i] == 0:
        histo_t0_0quark.Fill(top_mixed_0[i])
    elif top_mixed_n_quark[i] == 1:
        #print('prova')
        histo_t0_1quark.Fill(top_mixed_0[i])
    elif top_mixed_n_quark[i] == 2: 
        histo_t0_2quark.Fill(top_mixed_0[i])
    #histo_t0_mixed.Fill(top_mixed_0[i])
#c1 = ROOT.TCanvas("", "", 900,600)

#histo_0_resolved.SetLineColor(2)
#histo_0_resolved.SetName('score resolved truth = 0')
#histo_0_resolved.Draw()
#histo_1_resolved.SetLineColor(4)
#histo_1_resolved.SetName('score resolved truth = 1')

#histo_1_resolved.Draw('SAME')

#leg1 = ROOT.TLegend(0.4,0.8,0.6,0.9) 
#leg1.SetHeader("Legenda", "C")                         
#leg1.AddEntry(histo_1_resolved, "score resolved truth = 1","l")            
#leg1.AddEntry(histo_0_resolved, "score resolved truth = 0","l")
#leg1.Draw()

#c1.Draw()
#c1.SaveAs('grafico_resolved_scores.png')

c2 = ROOT.TCanvas("","",900,600)



histo_t0_0quark.SetLineColor(2)
histo_t0_0quark.SetName('score mixed truth = 0, 0 quark')
int_1 = histo_t0_0quark.Integral()
histo_t0_0quark.Scale(1.0/int_1)
histo_t0_0quark.Draw('hist')

histo_t0_1quark.SetLineColor(7)
histo_t0_1quark.SetName('score mixed truth = 0, 1 quark')
#int_1 = histo_t0_1quark.Integral()
#histo_t0_1quark.Scale(1.0/int_1)
histo_t0_1quark.Draw('SAMEhist')

histo_t0_2quark.SetLineColor(11)
histo_t0_2quark.SetName('score mixed truth = 0, 2 quark')
int_1 = histo_t0_2quark.Integral()
histo_t0_2quark.Scale(1.0/ int_1)
histo_t0_2quark.Draw('SAMEhist')

histo_t1_mixed.SetLineColor(4)
histo_t1_mixed.SetName('score mixed truth = 1') 
int_1 = histo_t1_mixed.Integral()
histo_t1_mixed.Scale(1.0/int_1)
histo_t1_mixed.Draw('SAMEhist')

leg2 = ROOT.TLegend(0.4,0.8,0.6,0.9) 
leg2.SetHeader("Legenda", "C")                         
leg2.AddEntry(histo_t1_mixed, "score mixed truth = 1","l")            
leg2.AddEntry(histo_t0_0quark, "score mixed truth = 0, 0 quark","l")
leg2.AddEntry(histo_t0_1quark, "score mixed truth = 0, 1 quark","l")
leg2.AddEntry(histo_t0_2quark, "score mixed truth = 0, 2 quark","l")


leg2.Draw()


#c2.Draw()
c2.SaveAs('grafico_mixed_score.png')

with open('PhysicsTools/NanoAODTools/python/postprocessing/data/dict_tresholds/tresholds.pkl', 'rb') as f:
    data = pickle.load(f)
    
keys, tsh = [],[]
for key in data.keys():
    keys.append(key)
    tsh.append(data[key])
    
tsh_fpr_10 = tsh[0]
tsh_fpr_5 = tsh[1]
tsh_fpr_1 = tsh[2]
tsh_fpr_01 = tsh[3]

print(tsh)

def Rate(tsh, values):
    rate = 0 
    for i in values: 
        if i >= tsh:
            rate +=1 
    rate = rate/(len(values))
    
    return rate

fpr_10_m = Rate(tsh_fpr_10, top_mixed_0)
eff_10_m = Rate(tsh_fpr_10, top_mixed_1) 

fpr_5_m = Rate(tsh_fpr_5, top_mixed_0)
eff_5_m = Rate(tsh_fpr_5, top_mixed_1) 

fpr_1_m = Rate(tsh_fpr_1, top_mixed_0)
eff_1_m = Rate(tsh_fpr_1, top_mixed_1) 

fpr_01_m = Rate(tsh_fpr_01, top_mixed_0)
eff_01_m = Rate(tsh_fpr_01, top_mixed_1) 

print('top mixed (10%), tsh = ', tsh_fpr_10, 'fpr = ',fpr_10_m,'eff = ',eff_10_m)
print('top mixed (5%), tsh = ', tsh_fpr_5, 'fpr = ',fpr_5_m,'eff = ',eff_5_m)
print('top mixed (1%), tsh = ', tsh_fpr_1, 'fpr = ',fpr_1_m,'eff = ',eff_1_m)
print('top mixed (0.1%), tsh = ', tsh_fpr_01, 'fpr = ',fpr_01_m,'eff = ',eff_01_m)



#print(len(top_mixed_0), len(top_mixed_1))
    