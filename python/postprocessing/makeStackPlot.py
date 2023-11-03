import ROOT
import os
from samples.samples import *
from CMS_lumi import CMS_lumi
from variables import *
import copy
#import math
#import pickle as pkl
#import numpy as np
#from datetime import datetime
ROOT.gROOT.SetBatch()

################## input parameters

cut = requirements  ### defined in variables.py 
lumi = 28.0 #59.7  #fb #RUN3 eraF
run2 = True
run3 = not run2
in_datasets = [
    DataHT_2018, 
    QCD_2018, TT_2018, ZJetsToNuNu_2018, WJets_2018, 
    TprimeToTZ_700_2018, TprimeToTZ_1000_2018, TprimeToTZ_1800_2018,
               ]
#[QCD_2022, TT_2022, DataHTF_2022,ZJetsToNuNu_2018, WJets_2018]#[QCD_2018, TT_2018, ZJetsToNuNu_2018, WJets_2018, DataHT_2022]#
#in_datasets = [TT_2018, DataHTF_2022]
blind = False#True#

print("Paremeters setted") 
print("cut = ",cut)      
print("lumi (fb) = ",str(lumi))
print("input datasets = ", [d.label for d in in_datasets])
print("blind: ", blind)

################# variables definition --> defined in variables.py 
# vars = []

# vars.append(variable(name = "MET_pt", title= "MET p_{T} [GeV]", taglio = cut, nbins = 20, xmin = 0, xmax=1000))
# vars.append(variable(name = "MET_phi", title= "MET #phi", taglio = cut, nbins = 6, xmin = -math.pi, xmax=math.pi))
# vars.append(variable(name = "LeadingJet_pt", title= "Leading Jet p_{T} [GeV]", taglio = cut, nbins = 30, xmin = 50, xmax=950))
# vars.append(variable(name = "nTopHighPt", title= "# Top Candidate Mix", taglio = cut, nbins = 80, xmin = -0.5, xmax=80.5))
# vars.append(variable(name = "nTopLowPt", title= "# Top Candidate Resolved", taglio = cut, nbins = 50, xmin = -0.5, xmax=50.5))
# vars.append(variable(name = "nJet", title= "# Jet", taglio = cut, nbins = 25, xmin = -0.5, xmax=25.5))
# vars.append(variable(name = "nFatJet", title= "# FatJet", taglio = cut, nbins = 25, xmin = -0.5, xmax=25.5))
# vars.append(variable(name = "MinDelta_phi", title= "min #Delta #phi", taglio = cut, nbins = 20, xmin = 0, xmax = 4))
# vars.append(variable(name = "MaxEta_jet", title= "max #eta jet", taglio = cut, nbins = 24, xmin = 0, xmax = 6))

# vars = [variable(name = "MET_pt", title= "MET p_{T} [GeV]", taglio = cut, nbins = 20, xmin = 0, xmax=1000)]
print("Producing the follow histos: ", [v._name for v in vars])

################ regions definition --> defined in variables.py  
# regions = {
#     "all_regions" : "" 
#     # "resolved_1fwjet": "EventTopCategory==3 && nForwardJet>0", 
#     # "mixed_1fwjet": "EventTopCategory==2 && nForwardJet>0", 
#     # "merged_1fwjet": "EventTopCategory==1 && nForwardJet>0",
#     # "resolved_0fwjet": "EventTopCategory==3 && nForwardJet==0", 
#     # "mixed_0fwjet": "EventTopCategory==2 && nForwardJet==0", 
#     # "merged_0fwjet" : "EventTopCategory==1 && nForwardJet==0",
#     # "noTopRegion" : "EventTopCategory==0"
# }

# regions = {"all_regions" : ""}

print("Regions considered :", regions.keys())

############### out folders
folder = "/eos/home-a/acagnott/DarkMatter/nosynch/run2018_benchmark_v3/"
if not os.path.exists(folder):
    os.mkdir(folder)
repohisto = folder+"plots/"
if not os.path.exists(repohisto):
    os.mkdir(repohisto)
repostack = folder+"stacks/"
if not os.path.exists(repostack):
    os.mkdir(repostack)

print("Created folders 'plots' and 'stacks' at ", folder)

################### utils ###################
def cut_string(cut):
    return cut.replace(" ", "").replace("&&","_").replace(">","_g_").replace(".","_").replace("==","_e_").replace("<", "_l_")


################## main code 
infile = {'Data': [], 'signal': [], 'bkg': []}
insample = {'Data': [], 'signal': [], 'bkg': []}
h_bkg = []
h_sign = []
h_err = []
h_bkg_err = []

cut_tag = cut_string(cut)

