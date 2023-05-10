import os
import sys
import ROOT
import math
from array import array
import ROOT
import numpy as np
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
import pickle as pkl
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *

ROOT.gROOT.SetBatch()
debug=False

#datasets = [TT_Mtt700to1000_2018,TT_Mtt1000toInf_2018,TT_semilep_2018,QCDHT_1000to1500_2018,QCDHT_1500to2000_2018, QCDHT_2000toInf_2018,tDM_mPhi1000_mChi1]

folderIn= "/eos/home-a/acagnott/DarkMatter/topcandidate_file/"
inputfile = sys.argv[1]+'_Skim.root'
#'QCD_HT1000_Skim_Skim_Skim.root'#'QCD-HT1500to2000_2018_Skim_Skim_Skim.root'#'TT_Hadr_2018_Skim_Skim_Skim.root'#'tDM_mPhi1000_mChi1_Skim_Skim_Skim.root'
#'TT_SemiLep_2018_Skim_Skim_Skim.root'#'QCD-HT2000toInf_2018_Skim_Skim_Skim.root'
folderOut= "/eos/home-a/acagnott/DarkMatter/testSelection/"
#outfile = "eventselection_tDM_mPhi1000.root"
of = inputfile
while('Skim' in of):
    of = of.replace("_Skim", "")
outfile = "eventselection_"+of
if not os.path.exists(folderOut):
    os.mkdir(folderOut)
verbose = True
outfile = ROOT.TFile.Open(folderOut+outfile,"RECREATE")    #<-----OutFile
#treshold upload
with open("/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/DNN_phase1_test_lowpt_LSTM/tresholds_LSTM.pkl", "rb") as f:
    trs_lowptLSTM = pkl.load(f)
with open("/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/DNN_phase1_test_lowpt_DNN/tresholds_DNN.pkl", "rb") as f:
    trs_lowptDNN = pkl.load(f)    
with open("/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/DNN_phase1_test_highpt/tresholds.pkl", "rb") as f:
    trs_highpt = pkl.load(f)
with open("/eos/home-a/acagnott/SWAN_projects/DM/DNNmodel/DNN_phase2_test2/tresholds.pkl", "rb") as f:
    trs_highpt_2 = pkl.load(f)
trs_res = trs_lowptDNN['fpr 1']
trs_mix = trs_highpt_2['fpr 10']
trs_mer = 0.99
# histos
#average of top selected in each category over every single event
h_top_sel = ROOT.TH1F("event_top_sel","number of top selected per event", 3, -0.5, 4.5) 
h_top_sel.GetXaxis().SetBinLabel(1, " top res")
h_top_sel.GetXaxis().SetBinLabel(2, " top mix")
h_top_sel.GetXaxis().SetBinLabel(3, " top mer")

h_top_res = ROOT.TH1F("event_top_res","number of top resolved selected per event", 31, -0.5, 30.5)
h_top_mix = ROOT.TH1F("event_top_mix","number of top mix selected per event", 31, -0.5, 30.5)
h_top_mer = ROOT.TH1F("event_top_mer","number of top merged selected per event", 31, -0.5, 30.5)

h_top_res_mix = ROOT.TH2F("event_top_res_mix","number of top resolved Vs top mix selected per event;# top resolved;# top mix", 16, -0.5, 15.5, 16, -0.5, 15.5)
h_top_mix_mer = ROOT.TH2F("event_top_mix_mer","number of top mix Vs top mer selected per event;# top mix;# top merged", 16, -0.5, 15.5, 16, -0.5, 15.5)
h_topres_mix_mer = ROOT.TH2F("h_topres_mix_mer","number of top mix Vs top mer with at least 1res per event;# top mix;# top merged", 16, -0.5, 15.5, 16, -0.5, 15.5)
h_topmix_res_mer = ROOT.TH2F("h_topmix_res_mer","number of top res Vs top mer with at least 1mix per event;# top resolved;# top merged", 16, -0.5, 15.5, 16, -0.5, 15.5)
h_topmer_res_mix = ROOT.TH2F("h_topmer_res_mix","number of top res Vs top mix with at least 1mer per event;# top resolved;# top mix", 16, -0.5, 15.5, 16, -0.5, 15.5)

h_topresmatch_mix_mer = ROOT.TH2F("event_topresmatch_mix_mer","number of top mix Vs top mer with at least 1res match per event;# top mix;# top merged", 16, -0.5, 15.5, 16, -0.5, 15.5)
h_topmixmatch_res_mer = ROOT.TH2F("event_topmixmatch_res_mer","number of top res Vs top mer with at least 1mix match per event;# top resolved;# top merged", 16, -0.5, 15.5, 16, -0.5, 15.5)
h_topmermatch_res_mix = ROOT.TH2F("event_topmermatch_res_mix","number of top res Vs top mix with at least 1mer match per event;# top resolved;# top mix", 16, -0.5, 15.5, 16, -0.5, 15.5)

