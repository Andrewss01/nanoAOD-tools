import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Event, InputTree, Collection
import numpy as np

#name = '_Skim_10k_ScoresMS.root'
TT_file  = 'TT_Skim_10k_ScoresMS.root'
ZJ1_file = 'ZJ_1_Skim_ScoresMS.root'
ZJ2_file = 'ZJ_2_Skim_ScoresMS.root'

#histo_ZJ = ROOT.TH1F('zj_histo', 'zj scores',50,0,1)
#histo_TT = ROOT.TH1F('tt_histo', 'tt scores',50,0,1)
h2_ZJ = ROOT.TH2F("h2", "Esempio di istogramma 2D;X;Y", 50, 0, 1, 50, 0, 1)
h2_true_top = ROOT.TH2F('h2 true top','istogramma 2d', 50, 0,1,50,0,1)
h2_false_top = ROOT.TH2F('h2 true top','istogramma 2d', 50, 0,1,50,0,1)

histo_zj_1 = ROOT.TH1F('zj histo', 'zj scores', 60, 0, 1)
histo_zj_2 = ROOT.TH1F('zj histo', 'zj scores', 60, 0, 1)

histo_tt_true_1 = ROOT.TH1F('true tt histo', 'true tt scores', 60, 0, 1)
histo_tt_true_2 = ROOT.TH1F('true tt histo', 'true tt scores', 60, 0, 1)

histo_tt_false_1 = ROOT.TH1F('false tt histo', 'false tt scores', 60, 0, 1)
histo_tt_false_2 = ROOT.TH1F('false tt histo', 'false tt scores', 60, 0, 1)

for fname in [TT_file, ZJ1_file, ZJ2_file]:
    
    file = ROOT.TFile(fname, 'READ')
    tree = file.Get('Events')
    tree = InputTree(tree)

    for i in range(tree.GetEntries()):
        tree.GetEntry(i)
        event = Event(tree,i)
        topmixed = Collection(event, 'TopMixed')

        scores_values = list(tree.TopMixed_TopScore)
    # print(scores_values)
        proba = [scores_values[j:j+3] for j in range(0, len(scores_values), 3)]

        for top_idx in range(len(topmixed)):
            # print(i)
            # print(proba[top_idx])
            score_zj = (proba[top_idx][0]/(proba[top_idx][2]+proba[top_idx][0]))
            score_tt = (proba[top_idx][0]/(proba[top_idx][1]+proba[top_idx][0]))
            
            if 'ZJ' in fname:
                h2_ZJ.Fill(score_zj, score_tt)
                histo_zj_1.Fill(score_zj)
                histo_zj_2.Fill(score_tt)
            else:
                if topmixed[top_idx].truth == 1: 
                    h2_true_top.Fill(score_zj, score_tt)
                    histo_tt_true_1.Fill(score_zj)
                    histo_tt_true_2.Fill(score_tt)
                else:
                    h2_false_top.Fill(score_zj, score_tt)
                    histo_tt_false_1.Fill(score_zj)
                    histo_tt_false_2.Fill(score_tt)
            




c1 = ROOT.TCanvas()
histo_zj_1.Scale(1.0/histo_zj_1.Integral())
histo_zj_2.Scale(1.0/histo_zj_2.Integral())
histo_zj_1.SetLineColor(8)
histo_zj_2.SetLineColor(2)
histo_zj_1.Draw('hist')
histo_zj_2.Draw('samehist')
leg = ROOT.TLegend(0.7,0.7, 0.5,0.9)
leg.SetHeader('legend', 'C')
leg.AddEntry(histo_zj_1, 'zj score')
leg.AddEntry(histo_zj_2, 'tt score')
leg.Draw()
c1.Draw()
c1.SetTitle('ZJ scores')
c1.SaveAs('ZJ_scores.png')

