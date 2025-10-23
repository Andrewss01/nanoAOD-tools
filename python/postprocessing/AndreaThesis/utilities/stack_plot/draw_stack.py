#!/usr/local/bin/python
import os
import ROOT
import cmsstyle as CMS
import math
from PhysicsTools.NanoAODTools.postprocessing.AndreaThesis.utilities.dataset import *
sample_dict = {  'TT_dilep_2022':TT_dilep_2022, 'TT_hadronic_2022': TT_hadr_2022, 'TT_semilep_2022': TT_semilep_2022,   'WtoLNu_4Jets_4J_2022':WtoLNu_4Jets_4J_2022, 'WtoLNu_4Jets_3J_2022':WtoLNu_4Jets_3J_2022, 
                'WtoLNu_4Jets_2J_2022':WtoLNu_4Jets_2J_2022, 'WtoLNu_4Jets_2022':WtoLNu_4Jets_2022,'TbarWplus_1L_2022':TbarWplus_1L_2022,'TWminus_1L_2022':TWminus_1L_2022,
                'QCD_HT70to100_2022': QCD_HT70to100_2022, 'QCD_HT100to200_2022': QCD_HT100to200_2022, 'QCD_HT200to400_2022':QCD_HT200to400_2022, 'QCD_HT400to600_2022':QCD_HT400to600_2022, 
                'QCD_HT600to800_2022': QCD_HT600to800_2022, 'QCD_HT800to1000_2022': QCD_HT800to1000_2022,'QCD_HT1000to1200_2022':QCD_HT1000to1200_2022, 'QCD_HT1200to1500_2022':QCD_HT1200to1500_2022,
                'QCD_HT1500to2000_2022':QCD_HT1500to2000_2022,
                'QCD_HT2000_2022':QCD_HT2000_2022}

# 'WtoLNu_HT120to200_2022':WtoLNu_HT120to200_2022, 'WtoLNu_HT200to400_2022':WtoLNu_HT200to400_2022,
#                 'WtoLNu_HT400to800_2022':WtoLNu_HT400to800_2022, 'WtoLNu_HT800to1500_2022':WtoLNu_HT800to1500_2022, 'WtoLNu_HT1500to2500_2022':WtoLNu_HT1500to2500_2022,
#                 'WtoLNu_HT2500to4000_2022':WtoLNu_HT2500to4000_2022, 'WtoLNu_HT4000to6000_2022':WtoLNu_HT4000to6000_2022, 'WtoLNu_HT6000_2022':WtoLNu_HT6000_2022,
mc_to_stack = sample_dict