h_2topres_mix_mer = ROOT.TH2F("event_2topres_mix_mer","number of top mix Vs top mer with at least 2res per event;# top mix;# top merged", 16, -0.5, 15.5, 16, -0.5, 15.5)
h_2topmix_res_mer = ROOT.TH2F("event_2topmix_res_mer","number of top res Vs top mer with at least 2mix per event;# top resolved;# top merged", 16, -0.5, 15.5, 16, -0.5, 15.5)
h_2topmer_res_mix = ROOT.TH2F("event_2topmer_res_mix","number of top res Vs top mix with at least 2mer per event;# top resolved;# top mix", 16, -0.5, 15.5, 16, -0.5, 15.5)
h_1topres_mix_mer = ROOT.TH2F("event_1topres_mix_mer","number of top mix Vs top mer with 1res per event;# top mix;# top merged", 16, -0.5, 15.5, 16, -0.5, 15.5)
h_1topmix_res_mer = ROOT.TH2F("event_1topmix_res_mer","number of top res Vs top mer with 1mix per event;# top resolved;# top merged", 16, -0.5, 15.5, 16, -0.5, 15.5)
h_1topmer_res_mix = ROOT.TH2F("event_1topmer_res_mix","number of top res Vs top mix with 1mer per event;# top resolved;# top mix", 16, -0.5, 15.5, 16, -0.5, 15.5)
# regions definition: # top overview
h_selectregions_res_mix_0mer = ROOT.TH2F("h_selectregions_res_mix_0mer", "# of event(with 0 merged) Vs # top resolved Vs # top mix;# top resolved;# top mix", 4, -0.5, 3.5, 4, -0.5, 3.5)
h_selectregions_res_mix_1mer = ROOT.TH2F("h_selectregions_res_mix_1mer", "# of event(with 1 merged) Vs # top resolved Vs # top mix;# top resolved;# top mix", 4, -0.5, 3.5, 4, -0.5, 3.5)
h_selectregions_mix_mer = ROOT.TH2F("h_selectregions_mix_mer", "# of event Vs # top mix Vs # top merged;# top mix;# top merged", 4, -0.5, 3.5, 4, -0.5, 3.5)

h_selectregions_resmatch_mix_0mer = ROOT.TH2F("h_selectregions_resmatch_mix_0mer", "# of event(with 0 merged) Vs # top resolved matchedVs # top mix;# top resolved;# top mix", 4, -0.5, 3.5, 4, -0.5, 3.5)
h_selectregions_resmatch_mix_1mer = ROOT.TH2F("h_selectregions_resmatch_mix_1mer", "# of event(with 1 merged) Vs # top resolved matched Vs # top mix;# top resolved;# top mix", 4, -0.5, 3.5, 4, -0.5, 3.5)
h_selectregions_res_mixmatch_0mer = ROOT.TH2F("h_selectregions_res_mixmatch_0mer", "# of event(with 0 merged) Vs # top resolved Vs # top mix matched;# top resolved;# top mix", 4, -0.5, 3.5, 4, -0.5, 3.5)
h_selectregions_res_mixmatch_1mer = ROOT.TH2F("h_selectregions_res_mixmatch_1mer", "# of event(with 1 merged) Vs # top resolved Vs # top mix matched;# top resolved;# top mix", 4, -0.5, 3.5, 4, -0.5, 3.5)
h_selectregions_res_mix_1mermatch = ROOT.TH2F("h_selectregions_res_mix_1mermatch", "# of event(with 1 merged matched) Vs # top resolved Vs # top mix matched;# top resolved;# top mix", 4, -0.5, 3.5, 4, -0.5, 3.5)

#workflow
h_workflow = ROOT.TH1F("h_workflow", "workflow: events passing each step", 5, -0.5, 4.5)
h_workflow.GetXaxis().SetBinLabel(1, "# events")
h_workflow.GetXaxis().SetBinLabel(2, "met")
h_workflow.GetXaxis().SetBinLabel(3, "# top resolved")
h_workflow.GetXaxis().SetBinLabel(4, "# top mix")
h_workflow.GetXaxis().SetBinLabel(5, "# top merged")
h_workflow_match = ROOT.TH1F("h_workflow_match", "workflow: events passing each step", 5, -0.5, 4.5)
h_workflow_match.GetXaxis().SetBinLabel(1, "# events")
h_workflow_match.GetXaxis().SetBinLabel(2, "met")
h_workflow_match.GetXaxis().SetBinLabel(3, "# top resolved")
h_workflow_match.GetXaxis().SetBinLabel(4, "# top mix")
h_workflow_match.GetXaxis().SetBinLabel(5, "# top merged")

