import ROOT

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Event, InputTree, Collection, Object
import math
from array import array
import numpy as np
import json
import argparse

usage       = 'python3 Scores_graph.py'
file_folder = "/eos/user/a/apuglia/SWAN_projects/thesis/CMSSW_14_1_7/src/Datasets/"

name_1 = '_Skim_Scores1.root'  #dataset con gli scores del modello TT
name_2 = '_Skim_Scores2.root'  #dataset con gli scores del modello TTZJ senza fondo TT

names = ['TT','ZJ_1','ZJ_2']

example= 'python3 Scores_graph.py -j /eos/user/a/apuglia/SWAN_projects/thesis/CMSSW_14_1_7/src/trainings/wpvalues_CutPt_model2.json'
    
parser      = argparse.ArgumentParser(usage)
#parser.add_argument('-j', '--outJson',    dest = 'outJson',   required = True,   default = './working_point_values.json',      type = str, 
#                    help = 'complete path to save the score thresholds (default "./score_thresholds.json")')
parser.add_argument('-m', '--model', dest = 'model', requireds = True, type = str)
args                    = parser.parse_args()
#path_to_outJson         = args.outJson
model = args.model

if model != '1' and model != '2':
    raise ValueError('inserire un modello che sia o 1 o 2') 
    
histo_TT_true = ROOT.TH1F('TT_true', 'tt true top mixed', 50, 0,1)
histo_TT_false = ROOT.TH1F('TT_false', 'tt false top mixed', 50,0,1)
histo_ZJ = ROOT.TH1F('ZJ', 'zj scores', 50,0,1)

#models = 'TT'
pt_cut = True
#check = True
path_json = []
for n in names: 
    if models == '1':
        file1 = ROOT.TFile(file_folder + n + name_1, 'READ')
    
    else:
        file1 = ROOT.TFile(file_folder + n + name_2, 'READ')

    tree = file1.Get('Events')
    tree = InputTree(tree)

    for i in range(tree.GetEntries()):
        event = Event(tree,i)
        topmixed = Collection(event, 'TopMixed')

        if n == 'TT':
            for top in topmixed:
                if top.truth == 1 and top.Cut ==1 and pt_cut:
                    histo_TT_true.Fill(top.TopScore)
                elif top.truth == 1 and not pt_cut:
                    histo_TT_true.Fill(top.TopScore)
                elif top.truth == 0 and top.Cut==1 and pt_cut: 
                    histo_TT_false.Fill(top.TopScore)
                elif top.truth == 0 and not pt_cut:
                    histo_TT_false.Fill(top.TopScore)
            
        else:
            for top in topmixed:
                if top.Cut == 1 and pt_cut:
                    histo_ZJ.Fill(top.TopScore)
                elif not pt_cut:
                    histo_ZJ.Fill(top.TopScore)


c1 = ROOT.TCanvas()

histo_TT_true.Scale(1.0/histo_TT_true.Integral())
histo_TT_true.SetLineColor(8)

histo_TT_false.SetLineColor(1)
histo_TT_false.Scale(1.0/histo_TT_false.Integral())

histo_ZJ.Scale(1.0/histo_ZJ.Integral())
histo_ZJ.SetLineColor(2)

nbins = histo_ZJ.GetNbinsX()
wk_points=  [0.1, 0.05, 0.01]
wk_values = {}

def working_points_values(histo, nbins, wp):
    trovato = False
    for i in range(1,nbins):
        rej = histo.Integral(i,nbins)
        if rej <= wp and not trovato:
            trovato = True
            out_rej = rej
            out_i = i
    return out_rej, out_i
        
def working_points(histo1,histo2 = None,histo3 = None,wp):
    nbins = histo1.GetNbinsX()
    found = False 
    for i in range(1,nbins):
        rej = histo1.Integral(i,nbins)
        if rej <= wp and not found:
            found = True
            score_cut = histo1.GetBinCenter(i)
            print('Working point: ', wp)
            print('score cut: ', score_cut)
            print(histo1.GetName(), ' value: ', rej)
            if histo2 not None:
                histo2_value = histo2.Integral(i,nbins)
                print(histo2.GetName(), ' value: ', histo2_value)
            if histo3 not None:
                histo3_value = histo3.Integral(i,nbins)
                print(histo3.GetName(), ' value: ', histo3_value)
    if histo2 not None and histo3 not None:
        return score_cut, rej, histo2_value, histo3_value
    elif histo2 not None:
        return score_cut, rej, histo2_value
    elif histo3 not None:
        return score_cut, rej, histo3_value
    else:
        return score_cut, rej
            
          


