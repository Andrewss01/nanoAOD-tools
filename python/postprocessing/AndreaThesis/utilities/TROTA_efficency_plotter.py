#!/usr/bin/env python
import os
import sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
import matplotlib.pyplot as plt
import mplhep as hep
import cmsstyle as CMS
from ROOT import TEfficiency
hep.style.use("CMS")

def plotEfficiency(h_den, h_eff_merged, h_eff_mixed, h_eff_resolved, g_mer, g_mix, g_res, canv_name = "canv" ,extraTest="Work in progress", iPos=0, energy="13.6", lumi = "",  addInfo="", ytitle = "", samplelabel = "t#bar{t}", ymax=0):
    CMS.SetExtraText(extraTest)
    iPos = iPos
    canv_name = canv_name
    CMS.SetLumi(lumi)
    CMS.SetEnergy(energy)
    CMS.ResetAdditionalInfo()
    CMS.AppendAdditionalInfo(addInfo)
    CMS.setCMSStyle()
    x_min = h_den.GetXaxis().GetXmin()
    x_max = h_den.GetXaxis().GetXmax()
    y_min = 0.
    if ymax!=0: y_max = ymax
    else: y_max = 1.5#max([eff.GetEfficiency(i) for i in range(eff.GetTotalHistogram().GetNbinsX())]) +0.2
    x_axis_name = h_den.GetXaxis().GetTitle()
    ytitle = h_den.GetYaxis().GetTitle()
    canv = CMS.cmsCanvas(canv_name,x_min,x_max, y_min ,y_max,x_axis_name,ytitle,square=CMS.kRectangular, extraSpace=20.0, iPos=iPos)
    hdf = CMS.GetcmsCanvasHist(canv)
    hdf.GetYaxis().SetMaxDigits(1)
    hdf.GetYaxis().SetLabelOffset(0.001)
    hdf.GetYaxis().SetLabelSize(0.045)
    hdf.GetYaxis().SetTitleOffset(1.1)
    hdf.GetYaxis().SetTitleSize(0.045)
    hdf.GetXaxis().SetLabelOffset(0.001)
    hdf.GetXaxis().SetLabelSize(0.045)
    hdf.GetXaxis().SetTitleOffset(1.1)
    hdf.GetXaxis().SetTitleSize(0.045)
    hdf.SetTitle(h_den.GetTitle())
    #g_mer.SetMarkerSize(0)  # oppure graph.SetMarkerStyle(0)
    g_mer.SetLineColor(2) 
    h_eff_merged.SetMarkerColor(2)
    h_eff_merged.SetLineColor(2)
    h_eff_merged.SetMarkerStyle(8)
      
    h_eff_mixed.SetMarkerColor(ROOT.kOrange-2)
    h_eff_mixed.SetLineColor(ROOT.kOrange-2)
    h_eff_mixed.SetMarkerStyle(8)
    #g_mix.SetMarkerSize(0)  
    g_mix.SetLineColor(ROOT.kOrange-2)
    h_eff_resolved.SetMarkerColor(7)
    h_eff_resolved.SetLineColor(7)
    h_eff_resolved.SetMarkerStyle(8)
    #g_res.SetMarkerSize(0)
    g_res.SetLineColor(7)
    h_eff_merged.SetTitle(h_den.GetTitle())
    h_eff_mixed.SetTitle(h_den.GetTitle())
    h_eff_resolved.SetTitle(h_den.GetTitle())
    #print("titolo", h_den.GetTitle())
    #print("titolo_res", h_eff_resolved.GetTitle())
    g_mer.Draw("same Z")
    h_eff_merged.Draw("same P")
    g_mix.Draw("same Z") 
    h_eff_mixed.Draw("same P")
    g_res.Draw("same Z")
    h_eff_resolved.Draw("same P")


    title = h_den.GetTitle()
    if title != "":
        title_text = ROOT.TLatex()
        title_text.SetNDC()
        title_text.SetTextFont(42)
        title_text.SetTextSize(0.03)
        title_text.DrawLatex(0.35, 0.88, title)
    # canv.SetLogy()
    # Shift multiplier position
    ROOT.TGaxis.SetExponentOffset(-0.10, 0.01, "Y")
    # leg = CMS.cmsLeg(0.5, 0.1, 0.98, 0.5, textSize=0.04)
    return canv




