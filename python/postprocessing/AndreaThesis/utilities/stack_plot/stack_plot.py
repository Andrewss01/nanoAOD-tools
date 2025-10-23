#!/usr/local/bin/python
import os
import ROOT

from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
import json

from argparse import ArgumentParser

# >ython3 stack_plot.py -type_histo best_single_top -normalization True -plot_data True -lumi 8000

# python3 stack_plot.py -lumi 900 -path_to_file_root /eos/user/a/apuglia/Thesis/Graphics/Stack_plot/ -normalization True -log_scale False -mc_to_stack TT_semilep_2022,TT_hadr_2022,WJets_HT120to200_2022,WJets_HT200to400_2022,WJets_HT400to800_2022,WJets_HT800to1500_2022,WJets_HT1500to2500_2022,WJets_HT2500to4000_2022,WJets_HT4000to6000_2022,WJets_HT6000_2022
usage = 'python3 stack_plot.py -normalization True -plot_data True -lumi 8000 -type_histo best_single_top -pt_cut False'

# parser          = ArgumentParser(usage)

# parser.add_argument("-save_graphics"    , dest="save_graphics"     , default=True , required=False, type=bool, help="True if want to save plots"     )
# parser.add_argument("-lumi"              , dest="lumi"              , default=None , required=False, type=int , help="lumi to normalize mc"           )
# parser.add_argument("-path_to_file_root" , dest="path_to_file_root" , default="/eos/user/a/apuglia/Master_Thesis/Graphics/Stack_plot/" , required=False, type=str , help="path root file"  )               
# parser.add_argument("-type_histo"        , dest="type_histo"        , default = None , required = True, type = str)
# parser.add_argument("-plot_data"         , dest="plot_data"         , default=False  , required = True, type=bool, help="folder of data to plot"         )
# parser.add_argument("-normalization"     , dest="normalization"     , default=False  , required = True, type=bool, help="True if want to normalize mc"   )
# parser.add_argument("-pt_cut"         , dest="pt_cut"         , default=False, required=True, type=bool, help="True if want the log scale on y")
# parser.add_argument("-mc_to_stack"       , dest="mc_to_stack"       , default=False, required=True , type=str , help="mc to stack")

# options         = parser.parse_args()

### ARGS ###

# save_graphics             = options.save_graphics      
lumi                      = 8000
path_to_file_root         =  "/eos/user/a/apuglia/Master_Thesis/Graphics/Stack_plot/"
type_histo                = "best_single_top"
plot_data                 = True
normalization             = True
pt_cut                    = False
# log_scale                 = options.log_scale
# mc_to_stack               = options.mc_to_stack.split(',')


if pt_cut:
    file = ROOT.TFile.Open(path_to_file_root+ 'histos_'+type_histo + '_ptcut.root','READ')
else:
    file = ROOT.TFile.Open(path_to_file_root+ 'histos_'+type_histo + '.root','READ')
keys = file.GetListOfKeys()
# print('keys are: ', keys)

sample_dict = {'TT_hadronic_2022': TT_hadr_2022, 'TT_semilep_2022':TT_semilep_2022 , 'WtoLNu_HT120to200_2022':WJets_HT120to200_2022, 'WtoLNu_HT200to400_2022':WJets_HT200to400_2022,
                'WtoLNu_HT400to800_2022':WJets_HT400to800_2022, 'WtoLNu_HT800to1500_2022':WJets_HT800to1500_2022, 'WtoLNu_HT1500to2500_2022':WJets_HT1500to2500_2022,
                'WtoLNu_HT2500to4000_2022':WJets_HT2500to4000_2022, 'WtoLNu_HT4000to6000_2022':WJets_HT4000to6000_2022, 'WtoLNu_HT6000_2022':WJets_HT6000_2022,
                'QCD_HT70to100_2022': QCD_HT70to100_2022, 'QCD_HT100to200_2022': QCD_HT100to200_2022, 'QCD_HT200to400_2022':QCD_HT200to400_2022, 'QCD_HT400to600_2022':QCD_HT400to600_2022, 
                'QCD_HT600to800_2022': QCD_HT600to800_2022, 'QCD_HT800to1000_2022': QCD_HT800to1000_2022,'QCD_HT1000to1200_2022':QCD_HT1000to1200_2022, 'QCD_HT1200to1500_2022':QCD_HT1200to1500_2022,  
                'QCD_HT1500to2000_2022':QCD_HT1500to2000_2022,
                'QCD_HT2000_2022':QCD_HT2000_2022}

mc_to_stack = sample_dict.keys()
list_keys =[]
for key in keys: 
    list_keys.append(key.GetName())

file_dict= path_to_file_root + 'dict_normalization.json'
with open(file_dict, "r", encoding="utf-8") as f:
    dict_normalization = json.load(f)


# print('normalization is: ', normalization)
# print('plot data is; ', plot_data)
# print('lumi is:', lumi)
'''
CREAZIONE DEGLI STACK   
'''

