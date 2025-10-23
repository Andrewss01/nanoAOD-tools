#!/usr/local/bin/python
import os
from draw_functions import * 
import ROOT
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
# from PhysicsTools.NanoAODTools.postprocessing.AndreaThesis.utilities.dataset import *

from argparse import ArgumentParser
'''
python3 make_histo.py -type_histo best_single_top -path_to_data /eos/user/a/apuglia/Master_Thesis/Data/MuonRun3C27Jun2023/Scores_cnn_model/ -path_to_mc /eos/user/a/apuglia/Master_Thesis/PostProcessed_Datasets/ -pt_cut False

'''

type_histo = 'best_single_top'
path_to_data = '/eos/user/a/apuglia/Master_Thesis/Data/MuonRun3C2022/Scores_cnn_model/'
path_to_mc  = '/eos/user/a/apuglia/Master_Thesis/PostProcessed_Datasets/'
pt_cut = True
folder = '/eos/user/a/apuglia/Master_Thesis/Graphics/Stack_plot/'
model = 'cnn'
list_hist = []

sample_dict = {'TT_dilep_2022':TT_dilep_2022, 'TbarWplus_1L_2022': TbarWplus_1L_2022, 'TT_hadronic_2022': TT_hadr_2022, 'TT_semilep_2022':TT_semilep_2022,  'TWminus_1L_2022':TWminus_1L_2022, 
                'QCD_HT70to100_2022': QCD_HT70to100_2022, 'QCD_HT100to200_2022': QCD_HT100to200_2022, 'QCD_HT200to400_2022':QCD_HT200to400_2022, 'QCD_HT400to600_2022':QCD_HT400to600_2022, 
                'QCD_HT600to800_2022': QCD_HT600to800_2022, 'QCD_HT800to1000_2022': QCD_HT800to1000_2022, 'QCD_HT1000to1200_2022':QCD_HT1000to1200_2022,  'QCD_HT1200to1500_2022': QCD_HT1200to1500_2022, 'QCD_HT1500to2000_2022':QCD_HT1500to2000_2022,
                'QCD_HT2000_2022': QCD_HT2000_2022, 'WtoLNu_4Jets_4J_2022':WtoLNu_4Jets_4J_2022, 'WtoLNu_4Jets_3J_2022':WtoLNu_4Jets_3J_2022, 'WtoLNu_4Jets_2J_2022':WtoLNu_4Jets_2J_2022, 'WtoLNu_4Jets_2022':WtoLNu_4Jets_2022}
                
                # 'WtoLNu_HT120to200_2022':WJets_HT120to200_2022, 'WtoLNu_HT200to400_2022':WJets_HT200to400_2022, 'WtoLNu_HT400to800_2022':WJets_HT400to800_2022, 
                # 'WtoLNu_HT800to1500_2022':WJets_HT800to1500_2022, 'WtoLNu_HT1500to2500_2022':WJets_HT1500to2500_2022, 'WtoLNu_HT2500to4000_2022':WJets_HT2500to4000_2022, 
                # 'WtoLNu_HT4000to6000_2022':WJets_HT4000to6000_2022, 'WtoLNu_HT6000_2022':WJets_HT6000_2022}


if not os.path.exists(folder):
    os.makedirs(folder)   


mc_to_stack = sample_dict.keys()
dict_normalization = {}
dict_normalization['sigma'] = {}
dict_normalization['num_events'] ={}
for dataset_str in mc_to_stack:
    dataset = sample_dict[dataset_str]
    # label = dataset.label

    if (dataset_str == 'TT_semilep_2022' or dataset_str == 'TT_hadronic_2022' ) and type_histo == 'all_tops':
        histo_1q_ft, histo_1q_qcd, histo_2q_ft, histo_2q_qcd, histo_3q_ft, histo_3q_qcd, histo_0q_ft, histo_0q_qcd, sigma, num_events = make_plot_tt(path_ = path_to_mc, dataset_ = dataset, data_name = dataset_str, pt_cut = pt_cut, model = model)
        list_hist.append(histo_1q_ft)
        list_hist.append(histo_2q_ft)
        list_hist.append(histo_3q_ft)
        list_hist.append(histo_1q_qcd)
        list_hist.append(histo_2q_qcd)
        list_hist.append(histo_3q_qcd)
        list_hist.append(histo_0q_ft)
        list_hist.append(histo_0q_qcd)
    else:
        histo_ft, histo_qcd, num_events, sigma = make_plot_scores_mc(path_ = path_to_mc, dataset_ = dataset,data_name = dataset_str, file_options = type_histo, pt_cut = pt_cut, model = model)
        list_hist.append(histo_ft)
        list_hist.append(histo_qcd)
    dict_normalization['sigma'][dataset_str] = sigma
    dict_normalization['num_events'][dataset_str] = num_events
    # h_stack_ft.Add(histo_ft)
    # h_stack_qcd.Add(histo_qcd)


histo_data_ft, histo_data_qcd = make_plot_scores_data(path_ = path_to_data, color_ = ROOT.kBlack, style_ = ROOT.kCircle, file_options = type_histo, pt_cut = pt_cut, model = model)
list_hist.append(histo_data_ft)
list_hist.append(histo_data_qcd)
if pt_cut:
    print('sbagliato')
    file_root_name = 'histos_' + type_histo + '_'+model+'_ptcut.root'
else:
    print('giusto')
    file_root_name = 'histos_'+type_histo + '_'+model+'.root'
file = ROOT.TFile(folder + file_root_name, 'RECREATE')
for histo in list_hist:
    histo.Write()



import json

# Salvare nel file
with open(folder+'dict_normalization.json', "w", encoding="utf-8") as file:
    json.dump(dict_normalization, file, ensure_ascii=False, indent=4)

# file.Close()