def efficiency_calculator(h_num, h_den, h_eff):
    if not TEfficiency.CheckConsistency(h_num, h_den):
        raise ValueError("Inconsistent histograms: numerator and denominator must be compatible.")

    efficiency = TEfficiency(h_num, h_den)
    efficiency.SetStatisticOption(TEfficiency.kFCP)  # Use Clopper-Pearson for error calculation
    efficiency.SetConfidenceLevel(0.683)  # Set confidence level for error calculation 

    for i in range(0, h_eff.GetNbinsX() + 2):
        num = h_num.GetBinContent(i)
        den = h_den.GetBinContent(i)
        eff = efficiency.GetEfficiency(i)
        err_up = efficiency.GetEfficiencyErrorUp(i)
        err_low = efficiency.GetEfficiencyErrorLow(i)
        # if eff!= 1 and den != 0:
        #     #print("num",num)
        #     #print("den",den)
        #     #print("eff",eff)
        #     error = ((eff * (1-eff))/den) ** 0.5
        #     h_eff.SetBinError(i, error)
        # elif eff== 1:
        #     h_eff.SetBinError(i, err_low) 
        #     #h_eff.SetBinError(i, eff.GetEfficiencyErrorUp(i))
        # elif den == 0:
        #    #h_eff.SetBinError(i, 0)
        #    h_eff.SetBinError(i, err_up)
        h_eff.SetBinContent(i, eff)
    return h_eff

def make_efficiency_graph(h_num, h_den, h_eff, key):
    n_bins = h_eff.GetNbinsX()
    g = ROOT.TGraphAsymmErrors(n_bins)
    efficiency = TEfficiency(h_num, h_den)
    efficiency.SetStatisticOption(TEfficiency.kFCP)  # Use Clopper-Pearson for error calculation
    efficiency.SetConfidenceLevel(0.683) 
    efficiency_1 = TEfficiency(h_num, h_den)
    efficiency_1.SetStatisticOption(TEfficiency.kFCP)  # Use Clopper-Pearson for error calculation
    efficiency_1.SetConfidenceLevel(0.841)
    point = 0
    mean_200 , mean_400, mean_600, mean_800 = 0,0,0,0
    num_200 , num_400, num_600, num_800 = 0,0,0,0
    for i in range(1, n_bins + 1): #no over e under flow  
        num = h_num.GetBinContent(i)
        den = h_den.GetBinContent(i)
        eff = efficiency.GetEfficiency(i)

        
        err_up = efficiency_1.GetEfficiencyErrorUp(i)
        err_low = efficiency_1.GetEfficiencyErrorLow(i)

        err_up_1 = efficiency.GetEfficiencyErrorUp(i)
        err_low_1 = efficiency.GetEfficiencyErrorLow(i)


        x = h_eff.GetBinCenter(i)
        ex = h_eff.GetBinWidth(i) / 2.0

        if x <= 200:
            mean_200 += eff
            num_200 +=1
        elif x>= 200 and x<= 400:
            mean_400 += eff
            num_400 +=1
        elif x>= 400 and x<= 600: 
            mean_600 += eff
            num_600 +=1
        elif x >= 600:
            mean_800 += eff
            num_800 +=1
        # if 'Reconstructable' in key:
        #     print('x is: ', x, 'eff is: ', eff)
        g.SetPoint(point, x, eff)
        if eff == 1:
            g.SetPointError(point, ex, ex, err_low_1, 0)
        elif eff == 0:
            g.SetPointError(point, ex, ex, 0, 0)
        else:
            g.SetPointError(point, ex, ex, err_low, err_up)
        point += 1
    print('mean 200: ', mean_200/num_200)
    print('mean 400: ', mean_400/num_400)
    print('mean 600: ', mean_600/num_600)
    print('mean 800: ', mean_800/num_800)
    

    return g

