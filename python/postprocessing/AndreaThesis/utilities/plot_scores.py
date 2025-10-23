import ROOT
import numpy
from tqdm import tqdm
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event, InputTree

# 
# name = ['ZJetsto2Nu_HT2500_2022_Skim_Scores.root']


histo_TT_true_top_tt_score = ROOT.TH1F('True_TT_scores', 'True_TT_scores', 100,0,1)
histo_TT_true_top_zj_score = ROOT.TH1F('True_TT_scores', 'True_TT_scores', 100,0,1)
histo_TT_false_top_tt_score= ROOT.TH1F('True_TT_scores', 'True_TT_scores', 100,0,1)
histo_TT_false_top_zj_score= ROOT.TH1F('True_TT_scores', 'True_TT_scores', 100,0,1)
histo_QCD_tt_score = ROOT.TH1F('QCD_scores', 'QCD_scores', 100,0,1)
histo_QCD_zj_score = ROOT.TH1F('QCD_scores', 'QCD_scores', 100,0,1)
histo_ZJ_tt_score = ROOT.TH1F('WJets_scores', 'WJets_scores', 100,0,1)
histo_ZJ_zj_score = ROOT.TH1F('WJets_scores', 'WJets_scores', 100,0,1)
path_to_folder = '/eos/user/a/apuglia/Thesis/Datasets/'


list_files = ['TT_semilep_2022/Scores/file_cluster_0_20June_Selected.root', 'QCD_HT2000_2022/Scores/file_cluster_0_20June_Selected.root',
'WJets_HT1500to2500_2022/Scores/file_cluster_0_20June_Selected.root']
for fileName in list_files:
    if fileName.endswith(".root") and not(fileName.startswith(".")):
        rfile = ROOT.TFile.Open(path_to_folder + fileName)
        print('file is: ', fileName)
        tree = InputTree(rfile.Get('Events'))
        print('num events is:', tree.GetEntries())
        for i in range(tree.GetEntries()):
            event = Event(tree, i)
            tops = Collection(event, 'TopMixed')

            for top_idx in range(len(tops)):

                score_tt = tops[top_idx].TTScore
                score_zj = tops[top_idx].ZJScore
                score_ft = tops[top_idx].FTScore

                score_1 = score_tt/(score_tt + score_ft)
                score_2 = score_tt/(score_tt + score_zj)
                
                if 'TT' in fileName:
                    if tops[top_idx].truth == 0:
                        histo_TT_false_top_tt_score.Fill(score_1)
                        histo_TT_false_top_zj_score.Fill(score_2)
                    if tops[top_idx].truth ==1:
                        histo_TT_true_top_tt_score.Fill(score_1)
                        histo_TT_true_top_zj_score.Fill(score_2)
                elif 'QCD' in fileName:
                    histo_QCD_tt_score.Fill(score_1)
                    histo_QCD_zj_score.Fill(score_2)
                elif 'WJ' in fileName:
                    histo_ZJ_tt_score.Fill(score_1)
                    histo_ZJ_zj_score.Fill(score_2)

            

histo_TT_false_top_tt_score.Scale(1.0/histo_TT_false_top_tt_score.Integral())
histo_ZJ_tt_score.Scale(1.0/histo_ZJ_tt_score.Integral())
histo_TT_true_top_tt_score.Scale(1.0/histo_TT_true_top_tt_score.Integral())
histo_QCD_tt_score.Scale(1.0/histo_QCD_tt_score.Integral())

histo_TT_false_top_zj_score.Scale(1.0/histo_TT_false_top_zj_score.Integral())
histo_ZJ_zj_score.Scale(1.0/histo_ZJ_zj_score.Integral())
histo_TT_true_top_zj_score.Scale(1.0/histo_TT_true_top_zj_score.Integral())
histo_QCD_zj_score.Scale(1.0/histo_QCD_zj_score.Integral())


histo_TT_false_top_tt_score.SetLineColor(ROOT.kRed+1)
histo_ZJ_tt_score.SetLineColor(ROOT.kBlue)
histo_TT_true_top_tt_score.SetLineColor(ROOT.kGreen)
histo_QCD_tt_score.SetLineColor(ROOT.kOrange - 3)

histo_TT_false_top_zj_score.SetLineColor(ROOT.kRed+1)
histo_ZJ_zj_score.SetLineColor(ROOT.kBlue)
histo_TT_true_top_zj_score.SetLineColor(ROOT.kGreen)
histo_QCD_zj_score.SetLineColor(ROOT.kOrange - 3)

c1 = ROOT.TCanvas()
histo_ZJ_tt_score.Draw('hist')
histo_QCD_tt_score.Draw('samehist')
histo_TT_true_top_tt_score.Draw('samehist')
histo_TT_false_top_tt_score.Draw('samehist')

c1.SetTitle('true tops vs false tops scores')

leg1 = ROOT.TLegend(0.7,0.7, 0.5,0.9)
leg1.SetHeader('legend', 'C')
leg1.AddEntry(histo_TT_false_top_tt_score, 'false tops')
leg1.AddEntry(histo_TT_true_top_tt_score, 'true tops')
leg1.AddEntry(histo_ZJ_tt_score, 'WJets')
leg1.AddEntry(histo_QCD_tt_score, 'QCD')
leg1.Draw()

c1.Draw()
c1.SaveAs('tt_scores.png')

