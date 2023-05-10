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
from tqdm import tqdm

ROOT.gROOT.SetBatch()
debug=False
verbose = True

datasets = [TT_Mtt700to1000_2018,TT_Mtt1000toInf_2018,TT_semilep_2018,QCDHT_1000to1500_2018,QCDHT_1500to2000_2018, QCDHT_2000toInf_2018,tDM_mPhi1000_mChi1]
#datasets = [TT_Mtt700to1000_2018,QCDHT_1000to1500_2018,tDM_mPhi1000_mChi1]

#parameter definition
dRmin = 0.8
ptmax_res = 200
ptmin_mix = 200
ptmax_mix = 600
ptmin_mer = 600
pt_met = 50
lumi = 59.7*1000

#selection func
def top_select(top, trs, ptmin, ptmax, dR, category):
    if 'mix' in category:
        tops = np.array(list(filter(lambda x : (x.pt<ptmax)*(x.pt>ptmin)*(x.score2>trs) , top)))
        scores = np.array([t.score2 for t in tops])
    elif 'res' in category:
        tops = np.array(list(filter(lambda x : (x.pt<ptmax)*(x.scoreDNN>trs) , top)))
        scores = np.array([t.scoreDNN for t in tops])
    elif 'mer' in category:
        tops = np.array(list(filter(lambda x : (x.pt>ptmin)*(x.deepTag_TvsQCD>trs) , top)))
        scores = np.array([t.deepTag_TvsQCD for t in tops])
    top_sel = []
    while(np.sum(scores!=0)>0):
        drs = np.array([deltaR(tops[np.argmax(scores)], t) for t in tops])
        for i, d in enumerate(drs):
            if i==np.argmax(scores): continue
            if d<dR: scores[i]=0
        top_sel.append(tops[np.argmax(scores)])
        scores[np.argmax(scores)]=0
        tops = tops[scores!=0]
        scores = scores[scores!=0]
        drs = np.array([deltaR(tops[np.argmax(scores)], t) for t in tops])
        if debug: print('top selezionati', len(top_sel))
        if debug: print('deltaRs', drs)
    return top_sel

# histos definition
def h_workflow(s):
    h_workflow = ROOT.TH1F("h_workflow_"+s, "", 5, -0.5, 4.5)
    #h_workflow.GetXaxis().SetBinLabel(1, "# events")
    h_workflow.GetXaxis().SetBinLabel(1, "met")
    h_workflow.GetXaxis().SetBinLabel(2, "# top resolved")
    h_workflow.GetXaxis().SetBinLabel(3, "# top mix")
    h_workflow.GetXaxis().SetBinLabel(4, "# top merged")
    return h_workflow

def histo(s, var_name, bins, x_min, x_max):
    h = ROOT.TH1F("h_"+var_name+"_"+s, "", bins, x_min, x_max)
    #h_workflow.GetXaxis().SetBinLabel(1, "# events")
    return h

categories = ["resolved", "mix","merged"]
outfolder = "/eos/home-a/acagnott/DarkMatter/testSelection/"

outfolder = outfolder+"met_"+str(pt_met)+"_dR_"+str(dRmin)+"_ptmaxres_"+str(ptmax_res)+"_ptmaxmix_"+str(ptmax_mix)+"/"

if not os.path.exists(outfolder):
    os.mkdir(outfolder)

outfile = ROOT.TFile.Open(outfolder+"weightedhists.root", "RECREATE")
ROOT.gROOT.SetStyle('Plain')
ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetOptStat(0)
ROOT.TH1.SetDefaultSumw2()
stack_wf = copy.deepcopy(ROOT.THStack("h_workflow_stack","workflow"))
stack_top_pt = {c: copy.deepcopy(ROOT.THStack("h_top_pt_"+c+"_stack","Top pt")) for c in categories}
stack_top_mass = {c: copy.deepcopy(ROOT.THStack("h_top_m_"+c+"_stack","Top mass")) for c in categories}
stack_met_pt = {c: copy.deepcopy(ROOT.THStack("h_met_pt_"+c+"_stack","MET pt")) for c in categories}

