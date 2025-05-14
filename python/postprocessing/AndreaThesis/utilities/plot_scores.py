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
histo_ZJ_tt_score = ROOT.TH1F('ZJets_scores', 'ZJets_scores', 100,0,1)
histo_ZJ_zj_score = ROOT.TH1F('ZJets_scores', 'ZJets_scores', 100,0,1)
path_to_folder = '/eos/user/a/apuglia/thesis/Datasets/Dataset_05_05_2025_Scores/'
for fileName in tqdm(os.listdir(path_to_folder)):
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
                elif 'ZJ' in fileName:
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


histo_TT_false_top_tt_score.SetLineColor(ROOT.kRed)
histo_ZJ_tt_score.SetLineColor(ROOT.kBlue)
histo_TT_true_top_tt_score.SetLineColor(ROOT.kGreen)
histo_QCD_tt_score.SetLineColor(ROOT.kOrange)

histo_TT_false_top_zj_score.SetLineColor(ROOT.kRed)
histo_ZJ_zj_score.SetLineColor(ROOT.kBlue)
histo_TT_true_top_zj_score.SetLineColor(ROOT.kGreen)
histo_QCD_zj_score.SetLineColor(ROOT.kOrange)

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
leg1.AddEntry(histo_ZJ_tt_score, 'ZJets')
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
leg1.AddEntry(histo_ZJ_zj_score, 'ZJets')
leg1.AddEntry(histo_QCD_zj_score, 'QCD')
leg1.Draw()

c2.Draw()
c2.SaveAs('zj_scores.png')
