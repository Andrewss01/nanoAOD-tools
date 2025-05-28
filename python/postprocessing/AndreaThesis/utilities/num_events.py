import ROOT
from tqdm import tqdm
import os 
path  = '/eos/user/a/apuglia/Thesis/Datasets/'
directories = ['QCD_HT400to600_2022', 'QCD_HT600to800_2022', 'QCD_HT800to1000_2022', 'QCD_HT1000to1200_2022', 'QCD_HT1200to1500_2022', 'QCD_HT1500to2000_2022', 
'QCD_HT2000_2022', 'TT_hadronic_2022', 'TT_inclusive_2022', 'TT_semilep_2022', 'TTZprimetoTT_3000_2022', 'ZJetsto2Nu_400to800_2022','ZJetsto2Nu_800to1500_2022', 'ZJetsto2Nu_HT1500to2500_2022', 
'ZJetsto2Nu_HT2500_2022']
for dir in directories:
    path_to_folder = path + dir
    num_tot = 0
    num_tot_sel = 0
    for fileName in tqdm(os.listdir(path_to_folder)):
        if fileName.endswith(".root") and not fileName.startswith(".") and fileName.startswith('file'): 
            if dir == 'TT_inclusive_2022' and fileName == 'file_cluster_3.root':
                continue
            if dir == 'TT_semilep_2022' and fileName == 'file_cluster_9.root':
                continue

            if dir == 'TTZprimetoTT_3000_2022' and fileName == 'file_cluster_2.root':
                continue
            print(fileName)
            # num_
            rfile = ROOT.TFile.Open(path_to_folder +"/"+  fileName)
            plot_dir = rfile.Get('plots')
            plot = plot_dir.Get('h_genweight')
            num_events = plot.GetBinContent(1)
            num_tot += num_events
            tree = rfile.Get('Events')
            sel_events=  tree.GetEntries()
            num_tot_sel += sel_events
    print('dataset: ', dir, ' total num of events: ', num_tot , ' selected events: ', num_tot_sel)
            # directory = file.Get('plots')
# directory.ls()
# tree = file.Get('Events')
# tree.GetEntries()