#event loop
infile = ROOT.TFile.Open(folderIn+inputfile)    #<---------------  InputFile
print("Input file: ", infile)
tree = InputTree(infile.Get("Events"))
nevents = tree.GetEntries()
if verbose: print('# total events:',nevents)
if verbose: print("starting loop")
n_top_res = []
n_top_mix = []
n_top_mer = []
n_top_res_true = []
n_top_mix_true = []
n_top_mer_true = []
region1, region2, region3 = 0,0,0
region1_m, region2_m, region3_m = 0,0,0
met_cut=0
dRmin = 0.8

'''def top_resolved(toplowpt, trs, ptmax, dR):
    t_sel = []
    for t in toplowpt:
        db = False
        for t_ in t_sel:
            if deltaR(t, t_)<dR: db = True
        if t.scoreDNN>trs and t.pt<ptmax and not db:
            t_sel.append(t)
    return t_sel
'''
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

n_event_with_truetop = 0
n_event_with_truetop_select = 0
for i in range (nevents):
    n_tres = 0
    n_tmix = 0 
    n_tmer = 0
    if verbose and i%10000==0: print("event ,",i)
    event = Event(tree, i)
    toplowpt = Collection(event, "TopLowPt")
    tophighpt = Collection(event, "TopHighPt")
    fatjet = Collection(event, "FatJet")
    met = Object(event, "MET")
    LHE = Collection(event, "LHEPart")

    if met.pt<50: 
        met_cut +=1
        continue

    thadr_res = False
    thadr_mix = False
    thadr_mer = False
    for t in toplowpt:
        if t.truth==1: thadr_res = True
    for t in tophighpt:
        if t.truth==1: thadr_mix = True
    for t in fatjet:
        if t.matched==3: thadr_mer = True
    if thadr_res or thadr_mix or thadr_mer:n_event_with_truetop+=1

    sel_top_res = []
    sel_top_mix = []
    sel_top_mer = []
    
    top_res = top_select(toplowpt, trs_res, ptmin=0, ptmax=200, dR =dRmin, category='res')
    top_mix = top_select(tophighpt, trs_mix, ptmin=200, ptmax=600, dR=dRmin, category='mix')
    top_mer = top_select(fatjet, trs_mer, ptmin=600, ptmax=10000, dR=dRmin, category='mer')
    thadr_res = False
    thadr_mix = False
    thadr_mer = False
    for t in top_res:
        if t.truth==1: thadr_res = True
    for t in top_mix:
        if t.truth==1: thadr_mix = True
    for t in top_mer:
        if t.matched==3: thadr_mer = True
    if thadr_res or thadr_mix or thadr_mer:n_event_with_truetop_select+=1


    n_tres=len(top_res)
    n_tmix= len(top_mix)
    n_tmer=len(top_mer)
    n_tres_true= np.sum([t.truth for t in top_res])
    n_tmix_true= np.sum([t.truth for t in top_mix])
    n_tmer_true= np.sum([t.matched==3 for t in top_mer])
    n_top_res.append(n_tres)
    n_top_mix.append(n_tmix)
    n_top_mer.append(n_tmer)
    n_top_res_true.append(n_tres_true)
    n_top_mix_true.append(n_tmix_true)
    n_top_mer_true.append(n_tmer_true)

    if n_tres>2 and n_tmix==0 and n_tmer==0: h_selectregions_res_mix_0mer.Fill(3, 0)
    elif n_tres>2 and n_tmix==1 and n_tmer==0: h_selectregions_res_mix_0mer.Fill(3, 1)
    elif n_tres>2 and n_tmix==2 and n_tmer==0: h_selectregions_res_mix_0mer.Fill(3, 2)
    elif n_tres>2 and n_tmix>2 and n_tmer==0: h_selectregions_res_mix_0mer.Fill(3, 3)
    elif n_tres==2 and n_tmix>2 and n_tmer==0: h_selectregions_res_mix_0mer.Fill(2, 3)
    elif n_tres==1 and n_tmix>2 and n_tmer==0: h_selectregions_res_mix_0mer.Fill(1, 3)
    elif n_tres==0 and n_tmix>2 and n_tmer==0: h_selectregions_res_mix_0mer.Fill(0, 3)
    elif n_tmer==0: h_selectregions_res_mix_0mer.Fill(n_tres, n_tmix)
    
    if n_tres_true>2 and n_tmix==0 and n_tmer==0: h_selectregions_resmatch_mix_0mer.Fill(3, 0)
    elif n_tres_true>2 and n_tmix==1 and n_tmer==0: h_selectregions_resmatch_mix_0mer.Fill(3, 1)
    elif n_tres_true>2 and n_tmix==2 and n_tmer==0: h_selectregions_resmatch_mix_0mer.Fill(3, 2)
    elif n_tres_true>2 and n_tmix>2 and n_tmer==0: h_selectregions_resmatch_mix_0mer.Fill(3, 3)
    elif n_tres_true==2 and n_tmix>2 and n_tmer==0: h_selectregions_resmatch_mix_0mer.Fill(2, 3)
    elif n_tres_true==1 and n_tmix>2 and n_tmer==0: h_selectregions_resmatch_mix_0mer.Fill(1, 3)
    elif n_tres_true==0 and n_tmix>2 and n_tmer==0: h_selectregions_resmatch_mix_0mer.Fill(0, 3)
    elif n_tmer==0: h_selectregions_resmatch_mix_0mer.Fill(n_tres_true, n_tmix)
    
    if n_tres>2 and n_tmix_true==0 and n_tmer==0: h_selectregions_res_mixmatch_0mer.Fill(3, 0)
    elif n_tres>2 and n_tmix_true==1 and n_tmer==0: h_selectregions_res_mixmatch_0mer.Fill(3, 1)
    elif n_tres>2 and n_tmix_true==2 and n_tmer==0: h_selectregions_res_mixmatch_0mer.Fill(3, 2)
    elif n_tres>2 and n_tmix_true>2 and n_tmer==0: h_selectregions_res_mixmatch_0mer.Fill(3, 3)
    elif n_tres==2 and n_tmix_true>2 and n_tmer==0: h_selectregions_res_mixmatch_0mer.Fill(2, 3)
    elif n_tres==1 and n_tmix_true>2 and n_tmer==0: h_selectregions_res_mixmatch_0mer.Fill(1, 3)
    elif n_tres==0 and n_tmix_true>2 and n_tmer==0: h_selectregions_res_mixmatch_0mer.Fill(0, 3)
    elif n_tmer==0: h_selectregions_res_mixmatch_0mer.Fill(n_tres, n_tmix_true)

    if n_tres>2 and n_tmix==0 and n_tmer==1: h_selectregions_res_mix_1mer.Fill(3, 0)
    elif n_tres>2 and n_tmix==1 and n_tmer==1: h_selectregions_res_mix_1mer.Fill(3, 1)
    elif n_tres>2 and n_tmix==2 and n_tmer==1: h_selectregions_res_mix_1mer.Fill(3, 2)
    elif n_tres>2 and n_tmix>2 and n_tmer==1: h_selectregions_res_mix_1mer.Fill(3, 3)
    elif n_tres==2 and n_tmix>2 and n_tmer==1: h_selectregions_res_mix_1mer.Fill(2, 3)
    elif n_tres==1 and n_tmix>2 and n_tmer==1: h_selectregions_res_mix_1mer.Fill(1, 3)
    elif n_tres==0 and n_tmix>2 and n_tmer==1: h_selectregions_res_mix_1mer.Fill(0, 3)
    elif n_tmer==1: h_selectregions_res_mix_1mer.Fill(n_tres, n_tmix)
    
    if n_tres_true>2 and n_tmix==0 and n_tmer==1: h_selectregions_resmatch_mix_1mer.Fill(3, 0)
    elif n_tres_true>2 and n_tmix==1 and n_tmer==1: h_selectregions_resmatch_mix_1mer.Fill(3, 1)
    elif n_tres_true>2 and n_tmix==2 and n_tmer==1: h_selectregions_resmatch_mix_1mer.Fill(3, 2)
    elif n_tres_true>2 and n_tmix>2 and n_tmer==1: h_selectregions_resmatch_mix_1mer.Fill(3, 3)
    elif n_tres_true==2 and n_tmix>2 and n_tmer==1: h_selectregions_resmatch_mix_1mer.Fill(2, 3)
    elif n_tres_true==1 and n_tmix>2 and n_tmer==1: h_selectregions_resmatch_mix_1mer.Fill(1, 3)
    elif n_tres_true==0 and n_tmix>2 and n_tmer==1: h_selectregions_resmatch_mix_1mer.Fill(0, 3)
    elif n_tmer==1: h_selectregions_resmatch_mix_1mer.Fill(n_tres_true, n_tmix)

    if n_tres>2 and n_tmix_true==0 and n_tmer==1: h_selectregions_res_mixmatch_1mer.Fill(3, 0)
    elif n_tres>2 and n_tmix_true==1 and n_tmer==1: h_selectregions_res_mixmatch_1mer.Fill(3, 1)
    elif n_tres>2 and n_tmix_true==2 and n_tmer==1: h_selectregions_res_mixmatch_1mer.Fill(3, 2)
    elif n_tres>2 and n_tmix_true>2 and n_tmer==1: h_selectregions_res_mixmatch_1mer.Fill(3, 3)
    elif n_tres==2 and n_tmix_true>2 and n_tmer==1: h_selectregions_res_mixmatch_1mer.Fill(2, 3)
    elif n_tres==1 and n_tmix_true>2 and n_tmer==1: h_selectregions_res_mixmatch_1mer.Fill(1, 3)
    elif n_tres==0 and n_tmix_true>2 and n_tmer==1: h_selectregions_res_mixmatch_1mer.Fill(0, 3)
    elif n_tmer==1: h_selectregions_res_mixmatch_1mer.Fill(n_tres, n_tmix_true)

    if n_tres>2 and n_tmix==0 and n_tmer_true==1: h_selectregions_res_mix_1mermatch.Fill(3, 0)
    elif n_tres>2 and n_tmix==1 and n_tmer_true==1: h_selectregions_res_mix_1mermatch.Fill(3, 1)
    elif n_tres>2 and n_tmix==2 and n_tmer_true==1: h_selectregions_res_mix_1mermatch.Fill(3, 2)
    elif n_tres>2 and n_tmix>2 and n_tmer_true==1: h_selectregions_res_mix_1mermatch.Fill(3, 3)
    elif n_tres==2 and n_tmix>2 and n_tmer_true==1: h_selectregions_res_mix_1mermatch.Fill(2, 3)
    elif n_tres==1 and n_tmix>2 and n_tmer_true==1: h_selectregions_res_mix_1mermatch.Fill(1, 3)
    elif n_tres==0 and n_tmix>2 and n_tmer_true==1: h_selectregions_res_mix_1mermatch.Fill(0, 3)
    elif n_tmer_true==1: h_selectregions_res_mix_1mermatch.Fill(n_tres, n_tmix)
    
    if n_tmix>2 and n_tmer==0: h_selectregions_mix_mer.Fill(3, 0)
    elif n_tmix>2 and n_tmer==1: h_selectregions_mix_mer.Fill(3, 1)
    elif n_tmix>2 and n_tmer==2: h_selectregions_mix_mer.Fill(3, 2)
    elif n_tmix>2 and n_tmer>2: h_selectregions_mix_mer.Fill(3, 3)
    elif n_tmix==2 and n_tmer>2: h_selectregions_mix_mer.Fill(2, 3)
    elif n_tmix==1 and n_tmer>2: h_selectregions_mix_mer.Fill(1, 3)
    elif n_tmix==0 and n_tmer>2: h_selectregions_mix_mer.Fill(0, 3)
    else: h_selectregions_mix_mer.Fill(n_tmix, n_tmer)
    

    if n_tres>0 and n_tmix==0 and n_tmer==0:
        region1 +=1
        if 1 in [t.truth for t in top_res]: region1_m+=1
    elif n_tres<2 and n_tmix>0 and n_tmer==0:
        region2 +=1
        if 1 in [t.truth for t in top_mix]: region2_m+=1
    elif n_tres==0 and n_tmix<2 and n_tmer>0:
        region3 +=1
        if 3 in [t.matched for t in top_mer]: region3_m+=1

    #filling histos
    h_top_res.AddBinContent(0)
    h_top_res.Fill(n_tres)
    h_top_mix.AddBinContent(0)
    h_top_mix.Fill(n_tmix)
    h_top_mer.AddBinContent(0)
    h_top_mer.Fill(n_tmer)
    
    h_top_res_mix.Fill(n_tres, n_tmix)
    h_top_mix_mer.Fill(n_tmix, n_tmer)
    
    if n_tres>0: h_topres_mix_mer.Fill(n_tmix, n_tmer)
    if n_tmix>0: h_topmix_res_mer.Fill(n_tres, n_tmer)
    if n_tmer>0: h_topmer_res_mix.Fill(n_tres, n_tmix)
    
    if n_tres_true>0: h_topresmatch_mix_mer.Fill(n_tmix, n_tmer)
    if n_tmix_true>0: h_topmixmatch_res_mer.Fill(n_tres, n_tmer)
    if n_tmer_true>0: h_topmermatch_res_mix.Fill(n_tres, n_tmix)
    
    if n_tres>1:h_2topres_mix_mer.Fill(n_tmix, n_tmer)
    if n_tmix>1:h_2topmix_res_mer.Fill(n_tres, n_tmer)
    if n_tmer>1:h_2topmer_res_mix.Fill(n_tres, n_tmix)
    
    if n_tres==1:h_1topres_mix_mer.Fill(n_tmix, n_tmer)
    if n_tmix==1:h_1topmix_res_mer.Fill(n_tres, n_tmer)
    if n_tmer==1:h_1topmer_res_mix.Fill(n_tres, n_tmix)


