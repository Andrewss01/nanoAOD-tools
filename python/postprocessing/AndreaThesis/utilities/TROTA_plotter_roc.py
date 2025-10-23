import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.tools import *
import numpy as np
from array import array
from sklearn.metrics import  roc_curve
import os
from tqdm import tqdm
import matplotlib.pyplot as plt
import mplhep as hep
import cmsstyle as CMS
hep.style.use("CMS")


def plotEfficiency( g_mer, g_mix, g_res, canv_name = "canv" ,extraTest="", iPos=0, energy="13.6", lumi = "",  addInfo="  p_{T}^{top} < 200 GeV", ytitle = "", samplelabel = "t#bar{t}", ymax=0):
    CMS.SetExtraText(extraTest)
    iPos = iPos
    canv_name = canv_name
    CMS.SetLumi(lumi)
    CMS.SetEnergy(energy)
    # CMS.ResetAdditionalInfo()
    # CMS.AppendAdditionalInfo(addInfo)
    # CMS.SetADD
    CMS.setCMSStyle()

    # max_mer = g_mer.GetMaximum()
    # max_res = g_res.GetMaximum()
    # max_mix = g_mix.GetMaximum()

    # y_max = max(max_mer, max_mix, max_res) * 1.2
    if key == '200': y_max = 0.4
    elif key == '200to400': y_max = 0.65
    elif key == '400to600' or key == '600': y_max = 1
    # x_min = g_mix.GetXaxis().GetXmin()
    x_min = 10**(-2)
    x_max = g_mix.GetXaxis().GetXmax()

    y_min = 0.
    # if ymax!=0: y_max = ymax
    # else: y_max = 1.2#max([eff.GetEfficiency(i) for i in range(eff.GetTotalHistogram().GetNbinsX())]) +0.2

    x_axis_name = 'Background efficiency'
    ytitle = 'Signal efficiency'
    canv = CMS.cmsCanvas(canv_name,x_min,x_max, y_min ,y_max,x_axis_name,ytitle,square=CMS.kRectangular,extraSpace= 0.01, iPos=iPos)
    hdf = CMS.GetcmsCanvasHist(canv)
    hdf.GetYaxis().SetMaxDigits(3)
    hdf.GetYaxis().SetLabelOffset(0.001)
    hdf.GetYaxis().SetLabelSize(0.045)
    hdf.GetYaxis().SetTitleOffset(1.1)
    hdf.GetYaxis().SetTitleSize(0.045)
    hdf.GetXaxis().SetLabelOffset(0.001)
    hdf.GetXaxis().SetLabelSize(0.045)
    hdf.GetXaxis().SetTitleOffset(1.1)
    hdf.GetXaxis().SetTitleSize(0.045)
    # hdf.SetTitle(g_mix.GetTitle())
    #g_mer.SetMarkerSize(0)  # oppure graph.SetMarkerStyle(0)
    g_mix.SetLineColor(ROOT.kOrange -2)
    g_mer.SetLineColor(2)
    g_res.SetLineColor(7)
    


    g_mix.SetLineStyle(ROOT.kSolid)
    g_res.SetLineStyle(ROOT.kSolid)
    g_mer.SetLineStyle(ROOT.kSolid)

    g_mix.SetLineWidth(2)
    g_res.SetLineWidth(2)
    g_mer.SetLineWidth(2)
      
    
    g_mer.Draw()
    g_mix.Draw("same") 
    g_res.Draw("same")

    if key == '200': addInfo = 'p_{T}^{top} < 200 GeV'
    elif key == '200to400': addInfo = '200 < p_{T}^{top} < 400 GeV'
    elif key == '400to600': addInfo = '400 < p_{T}^{top} < 600 GeV'
    elif key == '600': addInfo = 'p_{T}^{top} > 600 GeV'
    extra_info = ROOT.TLatex()
    extra_info.SetNDC()
    extra_info.SetTextFont(42)
    extra_info.SetTextSize(0.04)
    extra_info.DrawLatex(0.15, 0.85, addInfo)

    # title = h_den.GetTitle()
    # if title != "":
    #     title_text = ROOT.TLatex()
    #     title_text.SetNDC()
    #     title_text.SetTextFont(42)
    #     title_text.SetTextSize(0.03)
    #     title_text.DrawLatex(0.35, 0.88, title)
    canv.SetLogx()
    # Shift multiplier position
    ROOT.TGaxis.SetExponentOffset(-0.10, 0.01, "Y")
    # leg = CMS.cmsLeg(0.5, 0.1, 0.98, 0.5, textSize=0.04)
    
    # cmsstyle.addToLegend(plotlegend, *[(histos[i], labels[i], 'lpe' if i==0 else 'f') for i in range(len(histos))])
    # cmsstyle.addToLegend(plotlegend, (htotal_prediction, 'Uncertainty', 'f'))
    return canv