for wp in wk_points:
    wp_str = str(wp*100) + '%' + ' ZJ'
    wk_values[wp_str] = {}
    score_cut, zj_value, tt_true_value, tt_false_value = working_points(histo_ZJ, histo_TT_true, histo_TT_false, wp)
   
    wk_values[wp_str]['score value'] = score_cut
    wk_values[wp_str]['ZJ value'] = zj_value
    wk_values[wp_str]['True TT value'] = tt_true_value
    wk_values[wp_str]['False tt value'] = tt_false_value
    
    score_cut, tt_false_value, tt_true_value, zj_value = working_points(histo_TT_false, histo_TT_true, histo_ZJ, wp)
    wp_str = str(wp*100) + '%' + ' TT false'
    wk_values[wp_str] = {}
    
    wk_values[wp_str]['score value'] = score_cut
    wk_values[wp_str]['False tt value'] = tt_false_value
    wk_values[wp_str]['True TT value'] = tt_true_value
    wk_values[wp_str]['ZJ value'] = zj_value
    
    
    
    
check  =False             
if check: 
    check_point = 0.075
    check_point_str = str(check_point*100) + '%' + ' TT false' 
    to_do  =True
    wk_values[check_point_str]  = {}
    for i in range(1,nbins):
        rf = histo_TT_false.Integral(i,nbins)
        #print('rf is', rf)
        if rf <= check_point and to_do:
            print('ok sono entrato')
            zj_value = histo_ZJ.Integral(i,nbins)
            tt_true_value = histo_TT_true.Integral(i,nbins)
            score_cut = histo_TT_false.GetBinCenter(i)
            wk_values[check_point_str]['score value'] = score_cut
            wk_values[check_point_str]['ZJ value'] = zj_value
            wk_values[check_point_str]['True TT value'] = tt_true_value
            wk_values[check_point_str]['False TT value'] = rf
            to_do  = False
           
        
folder = '/eos/user/a/apuglia/SWAN_projects/thesis/CMSSW_14_1_7/src/trainings/'
if pt_cut and models == '1' :
    title = {'titolo file': 'TT fondo + TT segnale  + pt cut'} 
    path_to_outJson = folder + 'wpvalues_PtCut_model1'
    c1.SetTitle('Scores model 1 Cut Pt TT')
    c1.Draw()
    c1.SaveAs('Scores_CutPt_model1.png')
elif pt_cut and models == '2': 
    title = {'titolo file': 'ZJ fondo + TT segnale + pt cut'}
    path_to_outJson = folder + 'wpvalues_PtCut_model2'
    c1.SetTitle('Scores model 2 Cut Pt TT vs ZJ')
    c1.Draw()
    c1.SaveAs('Scores_CutPt_model2.png')
elif models == '1' and not pt_cut: 
    title = {'titolo file': 'TT fondo + TT segnale '} 
    path_to_outJson = folder + 'wpvalues_model1'
    c1.SetTitle('Scores model 1 TT')
    c1.Draw()
    c1.SaveAs('Scores_model1.png')
elif models == '2' and not pt_cut:
    title = {'titolo file': 'ZJ fondo + TT segnale'} 
    path_to_outJson = folder + 'wpvalues_model2'
    c1.SetTitle('Scores model 2 TT vs ZJ')
    c1.Draw()
    c1.SaveAs('Scores_model2.png')
    
with open(path_to_outJson, "w") as f:
    json.dump(title, f)  
    json.dump(wk_values, f, indent=4)
            
histo_ZJ.Draw('HIST')
histo_TT_true.Draw('SAME HIST')
histo_TT_false.Draw('SAME HIST')


Leg = ROOT.TLegend(0.7,0.7,0.5,0.9)
Leg.SetHeader("Legend","C")
Leg.AddEntry(histo_TT_true, "true top")
Leg.AddEntry(histo_TT_false, 'false top')
Leg.AddEntry(histo_ZJ, 'zj top scores')
Leg.Draw()







#Model 1 = TT vs ZJ no TT bkg
#Model 2 = TT con Bkg
    