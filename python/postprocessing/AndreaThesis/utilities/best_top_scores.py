import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event, InputTree

file =  ROOT.TFile('/eos/user/a/apuglia/thesis/Datasets/Dati_14_05_2025_Scores/tree_hadd_23_Scores_Selected.root', 'READ')

tree = InputTree(file.Get('Events'))

histo_ft = ROOT.TH1F('ft scores distribution for best zj score', 'ft scores distribution for best zj score',50, 0, 1)
histo_zj = ROOT.TH1F('zj scores distribution for best ft score', 'zj scores distribution for best ft score', 50, 0, 1)

score_cut_ft, score_cut_zj = 0.885, 0.985
for i in range(tree.GetEntries()):
    event = Event(tree, i)
    tops = Collection(event, 'TopMixed')

    best_top_idx_ft   , best_top_idx_zj  = 0,0
    best_top_score_ft , best_top_score_zj = 0,0
    
    for top_idx in range(len(tops)):
        top = tops[top_idx]
        
        score_ft= top.TTScore/(top.FTScore + top.TTScore)
        score_zj = top.TTScore/(top.TTScore + top.ZJScore)
        if score_ft > best_top_score_ft:
            best_top_idx_ft = top_idx
            best_top_score_ft = score_ft
        if score_zj > best_top_score_zj:
            best_top_idx_zj = top_idx
            best_top_score_zj = score_zj
        
    
    if len(tops) != 0:
        best_top_ft = tops[best_top_idx_ft]
        score_zj_best_top = best_top_ft.TTScore/(best_top_ft.ZJScore + best_top_ft.TTScore)
        if score_zj_best_top >= score_cut_zj:
            histo_zj.Fill(score_zj_best_top)
        best_top_zj = tops[best_top_idx_zj]
        score_ft_best_top = best_top_zj.TTScore/(best_top_zj.FTScore + best_top_zj.TTScore)
        if score_ft_best_top >= score_cut_ft:
            histo_ft.Fill(score_ft_best_top)


# histo_best_top = ROOT.TH1F('best_top_zj_scores', 'best_top_zj_scores', 50, 0, 1)






c1  =ROOT.TCanvas()

histo_ft.Scale(1.0/histo_ft.Integral())


histo_ft.Draw('hist')

c1.Draw()
c1.SaveAs('ft_distribution_scores_zj_best_tops.png')

c2  =ROOT.TCanvas()

histo_zj.Scale(1.0/histo_zj.Integral())

histo_zj.Draw('hist')

c2.Draw()
c2.SaveAs('zj_distribution_scores_ft_best_tops.png')

