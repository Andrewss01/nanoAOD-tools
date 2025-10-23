import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event, InputTree
from tqdm import tqdm
import os
path = '/eos/user/a/apuglia/Thesis/Data/MuonRun3C27Jun2023/Scores_8May_model/'
histo_1 = ROOT.TH1F('histo score 1', 'histo score 1', 50, 0, 1)
histo_2 = ROOT.TH1F('histo score 2', 'histo score 2', 50, 0, 1)
histo_3 = ROOT.TH1F('histo score 3', 'histo score 3', 50, 0, 1)
for fileName in tqdm(os.listdir(path)):
    if fileName.endswith(".root") and not(fileName.startswith(".")) and not 'hist' in fileName and not 'prova' in fileName:
        # file = path + fileName
        print('fileName is ', fileName)
        file = ROOT.TFile.Open(path+fileName, 'READ')
# file = ROOT.TFile.Open('/eos/user/a/apuglia/Thesis/Data/tree_hadd_23_Scores.root', 'READ')

        tree = InputTree(file.Get('Events'))
        # tree.Print('TopMixed*')


        for i in range(tree.GetEntries()):
            event = Event(tree,i)
            tops = Collection(event,'TopMixed')
            for top in tops: 
                score_1 = top.TTScore/(top.FTScore + top.TTScore)  #Histo True Top Score
                score_2 = top.TTScore/(top.TTScore + top.ZJScore) 
                # score_3 = top.TopScore
                histo_1.Fill(score_1)
                histo_2.Fill(score_2)
                # histo_3.Fill(score_3)

c1 = ROOT.TCanvas()
histo_1.Scale(1.0/histo_1.Integral())
histo_2.Scale(1.0/histo_2.Integral())
# histo_3.Scale(1.0/histo_3.Integral())
histo_2.SetLineColor(ROOT.kRed)   #Coloe rosso True/ZJets
histo_1.SetLineColor(ROOT.kBlue)    #Colore blu - True/False
# histo_3.SetLineColor(ROOT.kGreen) 
histo_1.Draw('hist')
histo_2.Draw('samehist')
# histo_3.Draw('samehist')
c1.Draw()
c1.SaveAs('data_scores.png')