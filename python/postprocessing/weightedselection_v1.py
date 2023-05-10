import os
import sys
import ROOT
from math import sqrt, cos
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
from datetime import datetime

usage = 'python weightedselection_v1.py'
parser = optparse.OptionParser(usage)
parser.add_option('-m', '--met', dest='met', type='float', default = 50, help="MET pt cut")
parser.add_option('-p', '--dphi', dest='dphi', type='float', default = 0, help="deltaPhi min jet-met")
parser.add_option('-R', '--dR', dest='dR', type='float', default = 0.8, help="delta R between top selected")
parser.add_option('-x', '--mix', dest='mix', type='float', default = 600, help="pt max mix top")
parser.add_option('-s', '--res', dest='res', type='float', default = 200, help="pt max res top")
parser.add_option('-e', '--maxeta', dest='maxeta', type='float', default = 3, help="max eta jet")
parser.add_option('-z', '--minmaxeta', dest='minmaxeta', default = False, action='store_true', help="min(True) or max(False) eta jet")
(opt, args) = parser.parse_args()

#parameters
dRmin = opt.dR
ptmax_res = opt.res
ptmin_mix = opt.res
ptmax_mix = opt.mix
ptmin_mer = opt.mix
pt_met = opt.met
mDPhi = opt.dphi
maxeta = opt.maxeta
minmax = opt.minmaxeta

ROOT.gROOT.SetBatch()
debug=False
verbose = True


    
datasets = [QCDHT_300to500_2018#TT_2018,
            #QCD_2018,
            #ZJetsToNuNu_2018,
            #tDM_mPhi50_mChi1_2018,tDM_mPhi500_mChi1_2018, tDM_mPhi1000_mChi1_2018,
            #TprimeToTZ_1800_2018,TprimeToTZ_1000_2018, TprimeToTZ_700_2018]
    ]

    #TT_2018,QCD_2018,ZJetsToNuNu_2018,tDM_mPhi50_mChi1_2018,tDM_mPhi500_mChi1_2018, tDM_mPhi1000_mChi1_2018]

print("datasets: ", datasets)
categories = ["resolved", "mix","merged"]

# minPhi , eta del jet a eta maggiore (solo jet con pt>50)

variables = [
    variable(name="top_pt", title="Top pT [GeV]", nbins=50, xmin=0, xmax=1000), 
    variable(name="top_m", title="Top mass [GeV]", nbins=30, xmin=0, xmax=500),
    variable(name="met_pt", title="MET pT [GeV]", nbins=50, xmin=0, xmax=1000),
    variable(name="min_dphi", title="#Delta #Phi", nbins=int(3/0.2), xmin=0, xmax=3),
    #variable(name="max_eta_jet", title="#eta", nbins=20, xmin=0, xmax=8),
    variable(name="mt", title="M_{T} [GeV]", nbins=30, xmin=0, xmax=1000)
    ]

lumi = 10**3#59.7*1000

outfolder = "/eos/home-a/acagnott/DarkMatter/testSelection/"
outfolder = outfolder+"met_"+str(pt_met)+"_mindphi_"+str(mDPhi)+"_dR_"+str(dRmin)+"_ptmaxres_"+str(ptmax_res)+"_ptmaxmix_"+str(ptmax_mix)+"/"

#if minmax: 
#    outfolder = outfolder+"met_"+str(pt_met)+"_mindphi_"+str(mDPhi)+"_etajet>"+str(maxeta)+"_dR_"+str(dRmin)+"_ptmaxres_"+str(ptmax_res)+"_ptmaxmix_"+str(ptmax_mix)+"/"
#else:
#    outfolder = outfolder+"met_"+str(pt_met)+"_mindphi_"+str(mDPhi)+"_etajet<"+str(maxeta)+"_dR_"+str(dRmin)+"_ptmaxres_"+str(ptmax_res)+"_ptmaxmix_"+str(ptmax_mix)+"/"
if not os.path.exists(outfolder):
    os.mkdir(outfolder)
outfolder = outfolder+"root_files/"
if not os.path.exists(outfolder):
    os.mkdir(outfolder)
#outfile = ROOT.TFile.Open(outfolder+"weightedhists.root", "RECREATE")
ROOT.gROOT.SetStyle('Plain')
ROOT.gStyle.SetPalette(1)
ROOT.gStyle.SetOptStat(0)
ROOT.TH1.SetDefaultSumw2()

