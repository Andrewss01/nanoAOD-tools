import ROOT
file_path = "davs://webdav.recas.ba.infn.it:8443/cms/store/user/apuglia/QCD-4Jets_HT-70to100_TuneCP5_13p6TeV_madgraphMLM-pythia8/QCD_HT70to100_2022_v2/251103_090511/0000/nano_mcRun3_1-1.root"
rootfile = ROOT.TFile.Open(file_path)
tree = rootfile.Get("Events")
tree.Print("Indexes*")
# list_branches = [key.GetName() for key in tree.GetListOfBranches()]
# print(list_branches)
# print(tree.GetListOfBranches())
# tree.GetEntry(0)
# eventweight = abs(tree.Generator_weight)
# # print(eventweight)
# runstree = rootfile.Get("Runs")
# runstree.GetEntry(0)
# geneventSumw = runstree.genEventSumw
# n = round(abs(geneventSumw/eventweight))
# print(n)
# print(tree.GetEntries())
# tree = f.Get('Events')
# tree.Print("Gen*")