for d in in_datasets:
    print(repohisto + d.label + ".root")
    if 'Data' in d.label:
        infile['Data'].append(ROOT.TFile.Open(repohisto + d.label + ".root"))
        insample['Data'].append(d)         
    elif 'tDM' in d.label or 'Tp' in d.label:
        infile['signal'].append(ROOT.TFile.Open(repohisto + d.label + ".root"))
        insample['signal'].append(d)
    else:
        infile['bkg'].append(ROOT.TFile.Open(repohisto + d.label + ".root"))
        insample['bkg'].append(d)
# print("Opened histos files")
# print(infile)

for v in vars:
    for r in regions.keys():
        h_sign = []
        print("Creating ..")
        print(v._name, r)
        ROOT.gROOT.SetStyle('Plain')
        #ROOT.gStyle.SetPalette(1)
        ROOT.gStyle.SetOptStat(0)
        ROOT.TH1.SetDefaultSumw2()
        stack = ROOT.THStack(v._name+"_"+r+"_"+cut_tag, v._name+"_"+r+"_"+cut_tag)
        leg_stack = ROOT.TLegend(0.45,0.88,0.9,0.75)
        leg_stack.SetNColumns(2)
        leg_stack.SetFillColor(0)
        leg_stack.SetFillStyle(0)
        leg_stack.SetTextFont(42)
        leg_stack.SetBorderSize(0)
        leg_stack.SetTextSize(0.03)

        for f,s in zip(infile["signal"], insample["signal"]):
            # print("Getting histo :", v._name+"_"+r+"_"+cut_tag)
            # print(" from:", f)
            print(v._name+"_"+r+"_"+cut_tag)
            tmp = copy.deepcopy(ROOT.TH1D(f.Get(v._name+"_"+r+"_"+cut_tag)))
            # print(tmp.GetBinContent(1))
            tmp.Scale(lumi)
            # print("scaled lumi "+str(lumi)+" from ", f)
            tmp.GetXaxis().SetTitle(v._title)
            tmp.SetName(s.leglabel)
            tmp.SetLineColor(s.color)
            tmp.SetLineWidth(1)
            tmp.SetTitle("")
            # print(tmp.GetBinContent(1))
            h_sign.append(tmp)
            # print(h_sign)
            leg_stack.AddEntry(tmp, s.leglabel, "l")
            #f.Close()

        for f, s in zip(infile["bkg"], insample['bkg']):
            # print("Getting histo :", v._name+"_"+r+"_"+cut_tag)
            # print(" from:", f)
            tmp = copy.deepcopy(ROOT.TH1D(f.Get(v._name+"_"+r+"_"+cut_tag)))
            tmp.Scale(lumi)
            tmp.GetXaxis().SetTitle(v._title)
            # tmp.SetLineColor(s.color)
            # tmp.SetFillColor(s.color)
            tmp.SetLineColor(s.color)
            tmp.SetLineWidth(0)
            tmp.SetFillColorAlpha(s.color, 0.5)
            tmp.SetName(s.leglabel)
            tmp.SetTitle("")
            stack.Add(tmp)
            leg_stack.AddEntry(tmp, s.leglabel, "f")
            #f.Close()

        if not blind:
            h_data = None #ROOT.TH1D()
            for f, s in zip(infile["Data"], insample["Data"]):
                # print("Getting histo :", v._name+"_"+r+"_"+cut_tag)
                # print(" from:", f, s.label)
                #print(type(f)
                tmp = copy.deepcopy(f.Get(v._name+"_"+r+"_"+cut_tag))
                tmp.SetTitle("")
                #tmp.SetLineColor(ROOT.kBlack)
                if h_data==None:
                    h_data = tmp.Clone("")
                else:
                    h_data.Add(tmp)
                #print("tmp", type(tmp))
                #print("h_data", type(h_data))
                #f.Close()
            # print("tmp", type(tmp))
            # print("h_data", type(h_data))
            leg_stack.AddEntry(h_data, "data", "ep")
            h_data.SetMarkerStyle(20)
            h_data.SetMarkerSize(1)
            #stack.SetMaximum(10000)

        
        canvasname = "canvas_"+v._name+"_"+r+"_"+cut_tag
        c1 = ROOT.TCanvas(canvasname,"c1",50,50,700,600)
        c1.SetFillColor(0)
        c1.SetBorderMode(0)
        c1.SetFrameFillStyle(0)
        c1.SetFrameBorderMode(0)
        c1.SetLeftMargin( 0.12 )
        c1.SetRightMargin( 0.9 )
        c1.SetTopMargin( 1 )
        c1.SetBottomMargin(-1)
        c1.SetTickx(1)
        c1.SetTicky(1)
        c1.Draw()
        c1.cd()

        pad1= ROOT.TPad("pad1", "pad1", 0, 0.31 , 1, 1)
        pad1.SetTopMargin(0.1)
        pad1.SetBottomMargin(0.02)
        pad1.SetLeftMargin(0.12)
        pad1.SetRightMargin(0.05)
        pad1.SetBorderMode(0)
        pad1.SetTickx(1)
        pad1.SetTicky(1)
        pad1.Draw()

        if not blind:
          maximum = max(stack.GetMaximum(),h_data.GetMaximum())
        #   minimum = min(stack.GetMinimum(),h_data.GetMinimum())
          if h_sign[-1].GetMinimum()!= 0:
              minimum = h_sign[-1].GetMinimum()
          elif stack.GetMinimum()!= 0:
              minimum = stack.GetMinimum()*1e-1
          else:
              minimum = 1e-1 #min(stack.GetMinimum(),1e-4)
        else:
          maximum = stack.GetMaximum()
          if h_sign[-1].GetMinimum()!= 0:
              minimum = h_sign[-1].GetMinimum()
          elif stack.GetMinimum()!= 0: 
              minimum = stack.GetMinimum()*1e-1
          else:
              minimum = 1e-1  
          #minimum = 1e-4
        
        logscale = True
        pad1.cd()
        if(logscale):
            stack.SetMaximum(maximum*10000)
            stack.SetMinimum(minimum)
            #stack.SetMinimum(minimum)
        else:
            stack.SetMaximum(maximum*1.6)
            stack.SetMinimum(minimum*0.5)
            #stack.SetMinimum(minimum)

        stack.SetTitle("")
        stack.Draw("HIST")
        # if "MinDelta_phi" in v._name:
        #         stack.GetXaxis().SetRange(1, 16)
        h_err = stack.GetStack().Last().Clone("h_err")
        h_err.SetTitle("")
        h_err.SetLineWidth(100)
        h_err.SetFillStyle(3154)
        h_err.SetMarkerSize(0)
        h_err.SetFillColor(ROOT.kGray+2)
        leg_stack.AddEntry(h_err, "Stat. Unc.", "f")
        h_err.Draw("e2same0")
        # stack.Draw()
        for h in h_sign: 
            # print(h.GetBinContent(1))
            h.Draw("hist same")
        if not blind:
            h_data.SetTitle("")
            h_data.Draw("eSAMEpx0")
        leg_stack.Draw("same")
        CMS_lumi.writeExtraText = 1
        CMS_lumi.extraText = ""
        if run2 :
            lumi_sqrtS = "%s fb^{-1}  (13 TeV)"%(lumi)
        elif run3:
             lumi_sqrtS = "%s fb^{-1}  (13.6 TeV)"%(lumi)
        iPeriod = 0
        iPos = 10
        CMS_lumi(pad1, lumi_sqrtS, iPos, r+"_"+regions[r])
        #CMS_lumi(pad1, lumi_sqrtS, iPos, r)
        # pad1.Draw()
        pad1.Update()
        if logscale:
            pad1.SetLogy()
        # pad1.Draw()
        # pad1.Draw()
        #####################################################
    
        hratio = stack.GetStack().Last()
     
        c1.cd()
        pad2= ROOT.TPad("pad2", "pad2", 0, 0.01 , 1, 0.315)
        pad2.SetTopMargin(0.06)
        pad2.SetBottomMargin(0.45)
        pad2.SetLeftMargin(0.12)
        pad2.SetRightMargin(0.05)
        ROOT.gStyle.SetHatchesSpacing(2)
        ROOT.gStyle.SetHatchesLineWidth(2)
        pad2.Draw()
        pad2.cd()
        if not blind:
            ratio = h_data.Clone("ratio")
            ratio.SetLineColor(ROOT.kBlack)
            ratio.SetMaximum(2)
            ratio.SetMinimum(0)
            # ratio.Sumw2()
            ratio.SetStats(0)
        
            ratio.Divide(hratio)
            ratio.SetMarkerStyle(20)
            ratio.SetMarkerSize(0.9)
            ratio.Draw("epx0e0")
            # if "MinDelta_phi" in v._name:
            #     ratio.GetXaxis().SetRange(1, 16)
            ratio.SetTitle("")
            ratio.GetYaxis().SetTitle("Data / MC")
            ratio.GetYaxis().SetNdivisions(503)
            ratio.GetXaxis().SetLabelFont(42)
            ratio.GetYaxis().SetLabelFont(42)
            ratio.GetXaxis().SetTitleFont(42)
            ratio.GetYaxis().SetTitleFont(42)
            ratio.GetXaxis().SetTitleOffset(1.1)
            ratio.GetYaxis().SetTitleOffset(0.35)
            ratio.GetXaxis().SetLabelSize(0.15)
            ratio.GetYaxis().SetLabelSize(0.15)
            ratio.GetXaxis().SetTitleSize(0.16)
            ratio.GetYaxis().SetTitleSize(0.16)
            ratio.GetYaxis().SetRangeUser(0.,2.0)
            ratio.GetXaxis().SetTitle(v._title)
            ratio.GetXaxis().SetLabelOffset(0.04)
            ratio.GetYaxis().SetLabelOffset(0.02)
            ratio.Draw("epx0e0same")
        else:
            ratio = h_sign[0].Clone("ratio")
            for i in range(1, ratio.GetNbinsX() + 1):
               ratio.SetBinContent(i, 1)
            ratio.SetLineColor(ROOT.kBlack)
            ratio.SetMaximum(2)
            ratio.SetMinimum(0)
            ratio.SetStats(0)
            #ratio.Divide(h_sign[0])
            ratio.SetMarkerStyle(20)
            ratio.SetMarkerSize(0.9)
            ratio.Draw("epx0e0")
            # if "MinDelta_phi" in v._name:
            #     ratio.GetXaxis().SetRange(1, 16)
            ratio.SetTitle("")
            ratio.GetYaxis().SetTitle("Data / MC")
            ratio.GetYaxis().SetNdivisions(503)
            ratio.GetXaxis().SetLabelFont(42)
            ratio.GetYaxis().SetLabelFont(42)
            ratio.GetXaxis().SetTitleFont(42)
            ratio.GetYaxis().SetTitleFont(42)
            ratio.GetXaxis().SetTitleOffset(1.1)
            ratio.GetYaxis().SetTitleOffset(0.35)
            ratio.GetXaxis().SetLabelSize(0.15)
            ratio.GetYaxis().SetLabelSize(0.15)
            ratio.GetXaxis().SetTitleSize(0.16)
            ratio.GetYaxis().SetTitleSize(0.16)
            ratio.GetYaxis().SetRangeUser(0.,2.0)
            ratio.GetXaxis().SetTitle(v._title)
            ratio.GetXaxis().SetLabelOffset(0.04)
            ratio.GetYaxis().SetLabelOffset(0.02)
            ratio.Draw("epx0e0same")
            
        
        h_bkg_err = hratio.Clone("h_err")
        h_bkg_err.Reset()
        #h_bkg_err.Sumw2()
        for i in range(1,hratio.GetNbinsX()+1):
            h_bkg_err.SetBinContent(i,1)
            if(hratio.GetBinContent(i)):
                h_bkg_err.SetBinError(i, (hratio.GetBinError(i)/hratio.GetBinContent(i)))
            else:
                h_bkg_err.SetBinError(i, 10^(-99))
        h_bkg_err.SetLineWidth(100)

        h_bkg_err.SetMarkerSize(0)
        h_bkg_err.SetFillColor(ROOT.kGray+1)
        h_bkg_err.Draw("e20same")
        
        f1 = ROOT.TLine(v._xmin, 1., v._xmax,1.)
        f1.SetLineColor(ROOT.kBlack)
        f1.SetLineStyle(ROOT.kDashed)
        f1.Draw("same")
        
        ratio.GetYaxis().SetTitle("Data / MC")
        ratio.GetYaxis().SetNdivisions(503)
        ratio.GetXaxis().SetLabelFont(42)
        ratio.GetYaxis().SetLabelFont(42)
        ratio.GetXaxis().SetTitleFont(42)
        ratio.GetYaxis().SetTitleFont(42)
        ratio.GetXaxis().SetTitleOffset(1.1)
        ratio.GetYaxis().SetTitleOffset(0.35)
        ratio.GetXaxis().SetLabelSize(0.15)
        ratio.GetYaxis().SetLabelSize(0.15)
        ratio.GetXaxis().SetTitleSize(0.16)
        ratio.GetYaxis().SetTitleSize(0.16)
        ratio.GetYaxis().SetRangeUser(0.,2.0)
        ratio.GetXaxis().SetTitle(v._title)
        ratio.GetXaxis().SetLabelOffset(0.04)
        ratio.GetYaxis().SetLabelOffset(0.02)
        ratio.Draw("epx0e0same")
        
        pad2.Draw()

        c1.cd()
        c1.RedrawAxis()
        pad2.RedrawAxis()
        #ROOT.TGaxis.SetMaxDigits(3)
        # c1.RedrawAxis()
        # pad2.RedrawAxis()
        # c1.Update()
        c1.Print(repostack+canvasname+".png")
        c1.Print(repostack+canvasname+".pdf")
        # tmp.Delete()
        # h.Delete()
    
        os.system('set LD_PRELOAD=libtcmalloc.so')
        #####################################################