def draw_stack_ft (file_name, dict_sample,dict_normalization,file_save, type_plot = 'best_single_top',rebin=None, canv_name = "FT Scores" ,extraTest="", iPos=11, energy="13.6", lumi = "",  addInfo="", ytitle = ""):
    CMS.SetExtraText(extraTest)
    iPos = iPos
    canv_name = canv_name
    CMS.SetLumi(lumi)
    
    CMS.SetEnergy(energy)
    CMS.ResetAdditionalInfo()
    CMS.AppendAdditionalInfo(addInfo)
    CMS.setCMSStyle()
    
    tt_leg, wjet_leg,qcd_leg = False, False, False

    hs_ft = ROOT.THStack('hs_ft_scores'  ,'Stack plot FT Scores ')
    
    infile = ROOT.TFile.Open(file_name, 'READ')
    # infile.ls()

    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)  # Posizione (x1, y1, x2, y2)
    # legend.SetBorderSize(1)  
    legend.SetFillColor(0)  
    legend.SetTextSize(0.04) 

    tt_1q, tt_2q, tt_3q = False, False, False
    tt_0q = False
    tw_leg = False
    histo_tt, histo_qcd, histo_wj, histo_1q, histo_2q, histo_3q, histo_0q, histo_tw = None, None, None, None, None, None, None, None
    histo_tt_dilep, tt_dilep_leg = None, None

    for key in dict_sample.keys():
        if (key == 'TT_semilep_2022' or key == 'TT_hadronic_2022' ) and type_plot == 'all_tops':
            histo_ft_1q = infile.Get('ttvsft_scores_1quark_'+ str(key))
            histo_ft_2q = infile.Get('ttvsft_scores_2quark_'+ str(key))
            histo_ft_3q = infile.Get('ttvsft_scores_3quark_'+ str(key))
            histo_ft_0q = infile.Get('ttvsft_scores_0quark_'+ str(key))
            
            sigma = dict_normalization['sigma'][key]
            num_event = dict_normalization['num_events'][key]
            lumi_pb = lumi_pb_0
            # print('key: ', key, ' num events: ', num_event, 'sigma: ', sigma)
            if num_event!= 0:
                histo_ft_1q.Scale((sigma * lumi_pb )/(num_event))
                histo_ft_2q.Scale((sigma * lumi_pb )/(num_event))
                histo_ft_3q.Scale((sigma * lumi_pb )/(num_event))
                histo_ft_0q.Scale((sigma * lumi_pb )/(num_event))
                # histo_qcd.Scale((sigma * lumi)/(num_event))
           
            histo_ft_1q.SetFillColor(ROOT.kCyan -6)
            histo_ft_1q.SetLineColor(ROOT.kCyan -6)
            # histo_ft_1q.SetFillColorAlpha(ROOT.kGreen-6, 0.7)

            histo_ft_2q.SetFillColor(ROOT.kOrange -3)
            histo_ft_2q.SetLineColor(ROOT.kOrange -3)
            # histo_ft_2q.SetFillColorAlpha(ROOT.kOrange -3, 0.7)

            histo_ft_3q.SetFillColor(ROOT.kGreen -6)
            histo_ft_3q.SetLineColor(ROOT.kGreen -6)
            # histo_ft_3q.SetFillColorAlpha(ROOT.kMagenta -6, 0.7)

            histo_ft_0q.SetFillColor(ROOT.kGray)
            histo_ft_0q.SetLineColor(ROOT.kGray)
            # histo_ft_0q.SetFillColorAlpha(ROOT.kCyan-6, 0.7)

            if rebin != None:
                histo_ft_1q.Rebin(rebin)
                histo_ft_2q.Rebin(rebin)
                histo_ft_3q.Rebin(rebin)
                histo_ft_0q.Rebin(rebin)

            if histo_1q is None:
                histo_1q = histo_ft_1q.Clone('histo_1q')
            else: 
                histo_1q.Add(histo_ft_1q)

            if histo_2q is None:
                histo_2q = histo_ft_2q.Clone('histo_2q')
            else: 
                histo_2q.Add(histo_ft_2q)
            
            if histo_3q is None:
                histo_3q = histo_ft_3q.Clone('histo_3q')
            else: 
                histo_3q.Add(histo_ft_3q)
            
            if histo_0q is None:
                histo_0q = histo_ft_0q.Clone('histo_0q')
            else: 
                histo_0q.Add(histo_ft_0q)
            
            # hs_ft.Add(histo_ft_1q)
            # hs_ft.Add(histo_ft_2q)
            # hs_ft.Add(histo_ft_3q)
            # hs_ft.Add(histo_ft_0q)

            if not tt_1q:
                legend.AddEntry(histo_ft_1q, 't#bar{t} 1 quark matched', 'f')
                tt_1q= True
            if not tt_2q:
                legend.AddEntry(histo_ft_2q, 't#bar{t} 2 quark matched', 'f')
                tt_2q= True
            if not tt_3q:
                legend.AddEntry(histo_ft_3q, 't#bar{t} 3 quark matched', 'f')
                tt_3q= True
            if not tt_0q:
                legend.AddEntry(histo_ft_0q, 't#bar{t} 0 quark matched', 'f')
                tt_0q= True


        else:
            histo_ft = infile.Get('ttvsft_scores_'+ str(key))
            # print(key)
            color = dict_sample[key].color
            label = key
            if ('TT_semilep' in label or 'TT_hadr' in label) and not tt_leg :
                legend.AddEntry(histo_ft, 't#bar{t}', 'f')
                tt_leg = True
            elif 'WtoLNu' in label and not wjet_leg:
                legend.AddEntry(histo_ft, 'W+Jets', 'f')
                wjet_leg = True
            elif 'QCD' in label and not qcd_leg:
                legend.AddEntry(histo_ft, 'QCD', 'f')
                qcd_leg = True
            elif ('TWminus' in label or 'TbarW' in label) and not tw_leg:
                legend.AddEntry(histo_ft, 'tW', 'f')
                tw_leg = True
            elif 'TT_dilep' in label and not tt_dilep_leg:
                legend.AddEntry(histo_ft, 't#bar{t} dilep', 'f')
                tt_dilep_leg = True

            sigma = dict_normalization['sigma'][key]
            num_event = dict_normalization['num_events'][key]
            lumi_pb = lumi_pb_0
            print('key: ', key, ' num events: ', num_event, 'sigma: ', sigma)
            # print('key: ', key, 'scale: ', (sigma*lumi_pb)/(num_event))
            
            
            if num_event != 0 :
                # print('before scale', histo_ft.GetBinContent(1))
                histo_ft.Scale((sigma * lumi_pb)/(num_event))
                # print('after scale', histo_ft.GetBinContent(1))
            print('color is: ', color)
            histo_ft.SetFillColor(color)
            histo_ft.SetTitle(label)
            histo_ft.SetLineColor(color)
            # histo_ft.SetFillColorAlpha(color, 0.7)
            if rebin != None:
                histo_ft.Rebin(rebin)

            if ('TT_hadronic' in label or 'TT_semilep' in label):
                if histo_tt is None:
                    histo_tt = histo_ft.Clone('histo_tt')  
                else:
                    histo_tt.Add(histo_ft)
            elif 'QCD' in label:
                if histo_qcd is None:
                    histo_qcd = histo_ft.Clone('histo_qcd')
                else:
                    histo_qcd.Add(histo_ft)
            elif 'WtoLNu' in label:
                if histo_wj is None:
                    histo_wj = histo_ft.Clone('histo_wj')
                else:
                    histo_wj.Add(histo_ft)
            elif ('TWminus' in label or 'TbarW' in label):
                if histo_tw is None:
                    histo_tw = histo_ft.Clone('histo_tw')
                else:
                    histo_tw.Add(histo_ft)
            elif 'TT_dilep' in label:
                if histo_tt_dilep is None:
                    histo_tt_dilep = histo_ft.Clone('histo_tt_dilep')
                else:
                    histo_tt_dilep.Add(histo_ft)

            if 'WtoLNu' in label:
                for i in range(histo_ft.GetNbinsX()):
                    bErr = histo_ft.GetBinError(i)
                    bVal = histo_ft.GetBinContent(i)
                    newErr = math.sqrt(bErr*bErr + 0.3*bVal*0.3*bVal)
                    histo_ft.SetBinError(i,newErr)  
            
            
            
            # hs_ft.Add(histo_ft)
    # hs_ft.Draw('hist')
    # print(hs_ft)
    
    # histo_qcd.Smooth(4)
    if smooth:
        histo_wj.Smooth()
        histo_qcd.Smooth()
        # histo_tw.Smooth()
        # histo_tt_dilep.Smooth()
    hs_ft.Add(histo_wj)
    hs_ft.Add(histo_qcd)
    if histo_tt_dilep != None:
        hs_ft.Add(histo_tt_dilep)
    hs_ft.Add(histo_tw)
    if histo_0q != None:
        hs_ft.Add(histo_0q)
    if histo_1q != None:
        hs_ft.Add(histo_1q)
    if histo_2q != None:
        hs_ft.Add(histo_2q)
    
    if histo_3q != None:
        hs_ft.Add(histo_3q)
    if histo_tt != None:
        hs_ft.Add(histo_tt)

    histo_ft_data = infile.Get('ttvsft_scores')
    histo_ft_data.SetMarkerStyle(20)
    histo_ft_data.SetMarkerColor(ROOT.kBlack)
    if rebin != None:
        histo_ft_data.Rebin(rebin)
    legend.AddEntry(histo_ft_data, 'Data', 'lpe')
    hs_ft.SetTitle('Stack plot')
    # hs_ft.GetXaxis().SetTitle('FT score')
    # hs_ft.GetXaxis().SetTitle('Num events')
    max_stack = hs_ft.GetMaximum()
    max_data = histo_ft_data.GetMaximum()
    y_max= max(max_stack, max_data) * 1.2  # Aggiungi 20% di margine
    x_max = histo_ft_data.GetXaxis().GetXmax()
    # x_max_stack = hs_ft.GetXaxis().GetXmax()

    # x_max = max(x_max_stack, x_max_data)
    x_min = 0
    # x_max = 1
    y_min = 0.
    # y_max = 10**6
    x_axis_name = 'True Top vs False Top Score'
    ytitle = 'Events '

    canv = CMS.cmsCanvas(canv_name,x_min,x_max, y_min ,y_max,x_axis_name,ytitle,square=CMS.kRectangular, extraSpace=20.0, iPos=iPos)
    hdf = CMS.GetcmsCanvasHist(canv)
    hdf.GetYaxis().SetMaxDigits(3)
    # ROOT.GetYaxis.SetLabelFormat("%.1e", "y")
    # ROOT.gStyle.SetLabelFormat("%.1e", "y")
    hdf.GetYaxis().SetNoExponent(False)

    hdf.GetYaxis().SetLabelOffset(0.001)
    hdf.GetYaxis().SetLabelSize(0.045)
    hdf.GetYaxis().SetTitleOffset(1.1)
    hdf.GetYaxis().SetTitleSize(0.045)
    hdf.GetXaxis().SetLabelOffset(0.001)
    hdf.GetXaxis().SetLabelSize(0.045)
    hdf.GetXaxis().SetTitleOffset(1.1)
    hdf.GetXaxis().SetTitleSize(0.045)

    lumi_text = ROOT.TLatex()
    lumi_text.SetNDC()
    lumi_text.SetTextAlign(31)  # Allineamento a destra
    lumi_text.SetTextSize(0.05)
    lumi_text.SetTextFont(42)
    lumi_text.DrawLatex(0.87, 0.94, "5.7 fb^{-1}")
    # # prepare a legend and fill it
    # plotlegend = cmsstyle.cmsLeg(0.42,0.55,0.92,0.9, textSize=0.04, columns=2)  # The legend!
    # cmsstyle.addToLegend(plotlegend, *[(histos[i], labels[i], 'lpe' if i==0 else 'f') for i in range(len(histos))])
    # cmsstyle.addToLegend(plotlegend, (htotal_prediction, 'Uncertainty', 'f'))
    # # draw the stack
    CMS.cmsObjectDraw(hs_ft,"SAMEHIST")
    CMS.cmsObjectDraw(histo_ft_data, 'PE')
    
    legend.Draw('same')


    h_total = None
    for hist in hs_ft.GetHists():
        if h_total is None:
            h_total = hist.Clone('total')
        else:
            h_total.Add(hist)

    h_total.SetFillStyle(3345)  # Stile di riempimento per errori   
    h_total.SetFillColor(ROOT.kBlack)
    h_total.SetMarkerSize(0)  # Rimuove i marker
    h_total.Draw("E2 SAME") 

    
    # Aggiunta delle voci alla legenda
   
    save_file = file_save
    file = ROOT.TFile.Open(save_file, 'RECREATE')
    canv.Write()

    # print('num data: ', histo_ft_data.Integral(1,50))
    # print('num wj: ', histo_wj.Integral(1,50))
    # print('num sig: ', histo_tt.Integral(1,50))
    # print('num bkg: ', histo_qcd.Integral(1,50))

    # c.SaveAs(f"{label}.png".replace(" ", "_"))


