import ROOT 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event, InputTree

file_no_sel = ROOT.TFile.Open('/eos/user/a/apuglia/thesis/Datasets/Dati_14_05_2025_Scores/tree_hadd_23_Scores.root', 'READ')
file_sel = ROOT.TFile.Open('/eos/user/a/apuglia/thesis/Datasets/Dati_14_05_2025_Scores/tree_hadd_23_Scores_Selected.root', 'READ')

tree_no_sel = InputTree(file_no_sel.Get('Events'))
tree_sel    = InputTree(file_sel.Get('Events'))
print('num events with no selection is: ', tree_no_sel.GetEntries() )
print('num events with selection is: ', tree_sel.GetEntries())

histo_ft_no_sel = ROOT.TH1F('histo_ft_scores' , 'histo_ft_scores', 100, 0, 1)
histo_zj_no_sel = ROOT.TH1F('histo_zj_scores', 'histo_zj_scores', 100, 0, 1)
histo_2D_no_sel = ROOT.TH2F('histo_2d_scores' , 'histo_2d_scores', 50, 0, 1, 50, 0 ,1 )

histo_ft_sel    = ROOT.TH1F('histo_ft_scores', 'histo_ft_scores', 100,0,1)
histo_zj_sel = ROOT.TH1F('histo_zj_scores', 'histo_zj_scores', 100, 0, 1)
histo_2D_sel = ROOT.TH2F('histo_2d_scores' , 'histo_2d_scores', 50, 0, 1, 50, 0 ,1 )

for i in range(tree_no_sel.GetEntries()):
    event = Event(tree_no_sel,i)
    tops = Collection(event,'TopMixed')
    for top in tops:
        if top.truth != 0: 
            print(top.truth)
        score_ft = top.TTScore/(top.FTScore + top.TTScore)
        score_zj = top.TTScore/(top.TTScore + top.ZJScore)
        
        histo_ft_no_sel.Fill(score_ft)
        histo_zj_no_sel.Fill(score_zj)
        
        histo_2D_no_sel.Fill(score_ft, score_zj)

for j in range(tree_sel.GetEntries()):
    event = Event(tree_sel, j)
    tops = Collection(event, 'TopMixed')
    for top in tops: 
        score_ft = top.TTScore/(top.FTScore + top.TTScore)
        score_zj = top.TTScore/(top.TTScore + top.ZJScore)

        histo_ft_sel.Fill(score_ft)
        histo_zj_sel.Fill(score_zj)

        histo_2D_sel.Fill(score_ft, score_zj)



c1 = ROOT.TCanvas()

histo_zj_no_sel.Scale(1.0/histo_zj_no_sel.Integral())
histo_ft_no_sel.Scale(1.0/histo_ft_no_sel.Integral())

histo_zj_no_sel.SetLineColor(ROOT.kRed)
histo_ft_no_sel.SetLineColor(ROOT.kBlue)

histo_ft_no_sel.Draw('hist')
histo_zj_no_sel.Draw('samehist')

c1.SaveAs('scores_separati_no_sel.png')

c2 = ROOT.TCanvas()
histo_2D_no_sel.Scale(1.0/histo_2D_no_sel.Integral())


histo_2D_no_sel.Draw('colz')
c2.SaveAs('scores_2d_no_sel.png')

c3 = ROOT.TCanvas()

histo_zj_sel.Scale(1.0/histo_zj_sel.Integral())
histo_ft_sel.Scale(1.0/histo_ft_sel.Integral())

histo_zj_sel.SetLineColor(ROOT.kRed)
histo_ft_sel.SetLineColor(ROOT.kBlue)

histo_ft_sel.Draw('hist')
histo_zj_sel.Draw('samehist')


c3.SaveAs('scores_separati_sel.png')

c4 = ROOT.TCanvas()

histo_2D_sel.Scale(1.0/histo_2D_sel.Integral())
histo_2D_sel.Draw('colz')

c4.SaveAs('scores_2d_sel.png')


found = False
for i in range(100,0,-1):

    bkg_rej = histo_zj_sel.Integral(1, i)
    print('bin: ', i, ' integral is: ', bkg_rej)
    # rej = histo1.Integral(i,nbins)
    if bkg_rej <= 0.95 and not found:
        found = True
        score_cut = histo_zj_sel.GetBinCenter(i)
        print('score cut for zj score at 95 [%] is: ', score_cut)

found = False
for j in range(100,0,-1):
    bkg_rej = histo_ft_sel.Integral(1,j)
    print('bin: ', j, ' integral is: ', bkg_rej)
    if bkg_rej <= 0.99 and not found:
        found = True
        score_cut = histo_ft_sel.GetBinCenter(j)
        print('score cut for ft score at 99[%] is: ', score_cut)