h_stack_ft = ROOT.THStack('hs_ft_scores'  ,'Stack plot FT Scores all tops')
h_stack_qcd = ROOT.THStack('hs_qcd_scores','Stack plot QCD Scores all tops')
# h_stack_ft_wjets = ROOT.THStack('hs_ft_scores'  ,'hs_ft_scores')
# h_stack_qcd_wjets = ROOT.THStack('hs_qcd_scores','hs_qcd_scores')

'''
INSERIMENTO DEI DATI NELLO STACK PLOT
'''    
if plot_data:
    histo_ft_data  = file.Get('ttvsft_scores' )
    histo_qcd_data = file.Get('ttvsqcd_scores')
    histo_ft_data.SetMarkerStyle(20)
    histo_qcd_data.SetMarkerStyle(20)


# ùlist_histo_ft_wjets, list_histo_qcd_wjets = [],[]
for dataset in mc_to_stack: 
    name_histo_ft = 'ttvsft_scores_'+dataset
    name_histo_qcd = 'ttvsqcd_scores_'+dataset
    if name_histo_ft in list_keys:
        histo_ft = file.Get(name_histo_ft)
    if name_histo_qcd in list_keys:
        histo_qcd = file.Get(name_histo_qcd)
    if (normalization == True) and (lumi != None):
        sigma = dict_normalization['sigma'][dataset]
        num_event = dict_normalization['num_events'][dataset]
        if num_event!= 0:
            histo_ft.Scale((sigma * lumi)/(num_event))
            histo_qcd.Scale((sigma * lumi)/(num_event))
    elif (normalization == True) and (lumi is None):
        print('error: there is no lumi inserted')
    # else:
    #     histo_ft.Scale(1.0/(histo_ft.Integral()))
    #     histo_qcd.Scale(1.0/(histo_qcd.Integral()))
    # elif normalization == True
    
    # histo_ft.SetFillColor(0)
    # histo_qcd.SetFillColor(0)
    
    h_stack_ft.Add(histo_ft)
    h_stack_qcd.Add(histo_qcd)
    
# h_stack_ft_tt.Scale(1.0/h_stack_ft_tt.Integral())
# h_stack_qcd_tt.Scale(1.0/h_stack_qcd_tt.Integral())
# h_stack_ft_wjets.Scale(1.0/h_stack_ft_wjets.Integral())
# h_stack_qcd_wjets.Scale(1.0/h_stack_qcd_wjets.Integral())


 

cs_1 = ROOT.TCanvas('cs_ft_scores', 'cs_ft_scores', 10, 10, 700, 900)

# h_stack_ft_wjets.Draw('histstack')

h_stack_ft.Draw('hist')

histo_ft_data.Draw('SAMEP')


h_stack_ft.GetXaxis().SetTitle('FT Scores')
h_stack_ft.SetMaximum(10**7)
h_stack_ft.GetYaxis().SetTitle('num tops')

cs_2 = ROOT.TCanvas('cd_qcd_scores', 'cs_qcd_scores', 10,10 ,700,900)

# h_stack_qcd_wjets.Draw('stackhist')
histo_qcd_data.Draw('P')
h_stack_qcd.Draw('samehist')




h_stack_qcd.GetXaxis().SetTitle('QCD Scores')

h_stack_qcd.GetYaxis().SetTitle('num tops')

# for histo_qcd_ in list_histo_qcd:
#     histo_qcd_.Draw('samehist')

if pt_cut:
    path_to_file_save = path_to_file_root + 'stack_plot_' + type_histo + '_ptcut.root'
else: 
    path_to_file_save = path_to_file_root + 'stack_plot_' + type_histo + '.root'
file_save = ROOT.TFile.Open(path_to_file_save, 'RECREATE')

cs_1.Write()
cs_2.Write()

# cs_1.SaveAs('stack_ft_scores.png')
# cs_2.SaveAs('stack_qcd_scores.png')
file_save.Close()
# # pad2 = cs.cd(2)
# # cs.cd(2)
# # # pad2.SetLogy()
# # histo_data_qcd.Draw('P')
# # h_stack_qcd.Draw('histsame')
# # histo_data_qcd.Draw('SAMEP')
# # for histo_qcd_ in list_hist_qcd:
# #     histo_qcd_.Draw('hist')

# # cs.SetLogy()
# cs.Draw()
# cs.SaveAs('dati.png')
# # cs->Divide(2,2)
# # cs->cd(1) hs->Draw() T.DrawTextNDC(.5,.95,"Default drawing option")
# # cs->cd(2) hs->Draw("nostack") T.DrawTextNDC(.5,.95,"Option \"nostack\"")
# # cs->cd(3) hs->Draw("nostackb") T.DrawTextNDC(.5,.95,"Option \"nostackb\"")
# # cs->cd(4) hs->Draw("lego1") T.DrawTextNDC(.5,.95,"Option \"lego1\"")