c2 = ROOT.TCanvas()
histo_tt_true_1.Scale(1.0/histo_tt_true_1.Integral())
histo_tt_true_2.Scale(1.0/histo_tt_true_2.Integral())
histo_tt_true_1.SetLineColor(8)
histo_tt_true_2.SetLineColor(2)
histo_tt_true_1.Draw('hist')
histo_tt_true_2.Draw('samehist')
leg1 = ROOT.TLegend(0.7,0.7, 0.5,0.9)
leg1.SetHeader('legend', 'C')
leg1.AddEntry(histo_tt_true_1, 'zj score')
leg1.AddEntry(histo_tt_true_2, 'tt score')
leg1.Draw()
c2.Draw()
c2.SetTitle('True TT scores')
c2.SaveAs('True TT_scores.png')


c3 = ROOT.TCanvas()
histo_tt_false_1.Scale(1.0/histo_tt_false_1.Integral())
histo_tt_false_2.Scale(1.0/histo_tt_false_2.Integral())
histo_tt_false_1.SetLineColor(8)
histo_tt_false_2.SetLineColor(2)
histo_tt_false_1.Draw('hist')
histo_tt_false_2.Draw('samehist')
leg2 = ROOT.TLegend(0.7,0.7, 0.5,0.9)
leg2.SetHeader('legend', 'C')
leg2.AddEntry(histo_tt_false_1, 'zj score')
leg2.AddEntry(histo_tt_false_2, 'tt score')
leg2.Draw()
c3.Draw()
c3.SetTitle('false TT scores')
c3.SaveAs('false TT_scores.png')

nbins = histo_zj_1.GetNbinsX()
print('number of bins is ', nbins)
working_points = [('15%',0.15),('10%',0.1), ('5%',0.05), ('1%',0.01)]
wp_values = {}
wp_values['ZJet score'] = {}
for wp in working_points:
    found = False
    wp_values['ZJet score'][wp[0]] = {}
    for i in range(1, nbins):
        zj_value = histo_zj_1.Integral(i,nbins)
        if zj_value <= wp[1] and not found:
            found = True
            wp_values['ZJet score'][wp[0]]['ZJ'] = zj_value
            print('working point: ', wp)
            score_cut = histo_zj_1.GetBinCenter(i)
            print('score zj cut at: ', score_cut)
            print('False tt value at score cut ', score_cut,' is ', histo_tt_false_1.Integral(i,nbins))
            print('True tt value at score cut ', score_cut, ' is ',  histo_tt_true_1.Integral(i,nbins))
            wp_values['ZJet score'][wp[0]]['True tt'] = histo_tt_true_1.Integral(i,nbins)
            wp_values['ZJet score'][wp[0]]['False tt'] = histo_tt_false_1.Integral(i,nbins)
            
wp_values['TT score'] = {}
for wp in working_points:
    found = False
    wp_values['TT score'][wp[0]] = {}
    for j in range(1,nbins):
        false_tt_value = histo_tt_false_2.Integral(j, nbins)
        if false_tt_value <= wp[1] and not found: 
            found = True
            print('working point: ', wp)
            score_cut = histo_tt_false_2.GetBinCenter(j)
            wp_values['TT score'][wp[0]]['false tt'] = false_tt_value
            print('score tt cut at: ', score_cut)
            print('Zj value at score cut ', score_cut,' is ', histo_zj_2.Integral(j,nbins))
            print('True tt value at score cut ', score_cut, ' is ',  histo_tt_true_2.Integral(j,nbins))
            wp_values['TT score'][wp[0]]['true tt'] = histo_tt_true_2.Integral(j,nbins)
            wp_values['TT score'][wp[0]]['zjets'] = histo_zj_2.Integral(j,nbins)

import json
path_to_outJson = '/eos/user/a/apuglia/SWAN_projects/thesis/CMSSW_14_1_7/src/2D_scores_cut'
with open(path_to_outJson, "w") as f:
    #json.dump(title, f)  
    json.dump(wp_values, f, indent=4)