print("# events dropped by met request", met_cut)
print("top resolved ", region1)
print("top mix ", region2)
print("top merged ", region3)
h_workflow.SetBinContent(1, nevents)
h_workflow.SetBinContent(2, nevents-met_cut)
h_workflow.SetBinContent(3, region1)
h_workflow.SetBinContent(4, region2)
h_workflow.SetBinContent(5, region3)

h_workflow_match.SetBinContent(1, nevents)
h_workflow_match.SetBinContent(2, nevents-met_cut)
h_workflow_match.SetBinContent(3, region1_m)
h_workflow_match.SetBinContent(4, region2_m)
h_workflow_match.SetBinContent(5, region3_m)

print("event with a true top :", n_event_with_truetop)
print("event with a true top select :", n_event_with_truetop_select)

print('average of top res in each event ', np.mean(n_top_res))
print('average of top res TRUE in each event ', np.mean(n_top_res_true))
print('average of top mix in each event ', np.mean(n_top_mix))
print('average of top mix TRUE in each event ', np.mean(n_top_mix_true))
print('average of top mer in each event ', np.mean(n_top_mer))
print('average of top mer TRUE in each event ', np.mean(n_top_mer_true))
h_top_sel.SetBinContent(1,np.mean(n_top_res))
h_top_sel.SetBinContent(2,np.mean(n_top_mix))
h_top_sel.SetBinContent(3,np.mean(n_top_mer))

