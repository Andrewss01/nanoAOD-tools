# caricare gli histo dal file root in testSelection e produrre gli stack
import os
import sys
import ROOT
import math
from array import array
import ROOT
import copy
import numpy as np
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
import pickle as pkl
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.tresholds_ml import *
from PhysicsTools.NanoAODTools.postprocessing.variables import *
from tqdm import tqdm
import optparse
from plot_parameters import *
from CMS_lumi import CMS_lumi

usage = 'python weightedselection_v1.py'
parser = optparse.OptionParser(usage)
parser.add_option('-m', '--met', dest='met', type='float', default = 50, help="MET pt cut")
parser.add_option('-p', '--dphi', dest='dphi', type='float', default = 0, help="deltaPhi min jet-met")
parser.add_option('-R', '--dR', dest='dR', type='float', default = 0.8, help="delta R between top selected")
parser.add_option('-x', '--mix', dest='mix', type='float', default = 600, help="pt max mix top")
parser.add_option('-s', '--res', dest='res', type='float', default = 200, help="pt max res top")
parser.add_option('-t', '--tprime', dest='tprime', action='store_true', default = False, help="signal=Tprime")
parser.add_option('-e', '--maxeta', dest='maxeta', type='float', default = 3, help="max eta jet")
parser.add_option('-z', '--minmaxeta', dest='minmaxeta', default = False, action='store_true', help="min(True) or max(False) eta jet")
(opt, args) = parser.parse_args()

ROOT.gROOT.SetBatch()
debug=False
verbose = True

#parameters
dRmin = opt.dR
ptmax_res = opt.res
ptmin_mix = opt.res
ptmax_mix = opt.mix
ptmin_mer = opt.mix
pt_met = opt.met
mindphi = opt.dphi
tprime=opt.tprime
maxeta = opt.maxeta
minmax = opt.minmaxeta

vars = [
    variable(name="top_pt", title="Top pT [GeV]", nbins=50, xmin=0, xmax=1000), 
    variable(name="top_m", title="Top mass [GeV]", nbins=30, xmin=0, xmax=250),
    variable(name="met_pt", title="MET pT [GeV]", nbins=50, xmin=0, xmax=1000),
    variable(name="min_dphi", title="#Delta #Phi", nbins=int(3/0.2), xmin=0, xmax=3),
    variable(name="max_eta_jet", title="#eta", nbins=20, xmin=0, xmax=8)
    ]
if tprime:
    datasets = [TT_2018,#TT_Mtt700to1000_2018,TT_Mtt1000toInf_2018,TT_semilep_2018,
            QCD_2018,#QCDHT_1000to1500_2018,QCDHT_1500to2000_2018, QCDHT_2000toInf_2018,
            ZJetsToNuNu_2018,
            TprimeToTZ_1800_2018,TprimeToTZ_1000_2018, TprimeToTZ_700_2018]
else:
    datasets = [TT_2018,#TT_Mtt700to1000_2018,TT_Mtt1000toInf_2018,TT_semilep_2018,
                QCD_2018,#QCDHT_1000to1500_2018,QCDHT_1500to2000_2018, QCDHT_2000toInf_2018,
                ZJetsToNuNu_2018,
                tDM_mPhi50_mChi1_2018,tDM_mPhi500_mChi1_2018, tDM_mPhi1000_mChi1_2018]

categories = ["resolved", "mix","merged"]
folder = "/eos/home-a/acagnott/DarkMatter/testSelection/"
folder = folder+"met_"+str(pt_met)+"_mindphi_"+str(mindphi)+"_dR_"+str(dRmin)+"_ptmaxres_"+str(ptmax_res)+"_ptmaxmix_"+str(ptmax_mix)+"/"
#if minmax:
#    folder = folder+"met_"+str(pt_met)+"_mindphi_"+str(mindphi)+"_etajet>"+str(maxeta)+"_dR_"+str(dRmin)+"_ptmaxres_"+str(ptmax_res)+"_ptmaxmix_"+str(ptmax_mix)+"/"
#else:
#    folder = folder+"met_"+str(pt_met)+"_mindphi_"+str(mindphi)+"_etajet<"+str(maxeta)+"_dR_"+str(dRmin)+"_ptmaxres_"+str(ptmax_res)+"_ptmaxmix_"+str(ptmax_mix)+"/"
infolder = folder+"root_files/"

if tprime :
    folder = folder+'Tprime/'
    if not os.path.exists(folder):
        os.mkdir(folder)

ROOT.gROOT.SetStyle('Plain')
ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetOptStat(0)
ROOT.TH1.SetDefaultSumw2()