key = '600'
name = 'roc_curve_Pt'+ key
file_path = '/afs/cern.ch/user/a/apuglia/CMSSW_14_1_7/src/PhysicsTools/NanoAODTools/python/postprocessing/AndreaThesis/utilities/histos_'+name+'.root'

rec_eff ={'resolved': {'200':0.29 , '200to400':0.45 , '400to600':0.39, '600':0.09}, 
          'mixed'   : {'200':0.04 , '200to400':0.47 , '400to600':0.71, '600':0.64},
          'merged'  : {'200':0.02, '200to400':0.05, '400to600':0.45, '600':0.75 }}


def create_ROC(file_path):
    file = ROOT.TFile.Open(file_path, 'READ')
    sig_resolved = file.Get('scores_sig_resolved')
    sig_merged = file.Get('scores_sig_merged')
    sig_mixed = file.Get('scores_sig_mixed')

    bkg_resolved = file.Get('scores_bkg_resolved')
    bkg_merged = file.Get('scores_bkg_merged')
    bkg_mixed = file.Get('scores_bkg_mixed')

    FPRs_res, TPRs_res = [],[]
    FPRs_mix, TPRs_mix = [],[]
    FPRs_mer, TPRs_mer = [],[]

    for i in range(0, 200):
        tp_res = sig_resolved.Integral(i, 200)
        tp_mix = sig_mixed.Integral(i, 200)
        tp_mer = sig_merged.Integral(i, 200)

        fn_res = 1-tp_res
        fn_mix = 1-tp_mix
        fn_mer = 1-tp_mer

        fp_res = bkg_resolved.Integral(i, 200)
        fp_mix = bkg_mixed.Integral(i, 200)
        fp_mer = bkg_merged.Integral(i, 200)

        tn_res = 1-fp_res
        tn_mix = 1-fp_mix
        tn_mer = 1-fp_mer

        tpr_res = tp_res/(tp_res + fn_res)
        tpr_mix = tp_mix/(tp_mix + fn_mix)
        tpr_mer = tp_mer/(tp_mer + fn_mer)

        fpr_res = fp_res/(fp_res + tn_res)
        fpr_mix = fp_mix/(fp_mix + tn_mix)
        fpr_mer = fp_mer/(fp_mer + tn_mer)

        FPRs_res.append(fpr_res)
        TPRs_res.append(tpr_res)

        FPRs_mix.append(fpr_mix)
        TPRs_mix.append(tpr_mix)

        FPRs_mer.append(fpr_mer)
        TPRs_mer.append(tpr_mer)

    return FPRs_res, TPRs_res, FPRs_mix, TPRs_mix, FPRs_mer, TPRs_mer
        

# 0.00001        

file = ROOT.TFile.Open(file_path, 'READ')
# file.ls()

FPRs_res, TPRs_res, FPRs_mix, TPRs_mix, FPRs_mer, TPRs_mer = create_ROC(file_path = file_path)


FPRs_mer = np.array(FPRs_mer)
TPRs_mer = np.array(TPRs_mer)*rec_eff['merged'][key]

FPRs_mix = np.array(FPRs_mix)
TPRs_mix = np.array(TPRs_mix)*rec_eff['mixed'][key]

FPRs_res = np.array(FPRs_res)
TPRs_res = np.array(TPRs_res) *rec_eff['resolved'][key]

g_mer = ROOT.TGraph(len(FPRs_mer), FPRs_mer, TPRs_mer)
g_mix = ROOT.TGraph(len(FPRs_mix), FPRs_mix, TPRs_mix)
g_res = ROOT.TGraph(len(FPRs_res), FPRs_res, TPRs_res)
g_mix.GetYaxis().SetNoExponent(True)
g_mer.GetYaxis().SetNoExponent(True)
g_res.GetYaxis().SetNoExponent(True)

# g_mix.GetXaxis()
c1 = plotEfficiency(g_mer, g_mix, g_res)
plotlegend = ROOT.TLegend(0.7,0.8,0.95,0.9)  # The legend!
plotlegend.AddEntry(g_mix, 'Top Mixed', 'l')
plotlegend.AddEntry(g_mer, 'Top Merged', 'l')
plotlegend.AddEntry(g_res, 'Top Resolved', 'l')
plotlegend.Draw()
c1.Draw()
c1.SaveAs(name +'_manual_WReco.png')

# g_mer = file.Get('Roc_curve_merged')
# g_mix = file.Get('Roc_curve_mixed')
# g_res = file.Get('Roc_curve_resolved')
# c2 = plotEfficiency(g_mer, g_mix, g_res)
# plotlegend = ROOT.TLegend(0.7,0.8,0.95,0.9)  # The legend!
# plotlegend.AddEntry(g_mix, 'Top Mixed', 'l')
# plotlegend.AddEntry(g_mer, 'Top Merged', 'l')
# plotlegend.AddEntry(g_res, 'Top Resolved', 'l')
# plotlegend.Draw()
# c2.Draw()
# c2.SaveAs(name +'_auto_CNN.png')