outfile.cd()
h_top_sel.Write()
h_top_res.Write()
h_top_mix.Write()
h_top_mer.Write()
if h_top_res_mix.GetEntries()!=0: h_top_res_mix.Scale(1./h_top_res_mix.GetEntries())
h_top_res_mix.SetBinContent(1,1, h_top_res_mix.GetBinContent(1,1)*0.1)
h_top_res_mix.SetStats(0)
h_top_res_mix.Write()
if h_top_mix_mer.GetEntries()!=0: h_top_mix_mer.Scale(1./h_top_mix_mer.GetEntries())
h_top_mix_mer.SetBinContent(1, 1, h_top_mix_mer.GetBinContent(1,1)*0.1)
h_top_mix_mer.SetStats(0)
h_top_mix_mer.Write()
if h_topres_mix_mer.GetEntries()!=0: h_topres_mix_mer.Scale(1./h_topres_mix_mer.GetEntries())
h_topres_mix_mer.SetBinContent(1, 1, h_topres_mix_mer.GetBinContent(1,1)*0.1)
h_topres_mix_mer.SetStats(0)
h_topres_mix_mer.Write()
if h_topmix_res_mer.GetEntries()!=0: h_topmix_res_mer.Scale(1./h_topmix_res_mer.GetEntries())
h_topmix_res_mer.SetBinContent(1, 1, h_topmix_res_mer.GetBinContent(1,1)*0.1)
h_topmix_res_mer.SetStats(0)
h_topmix_res_mer.Write()
if h_topmer_res_mix.GetEntries()!=0: h_topmer_res_mix.Scale(1./h_topmer_res_mix.GetEntries())
h_topmer_res_mix.SetBinContent(1, 1, h_topmer_res_mix.GetBinContent(1,1)*0.1)
h_topmer_res_mix.SetStats(0)
h_topmer_res_mix.Write()
if h_topresmatch_mix_mer.GetEntries()!=0: h_topresmatch_mix_mer.Scale(1./h_topresmatch_mix_mer.GetEntries())
h_topresmatch_mix_mer.SetBinContent(1, 1, h_topresmatch_mix_mer.GetBinContent(1,1)*0.1)
h_topresmatch_mix_mer.SetStats(0)
h_topresmatch_mix_mer.Write()
if h_topmixmatch_res_mer.GetEntries()!=0: h_topmixmatch_res_mer.Scale(1./h_topmixmatch_res_mer.GetEntries())
h_topmixmatch_res_mer.SetBinContent(1, 1, h_topmixmatch_res_mer.GetBinContent(1,1)*0.1)
h_topmixmatch_res_mer.SetStats(0)
h_topmixmatch_res_mer.Write()
if h_topmermatch_res_mix.GetEntries()!=0: h_topmermatch_res_mix.Scale(1./h_topmermatch_res_mix.GetEntries())
h_topmermatch_res_mix.SetBinContent(1, 1, h_topmermatch_res_mix.GetBinContent(1,1)*0.1)
h_topmermatch_res_mix.SetStats(0)
h_topmermatch_res_mix.Write()
if h_2topres_mix_mer.GetEntries()!=0: h_2topres_mix_mer.Scale(1./h_2topres_mix_mer.GetEntries())
h_2topres_mix_mer.SetBinContent(1, 1, h_2topres_mix_mer.GetBinContent(1,1)*0.1)
h_2topres_mix_mer.SetStats(0)
h_2topres_mix_mer.Write()
if h_2topmix_res_mer.GetEntries()!=0: h_2topmix_res_mer.Scale(1./h_2topmix_res_mer.GetEntries())
h_2topmix_res_mer.SetBinContent(1, 1, h_2topmix_res_mer.GetBinContent(1,1)*0.1)
h_2topmix_res_mer.SetStats(0)
h_2topmix_res_mer.Write()
if h_2topmer_res_mix.GetEntries()!=0: h_2topmer_res_mix.Scale(1./h_2topmer_res_mix.GetEntries())
h_2topmer_res_mix.SetBinContent(1, 1, h_2topmer_res_mix.GetBinContent(1,1)*0.1)
h_2topmer_res_mix.SetStats(0)
h_2topmer_res_mix.Write()
if h_1topres_mix_mer.GetEntries()!=0: h_1topres_mix_mer.Scale(1./h_1topres_mix_mer.GetEntries())
h_1topres_mix_mer.SetBinContent(1, 1, h_1topres_mix_mer.GetBinContent(1,1)*0.1)
h_1topres_mix_mer.SetStats(0)
h_1topres_mix_mer.Write()
if h_1topmix_res_mer.GetEntries()!=0: h_1topmix_res_mer.Scale(1./h_1topmix_res_mer.GetEntries())
h_1topmix_res_mer.SetBinContent(1, 1, h_1topmix_res_mer.GetBinContent(1,1)*0.1)
h_1topmix_res_mer.SetStats(0)
h_1topmix_res_mer.Write()
if h_1topmer_res_mix.GetEntries()!=0: h_1topmer_res_mix.Scale(1./h_1topmer_res_mix.GetEntries())
h_1topmer_res_mix.SetBinContent(1, 1, h_1topmer_res_mix.GetBinContent(1,1)*0.1)
h_1topmer_res_mix.SetStats(0)
h_1topmer_res_mix.Write()

