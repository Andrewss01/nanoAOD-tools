import ROOT
from tqdm import tqdm
import os
data_name_ = 'WtoLNu_4Jets_2J_2022'
path = '/eos/user/a/apuglia/Master_Thesis/PostProcessed_Datasets/' + data_name_ + '/'

# file_mc = ROOT.TFile.Open(path_mc)
# tree_mc = file_mc.Get('Events')
# print(tree_mc.GetEntries())
# for i in range(tree_mc.GetEntries()):
#     tree_mc.GetEntry(i)
    
#     print(i,' ', tree_mc.HLT_IsoMu24)
num = 0
num_tot_events = 0
if data_name_ == 'WtoLNu_4Jets_2022' or data_name_ == 'WtoLNu_4Jets_2J_2022' or data_name_ == 'WtoLNu_4Jets_3J_2022':
        file_list = ['file_1', 'file_2', 'file_3', 'file_4', 'file_5', 'file_6','file_7', 'file_8', 'file_9', 'file_10', 'file_0' ]
elif 'QCD_HT' in data_name_  :
    file_list = ['file_0', 'file_1', 'file_2', 'file_3', 'file_4', 'file_5', 'file_6', 'file_7', 'file_8', 'file_9', 'file_10', 'file_11', 'file_12', 'file_13', 'file_14', 'file_15', 'file_16', 'file_17', 'file_18', 'file_19', 'file_20', 'file_21', 'file_22', 'file_23', 'file_24', 'file_25', 'file_26', 'file_27', 'file_28', 'file_29']
elif 'WtoLNu_4Jets_4J' in data_name_:
    file_list = ['file_1', 'file_2', 'file_3', 'file_4', 'file_5', 'file_6','file_7', 'file_0']
else:
    file_list = ['file_0', 'file_1', 'file_2', 'file_3']
for fileName in tqdm(os.listdir(path)):
    if  fileName in file_list:
        # file  = ROOT.TFile.Open(path + fileName + '/' +fileName + '.root')
        # tree = file.Get('Events')
        # num +=  tree.GetEntries()
        file_2 = ROOT.TFile.Open(path + fileName + '/histOut_'+ fileName + '.root')
        dir_plot = file_2.Get('plots')
        h_gen  =dir_plot.Get('h_genweight')
        num_tot_events += int(h_gen.GetBinContent(1))

print( ' num_tot_events is: ', num_tot_events)

# print(num)