def draw_stack_qcd (file_name, dict_sample,dict_normalization,file_save,rebin = None, type_plot = 'best_single_top',canv_name = "QCD Scores" ,extraTest="", iPos=11, energy="13.6", lumi = "",  addInfo="", ytitle = ""):
    CMS.SetExtraText(extraTest)
    iPos = iPos
    canv_name = canv_name
    CMS.SetLumi(lumi)
    
    CMS.SetEnergy(energy)
    CMS.ResetAdditionalInfo()
    CMS.AppendAdditionalInfo(addInfo)
    CMS.setCMSStyle()
    
    tt_leg, wjet_leg,qcd_leg = False, False, False

    hs_qcd = ROOT.THStack('hs_qcd_scores'  ,'Stack plot QCD Scores')
    
    infile = ROOT.TFile.Open(file_name, 'READ')
    # infile.ls()

    legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)  # Posizione (x1, y1, x2, y2)
    # legend.SetBorderSize(1)  
    legend.SetFillColor(0)  
    legend.SetTextSize(0.04) 
    tt_1q, tt_2q, tt_3q = False, False, False
    tt_0q = False
    tw_leg = False
    tt_dilep_leg, histo_tt_dilep = None, None
    histo_tt, histo_QCD, histo_wj, histo_1q, histo_2q, histo_3q, histo_0q, histo_tw = None, None, None, None, None, None, None, None

    for key in dict_sample.keys():
        if ( key == 'TT_semilep_2022' or key == 'TT_hadronic_2022' ) and type_plot == 'all_tops':
            histo_qcd_1q = infile.Get('ttvsqcd_scores_1quark_'+ str(key))
            histo_qcd_2q = infile.Get('ttvsqcd_scores_2quark_'+ str(key))
            histo_qcd_3q = infile.Get('ttvsqcd_scores_3quark_'+ str(key))
            histo_qcd_0q = infile.Get('ttvsqcd_scores_0quark_'+ str(key))
            
            sigma = dict_normalization['sigma'][key]
            num_event = dict_normalization['num_events'][key]
            lumi_pb = lumi_pb_0
            # print('key: ', key, ' num events: ', num_event, 'sigma: ', sigma)
            if num_event!= 0:
                histo_qcd_1q.Scale((sigma * lumi_pb)/(num_event))
                histo_qcd_2q.Scale((sigma * lumi_pb)/(num_event))
                histo_qcd_3q.Scale((sigma * lumi_pb)/(num_event))
                histo_qcd_0q.Scale((sigma * lumi_pb)/(num_event))
                # histo_qcd.Scale((sigma * lumi)/(num_event))
           
            histo_qcd_1q.SetFillColor(ROOT.kCyan -6)
            histo_qcd_1q.SetLineColor(ROOT.kCyan -6)
            # histo_qcd_1q.SetFillColorAlpha(ROOT.kGreen-6, 0.7)

            histo_qcd_2q.SetFillColor(ROOT.kOrange-3)
            histo_qcd_2q.SetLineColor(ROOT.kOrange-3)
            # histo_qcd_2q.SetFillColorAlpha(ROOT.kOrange -3, 0.7)

            histo_qcd_3q.SetFillColor(ROOT.kGreen -6)
            histo_qcd_3q.SetLineColor(ROOT.kGreen -6)
            # histo_qcd_3q.SetFillColorAlpha(ROOT.kMagenta -6, 0.7)

            histo_qcd_0q.SetFillColor(ROOT.kGray)
            histo_qcd_0q.SetLineColor(ROOT.kGray)
            # histo_qcd_0q.SetFillColorAlpha(ROOT.kCyan-6, 0.7)

            if rebin != None:
                histo_qcd_1q.Rebin(rebin)
                histo_qcd_2q.Rebin(rebin)
                histo_qcd_3q.Rebin(rebin)
                histo_qcd_0q.Rebin(rebin)

            # hs_qcd.Add(histo_qcd_1q)
            # hs_qcd.Add(histo_qcd_2q)
            # hs_qcd.Add(histo_qcd_3q)
            # hs_qcd.Add(histo_qcd_0q)

            if not tt_1q:
                legend.AddEntry(histo_qcd_1q, 't#bar{t} 1 quark matched', 'f')
                tt_1q= True
            if not tt_2q:
                legend.AddEntry(histo_qcd_2q, 't#bar{t} 2 quark matched', 'f')
                tt_2q= True
            if not tt_3q:
                legend.AddEntry(histo_qcd_3q, 't#bar{t} 3 quark matched', 'f')
                tt_3q= True
            if not tt_0q:
                legend.AddEntry(histo_qcd_0q, 't#bar{t} 0 quark matched', 'f')
                tt_0q= True

            if histo_1q is None:
                histo_1q = histo_qcd_1q.Clone('histo_1q')
            else: 
                histo_1q.Add(histo_qcd_1q)

            if histo_2q is None:
                histo_2q = histo_qcd_2q.Clone('histo_2q')
            else: 
                histo_2q.Add(histo_qcd_2q)
            
            if histo_3q is None:
                histo_3q = histo_qcd_3q.Clone('histo_3q')
            else: 
                histo_3q.Add(histo_qcd_3q)
            
            if histo_0q is None:
                histo_0q = histo_qcd_0q.Clone('histo_0q')
            else: 
                histo_0q.Add(histo_qcd_0q)

        else:
            histo_qcd = infile.Get('ttvsqcd_scores_'+ str(key))
            # print('fff',dict_sample[key].color)
            color = dict_sample[key].color
            label = key
            if ('TT_hadronic' in label or 'TT_semilep' in label) and not tt_leg :
                legend.AddEntry(histo_qcd, 't#bar{t}', 'f')
                tt_leg = True
            elif 'WtoLNu' in label and not wjet_leg:
                legend.AddEntry(histo_qcd, 'W+Jets', 'f')
                wjet_leg = True
            elif 'QCD' in label and not qcd_leg:
                legend.AddEntry(histo_qcd, 'QCD', 'f')
                qcd_leg = True
            elif ('TWminus' in label or 'TbarW' in label) and not tw_leg:
                legend.AddEntry(histo_qcd, 'tW', 'f')
                tw_leg = True
            elif 'TT_dilep' in label and not tt_dilep_leg:
                legend.AddEntry(histo_qcd, 't#bar{t} dilep', 'f')
                tt_dilep_leg = True

            sigma = dict_normalization['sigma'][key]
            num_event = dict_normalization['num_events'][key]
            # print('key: ', key, ' num events: ', num_event, 'sigma: ', sigma)
            lumi_pb = lumi_pb_0


            if num_event != 0 :
                histo_qcd.Scale((sigma * lumi_pb)/(num_event))
                # histo_qcd.Scale((sigma * lumi)/(num_event))
            histo_qcd.SetFillColor(color)
            histo_qcd.SetTitle(label)
            histo_qcd.SetLineColor(color)
            # histo_qcd.SetFillColorAlpha(color, 0.7)
            if rebin != None:
                histo_qcd.Rebin(rebin)
            
            if ('TT_hadronic' in label or 'TT_semilep' in label):
                if histo_tt is None:
                    histo_tt = histo_qcd.Clone('histo_tt')  
                else:
                    histo_tt.Add(histo_qcd)
            elif 'QCD' in label:
                if histo_QCD is None:
                    histo_QCD = histo_qcd.Clone('histo_QCD')
                else:
                    histo_QCD.Add(histo_qcd)
            elif 'WtoLNu' in label:
                if histo_wj is None:
                    histo_wj = histo_qcd.Clone('histo_wj')
                else:
                    histo_wj.Add(histo_qcd)
            elif ('TWminus' in label or 'TbarW' in label):
                if histo_tw is None:
                    histo_tw = histo_qcd.Clone('histo_tw')
                else:
                    histo_tw.Add(histo_qcd)
            elif 'TT_dilep' in label:
                if histo_tt_dilep is None:
                    histo_tt_dilep = histo_qcd.Clone('histo_tt_dilep')
                else:
                    histo_tt_dilep.Add(histo_qcd)
            
            if 'WtoLNu' in label:
                for i in range(histo_qcd.GetNbinsX()):
                    bErr = histo_qcd.GetBinError(i)
                    bVal = histo_qcd.GetBinContent(i)
                    newErr = math.sqrt(bErr*bErr + 0.3*bVal*0.3*bVal)
                    histo_qcd.SetBinError(i,newErr)  
            # hs_qcd.Add(histo_qcd)
    # hs_ft.Draw('hist')
    # print(hs_ft)
    # histo_QCD.Smooth()
    if smooth:
        histo_wj.Smooth()
        histo_QCD.Smooth()
        # histo_tw.Smooth()
        # histo_tt_dilep.Smooth()
    hs_qcd.Add(histo_wj)
    hs_qcd.Add(histo_QCD)
    if histo_tt_dilep != None:
        hs_qcd.Add(histo_tt_dilep)
    hs_qcd.Add(histo_tw)
    
    if histo_0q != None:
        hs_qcd.Add(histo_0q)
    if histo_1q != None:
        hs_qcd.Add(histo_1q)
    if histo_2q != None:
        hs_qcd.Add(histo_2q)
    if histo_3q != None:
        hs_qcd.Add(histo_3q)
    if histo_tt != None:
        print('PROBLEMA')
        hs_qcd.Add(histo_tt)    
    
    histo_qcd_data = infile.Get('ttvsqcd_scores')
    histo_qcd_data.SetMarkerStyle(20)
    histo_qcd_data.SetMarkerColor(ROOT.kBlack)
    if rebin != None:
        histo_qcd_data.Rebin(rebin)
    legend.AddEntry(histo_qcd_data, 'Data', 'lpe')
    hs_qcd.SetTitle('Stack plot')
    # hs_ft.GetXaxis().SetTitle('FT score')
    # hs_ft.GetXaxis().SetTitle('Num events')
    max_stack = hs_qcd.GetMaximum()
    max_data = histo_qcd_data.GetMaximum()
    y_max= max(max_stack, max_data) * 1.2  # Aggiungi 20% di margine
    x_max = histo_qcd_data.GetXaxis().GetXmax()
    # x_max_stack = hs_ft.GetXaxis().GetXmax()

    # x_max = max(x_max_stack, x_max_data)
    x_min = 0
    # x_max = 1
    y_min = 0.
    # y_max = 10**6
    x_axis_name = 'True Top vs QCD Top Score'
    ytitle = 'Events '

    canv = CMS.cmsCanvas(canv_name,x_min,x_max, y_min ,y_max,x_axis_name,ytitle,square=CMS.kRectangular, extraSpace=20.0, iPos=iPos)
    hdf = CMS.GetcmsCanvasHist(canv)
    hdf.GetYaxis().SetMaxDigits(2)
    hdf.GetYaxis().SetLabelOffset(0.001)
    hdf.GetYaxis().SetLabelSize(0.045)
    hdf.GetYaxis().SetTitleOffset(1.1)
    hdf.GetYaxis().SetTitleSize(0.045)
    hdf.GetXaxis().SetLabelOffset(0.001)
    hdf.GetXaxis().SetLabelSize(0.045)
    hdf.GetXaxis().SetTitleOffset(1.1)
    hdf.GetXaxis().SetTitleSize(0.045)

    lumi_text = ROOT.TLatex()
    lumi_text.SetNDC()
    lumi_text.SetTextAlign(31)  # Allineamento a destra
    lumi_text.SetTextSize(0.05)
    lumi_text.SetTextFont(42)
    lumi_text.DrawLatex(0.87, 0.94, "5.7 fb^{-1}")
 
    CMS.cmsObjectDraw(hs_qcd,"SAMEHIST")
    CMS.cmsObjectDraw(histo_qcd_data, 'PE')
    
    legend.Draw('same')

    h_total = None
    for hist in hs_qcd:
        if h_total is None: 
            h_total = hist.Clone('total')
        else:
            h_total.Add(hist)
    h_total.SetFillStyle(3345)  # Stile di riempimento per errori   
    h_total.SetFillColor(ROOT.kBlack)
    h_total.SetMarkerSize(0)  # Rimuove i marker
    h_total.Draw("E2 SAME")  # E
   
    save_file = file_save
    file = ROOT.TFile.Open(save_file, 'UPDATE')
    canv.Write()