if h_selectregions_res_mix_0mer.GetEntries()!=0 : h_selectregions_res_mix_0mer.Scale(1./h_workflow.GetBinContent(2))
h_selectregions_res_mix_0mer.SetStats(0)
h_selectregions_res_mix_0mer.GetXaxis().SetBinLabel(1, "0")
h_selectregions_res_mix_0mer.GetXaxis().SetBinLabel(2, "1")
h_selectregions_res_mix_0mer.GetXaxis().SetBinLabel(3, "2")
h_selectregions_res_mix_0mer.GetXaxis().SetBinLabel(4, ">2")
h_selectregions_res_mix_0mer.GetYaxis().SetBinLabel(1, "0")
h_selectregions_res_mix_0mer.GetYaxis().SetBinLabel(2, "1")
h_selectregions_res_mix_0mer.GetYaxis().SetBinLabel(3, "2")
h_selectregions_res_mix_0mer.GetYaxis().SetBinLabel(4, ">2")
h_selectregions_res_mix_0mer.Write()

if h_selectregions_res_mix_1mer.GetEntries()!=0 : h_selectregions_res_mix_1mer.Scale(1./h_workflow.GetBinContent(2))
h_selectregions_res_mix_1mer.SetStats(0)
h_selectregions_res_mix_1mer.GetXaxis().SetBinLabel(1, "0")
h_selectregions_res_mix_1mer.GetXaxis().SetBinLabel(2, "1")
h_selectregions_res_mix_1mer.GetXaxis().SetBinLabel(3, "2")
h_selectregions_res_mix_1mer.GetXaxis().SetBinLabel(4, ">2")
h_selectregions_res_mix_1mer.GetYaxis().SetBinLabel(1, "0")
h_selectregions_res_mix_1mer.GetYaxis().SetBinLabel(2, "1")
h_selectregions_res_mix_1mer.GetYaxis().SetBinLabel(3, "2")
h_selectregions_res_mix_1mer.GetYaxis().SetBinLabel(4, ">2")
h_selectregions_res_mix_1mer.Write()

