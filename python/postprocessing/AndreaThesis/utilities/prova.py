import ROOT
# file = 'root://cms-xrd-global.cern.ch//store/user/fsalerno/PFNano/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/TT_semilep_2022/250314_154005/0000/PFnano_mcRun3_TT_inclusive_1000_1.root'
file = 'histos_roc_curve_200pt.root'
file_1= ROOT.TFile.Open(file,'READ')
file_1.ls()
# tree=  file_1.Get('Events')
# tree.GetEntries()
# tree.Print('*HLT*')