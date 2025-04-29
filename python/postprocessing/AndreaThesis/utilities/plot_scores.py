import ROOT
import numpy
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event, InputTree

path = '/eos/user/a/apuglia/thesis/Datasets/Dataset_26_04_2025_Scores/'
name = ['ZJetsto2Nu_HT2500_2022_Skim_Scores.root']

rfile  = ROOT.TFile.Open(path + name[0])
# file.ls()
# tree = file.Get('Events')
tree          = InputTree(rfile.Get("Events"))
c1 = ROOT.TCanvas()
histo_1 = ROOT.TH1F('histo_top_mixed_tt_score', 'histo_top_mixed_tt_score', 100,0,1)
# tree.Print('TopMixed_*')
for i in range(tree.GetEntries()):
    event = Event(tree,i)
    tops = Collection(event, 'TopMixed')
    for top in tops:
        histo_1.Fill(top.TTScore)
        # print(j)

histo_1.Scale(1.0/histo_1.Integral())
histo_1.Draw('hist')
c1.Draw()
c1.SaveAs('Scores.png')