leg_stack = ROOT.TLegend(0.33,0.62,0.91,0.87)
for d in datasets:
    print("### processing :", d.label)
    if 'tDM' in d.label: 
        signal = True
    else: 
        signal = False
    infile = ROOT.TFile.Open(d.local_path)
    tree = InputTree(infile.Get("Events"))
    nevents = tree.GetEntries()
    if verbose: print('# total events:',nevents)
    if verbose: print("starting loop")
    region1, region2, region3 = 0,0,0
    met_cut=0
    if not signal:
        h_wf = copy.deepcopy(ROOT.TH1F(h_workflow(d.label)))
        h_top_pt = {c: copy.deepcopy(ROOT.TH1F(histo(d.label,"top_pt_"+c, 50, 0, 1000))) for c in categories}
        h_top_mass = {c: copy.deepcopy(ROOT.TH1F(histo(d.label,"top_m_"+c, 30, 0, 500))) for c in categories}
        h_met_pt = {c: copy.deepcopy(ROOT.TH1F(histo(d.label,"met_pt_"+c, 50, 0, 1000))) for c in categories}
    else:
        h_wf_sgn = copy.deepcopy(ROOT.TH1F(h_workflow(d.label+"*100")))
        h_top_pt_sgn = {c: copy.deepcopy(ROOT.TH1F(histo(d.label+"*100","top_pt_"+c, 50, 0, 1000))) for c in categories}
        h_top_mass_sgn = {c: copy.deepcopy(ROOT.TH1F(histo(d.label+"*100","top_m_"+c, 30, 0, 500))) for c in categories}
        h_met_pt_sgn = {c: copy.deepcopy(ROOT.TH1F(histo(d.label+"*100","met_pt_"+c, 50, 0, 1000))) for c in categories}
        
    for i in tqdm(range(nevents)):
        event = Event(tree, i)
        toplowpt = Collection(event, "TopLowPt")
        tophighpt = Collection(event, "TopHighPt")
        fatjet = Collection(event, "FatJet")
        met = Object(event, "MET")
        LHE = Collection(event, "LHEPart")
        if met.pt<pt_met:
            met_cut +=1
            continue
        top_res = top_select(toplowpt, trs_res, ptmin=0, ptmax=200, dR =dRmin, category='res')
        top_mix = top_select(tophighpt, trs_mix, ptmin=200, ptmax=600, dR=dRmin, category='mix')
        top_mer = top_select(fatjet, trs_mer, ptmin=600, ptmax=10000, dR=dRmin, category='mer')
        n_tres=len(top_res)
        n_tmix= len(top_mix)
        n_tmer=len(top_mer)
        if n_tres>0 and n_tmix==0 and n_tmer==0:
            region1 +=1
            best_top = np.argmax([t.scoreDNN for t in top_res])
            if signal:
                h_top_pt_sgn["resolved"].Fill(top_res[best_top].pt)
                h_top_mass_sgn["resolved"].Fill(top_res[best_top].mass)
                h_met_pt_sgn["resolved"].Fill(met.pt)
            else:    
                h_top_pt["resolved"].Fill(top_res[best_top].pt)
                h_top_mass["resolved"].Fill(top_res[best_top].mass)
                h_met_pt["resolved"].Fill(met.pt)
        elif n_tres<2 and n_tmix>0 and n_tmer==0:
            region2 +=1
            best_top = np.argmax([t.score2 for t in top_mix])
            if signal:
                h_top_pt_sgn["mix"].Fill(top_mix[best_top].pt)
                h_top_mass_sgn["mix"].Fill(top_mix[best_top].mass)
                h_met_pt_sgn["mix"].Fill(met.pt)
            else:
                h_top_pt["mix"].Fill(top_mix[best_top].pt)
                h_top_mass["mix"].Fill(top_mix[best_top].mass)
                h_met_pt["mix"].Fill(met.pt)
        elif n_tres==0 and n_tmix<2 and n_tmer>0:
            region3 +=1
            best_top = np.argmax([t.deepTag_TvsQCD for t in top_mer])
            if signal:
                h_top_pt_sgn["merged"].Fill(top_mer[best_top].pt)
                h_top_mass_sgn["merged"].Fill(top_mer[best_top].mass)
                h_met_pt_sgn["merged"].Fill(met.pt)
            else:
                h_top_pt["merged"].Fill(top_mer[best_top].pt)
                h_top_mass["merged"].Fill(top_mer[best_top].mass)
                h_met_pt["merged"].Fill(met.pt)
    if verbose:
        print("# events dropped by met request", met_cut)
        print("top resolved ", region1)
        print("top mix ", region2)
        print("top merged ", region3)
    if not signal:
        h_wf.SetBinContent(0, nevents)
        h_wf.SetBinContent(1, ((nevents-met_cut)/nevents)*d.sigma*lumi)
        h_wf.SetBinContent(2, (region1/nevents)*d.sigma*lumi)
        h_wf.SetBinContent(3, (region2/nevents)*d.sigma*lumi)
        h_wf.SetBinContent(4, (region3/nevents)*d.sigma*lumi)
        h_wf.SetName(d.label)
    else:
        h_wf_sgn.SetBinContent(0, nevents)
        h_wf_sgn.SetBinContent(1, ((nevents-met_cut)/nevents)*d.sigma*lumi)
        h_wf_sgn.SetBinContent(2, (region1/nevents)*d.sigma*lumi)
        h_wf_sgn.SetBinContent(3, (region2/nevents)*d.sigma*lumi)
        h_wf_sgn.SetBinContent(4, (region3/nevents)*d.sigma*lumi)
        h_wf_sgn.SetName(d.label+"*100")
    
    if signal:
        h_wf_sgn.SetLineColor(d.color)
        leg_stack.AddEntry(h_wf_sgn, h_wf_sgn.GetName(), "l")
        h_top_pt_sgn[c].SetLineColor(d.color)
        h_top_mass_sgn[c].SetLineColor(d.color)
        h_met_pt_sgn[c].SetLineColor(d.color)
        outfile.cd()
        h_wf_sgn.Write()
        for c in categories:
            h_top_pt_sgn[c].Write()
            h_top_mass_sgn[c].Write()
            h_met_pt_sgn[c].Write()
    else:
        h_wf.SetFillColor(d.color)
        h_wf.SetLineColor(d.color)
        for c in categories:
            h_top_pt[c].SetFillColor(d.color)
            h_top_pt[c].SetLineColor(d.color)
            h_top_mass[c].SetFillColor(d.color)
            h_top_mass[c].SetLineColor(d.color)
            h_met_pt[c].SetFillColor(d.color)
            h_met_pt[c].SetLineColor(d.color)

            stack_top_pt[c].Add(h_top_pt[c])
            stack_top_mass[c].Add(h_top_mass[c])
            stack_met_pt[c].Add(h_met_pt[c])
        leg_stack.AddEntry(h_wf, h_wf.GetName(), "f")
        stack_wf.Add(h_wf)#.Clone(""))
        outfile.cd()
        h_wf.Write()
        for c in categories:
            h_top_pt[c].Write()
            h_top_mass[c].Write()
            h_met_pt[c].Write()