year = 2022
score_type = 'FT'
if year == 2018:
    dirpath = "/eos/user/f/fsalerno/Evaluation/TROTA_2018_studies/Histo_files"
    path_to_graphic_folder = "/eos/user/f/fsalerno/Evaluation/TROTA_2018_studies/RecoEff_TROTA_plots_only_CP"
elif year == 2022:
    dirpath = "/eos/user/a/apuglia/Master_Thesis/TROTA_performances/" +score_type+"Score/Histo_files"
    path_to_graphic_folder = "/eos/user/a/apuglia/Master_Thesis/TROTA_performances/"+ score_type+"Score/RecoEff_TROTA_plots_only_CP"
if not os.path.exists(path_to_graphic_folder):  
    os.makedirs(path_to_graphic_folder)
file_name="output_TROTA_efficiency_Study_ttsemilep_noResInMix.root"
inFile = f"{dirpath}/{file_name}"
histos_file = ROOT.TFile.Open(inFile)

h_den = histos_file.Get("h_gentop_pt")
#print(f"denominator: {h_den.Integral()}")
#print(f"denominator_2: {h_den.GetEntries()}")
eff_types = ["Reconstructable","Selection","RealLife","TagMediumWP", 'TagTightWP']
top_types = ["Resolved","Mixed","Merged"]
match_types = ["QuarkMatch","GenTopMatch02","GenTopMatch04"]

keys=[]
plot_types = []
for eff_type in eff_types:
   for match_type in match_types:
        plot_types.append(f"{eff_type}_{match_type}")
        for top_type in top_types:
            key = f"{eff_type}_{match_type}_{top_type}"
            keys.append(key)
    # print(h_reco_num_mixed)
keys.append("RealLife_OldMatch_Resolved")
keys.append("RealLife_OldMatch_Mixed")
keys.append("RealLife_OldMatch_Merged")
plot_types.append("RealLife_OldMatch")

h_Top_pt = {}

for key in keys:
    h_Top_pt[key] = histos_file.Get(f"h_Top_pt_{key}")


keys_2=[]
for k in ["ExistsMatched","BestMatched","NotMatched"]:
    for match_type in match_types:
        for top_type in top_types:
            keys_2.append(f"{k}_{match_type}_{top_type}")

h2_num_cands = {} 

for key in keys_2:
    h2_num_cands[key] = histos_file.Get(f"h2_Num_cand_GenTop_pt_{key}")
    print(f"h2_Num_cand_GenTop_pt_ExistsMatched_{key}")
histos_file.ls()
ROOT.gStyle.SetOptStat(0)
for key in keys_2:
    h2 = h2_num_cands[key].Clone()
    canvas = ROOT.TCanvas("canvas", "Canvas", 800, 600)

    h2_name = h2.GetName()
    h2.SetTitle(f"{h2.GetName()}_{year}"";p_{T}^{gen}[GeV];Candidates[#]")  # Personalizza assi se necessario
    h2.GetZaxis().SetTitle("Events [#]")

    h2.Draw("COLZ text")
    canvas.SetLogz(False)  # Imposta True se vuoi scala log sulla Z

    canvas.SaveAs(f"{path_to_graphic_folder}/{h2.GetName()}.png")  # Salva il plot


h2_deltaR = histos_file.Get(f"h2_DeltaR_BestTop_GenTop_pt_Resolved")

ROOT.gStyle.SetOptStat(0)

h2 = h2_deltaR.Clone()
canvas = ROOT.TCanvas("canvas", "Canvas", 800, 600)

h2_name = h2.GetName()
h2.SetTitle(f"{h2.GetName()}_{year}"";p_{T}^{gen}[GeV];Candidates[#]")  # Personalizza assi se necessario
h2.GetZaxis().SetTitle("Events [#]")

h2.Draw("COLZ text")
canvas.SetLogz(False)  # Imposta True se vuoi scala log sulla Z

canvas.SaveAs(f"{path_to_graphic_folder}/{h2.GetName()}.png")  # Salva il plot