stack_wf = ROOT.THStack("h_workflow", "workflow")
stack_ef = ROOT.THStack("h_efficiency", "efficiency")
stack ={v._name: {c: ROOT.THStack("h_"+v._name+"_"+c, "h_"+v._name+"_"+c) for c in categories} for v in vars}
leg_stack = ROOT.TLegend(0.45,0.88,0.9,0.75)
leg_stack.SetNColumns(2)
leg_stack.SetFillColor(0)
leg_stack.SetFillStyle(0)
leg_stack.SetTextFont(42)
leg_stack.SetBorderSize(0)
leg_stack.SetTextSize(0.03)

canv_wf = ROOT.TCanvas("c_wf", "c_wf")
canv_wf.SetLogy()
canv_ef = ROOT.TCanvas("c_ef", "c_ef")
canv_ef.SetLogy()
canv = {v._name:{c: ROOT.TCanvas("c_"+v._name+"_"+c, "c_"+v._name+"_"+c) for c in categories}for v in vars}

signals, bkgs = [],[]
for d in datasets:
    if 'tDM' in d.label or 'Tprime' in d.label:
        signals.append(d.label)
    else:
        bkgs.append(d.label)

significance_ttasS = { s: ROOT.TH1F("h_significance_"+s, "Significance tt as signal", 6, -0.5,5.5) for s in signals}
significance_ttasB = { s: ROOT.TH1F("h_significance_"+s, "Significance tt as bkg", 6, -0.5,5.5)  for s in signals}
n_sgn = {s:{c: 0 for c in categories} for s in signals}
n_bkg = {b: {c: 0 for c in categories} for b in bkgs}

h_sgn_wf = []
h_sgn_ef = []
his_sgn = {v._name: {c: [] for c in categories} for v in vars}

for d in datasets:
    infile = ROOT.TFile.Open(infolder+d.label+"_weightedhists.root")
    if 'tDM' in d.label or 'Tprime' in d.label:
        tmp_ =copy.deepcopy(infile.Get("h_workflow_"+d.label))#.Clone()
        tmp_.SetLineColor(d.color)
        tmp_.SetLineWidth(2)
        tmp_e =copy.deepcopy(infile.Get("h_efficiency_"+d.label))#.Clone()
        tmp_e.SetLineColor(d.color)
        tmp_e.SetLineWidth(2)
        leg_stack.AddEntry(tmp_, d.leglabel, "l")
        h_sgn_wf.append(tmp_)
        h_sgn_ef.append(tmp_e)
        for v in vars:
            for c in categories:
                tmp_ = copy.deepcopy(infile.Get("h_"+v._name+"_"+c+"_"+d.label))
                tmp_.SetLineColor(d.color)
                tmp_.SetLineWidth(2)
                his_sgn[v._name][c].append(tmp_)
                if 'min_dphi' in v._name :
                    n_sgn[d.label][c] = tmp_.Integral()
    else:
        h_bkg = copy.deepcopy(infile.Get("h_workflow_"+d.label))#.Clone()
        h_bkg.SetFillColor(d.color)
        h_bkg.SetLineColor(d.color)
        h_bkg.SetName(d.leglabel)
        stack_wf.Add(h_bkg)
        h_bkg = copy.deepcopy(infile.Get("h_efficiency_"+d.label))#.Clone()
        h_bkg.SetFillColor(d.color)
        h_bkg.SetLineColor(d.color)
        h_bkg.SetName(d.leglabel)
        stack_ef.Add(h_bkg)
        #stack_ef.Add(h_bkg)
        for v in vars:
            for c in categories:
                h_bkg = copy.deepcopy(infile.Get("h_"+v._name+"_"+c+"_"+d.label))#.Clone()
                h_bkg.SetFillColor(d.color)
                h_bkg.SetLineColor(d.color)
                h_bkg.SetName(d.leglabel)
                stack[v._name][c].Add(h_bkg)
                if 'min_dphi' in v._name :
                    n_bkg[d.label][c]=h_bkg.Integral()
        
        leg_stack.AddEntry(h_bkg, h_bkg.GetName(), "f")
    infile.Close()

if tprime:
    s='Tprime'
else:
    s='DM'


canv_wf.cd()
#canv_wf.Draw()
'''pad1= ROOT.TPad("pad1", "pad1", -.9, .5, .0, .9 )
pad1.SetTopMargin(0.1)
pad1.SetBottomMargin(0.02)
pad1.SetLeftMargin(0.12)
pad1.SetRightMargin(0.05)
pad1.SetBorderMode(0)
pad1.SetTickx(1)
pad1.SetTicky(1)
pad1.Draw()
pad1.cd()
'''
canv_wf.cd()
stack_wf.SetMinimum(minimum_stack[s]['workflow'])    
stack_wf.Draw("HIST")
stack_wf.SetMaximum(stack_wf.GetHistogram().GetMaximum()*10000)
stack_wf.GetYaxis().SetTitle("# Events")
stack_wf.GetYaxis().SetTitleFont(42)
stack_wf.GetXaxis().SetLabelOffset(1.8)
stack_wf.GetYaxis().SetTitleOffset(0.85)
stack_wf.GetXaxis().SetLabelSize(0.13)
stack_wf.GetYaxis().SetLabelSize(0.05)
stack_wf.GetYaxis().SetTitleSize(0.07)
stack_wf.Draw("HIST")
for h in h_sgn_wf: h.Draw("same")
leg_stack.Draw("same")