def get_files_string(d):
    folder_files = "../../crab/macros/files/"
    infile_string = open(folder_files+d.label+".txt")
    strings = infile_string.readlines()
    for s in strings: s.replace('\n', '')
    return strings

def h_workflow(s):
    h_workflow = ROOT.TH1F("h_workflow_"+s, "", 4, -0.5, 3.5)
    #h_workflow.GetXaxis().SetBinLabel(1, "# events")
    h_workflow.GetXaxis().SetBinLabel(1, "met")
    h_workflow.GetXaxis().SetBinLabel(2, "#Delta#Phi")
    h_workflow.GetXaxis().SetBinLabel(3, "# top resolved")
    h_workflow.GetXaxis().SetBinLabel(4, "# top mix")
    h_workflow.GetXaxis().SetBinLabel(5, "# top merged")
    return h_workflow
    
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


t1 = datetime.now()

for d in datasets:
    print("### processing :", d.label)
    outfile = ROOT.TFile.Open(outfolder+d.label+"_weightedhists.root", "RECREATE")
    print(outfile)
    if 'tDM' in d.label or 'Tprime' in d.label: 
        signal = True
    else: 
        signal = False
    if hasattr(d, "components"):
        samples = d.components
        print(samples)
        tosum =True
    else:
        samples = [d]
        tosum = False
    h_wf = ROOT.TH1F("h_workflow_"+d.label, "", 5, -0.5, 4.5)
    h_wf.GetXaxis().SetBinLabel(1, "met")
    h_wf.GetXaxis().SetBinLabel(2, "#Delta#Phi")
    h_wf.GetXaxis().SetBinLabel(3, "# top resolved")
    h_wf.GetXaxis().SetBinLabel(4, "# top mix")
    h_wf.GetXaxis().SetBinLabel(5, "# top merged")

    h_ef = ROOT.TH1F("h_efficiency_"+d.label, "", 5, -0.5, 4.5)
    h_ef.GetXaxis().SetBinLabel(1, "met")
    h_ef.GetXaxis().SetBinLabel(2, "#Delta#Phi")
    h_ef.GetXaxis().SetBinLabel(3, "# top resolved")
    h_ef.GetXaxis().SetBinLabel(4, "# top mix")
    h_ef.GetXaxis().SetBinLabel(5, "# top merged")
        
    h = {v._name:{c: ROOT.TH1F("h_"+v._name+"_"+c+"_"+d.label, v._title, nbins[v._name][c], xmin[v._name][c], xmax[v._name][c]) for c in categories} for v in variables}

    for s in samples:
        strings = get_files_string(s)
        print("- ", s.label)
        chain = ROOT.TChain("Events")
        nevents = 0
        for fi in strings[:1]:
            chain.Add(fi)
            infile = ROOT.TFile.Open(fi)
            #tree = InputTree(infile.Get("Events"))
            h_genweight = ROOT.TH1F(infile.Get("plots/h_genweight"))
            nevents+=int(h_genweight.GetBinContent(1))
            infile.Close()
        if verbose: print('# total events:',nevents)
        if verbose: print("starting loop")
        region1, region2, region3 = 0,0,0
        met_cut=0
        dphi_cut = 0
        w = (s.sigma*lumi)/nevents
        
        tmp_wf = ROOT.TH1F("h_workflow_"+s.label, "", 5, -0.5, 4.5)
        tmp_wf.GetXaxis().SetBinLabel(1, "met")
        tmp_wf.GetXaxis().SetBinLabel(2, "#Delta#Phi")
        tmp_wf.GetXaxis().SetBinLabel(3, "# top resolved")
        tmp_wf.GetXaxis().SetBinLabel(4, "# top mix")
        tmp_wf.GetXaxis().SetBinLabel(5, "# top merged")
        tmp_ef = ROOT.TH1F("h_efficiency_"+s.label, "", 5, -0.5, 4.5)
        tmp_ef.GetXaxis().SetBinLabel(1, "met")
        tmp_ef.GetXaxis().SetBinLabel(2, "#Delta#Phi")
        tmp_ef.GetXaxis().SetBinLabel(3, "# top resolved")
        tmp_ef.GetXaxis().SetBinLabel(4, "# top mix")
        tmp_ef.GetXaxis().SetBinLabel(5, "# top merged")
        tmp = {v._name:{c: ROOT.TH1F("h_"+v._name+"_"+c+"_"+s.label, v._title, nbins[v._name][c], xmin[v._name][c], xmax[v._name][c]) for c in categories} for v in variables}
        
        for i in range(chain.GetEntries()):#tqdm(range(nevents)):
            tree = InputTree(chain)
            event = Event(tree, i)
            toplowpt = Collection(event, "TopLowPt")
            tophighpt = Collection(event, "TopHighPt")
            fatjet = Collection(event, "FatJet")
            goodfatjet = get_fatjet(fatjet)
            jet = Collection(event, "Jet")
            goodjet = get_jet(jet)
            met = Object(event, "MET")
            LHE = Collection(event, "LHEPart")
            if met.pt<pt_met:
                met_cut +=1
                continue
            midphi = Object(event, "MinDelta")
            mindphi = midphi.phi
            '''mindphi=1000
            maxetajet=0
            for j in goodjet:
                if j.pt<30 and j.jetId<2: continue
                dphi = abs(deltaPhi(j.phi,met.phi))
                if dphi<mindphi: mindphi = dphi
                if j.pt<50: continue
                if abs(j.eta)>maxetajet: maxetajet=abs(j.eta)
            '''
            if mindphi<mDPhi: 
                dphi_cut +=1
                continue
            #if minmax and maxetajet<maxeta:
            #    continue
            #if not minmax and maxetajet>maxeta:
            #    continue
                
            top_res = top_select(toplowpt, trs_res, ptmin=0, ptmax=ptmax_res, dR =dRmin, category='res')
            top_mix = top_select(tophighpt, trs_mix, ptmin=ptmax_res, ptmax=ptmax_mix, dR=dRmin, category='mix')
            top_mer = top_select(goodfatjet, trs_mer, ptmin=ptmax_mix, ptmax=10000, dR=dRmin, category='mer')
            n_tres=len(top_res)
            n_tmix= len(top_mix)
            n_tmer=len(top_mer)
            
            if n_tres>0 and n_tmix==0 and n_tmer==0:
                cat = "resolved"
                region1 +=1
                best_top = np.argmax([t.scoreDNN for t in top_res])
                tmp[variables[0]._name][cat].Fill(top_res[best_top].pt, w)
                if top_res[best_top].pt>xmax[variables[0]._name][cat]: tmp[variables[0]._name][cat].AddBinContent(nbins[variables[0]._name][cat], w)
                tmp[variables[1]._name][cat].Fill(top_res[best_top].mass, w)
                if top_res[best_top].mass>xmax[variables[1]._name][cat]: tmp[variables[1]._name][cat].AddBinContent(nbins[variables[1]._name][cat], w)
                tmp[variables[2]._name][cat].Fill(met.pt, w)
                if met.pt>xmax[variables[2]._name][cat]: tmp[variables[2]._name][cat].AddBinContent(nbins[variables[2]._name][cat], w)
                tmp[variables[3]._name][cat].Fill(mindphi, w)
                if mindphi>xmax[variables[3]._name][cat]: tmp[variables[3]._name][cat].AddBinContent(nbins[variables[3]._name][cat], w)
                #tmp[variables[4]._name][cat].Fill(maxetajet, w)
                #if maxetajet>xmax[variables[4]._name][cat]: tmp[variables[4]._name][cat].AddBinContent(nbins[variables[4]._name][cat], w)
                mt = sqrt(2*top_res[best_top].pt*met.pt*(1-cos(top_res[best_top].phi -met.phi)))
                tmp[variables[4]._name][cat].Fill(mt, w)
                if mt>xmax[variables[4]._name][cat]: tmp[variables[4]._name][cat].AddBinContent(nbins[variables[4]._name][cat], w)
            elif n_tres<2 and n_tmix>0 and n_tmer==0:
                cat = "mix"
                region2 +=1
                best_top = np.argmax([t.score2 for t in top_mix])
                tmp[variables[0]._name][cat].Fill(top_mix[best_top].pt, w)
                if top_mix[best_top].pt>xmax[variables[0]._name][cat]: tmp[variables[0]._name][cat].AddBinContent(nbins[variables[0]._name][cat], w)
                tmp[variables[1]._name][cat].Fill(top_mix[best_top].mass, w)
                if top_mix[best_top].mass>xmax[variables[1]._name][cat]: tmp[variables[1]._name][cat].AddBinContent(nbins[variables[1]._name][cat], w)
                tmp[variables[2]._name][cat].Fill(met.pt, w)
                if met.pt>xmax[variables[2]._name][cat]: tmp[variables[2]._name][cat].AddBinContent(nbins[variables[2]._name][cat], w)
                tmp[variables[3]._name][cat].Fill(mindphi, w)
                if mindphi>xmax[variables[3]._name][cat]: tmp[variables[3]._name][cat].AddBinContent(nbins[variables[3]._name][cat], w)
                #tmp[variables[4]._name][cat].Fill(maxetajet, w)
                #if maxetajet>xmax[variables[4]._name][cat]: tmp[variables[4]._name][cat].AddBinContent(nbins[variables[4]._name][cat], w)
                mt = sqrt(2*top_mix[best_top].pt*met.pt*(1-cos(top_mix[best_top].phi -met.phi)))
                tmp[variables[4]._name][cat].Fill(mt, w)
                if mt>xmax[variables[4]._name][cat]: tmp[variables[4]._name][cat].AddBinContent(nbins[variables[4]._name][cat], w)
            elif n_tres==0 and n_tmix<2 and n_tmer>0:
                cat = "merged"
                region3 +=1
                best_top = np.argmax([t.deepTag_TvsQCD for t in top_mer])
                tmp[variables[0]._name][cat].Fill(top_mer[best_top].pt, w)
                if top_mer[best_top].pt>xmax[variables[0]._name][cat]: tmp[variables[0]._name][cat].AddBinContent(nbins[variables[0]._name][cat], w)
                tmp[variables[1]._name][cat].Fill(top_mer[best_top].mass, w)
                if top_mer[best_top].mass>xmax[variables[1]._name][cat]: tmp[variables[1]._name][cat].AddBinContent(nbins[variables[1]._name][cat], w)
                tmp[variables[2]._name][cat].Fill(met.pt, w)
                if met.pt>xmax[variables[2]._name][cat]: tmp[variables[2]._name][cat].AddBinContent(nbins[variables[2]._name][cat], w)
                tmp[variables[3]._name][cat].Fill(mindphi, w)
                if mindphi>xmax[variables[3]._name][cat]: tmp[variables[3]._name][cat].AddBinContent(nbins[variables[3]._name][cat], w)
                #tmp[variables[4]._name][cat].Fill(maxetajet, w)
                #if maxetajet>xmax[variables[4]._name][cat]: tmp[variables[4]._name][cat].AddBinContent(nbins[variables[4]._name][cat], w)
                mt = sqrt(2*top_mer[best_top].pt*met.pt*(1-cos(top_mer[best_top].phi -met.phi)))
                tmp[variables[4]._name][cat].Fill(mt, w)
                if mt>xmax[variables[4]._name][cat]: tmp[variables[4]._name][cat].AddBinContent(nbins[variables[4]._name][cat], w)
        if verbose:
            print("# events dropped by met request", met_cut)
            print("top resolved ", region1)
            print("top mix ", region2)
            print("top merged ", region3)
        tmp_wf.SetBinContent(0, nevents)
        tmp_wf.SetBinContent(1, ((nevents-met_cut))*w)
        tmp_wf.SetBinContent(2, ((nevents-met_cut-dphi_cut))*w)
        tmp_wf.SetBinContent(3, (region1)*w)
        tmp_wf.SetBinContent(4, (region2)*w)
        tmp_wf.SetBinContent(5, (region3)*w)
        tmp_ef.SetBinContent(0, nevents)
        tmp_ef.SetBinContent(1, (nevents-met_cut)/nevents)
        tmp_ef.SetBinContent(2, (nevents-met_cut-dphi_cut)/nevents)
        tmp_ef.SetBinContent(3, (region1)/nevents)
        tmp_ef.SetBinContent(4, (region2)/nevents)
        tmp_ef.SetBinContent(5, (region3)/nevents)
        if tosum:
            h_wf.Add(tmp_wf)
            h_ef.Add(tmp_ef)
            for v in variables:
                for c in categories:
                    h[v._name][c].Add(tmp[v._name][c])
        else:
            h_wf = tmp_wf
            h_ef = tmp_ef
            for v in variables:
                for c in categories:
                    h[v._name][c]=tmp[v._name][c]
    outfile.cd()
    h_wf.Write()
    h_ef.Write()
    for v in variables:
        for c in categories:
            h[v._name][c].Write()
    outfile.Close()

t2 = datetime.now()
print(t2-t1)