h_reco_eff = {}
g_reco_eff = {}
for key in keys:
    h_reco_eff[key] = h_Top_pt[key].Clone()
    #h_reco_eff_mixed[key].Divide(h_den)
    if not "Selection" in key:
        print('key is: ', key)
        h_reco_eff[key] = efficiency_calculator(h_Top_pt[key], h_den, h_reco_eff[key])
        g_reco_eff[key] = make_efficiency_graph(h_Top_pt[key], h_den, h_reco_eff[key], key)
    else:
        print('key is: ', key)
        den_key = key.replace("Selection", "Reconstructable")
        h_den_selection = h_Top_pt[den_key].Clone()
        #print(f"key: {key}")
        #print(f"den_key: {den_key}")
        #print(f"num: {h_Top_pt[key].Integral()}")
        #print(f"den: {h_den_selection.Integral()}")
        #print(f"num: {h_Top_pt[key].Integral()}")
        h_reco_eff[key] = efficiency_calculator(h_Top_pt[key], h_den_selection, h_reco_eff[key])
        g_reco_eff[key] = make_efficiency_graph(h_Top_pt[key], h_den_selection, h_reco_eff[key], key)



outFile = ROOT.TFile(f"{path_to_graphic_folder}/RecoEff.root", "RECREATE")    
for key in keys:
    h_reco_eff[key].Write()

outFile.Close()

c_reco={}
for plot_type in plot_types:
    print("plot_type", plot_type)
    h_den.SetTitle(f"{plot_type}_{year}")
    h_den.GetXaxis().SetTitle("p_{T}^{gen} [GeV]")
    h_den.GetYaxis().SetTitle("Efficiency")
    key_resolved = f"{plot_type}_Resolved"
    key_mixed = f"{plot_type}_Mixed"
    key_merged = f"{plot_type}_Merged"
    if "Selection" not in plot_type:
        c_reco[plot_type]=plotEfficiency(h_den=h_den, h_eff_merged=h_reco_eff[key_merged], h_eff_mixed=h_reco_eff[key_mixed], h_eff_resolved=h_reco_eff[key_resolved], g_mer=g_reco_eff[key_merged], g_mix=g_reco_eff[key_mixed], g_res=g_reco_eff[key_resolved], canv_name=f"c_reco_efficiency_{plot_type}") 
    else:
        den_key = key.replace("Selection", "Reconstructable")
        h_den_selection = h_Top_pt[den_key].Clone()
        h_den_selection.SetTitle(f"{plot_type}")
        h_den_selection.GetXaxis().SetTitle("p_{T}^{gen} [GeV]")
        h_den_selection.GetYaxis().SetTitle("Efficiency")
        c_reco[plot_type]=plotEfficiency(h_den=h_den_selection, h_eff_merged=h_reco_eff[key_merged], h_eff_mixed=h_reco_eff[key_mixed], h_eff_resolved=h_reco_eff[key_resolved], g_mer=g_reco_eff[key_merged], g_mix=g_reco_eff[key_mixed], g_res=g_reco_eff[key_resolved], canv_name=f"c_reco_efficiency_{plot_type}")
        

    legend = ROOT.TLegend(0.1, 0.7, 0.3, 0.9)  # Posizione (x1, y1, x2, y2)
    legend.SetBorderSize(1)  
    legend.SetFillColor(0)  
    legend.SetTextSize(0.04) 
    # Aggiunta delle voci alla legenda
    legend.AddEntry(h_reco_eff[key_merged], "merged", "l")
    legend.AddEntry(h_reco_eff[key_mixed], "mixed", "l")
    legend.AddEntry(h_reco_eff[key_resolved], "resolved", "l")
    legend.Draw()
    c_reco[plot_type].SaveAs(f"{path_to_graphic_folder}/RecoEff_{plot_type}.png")



ROOT.gStyle.SetOptTitle(0)