c2 = ROOT.TCanvas()
histo_ZJ_zj_score.Draw('hist')
histo_QCD_zj_score.Draw('samehist')
histo_TT_true_top_zj_score.Draw('samehist')
histo_TT_false_top_zj_score.Draw('samehist')

c2.SetTitle('true tops vs zjets scores')

leg1 = ROOT.TLegend(0.7,0.7, 0.5,0.9)
leg1.SetHeader('legend', 'C')
leg1.AddEntry(histo_TT_false_top_zj_score, 'false tops')
leg1.AddEntry(histo_TT_true_top_zj_score, 'true tops')
leg1.AddEntry(histo_ZJ_zj_score, 'WJets')
leg1.AddEntry(histo_QCD_zj_score, 'QCD')
leg1.Draw()

c2.Draw()
c2.SaveAs('zj_scores.png')


nbins = histo_ZJ_zj_score.GetNbinsX()
print('number of bins is ', nbins)
working_points = [('15%',0.15),('10%',0.1), ('5%',0.05), ('1%',0.01)]
wp_values = {}
wp_values['ZJet score'] = {}
for wp in working_points:
    found = False
    wp_values['ZJet score'][wp[0]] = {}
    for i in range(1, nbins):
        zj_value = histo_ZJ_zj_score.Integral(i,nbins)
        if zj_value <= wp[1] and not found:
            found = True
            wp_values['ZJet score'][wp[0]]['ZJ'] = zj_value
            print('working point: ', wp)
            score_cut = histo_ZJ_zj_score.GetBinCenter(i)
            print('score zj cut at: ', score_cut)
            print('False tt value at score cut ', score_cut,' is ', histo_TT_false_top_zj_score.Integral(i,nbins))
            print('True tt value at score cut ', score_cut, ' is ',  histo_TT_true_top_zj_score.Integral(i,nbins))
            print('QCD value at score cut ', score_cut, ' is ',  histo_QCD_zj_score.Integral(i,nbins))
            wp_values['ZJet score'][wp[0]]['True tt'] = histo_TT_true_top_zj_score.Integral(i,nbins)
            wp_values['ZJet score'][wp[0]]['False tt'] = histo_TT_false_top_zj_score.Integral(i,nbins)
            wp_values['ZJet score'][wp[0]]['QCD'] = histo_QCD_zj_score.Integral(i,nbins)


nbins = histo_QCD_zj_score.GetNbinsX()
print('number of bins is ', nbins)
working_points = [('15%',0.15),('10%',0.1), ('5%',0.05), ('1%',0.01)]
wp_values = {}
wp_values['QCD score'] = {}
for wp in working_points:
    found = False
    wp_values['QCD score'][wp[0]] = {}
    for i in range(1, nbins):
        qcd_value = histo_QCD_zj_score.Integral(i,nbins)
        if qcd_value <= wp[1] and not found:
            found = True
            wp_values['QCD score'][wp[0]]['ZJ'] = qcd_value
            print('working point: ', wp)
            score_cut = histo_QCD_zj_score.GetBinCenter(i)
            print('score zj cut at: ', score_cut)
            print('False tt value at score cut ', score_cut,' is ', histo_TT_false_top_zj_score.Integral(i,nbins))
            print('True tt value at score cut ', score_cut, ' is ',  histo_TT_true_top_zj_score.Integral(i,nbins))
            print('WJets value at score cut ', score_cut, ' is ',  histo_ZJ_zj_score.Integral(i,nbins))
            wp_values['QCD score'][wp[0]]['True tt'] = histo_TT_true_top_zj_score.Integral(i,nbins)
            wp_values['QCD score'][wp[0]]['False tt'] = histo_TT_false_top_zj_score.Integral(i,nbins)
            wp_values['QCD score'][wp[0]]['Wjets'] = histo_ZJ_zj_score.Integral(i,nbins)


nbins = histo_TT_false_top_tt_score.GetNbinsX()
print('number of bins is ', nbins)
working_points = [('15%',0.15),('10%',0.1), ('5%',0.05), ('1%',0.01)]
wp_values = {}
wp_values['TTfalse score'] = {}
for wp in working_points:
    found = False
    wp_values['TTfalse score'][wp[0]] = {}
    for i in range(1, nbins):
        tt_value = histo_TT_false_top_tt_score.Integral(i,nbins)
        if tt_value <= wp[1] and not found:
            found = True
            wp_values['TTfalse score'][wp[0]]['ZJ'] = tt_value
            print('working point: ', wp)
            score_cut = histo_TT_false_top_tt_score.GetBinCenter(i)
            print('score zj cut at: ', score_cut)
            print('ZJets value at score cut ', score_cut,' is ', histo_ZJ_tt_score.Integral(i,nbins))
            print('True tt value at score cut ', score_cut, ' is ',  histo_TT_true_top_tt_score.Integral(i,nbins))
            print('QCD value at score cut ', score_cut, ' is ', histo_QCD_tt_score.Integral(i,nbins))
            wp_values['TTfalse score'][wp[0]]['True tt'] = histo_TT_true_top_tt_score.Integral(i,nbins)
            wp_values['TTfalse score'][wp[0]]['zjets'] = histo_ZJ_tt_score.Integral(i,nbins)
            wp_values['TTfalse score'][wp[0]]['QCD'] = histo_QCD_tt_score.Integral(i,nbins)