if h_selectregions_mix_mer.GetEntries()!=0 : h_selectregions_mix_mer.Scale(1./h_workflow.GetBinContent(2))
h_selectregions_mix_mer.SetStats(0)
h_selectregions_mix_mer.GetXaxis().SetBinLabel(1, "0")
h_selectregions_mix_mer.GetXaxis().SetBinLabel(2, "1")
h_selectregions_mix_mer.GetXaxis().SetBinLabel(3, "2")
h_selectregions_mix_mer.GetXaxis().SetBinLabel(4, ">2")
h_selectregions_mix_mer.GetYaxis().SetBinLabel(1, "0")
h_selectregions_mix_mer.GetYaxis().SetBinLabel(2, "1")
h_selectregions_mix_mer.GetYaxis().SetBinLabel(3, "2")
h_selectregions_mix_mer.GetYaxis().SetBinLabel(4, ">2")
h_selectregions_mix_mer.Write()

if h_selectregions_resmatch_mix_0mer.GetEntries()!=0 : h_selectregions_resmatch_mix_0mer.Scale(1./h_workflow.GetBinContent(2))
h_selectregions_resmatch_mix_0mer.SetStats(0)
h_selectregions_resmatch_mix_0mer.GetXaxis().SetBinLabel(1, "0")
h_selectregions_resmatch_mix_0mer.GetXaxis().SetBinLabel(2, "1")
h_selectregions_resmatch_mix_0mer.GetXaxis().SetBinLabel(3, "2")
h_selectregions_resmatch_mix_0mer.GetXaxis().SetBinLabel(4, ">2")
h_selectregions_resmatch_mix_0mer.GetYaxis().SetBinLabel(1, "0")
h_selectregions_resmatch_mix_0mer.GetYaxis().SetBinLabel(2, "1")
h_selectregions_resmatch_mix_0mer.GetYaxis().SetBinLabel(3, "2")
h_selectregions_resmatch_mix_0mer.GetYaxis().SetBinLabel(4, ">2")
h_selectregions_resmatch_mix_0mer.Write()