lumi = 59.7
lumi_sqrtS = "%s fb^{-1}  (13 TeV)"%(lumi)

iPeriod = 0
iPos = 11
#CMS_lumi(pad1, lumi_sqrtS, iPos, '')
#hratio = stack_wf.GetStack().Last()
#pad1.cd()


canv_wf.SaveAs(folder+"h_workflow.png", "png")
canv_wf.SaveAs(folder+"h_workflow.pdf", "pdf")

canv_ef.cd()
stack_ef.SetMinimum(minimum_stack[s]['efficiency'])    
stack_ef.Draw("HIST")
for h in h_sgn_ef: h.Draw("same")
leg_stack.Draw("same")    
canv_ef.SaveAs(folder+"h_efficiency.png", "png")
canv_ef.SaveAs(folder+"h_efficiency.pdf", "pdf")
for v in vars:
    for c in categories:
        canv[v._name][c].Draw()
        canv[v._name][c].SetLogy()
        canv[v._name][c].cd()
        stack[v._name][c].SetMinimum(minimum_stack[s][v._name])
        stack[v._name][c].Draw("HIST")
        for h in his_sgn[v._name][c]: h.Draw("same")
        leg_stack.Draw("same")
        canv[v._name][c].SaveAs(folder+"h_"+v._name+"_"+c+".png", "png")
        canv[v._name][c].SaveAs(folder+"h_"+v._name+"_"+c+".pdf", "pdf")

#significance_ttasS = { s: {c: ROOT.TH1F("h_significance_"+s.label, "Significance", 6, -0.5,5.5) for c in categories} for s in signals}
#significance_ttasB = { s: {c: ROOT.TH1F("h_significance_"+s.label, "Significance", 6, -0.5,5.5) for c in categories} for s in signals}

for s in signals:
    for c in categories:
        n_bkg_w_tt = 0
        n_bkg_wo_tt = 0
        n_sgn_w_tt = n_sgn[s][c]+n_bkg['TT_2018'][c]
        for b in bkgs:
            n_bkg_w_tt += n_bkg[b][c]
            if not 'TT' in b:n_bkg_wo_tt+=n_bkg[b][c]
        if 'res' in c : nbin=1
        elif 'mix' in c : nbin=3
        else: nbin=5
        
        if n_sgn_w_tt==0 or n_bkg_wo_tt==0: continue
        print(s+"+++++++++++++++++++++++++++++++++++++++")
        significance_ttasS[s].GetXaxis().SetBinLabel(nbin,c+" rad(s+b)")
        significance_ttasS[s].SetBinContent(nbin, n_sgn_w_tt/math.sqrt(n_bkg_wo_tt+n_sgn_w_tt))
        significance_ttasB[s].GetXaxis().SetBinLabel(nbin,c+" rad(s+b)")
        significance_ttasB[s].SetBinContent(nbin, n_sgn[s][c]/math.sqrt(n_bkg_w_tt+n_sgn[s][c]))
        print(c+" rad(s+b)",n_sgn[s][c]/math.sqrt(n_bkg_w_tt+n_sgn[s][c]))
        significance_ttasS[s].GetXaxis().SetBinLabel(nbin+1,c+" rad(b)")
        significance_ttasS[s].SetBinContent(nbin+1, n_sgn_w_tt/math.sqrt(n_bkg_wo_tt))
        significance_ttasB[s].GetXaxis().SetBinLabel(nbin+1,c+" rad(b)")
        significance_ttasB[s].SetBinContent(nbin+1, n_sgn[s][c]/math.sqrt(n_bkg_w_tt))
        print(c+" rad(b)", n_sgn[s][c]/math.sqrt(n_bkg_w_tt))

outfolder =  folder
for s in signals :
    for c in categories:
        c1 = ROOT.TCanvas()
        significance_ttasS[s].Draw()
        c1.SaveAs(outfolder+"significance_"+s+"_tts.png")
        c1.SaveAs(outfolder+"significance_"+s+"_tts.pdf")
        c1 = ROOT.TCanvas()
        significance_ttasB[s].Draw()
        c1.SaveAs(outfolder+"significance_"+s+"_ttb.png")
        c1.SaveAs(outfolder+"significance_"+s+"_ttb.pdf")