type_plot = 'all_tops'
pt_cut  = False
model = 'lstm'
smooth = False
lumi_pb_0 = 5670
if pt_cut:
    file_path = '/eos/user/a/apuglia/Master_Thesis/Graphics/Stack_plot/histos_'+type_plot+ '_' +model +'_ptcut.root'
    file_save = '/eos/user/a/apuglia/Master_Thesis/Graphics/' + model+ '/stack_plot_' + type_plot + '_ptcut.root'
else:
    file_path = '/eos/user/a/apuglia/Master_Thesis/Graphics/Stack_plot/histos_'+type_plot+ '_' + model+ '.root'
    file_save = '/eos/user/a/apuglia/Master_Thesis/Graphics/' +model+ '/stack_plot_' + type_plot + '.root'


file_dict= '/eos/user/a/apuglia/Master_Thesis/Graphics/Stack_plot/dict_normalization.json'
with open(file_dict, "r", encoding="utf-8") as f:
    dict_normalization = json.load(f)
draw_stack_ft(file_path, mc_to_stack, dict_normalization, file_save,rebin = 4,canv_name = 'FT Scores '+ type_plot, type_plot = type_plot)
draw_stack_qcd(file_path, mc_to_stack, dict_normalization, file_save, rebin = 4, canv_name = 'QCD Scores '+type_plot, type_plot = type_plot)