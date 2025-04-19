import ROOT
# file = ROOT.TFile.Open('root://cms-xrd-global.cern.ch//store/user/fsalerno/PFNano/Zto2Nu-4Jets_HT-800to1500_TuneCP5_13p6TeV_madgraphMLM-pythia8/QCD_HT_800_1500_2022/250314_172417/0000/PFnano_mcRun3_TT_inclusive_1000_15.root')
# file = ROOT.TFile.Open('/eos/user/a/apuglia/thesis/Datasets/ZtoNu_4Jets_800to1500_Skim.root')
file = ROOT.TFile.Open('histOut.root')
file.ls()
dir = file.Get('plots')
dir.ls()
# histo = dir.Get('plots')

# c1 = ROOT.TCanvas()
# histo.Draw()
# c1.Draw()
# c1.SaveAs('prova.png')