for plot_type in plot_types:
    key_resolved_num = f"{plot_type}_Resolved"
    key_mixed_num = f"{plot_type}_Mixed"
    key_merged_num = f"{plot_type}_Merged"
    if "Selection" in plot_type:
        c_num = ROOT.TCanvas(f"c_num", f"Number of events with the best top candidate matched", 800, 600)
        c_num.SetLogy()
        h_merged_num = h_Top_pt[key_merged_num].Clone()
        h_mixed_num = h_Top_pt[key_mixed_num].Clone()
        h_resolved_num = h_Top_pt[key_resolved_num].Clone()

        h_resolved_num.GetXaxis().SetTitle("p_{T}^{gen} [GeV]")
        h_resolved_num.GetYaxis().SetTitle("Events [#]") 
        h_merged_num.SetLineColor(2)
        h_mixed_num.SetLineColor(ROOT.kOrange-2)
        h_resolved_num.SetLineColor(7)

        h_merged_num.SetTitle("Number of events with the best top candidate matched")
        h_mixed_num.SetTitle("Number of events with the best top candidate matched")
        h_resolved_num.SetTitle("Number of events with the best top candidate matched")
        #print("titolo", h_den.GetTitle())
        #print("titolo_res", h_resolved_num.GetTitle())

        #print("titolo", h_den.GetTitle())
        #print("titolo_res", h_resolved_num.GetTitle())
        h_resolved_num.SetMinimum(0.1)
        h_resolved_num.SetMaximum(1e5)
        h_resolved_num.Draw()
        h_mixed_num.Draw("same")
        h_merged_num.Draw("same")
        legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)  # Posizione (x1, y1, x2, y2)
        legend.SetBorderSize(1)  
        legend.SetFillColor(0)  
        legend.SetTextSize(0.04) 
        # Aggiunta delle voci alla legenda
        legend.AddEntry(h_merged_num, "merged", "l")
        legend.AddEntry(h_mixed_num, "mixed", "l")
        legend.AddEntry(h_resolved_num, "resolved", "l")
        legend.Draw()
        c_num.SaveAs(f"{path_to_graphic_folder}/Event_best_top_match_{plot_type}.png")

#
for plot_type in plot_types:
    key_resolved_den = f"{plot_type}_Resolved"
    key_mixed_den = f"{plot_type}_Mixed"
    key_merged_den = f"{plot_type}_Merged"
    if "Reconstructable" in plot_type:
        c_den = ROOT.TCanvas(f"c_den", f"Number of events with at least top candidate matched", 800, 600)
        c_den.SetLogy()
        h_merged_den = h_Top_pt[key_merged_den].Clone()
        h_mixed_den = h_Top_pt[key_mixed_den].Clone()
        h_resolved_den = h_Top_pt[key_resolved_den].Clone()

        h_resolved_den.GetXaxis().SetTitle("p_{T}^{gen} [GeV]")
        h_resolved_den.GetYaxis().SetTitle("Events [#]") 
        h_merged_den.SetLineColor(2)
        h_mixed_den.SetLineColor(ROOT.kOrange-2)
        h_resolved_den.SetLineColor(7)

        h_merged_den.SetTitle("Number of events with at least top candidate matched")
        h_mixed_den.SetTitle("Number of events with at least top candidate matched")
        h_resolved_den.SetTitle("Number of events with at least top candidate matched")
        #print("titolo", h_den.GetTitle())
        print("titolo_res", h_resolved_den.GetTitle())
        h_resolved_den.SetMinimum(0.1)
        h_resolved_den.SetMaximum(1e5)
        h_resolved_den.Draw("hist")
        h_mixed_den.Draw("same")
        h_merged_den.Draw("same")
        legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)  # Posizione (x1, y1, x2, y2)
        legend.SetBorderSize(1)  
        legend.SetFillColor(0)  
        legend.SetTextSize(0.04) 
        # Aggiunta delle voci alla legenda
        legend.AddEntry(h_merged_den, "merged", "l")
        legend.AddEntry(h_mixed_den, "mixed", "l")
        legend.AddEntry(h_resolved_den, "resolved", "l")
        legend.Draw()
        c_den.SaveAs(f"{path_to_graphic_folder}/Event_one_top_match_{plot_type}.png")