canv_wf = ROOT.TCanvas("c_wf", "c_wf")

canv_top_pt = {c: copy.deepcopy(ROOT.TCanvas("c_top_pt_"+c, "Top pt "+c)) for c in categories}
canv_top_mass = {c: copy.deepcopy(ROOT.TCanvas("c_top_m_"+c, "Top mass "+c)) for c in categories}
canv_met_pt = {c: copy.deepcopy(ROOT.TCanvas("c_top_m_"+c, "MET pt "+c)) for c in categories}

leg_stack.SetNColumns(2)
leg_stack.SetFillColor(0)
leg_stack.SetFillStyle(0)
leg_stack.SetTextFont(42)
leg_stack.SetBorderSize(0)
leg_stack.SetTextSize(0.05)

canv_wf.Draw()
canv_wf.SetLogy()
canv_wf.cd()
stack_wf.Draw("HIST")
h_wf_sgn.Draw("HIST same")
leg_stack.Draw("same")

canv_wf.SaveAs(outfolder+"h_workflow.png")
canv_wf.SaveAs(outfolder+"h_workflow.pdf")

for c in categories:
    canv_top_pt[c].Draw()
    canv_top_pt[c].SetLogy()
    stack_top_pt[c].Draw("HIST")
    h_top_pt_sgn[c].Draw("HIST same")
    leg_stack.Draw("same")
    canv_top_pt[c].SaveAs(outfolder+"h_top_pt_"+c+".png")
    canv_top_pt[c].SaveAs(outfolder+"h_top_pt_"+c+".pdf")
    canv_top_mass[c].Draw()
    canv_top_mass[c].SetLogy()
    stack_top_mass[c].Draw("HIST")
    h_top_mass_sgn[c].Draw("HIST same")
    leg_stack.Draw("same")
    canv_top_mass[c].SaveAs(outfolder+"h_top_m_"+c+".png")
    canv_top_mass[c].SaveAs(outfolder+"h_top_m_"+c+".pdf")
    canv_met_pt[c].Draw()
    canv_met_pt[c].SetLogy()
    stack_met_pt[c].Draw("HIST")
    h_met_pt_sgn[c].Draw("HIST same")
    leg_stack.Draw("same")
    canv_met_pt[c].SaveAs(outfolder+"h_met_pt_"+c+".png")
    canv_met_pt[c].SaveAs(outfolder+"h_met_pt_"+c+".pdf")
    
stack_wf.Write()
for c in categories:
    stack_top_pt[c].Write()
    stack_top_mass[c].Write()
    stack_met_pt[c].Write()

outfile.Close()
    