if h_selectregions_resmatch_mix_1mer.GetEntries()!=0 : h_selectregions_resmatch_mix_1mer.Scale(1./h_workflow.GetBinContent(2))
h_selectregions_resmatch_mix_1mer.SetStats(0)
h_selectregions_resmatch_mix_1mer.GetXaxis().SetBinLabel(1, "0")
h_selectregions_resmatch_mix_1mer.GetXaxis().SetBinLabel(2, "1")
h_selectregions_resmatch_mix_1mer.GetXaxis().SetBinLabel(3, "2")
h_selectregions_resmatch_mix_1mer.GetXaxis().SetBinLabel(4, ">2")
h_selectregions_resmatch_mix_1mer.GetYaxis().SetBinLabel(1, "0")
h_selectregions_resmatch_mix_1mer.GetYaxis().SetBinLabel(2, "1")
h_selectregions_resmatch_mix_1mer.GetYaxis().SetBinLabel(3, "2")
h_selectregions_resmatch_mix_1mer.GetYaxis().SetBinLabel(4, ">2")
h_selectregions_resmatch_mix_1mer.Write()

if h_selectregions_res_mixmatch_0mer.GetEntries()!=0 : h_selectregions_res_mixmatch_0mer.Scale(1./h_workflow.GetBinContent(2))
h_selectregions_res_mixmatch_0mer.SetStats(0)
h_selectregions_res_mixmatch_0mer.GetXaxis().SetBinLabel(1, "0")
h_selectregions_res_mixmatch_0mer.GetXaxis().SetBinLabel(2, "1")
h_selectregions_res_mixmatch_0mer.GetXaxis().SetBinLabel(3, "2")
h_selectregions_res_mixmatch_0mer.GetXaxis().SetBinLabel(4, ">2")
h_selectregions_res_mixmatch_0mer.GetYaxis().SetBinLabel(1, "0")
h_selectregions_res_mixmatch_0mer.GetYaxis().SetBinLabel(2, "1")
h_selectregions_res_mixmatch_0mer.GetYaxis().SetBinLabel(3, "2")
h_selectregions_res_mixmatch_0mer.GetYaxis().SetBinLabel(4, ">2")
h_selectregions_res_mixmatch_0mer.Write()

if h_selectregions_res_mixmatch_1mer.GetEntries()!=0 : h_selectregions_res_mixmatch_1mer.Scale(1./h_workflow.GetBinContent(2))
h_selectregions_res_mixmatch_1mer.SetStats(0)
h_selectregions_res_mixmatch_1mer.GetXaxis().SetBinLabel(1, "0")
h_selectregions_res_mixmatch_1mer.GetXaxis().SetBinLabel(2, "1")
h_selectregions_res_mixmatch_1mer.GetXaxis().SetBinLabel(3, "2")
h_selectregions_res_mixmatch_1mer.GetXaxis().SetBinLabel(4, ">2")
h_selectregions_res_mixmatch_1mer.GetYaxis().SetBinLabel(1, "0")
h_selectregions_res_mixmatch_1mer.GetYaxis().SetBinLabel(2, "1")
h_selectregions_res_mixmatch_1mer.GetYaxis().SetBinLabel(3, "2")
h_selectregions_res_mixmatch_1mer.GetYaxis().SetBinLabel(4, ">2")
h_selectregions_res_mixmatch_1mer.Write()

if h_selectregions_res_mix_1mermatch.GetEntries()!=0 : h_selectregions_res_mix_1mermatch.Scale(1./h_workflow.GetBinContent(2))
h_selectregions_res_mix_1mermatch.SetStats(0)
h_selectregions_res_mix_1mermatch.GetXaxis().SetBinLabel(1, "0")
h_selectregions_res_mix_1mermatch.GetXaxis().SetBinLabel(2, "1")
h_selectregions_res_mix_1mermatch.GetXaxis().SetBinLabel(3, "2")
h_selectregions_res_mix_1mermatch.GetXaxis().SetBinLabel(4, ">2")
h_selectregions_res_mix_1mermatch.GetYaxis().SetBinLabel(1, "0")
h_selectregions_res_mix_1mermatch.GetYaxis().SetBinLabel(2, "1")
h_selectregions_res_mix_1mermatch.GetYaxis().SetBinLabel(3, "2")
h_selectregions_res_mix_1mermatch.GetYaxis().SetBinLabel(4, ">2")
h_selectregions_res_mix_1mermatch.Write()


h_workflow.Write()
h_workflow_match.Write()
outfile.Close()
print("Output file: ", outfile)
