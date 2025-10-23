import ROOT 
import numpy as np 
from tqdm import tqdm
import os
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Event, InputTree, Collection

path  = '/eos/user/a/apuglia/Thesis/Datasets/'

directories = [ 'TT_semilep_2022', 'TT_inclusive_2022', 
'TT_hadr_2022', 'QCD_HT2000_2022', 'QCD_HT1500to2000_2022', 'QCD_HT1200to1500_2022',
'QCD_HT1000to1200_2022', 'QCD_HT800to1000_2022', 'QCD_HT600to800_2022', 'QCD_HT400to600_2022', 
'QCD_HT200to400_2022', 'QCD_HT100to200_2022', 'QCD_HT70to100_2022']


# c1 = ROOT.TCanvas()

corr_qcd_score = ROOT.TH2F('pt_vs_score_qcd','top pt vs qcd score QCD dataset score <0.05 ot score >0.9', 50,0,1, 100, 0, 1000 )

corr_tt_score = ROOT.TH2F('pt_vs_score_tt','top pt vs qcd score TT dataset score <0.05 ot score >0.9', 50,0,1, 100, 0, 1000 )

histo_qcd_low_cut = ROOT.TH1F('pt for score < 0.05 QCD dataset', 'pt for score < 0.05 QCD dataset', 100, 0, 1000)
histo_tt_low_cut = ROOT.TH1F('pt for score < 0.05 TT dataset', 'pt for score < 0.05 TT dataset', 100, 0, 1000)
histo_qcd_high_cut = ROOT.TH1F('pt for score >0.9 QCD dataset', 'pt for score >0.9 QCD dataset', 100, 0, 1000)
histo_tt_high_cut = ROOT.TH1F('pt for score >0.9 TT dataset', 'pt for score >0.9 TT dataset', 100, 0, 1000)

h2d_plot =False
if h2d_plot :
    for dir in directories:
        path_files = path + dir + '/Scores/'
        for fileName in tqdm(os.listdir(path_files)):
            if '20June' in fileName:
                file = ROOT.TFile(path_files+ fileName, 'READ')
                tree = file.Get('Events')
                tree = InputTree(tree)
    
                for i in range(tree.GetEntries()):
                    tree.GetEntry(i)
                    event = Event(tree,i)
                    topmixed = Collection(event, 'TopMixed')
    
                    for top in topmixed:
                        score_qcd = top.TTScore/(top.ZJScore + top.TTScore)
                       
                        if 'QCD' in dir:
                            corr_qcd_score.Fill(score_qcd, top.pt)
                        else: 
                            corr_tt_score.Fill(score_qcd, top.pt)
else:
    for dir in directories:
        path_files = path + dir + '/Scores/'
        for fileName in tqdm(os.listdir(path_files)):
            if '20June' in fileName:
                file = ROOT.TFile(path_files+ fileName, 'READ')
                tree = file.Get('Events')
                tree = InputTree(tree)

                for i in range(tree.GetEntries()):
                    tree.GetEntry(i)
                    event = Event(tree,i)
                    topmixed = Collection(event, 'TopMixed')

                    for top in topmixed:
                        score_qcd = top.TTScore/(top.ZJScore + top.TTScore)

                        if 'QCD' in dir:
                            if score_qcd < 0.05:
                                histo_qcd_low_cut.Fill(top.pt)
                            elif score_qcd > 0.9:
                                histo_qcd_high_cut.Fill(top.pt)
                        else:
                            if score_qcd < 0.05:
                                histo_tt_low_cut.Fill(top.pt)
                            elif score_qcd > 0.9:
                                histo_tt_high_cut.Fill(top.pt)
                   


folder=  '/eos/user/a/apuglia/Thesis/Graphics/Correlations/'
file_root_name = 'histo_1d_pt_scores_cuts.root'

file = ROOT.TFile(folder + file_root_name, 'RECREATE')

# corr_qcd_pt_high.Scale(1.0/corr_qcd_pt_high.Integral())
# corr_qcd_pt_low.Scale(1.0/corr_qcd_pt_low.Integral())
# corr_qcd_score.Scale(1.0/corr_qcd_score.Integral())
# corr_tt_pt_high.Scale(1.0/corr_tt_pt_high.Integral())
# corr_tt_pt_low.Scale(1.0/corr_tt_pt_low.Integral())
# corr_tt_score.Scale(1.0/corr_tt_score.Integral())
# corr_qcd_pt_high.Write()
# corr_qcd_pt_low.Write()
# corr_qcd_score.Write()
# corr_tt_pt_high.Write()
# corr_tt_pt_low.Write()
# corr_tt_score.Write()
histo_qcd_high_cut.Scale(1.0/histo_qcd_high_cut.Integral())
histo_qcd_low_cut.Scale(1.0/histo_qcd_low_cut.Integral())
histo_tt_high_cut.Scale(1.0/histo_tt_high_cut.Integral())
histo_tt_low_cut.Scale(1.0/histo_tt_low_cut.Integral())

histo_qcd_high_cut.Write()
histo_qcd_low_cut.Write()
histo_tt_high_cut.Write()
histo_tt_low_cut.Write()