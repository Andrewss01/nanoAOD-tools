import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.tools import *
import numpy as np
from array import array
from collections import Counter
import itertools
import json
import os
from tqdm import tqdm


Top_Thr = {'Resolved': {'QCD': {'WPloose':0.7311983704566956,  'WPmedium':0.949266791343689, 'WPtight':0.9929128289222717}, 
                        'FT' : {'WPloose':0.8179053068161011, 'WPmedium':0.8997184038162231, 'WPtight':0.9483823776245117}, 
                        'TT' : {'WPloose':0.8011206388473511, 'WPmedium':0.8925945162773132, 'WPtight':0.9437039494514465}},
            'Mixed'  : {'QCD': {'WPloose':0.5236214399337769, 'WPmedium':0.9527022838592529, 'WPtight':0.9980961680412292},
                        'FT' : {'WPloose':0.8277362585067749,  'WPmedium':0.9405375123023987, 'WPtight':0.9811272025108337}, 
                        'TT' : {'WPloose':0.796029806137085 , 'WPmedium':0.9340529441833496, 'WPtight':0.9792388081550598}},
            'Merged':{'WPloose': 0.79, 'WPmedium': 0.8 , 'WPtight': 0.97}}

def check_same_top(topmixed1, topmixed2, resolved = False):
    '''
    Controlla se due top sono uguali, sono definiti uguali 
    se hanno almeno un jet o il fatjet in comune se sono mixed
    se sono resolved il fatjet non conta ma guarda solo i jet
    '''
 
    if not resolved: 
        idx_fj_1, idx_jet0_1, idx_jet1_1, idx_jet2_1 = topmixed1.idxFatJet, topmixed1.idxJet0, topmixed1.idxJet1, topmixed1.idxJet2
        idx_fj_2, idx_jet0_2, idx_jet1_2, idx_jet2_2 = topmixed2.idxFatJet, topmixed2.idxJet0, topmixed2.idxJet1, topmixed2.idxJet2
    else:
        idx_fj_1, idx_jet0_1, idx_jet1_1, idx_jet2_1 = -1, topmixed1.idxJet0, topmixed1.idxJet1, topmixed1.idxJet2
        idx_fj_2, idx_jet0_2, idx_jet1_2, idx_jet2_2 = -1, topmixed2.idxJet0, topmixed2.idxJet1, topmixed2.idxJet2
    list_1 = [idx_jet0_1, idx_jet1_1, idx_jet2_1]
    list_2 = [idx_jet0_2, idx_jet1_2, idx_jet2_2]

    intersection = list(set(list_1) & set(list_2))
    check_jets = len(intersection) >0
    check_fj = (idx_fj_1 == idx_fj_2) and (idx_fj_1 != -1 and idx_fj_2 != -1)
    return check_jets or check_fj



def selectTop(topmixed, resolved = False, year = 2022, score_type=None):
    ''''
    La prima cosa che fa è riordinare i top in base allo score in ordine crescente dopocihè li seleziona
    Il primo top della lista lo prende sempre, quindi il best score
    '''
    if len(topmixed) == 0:
        return []
    if year == 2018:
        topmixed_sorted = sorted(topmixed, key = lambda x: x.TTScore, reverse = True)
    elif year == 2022:
        if score_type == 'TT':
            topmixed_sorted = sorted(topmixed, key=lambda x: x.TTScore, reverse = True)
        elif score_type == 'QCD':
            topmixed_sorted = sorted(topmixed, key= lambda x: (x.TTScore/(x.TTScore + x.QCDScore)), reverse = True)
        elif score_type == 'FT':
            topmixed_sorted= sorted(topmixed, key = lambda x: (x.TTScore/(x.TTScore + x.FTScore)), reverse = True)

    topselected = []

    
    for i,top in enumerate(topmixed_sorted):
        if (i==0):
            
            topselected.append(top)
        else:
            same_top = False
            for bestTop in topselected:
                same_top = check_same_top(top,bestTop,resolved = resolved)
                if same_top: break
            if not same_top: 
                topselected.append(top)
    return topselected




def removeResolved(topmixed):
    '''
    Questa parte separa i top resolved che si trovano dentro i top mixed 
    '''

    if len(topmixed) == 0 :
        return []
    topselected = []

    for top in topmixed:
        if top.idxFatJet != -1:
            topselected.append(top)
    
    return topselected

def matchingTopResGenPart(genpart, top_res, jets):
    top_res_matched_q = []

    b  = None
    q  = None
    q_ = None
    sign_w = 0
    
    for part in genpart:
        #se non è prompt(non generata dai gluoni) e prima copia 
        if(part.genPartIdxMother_prompt>-1 and (part.statusFlags & (1<<12))): #la parte su statusFlag controlla se il 12esimo bit è 0 o 1 (1 << 12:Sposta il bit "1" di 12 posizioni verso sinistra & controlla bit a bit) il 12 slot indica se è la prima copia della particella
            #se è un quark non top e la madre è un w e la nonna è un top
            if(abs(part.pdgId)<6 and abs(genpart[part.genPartIdxMother_prompt].pdgId)==24 and abs(genpart[genpart[part.genPartIdxMother_prompt].genPartIdxMother_prompt].pdgId)==6):
                sign_w = genpart[part.genPartIdxMother_prompt].pdgId/24
                #assegna a q o q_ la particella selezionata (non importa quale a q o q_)
                if(q==None): q = part
                elif(q_==None): q_ = part
                else: continue
    for part in genpart:
        if(part.genPartIdxMother_prompt>-1 and (part.statusFlags & (1<<12))):
            if(part.pdgId ==5*sign_w and abs(genpart[part.genPartIdxMother_prompt].pdgId)==6):
                b = part  

    #print(top_res)
    for top in top_res:
        # print('idx_0: ',top.idxJet0)
        # print('len jets: ', len(jets))
        j0 = jets[top.idxJet0]
        j1 = jets[top.idxJet1]
        j2 = jets[top.idxJet2]
        top_jets = [j0, j1, j2]
        quarks = [b,q,q_]
        #se tutti i quark sono stati trovati
        if (b!=None and q!=None and q_!=None):
            for jets_comb in itertools.permutations(top_jets, len(quarks)):
                # Calcola le distanze per questa combinazione
                valid_combination = True
                for jet, quark in zip(jets_comb, quarks):
                    #questa cosa è fatta jet per jet e quark per quark, l'ordine dei quark rimane invariato, mentre quello dei 
                    # jet varia a ogni permutazione risultando in tutte le possibili combinazioni
                    #dr = deltaR(quark.eta, quark.phi, jet.eta, jet.phi) 
                    _, dr = closest(quark, [jet]) 
                    if dr >= 0.4:
                        valid_combination = False
                        break  # Se una distanza è maggiore della soglia, salta questa combinazione
        
                if valid_combination==True:                   
                    top_res_matched_q.append(top)
                    #break
                    #print(bjet,qjet,q_jet)

    return top_res_matched_q

def matchingTopMerGenPart(genpart, top_mer):
    top_mer_matched_q = []

    b  = None
    q  = None
    q_ = None
    sign_w = 0

    for part in genpart:
        #se non è prompt(non generata dai gluoni) e prima copia 
        if(part.genPartIdxMother_prompt>-1 and (part.statusFlags & (1<<12))): 
            #la parte su statusFlag controlla se il 12esimo bit è 0 o 1 (1 << 12:Sposta il bit "1" di 12 posizioni verso sinistra & controlla bit a bit) il 12 slot indica se è la prima copia della particella
            #se è un quark non top e la madre è un w e la nonna è un top
            if(abs(part.pdgId)<6 and abs(genpart[part.genPartIdxMother_prompt].pdgId)==24 and abs(genpart[genpart[part.genPartIdxMother_prompt].genPartIdxMother_prompt].pdgId)==6):
                sign_w = genpart[part.genPartIdxMother_prompt].pdgId/24
                #assegna a q o q_ la particella selezionata (non importa quale a q o q_)
                if(q==None): q = part
                elif(q_==None): q_ = part
                else: continue
    for part in genpart:
        if(part.genPartIdxMother_prompt>-1 and (part.statusFlags & (1<<12))):
            if(part.pdgId ==5*sign_w and abs(genpart[part.genPartIdxMother_prompt].pdgId)==6):
                b = part 

    for top in top_mer:
        #se tutti i quark sono stati trovati
        if (b!=None and q!=None and q_!=None): 
            #!!qui sto introducendo una gerarchia intrinseca tra quark
            drb    = deltaR(b.eta, b.phi, top.eta, top.phi)
            drq    = deltaR(q.eta, q.phi, top.eta, top.phi)
            drq_   = deltaR(q_.eta, q_.phi, top.eta, top.phi)
        else:
            drb, drq, drq_ = 1000, 1000, 1000
        #se la distanza tra ogni quark e il proprio jet è minore di 0.4 ritorna i 3 oggetti
        if(drb<0.8 and drq<0.8 and drq_<0.8):
            top_mer_matched_q.append(top)
            
            
            # top_mer_matched_q.append(top)  


    return top_mer_matched_q

def matchingRecoTopGenTop(gentop, recotop, dR,):
    # if len(gentop)==1:  top = gentop[0] # sempre vero per tt semilep

  
    top_reco_matched = []
    for top_r in recotop: 
        #prende i top adronici e controlla che abbiamo un DR < di un certo valore
        #Rispetto ai ricostruiti
        # Funziona solo per semilep
        dRGenTopRecoTop = deltaR(gentop[0].eta, gentop[0].phi, top_r.eta, top_r.phi) 
        if(dRGenTopRecoTop<dR): 
            top_reco_matched.append(top_r)

    return top_reco_matched


def thresholdTopScore(topreco, Top_threshold, top_type, year, score_type):
    topselected_loose = []
    topselected_medium = []
    topselected_tight = []
    if top_type == 'Resolved':
        attr_name = score_type + 'Score'
    elif top_type == 'Mixed':
        attr_name = score_type + 'Score'
    elif top_type == 'Merged':
        if year == 2018:
            attr_name = f"particleNet_TvsQCD"
        elif year == 2022:
            attr_name = f"particleNetWithMass_TvsQCD"
    
    for i, t in enumerate(topreco):
        if attr_name == 'FTScore':
            score_ft = getattr(t, attr_name) 
            score_tt = getattr(t, 'TTScore')
            score = score_tt/(score_tt + score_ft)
        elif attr_name == 'QCDScore':
            score_qcd = getattr(t,attr_name)
            score_tt = getattr(t, 'TTScore')
            score = score_tt/(score_tt + score_qcd)
        else:
            score = getattr(t, attr_name)
        if top_type != 'Merged':
            if score > float(Top_threshold[top_type][score_type]['WPloose']):
                topselected_loose.append(t)
            if score > float(Top_threshold[top_type][score_type]['WPmedium']):
                topselected_medium.append(t)
            if score > float(Top_threshold[top_type][score_type]['WPtight']):
                topselected_tight.append(t)
        else:
            if score > float(Top_threshold[top_type]['WPloose']):
                topselected_loose.append(t)
            if score > float(Top_threshold[top_type]['WPmedium']):
                topselected_medium.append(t)
            if score > float(Top_threshold[top_type]['WPtight']):
                topselected_tight.append(t)

    return topselected_loose, topselected_medium, topselected_tight 



year = 2022
score_type  ='FT'
if year == 2022:
    path = '/eos/user/a/apuglia/Master_Thesis/PostProcessed_Datasets/TT_semilep_2022/'
    chain = ROOT.TChain('Events')

    for fileName in tqdm(os.listdir(path)):
        if not (fileName.startswith('.')) :
            file = path + fileName + '/' + 'scores_model_cnn/' + fileName +'_cnn_model.root'
            chain.Add(file)

tree = InputTree(chain)
print('num events is: ', tree.GetEntries())

dir_path = '/eos/user/a/apuglia/Master_Thesis/TROTA_performances/' +score_type + 'Score/Histo_files'
if not os.path.exists(dir_path):
    os.makedirs(dir_path)

outfile  =ROOT.TFile(f"{dir_path}/output_TROTA_efficiency_Study_ttsemilep_noResInMix.root", "RECREATE")


h_GenTop_pt              = ROOT.TH1D("h_gentop_pt","; genTop pT", 20, 0, 1000)
h_GenTop_pt_exist_resolved              = ROOT.TH1D("h_gentop_pt_exist_resolved","; genTop pT", 20, 0, 1000)
h_GenTop_pt_exist_mixed              = ROOT.TH1D("h_gentop_pt_exist_mixed","; genTop pT", 20, 0, 1000)
h_GenTop_pt_exist_merged              = ROOT.TH1D("h_gentop_pt_exist_merged","; genTop pT", 20, 0, 1000)
h_GenTop_pt_Reconstructable_QuarkMatch_Resolved    = ROOT.TH1D("h_Top_pt_Reconstructable_QuarkMatch_Resolved","; genTop pT matched with top resolved with quark", 20, 0, 1000)
h_GenTop_pt_Reconstructable_QuarkMatch_Mixed       = ROOT.TH1D("h_Top_pt_Reconstructable_QuarkMatch_Mixed","; genTop pT matched with top mixed with quark", 20, 0, 1000)
h_GenTop_pt_Reconstructable_QuarkMatch_Merged      = ROOT.TH1D("h_Top_pt_Reconstructable_QuarkMatch_Merged","; genTop pT matched with top merged with quark", 20, 0, 1000)
h_GenTop_pt_Reconstructable_GenTopMatch02_Resolved    = ROOT.TH1D("h_Top_pt_Reconstructable_GenTopMatch02_Resolved","; genTop pT matched with top resolved with dr 0.2", 20, 0, 1000)
h_GenTop_pt_Reconstructable_GenTopMatch02_Mixed       = ROOT.TH1D("h_Top_pt_Reconstructable_GenTopMatch02_Mixed","; genTop pT matched with top mixed with dr 0.2", 20, 0, 1000)
h_GenTop_pt_Reconstructable_GenTopMatch02_Merged      = ROOT.TH1D("h_Top_pt_Reconstructable_GenTopMatch02_Merged","; genTop pT matched with top merged with dr 0.2", 20, 0, 1000)
h_GenTop_pt_Reconstructable_GenTopMatch04_Resolved    = ROOT.TH1D("h_Top_pt_Reconstructable_GenTopMatch04_Resolved","; genTop pT matched with top resolved with dr 0.4", 20, 0, 1000)
h_GenTop_pt_Reconstructable_GenTopMatch04_Mixed       = ROOT.TH1D("h_Top_pt_Reconstructable_GenTopMatch04_Mixed","; genTop pT matched with top mixed with dr 0.4", 20, 0, 1000)
h_GenTop_pt_Reconstructable_GenTopMatch04_Merged      = ROOT.TH1D("h_Top_pt_Reconstructable_GenTopMatch04_Merged","; genTop pT matched with top merged with dr 0.4", 20, 0, 1000)
h_GenTop_pt_Selection_QuarkMatch_Resolved    = ROOT.TH1D("h_Top_pt_Selection_QuarkMatch_Resolved","; genTop pT matched with top resolved with quark", 20, 0, 1000)
h_GenTop_pt_Selection_QuarkMatch_Mixed       = ROOT.TH1D("h_Top_pt_Selection_QuarkMatch_Mixed","; genTop pT matched with top mixed with quark", 20, 0, 1000)
h_GenTop_pt_Selection_QuarkMatch_Merged      = ROOT.TH1D("h_Top_pt_Selection_QuarkMatch_Merged","; genTop pT matched with top merged with quark", 20, 0, 1000)
h_GenTop_pt_Selection_GenTopMatch02_Resolved    = ROOT.TH1D("h_Top_pt_Selection_GenTopMatch02_Resolved","; genTop pT matched with top resolved with dr 0.2", 20, 0, 1000)
h_GenTop_pt_Selection_GenTopMatch02_Mixed       = ROOT.TH1D("h_Top_pt_Selection_GenTopMatch02_Mixed","; genTop pT matched with top mixed with dr 0.2", 20, 0, 1000)
h_GenTop_pt_Selection_GenTopMatch02_Merged      = ROOT.TH1D("h_Top_pt_Selection_GenTopMatch02_Merged","; genTop pT matched with top merged with dr 0.2", 20, 0, 1000)
h_GenTop_pt_Selection_GenTopMatch04_Resolved    = ROOT.TH1D("h_Top_pt_Selection_GenTopMatch04_Resolved","; genTop pT matched with top resolved with dr 0.4", 20, 0, 1000)
h_GenTop_pt_Selection_GenTopMatch04_Mixed       = ROOT.TH1D("h_Top_pt_Selection_GenTopMatch04_Mixed","; genTop pT matched with top mixed with dr 0.4", 20, 0, 1000)
h_GenTop_pt_Selection_GenTopMatch04_Merged      = ROOT.TH1D("h_Top_pt_Selection_GenTopMatch04_Merged","; genTop pT matched with top merged with dr 0.4", 20, 0, 1000)
h_GenTop_pt_RealLife_QuarkMatch_Resolved    = ROOT.TH1D("h_Top_pt_RealLife_QuarkMatch_Resolved","; genTop pT matched with top resolved with quark", 20, 0, 1000)
h_GenTop_pt_RealLife_QuarkMatch_Mixed       = ROOT.TH1D("h_Top_pt_RealLife_QuarkMatch_Mixed","; genTop pT matched with top mixed with quark", 20, 0, 1000)
h_GenTop_pt_RealLife_QuarkMatch_Merged      = ROOT.TH1D("h_Top_pt_RealLife_QuarkMatch_Merged","; genTop pT matched with top merged with quark", 20, 0, 1000)
h_GenTop_pt_RealLife_OldMatch_Resolved    = ROOT.TH1D("h_Top_pt_RealLife_OldMatch_Resolved","; genTop pT matched with top resolved with quark", 20, 0, 1000)
h_GenTop_pt_RealLife_OldMatch_Mixed       = ROOT.TH1D("h_Top_pt_RealLife_OldMatch_Mixed","; genTop pT matched with top mixed with quark", 20, 0, 1000)
h_GenTop_pt_RealLife_OldMatch_Merged      = ROOT.TH1D("h_Top_pt_RealLife_OldMatch_Merged","; genTop pT matched with top merged with quark", 20, 0, 1000)
h_GenTop_pt_RealLife_GenTopMatch02_Resolved    = ROOT.TH1D("h_Top_pt_RealLife_GenTopMatch02_Resolved","; genTop pT matched with top resolved with dr 0.2", 20, 0, 1000)
h_GenTop_pt_RealLife_GenTopMatch02_Mixed       = ROOT.TH1D("h_Top_pt_RealLife_GenTopMatch02_Mixed","; genTop pT matched with top mixed with dr 0.2", 20, 0, 1000)
h_GenTop_pt_RealLife_GenTopMatch02_Merged      = ROOT.TH1D("h_Top_pt_RealLife_GenTopMatch02_Merged","; genTop pT matched with top merged with dr 0.2", 20, 0, 1000)
h_GenTop_pt_RealLife_GenTopMatch04_Resolved    = ROOT.TH1D("h_Top_pt_RealLife_GenTopMatch04_Resolved","; genTop pT matched with top resolved with dr 0.4", 20, 0, 1000)
h_GenTop_pt_RealLife_GenTopMatch04_Mixed       = ROOT.TH1D("h_Top_pt_RealLife_GenTopMatch04_Mixed","; genTop pT matched with top mixed with dr 0.4", 20, 0, 1000)
h_GenTop_pt_RealLife_GenTopMatch04_Merged      = ROOT.TH1D("h_Top_pt_RealLife_GenTopMatch04_Merged","; genTop pT matched with top merged with dr 0.4", 20, 0, 1000)
h_GenTop_pt_TagMediumWP_QuarkMatch_Resolved    = ROOT.TH1D("h_Top_pt_TagMediumWP_QuarkMatch_Resolved","; genTop pT matched with top resolved with quark", 20, 0, 1000)
h_GenTop_pt_TagMediumWP_QuarkMatch_Mixed       = ROOT.TH1D("h_Top_pt_TagMediumWP_QuarkMatch_Mixed","; genTop pT matched with top mixed with quark", 20, 0, 1000)
h_GenTop_pt_TagMediumWP_QuarkMatch_Merged      = ROOT.TH1D("h_Top_pt_TagMediumWP_QuarkMatch_Merged","; genTop pT matched with top merged with quark", 20, 0, 1000)
h_GenTop_pt_TagMediumWP_GenTopMatch02_Resolved    = ROOT.TH1D("h_Top_pt_TagMediumWP_GenTopMatch02_Resolved","; genTop pT matched with top resolved with dr 0.2", 20, 0, 1000)
h_GenTop_pt_TagMediumWP_GenTopMatch02_Mixed       = ROOT.TH1D("h_Top_pt_TagMediumWP_GenTopMatch02_Mixed","; genTop pT matched with top mixed with dr 0.2", 20, 0, 1000)
h_GenTop_pt_TagMediumWP_GenTopMatch02_Merged      = ROOT.TH1D("h_Top_pt_TagMediumWP_GenTopMatch02_Merged","; genTop pT matched with top merged with dr 0.2", 20, 0, 1000)
h_GenTop_pt_TagMediumWP_GenTopMatch04_Resolved    = ROOT.TH1D("h_Top_pt_TagMediumWP_GenTopMatch04_Resolved","; genTop pT matched with top resolved with dr 0.4", 20, 0, 1000)
h_GenTop_pt_TagMediumWP_GenTopMatch04_Mixed       = ROOT.TH1D("h_Top_pt_TagMediumWP_GenTopMatch04_Mixed","; genTop pT matched with top mixed with dr 0.4", 20, 0, 1000)
h_GenTop_pt_TagMediumWP_GenTopMatch04_Merged      = ROOT.TH1D("h_Top_pt_TagMediumWP_GenTopMatch04_Merged","; genTop pT matched with top merged with dr 0.4", 20, 0, 1000)
h_GenTop_pt_TagTightWP_QuarkMatch_Resolved    = ROOT.TH1D("h_Top_pt_TagTightWP_QuarkMatch_Resolved","; genTop pT matched with top resolved with quark", 20, 0, 1000)
h_GenTop_pt_TagTightWP_QuarkMatch_Mixed       = ROOT.TH1D("h_Top_pt_TagTightWP_QuarkMatch_Mixed","; genTop pT matched with top mixed with quark", 20, 0, 1000)
h_GenTop_pt_TagTightWP_QuarkMatch_Merged      = ROOT.TH1D("h_Top_pt_TagTightWP_QuarkMatch_Merged","; genTop pT matched with top merged with quark", 20, 0, 1000)
h_GenTop_pt_TagTightWP_GenTopMatch02_Resolved    = ROOT.TH1D("h_Top_pt_TagTightWP_GenTopMatch02_Resolved","; genTop pT matched with top resolved with dr 0.2", 20, 0, 1000)
h_GenTop_pt_TagTightWP_GenTopMatch02_Mixed       = ROOT.TH1D("h_Top_pt_TagTightWP_GenTopMatch02_Mixed","; genTop pT matched with top mixed with dr 0.2", 20, 0, 1000)
h_GenTop_pt_TagTightWP_GenTopMatch02_Merged      = ROOT.TH1D("h_Top_pt_TagTightWP_GenTopMatch02_Merged","; genTop pT matched with top merged with dr 0.2", 20, 0, 1000)
h_GenTop_pt_TagTightWP_GenTopMatch04_Resolved    = ROOT.TH1D("h_Top_pt_TagTightWP_GenTopMatch04_Resolved","; genTop pT matched with top resolved with dr 0.4", 20, 0, 1000)
h_GenTop_pt_TagTightWP_GenTopMatch04_Mixed       = ROOT.TH1D("h_Top_pt_TagTightWP_GenTopMatch04_Mixed","; genTop pT matched with top mixed with dr 0.4", 20, 0, 1000)
h_GenTop_pt_TagTightWP_GenTopMatch04_Merged      = ROOT.TH1D("h_Top_pt_TagTightWP_GenTopMatch04_Merged","; genTop pT matched with top merged with dr 0.4", 20, 0, 1000)
h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Resolved    = ROOT.TH2D("h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Resolved","; num candidates vs genTop pT matched with top resolved with quark", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Mixed       = ROOT.TH2D("h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Mixed","; num candidates vs genTop pT matched with top mixed with quark", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Merged      = ROOT.TH2D("h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Merged","; num candidates vs genTop pT matched with top merged with quark", 20, 0, 1000, 10, 0, 10)
h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Resolved    = ROOT.TH2D("h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Resolved","; num candidates vs num candidates vs genTop pT matched with top resolved with dr 0.2", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Mixed       = ROOT.TH2D("h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Mixed","; num candidates vs genTop pT matched with top mixed with dr 0.2", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Merged      = ROOT.TH2D("h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Merged","; num candidates vs genTop pT matched with top merged with dr 0.2", 20, 0, 1000, 10, 0, 10)
h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Resolved    = ROOT.TH2D("h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Resolved","; num candidates vs genTop pT matched with top resolved with dr 0.4", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Mixed       = ROOT.TH2D("h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Mixed","; num candidates vs genTop pT matched with top mixed with dr 0.4", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Merged      = ROOT.TH2D("h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Merged","; num candidates vs genTop pT matched with top merged with dr 0.4", 20, 0, 1000, 10, 0, 10)
h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Resolved    = ROOT.TH2D("h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Resolved","; num candidates vs genTop pT matched with top resolved with quark", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Mixed       = ROOT.TH2D("h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Mixed","; num candidates vs genTop pT matched with top mixed with quark", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Merged      = ROOT.TH2D("h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Merged","; num candidates vs genTop pT matched with top merged with quark", 20, 0, 1000, 10, 0, 10)
h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Resolved    = ROOT.TH2D("h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Resolved","; num candidates vs genTop pT matched with top resolved with dr 0.2", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Mixed       = ROOT.TH2D("h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Mixed","; num candidates vs genTop pT matched with top mixed with dr 0.2", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Merged      = ROOT.TH2D("h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Merged","; num candidates vs genTop pT matched with top merged with dr 0.2", 20, 0, 1000, 10, 0, 10)
h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Resolved    = ROOT.TH2D("h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Resolved","; num candidates vs genTop pT matched with top resolved with dr 0.4", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Mixed       = ROOT.TH2D("h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Mixed","; num candidates vs genTop pT matched with top mixed with dr 0.4", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Merged      = ROOT.TH2D("h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Merged","; num candidates vs genTop pT matched with top merged with dr 0.4", 20, 0, 1000, 10, 0, 10)
h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Resolved    = ROOT.TH2D("h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Resolved","; num candidates vs genTop pT matched with top resolved with quark", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Mixed       = ROOT.TH2D("h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Mixed","; num candidates vs genTop pT matched with top mixed with quark", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Merged      = ROOT.TH2D("h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Merged","; num candidates vs genTop pT matched with top merged with quark", 20, 0, 1000, 10, 0, 10)
h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Resolved    = ROOT.TH2D("h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Resolved","; num candidates vs num candidates vs genTop pT matched with top resolved with dr 0.2", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Mixed       = ROOT.TH2D("h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Mixed","; num candidates vs genTop pT matched with top mixed with dr 0.2", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Merged      = ROOT.TH2D("h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Merged","; num candidates vs genTop pT matched with top merged with dr 0.2", 20, 0, 1000, 10, 0, 10)
h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Resolved    = ROOT.TH2D("h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Resolved","; num candidates vs genTop pT matched with top resolved with dr 0.4", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Mixed       = ROOT.TH2D("h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Mixed","; num candidates vs genTop pT matched with top mixed with dr 0.4", 20, 0, 1000, 10, 0, 100)
h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Merged      = ROOT.TH2D("h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Merged","; num candidates vs genTop pT matched with top merged with dr 0.4", 20, 0, 1000, 10, 0, 10)

h2_DeltaR_BestTop_GenTop_pt_Resolved       = ROOT.TH2D("h2_DeltaR_BestTop_GenTop_pt_Resolved","DeltaR besttop-gentop vs genTop pT for top resolved", 20, 0, 1000, 100, 0, 10)
h2_DeltaR_BestTop_GenTop_pt_Mixed       = ROOT.TH2D("h2_DeltaR_BestTop_GenTop_pt_Mixed","DeltaR besttop-gentop vs genTop pT for top mixed", 20, 0, 1000, 100, 0, 10)
h2_DeltaR_BestTop_GenTop_pt_Merged       = ROOT.TH2D("h2_DeltaR_BestTop_GenTop_pt_Merged","DeltaR besttop-gentop vs genTop pT for top merged", 20, 0, 1000, 100, 0, 10)


nEvRecoTopGenQuarktMatched = 0
nEvRecoTopGenTop02Matched = 0
nEvRecoTopGenTop04Matched = 0
nEvBestRecoTopGenQuarktMatched = 0
nEvBestRecoTopGenTop02Matched = 0
nEvBestRecoTopGenTop04Matched = 0

for i in tqdm(range(tree.GetEntries())):
    event = Event(tree,i)
    genpart = Collection(event, "GenPart")
    if year == 2018:
        topgen = Collection(event, "TopGenTopPart", lenVar = "nTopGenHadr")
    elif year == 2022:
        is_hadronic_top = np.zeros(len(genpart), dtype=int)
        hadronic_top_idx =[]
        quark_flavs = [int(1),int(2),int(3),int(4)]
        for particle in genpart:
            #print("la particella analizzata è", particle.pdgId, "con indice della madre:", particle.genPartIdxMother, "ed è:", genpart[0].pdgId)
            mom_id = particle.genPartIdxMother
            #se è un quark nella catena del top
            if abs(int(particle.pdgId)) in quark_flavs and mom_id!=-1: 
                #Print("è un quark")
                #se non è la propagazione di sè stessa
                if int(genpart[mom_id].pdgId) != int(particle.pdgId):
                    mom = genpart[mom_id] 
                    grandmom_id = mom.genPartIdxMother
                    #Print("non è propagato e la madre è:",mom.pdgId)
                    #se la madre è un w
                    if abs(int(mom.pdgId))==24 and grandmom_id!=-1:
                        #Print("la madre è un w prodotto di decadimento")
                        grandmom = genpart[grandmom_id]
                        #Print("la nonna è:",grandmom.pdgId)
                        #se non è la propagazione di sè stessa
                        if int(grandmom.pdgId) != int(mom.pdgId):
                            #se la madre della w è un top
                            #print("non è propagato")
                            if abs(grandmom.pdgId) == 6:
                                #Print("la nonna è un top")
                                top = grandmom
                                top_id = grandmom_id
                                top_mom_id = top.genPartIdxMother
                                top_mom = genpart[top.genPartIdxMother]
                                #metti 1 nella posizione corrispondete al top
                                if genpart[top_id].pdgId!=6 and genpart[top_id].pdgId!=-6:
                                            print("1) il top è", top.pdgId, "e la madre del top è:",top_mom.pdgId)
                                is_hadronic_top[top_id]=int(1)
                                hadronic_top_idx.append(top_id)
                                #Print("salvato indice:",is_hadronic_top)
                                #fai lo stesso per i top da cui è stato propagato
                                while top_mom.pdgId==top.pdgId:
                                    #print("1:",genpart[top_id].pdgId,genpart[top_mom_id].pdgId)
                                    if genpart[top_id].pdgId!=6 and genpart[top_id].pdgId!=-6:
                                            print("2.0) il top è", top.pdgId, "e la madre del top è:",top_mom.pdgId)
                                    top=top_mom
                                    top_id = top_mom_id
                                    top_mom_id = top_mom.genPartIdxMother
                                    top_mom=genpart[top_mom.genPartIdxMother]
                                    #print("2:",genpart[top_id].pdgId)
                                    if genpart[top_id].pdgId!=6 and genpart[top_id].pdgId!=-6:
                                            print("2) il top è", top.pdgId, "e la madre del top è:",top_mom.pdgId)
                                    is_hadronic_top[top_id]=int(1)
                                    hadronic_top_idx.append(top_id)
                                    #Print("salvato indice:",is_hadronic_top)

                        else:
                           #print("è propagato")
                           while (grandmom.pdgId==mom.pdgId): 
                                mom=grandmom
                                mom_id = grandmom_id
                                grandmom= genpart[mom.genPartIdxMother]  
                                grandmom_id = mom.genPartIdxMother
                                #Print("la nuova nonna è:",grandmom.pdgId)
                                #se la madre della w è un top
                                if abs(grandmom.pdgId) == 6:
                                    top = grandmom
                                    top_id = grandmom_id
                                    top_mom_id = top.genPartIdxMother
                                    top_mom = genpart[top.genPartIdxMother]
                                    #print("la nonna era ", top.pdgId, "e la madre del top è:",top_mom.pdgId)
                                    #metti 1 nella posizione corrispondete al top
                                    if genpart[top_id].pdgId!=6 and genpart[top_id].pdgId!=-6:
                                            print("3) il top è", top.pdgId, "e la madre del top è:",top_mom.pdgId)
                                    is_hadronic_top[top_id]=int(1)
                                    hadronic_top_idx.append(top_id)
                                    #Print("salvato indice:",is_hadronic_top)
                                    #fai lo stesso per i top da cui è stato propagato
                                    while top_mom.pdgId==top.pdgId:
                                        top=top_mom
                                        top_id = top_mom_id
                                        top_mom_id = top_mom.genPartIdxMother
                                        top_mom=genpart[top_mom.genPartIdxMother]
                                        if genpart[top_id].pdgId!=6 and genpart[top_id].pdgId!=-6:
                                            print("4) il top è", top.pdgId, "e la madre del top è:",top_mom.pdgId)
                                        is_hadronic_top[top_id]=int(1)
                                        hadronic_top_idx.append(top_id)
                                        #Print("salvato indice:",is_hadronic_top
        topgen = [particle for particle, is_hadr_top in zip(genpart, is_hadronic_top) if is_hadr_top==1]
    # topgen = [genpart[i] for i in hadronic_top_idx]
    # if len(topgen) != 2:
    #     print("numero di top hadronici trovati:", len(topgen))
    #     print("top hadronici trovati:", [top.pdgId for top in topgen])
    #     print("hadronic top idx:", hadronic_top_idx)
    #     print("i top sono:", [genpart[idx].pdgId for idx in hadronic_top_idx])
    #     for i,part in enumerate(genpart):
    #         print(i,"part pdgId:", part.pdgId, "e idx madre:", part.genPartIdxMother)
    if year == 2022:
        for top in topgen:
            if top.pdgId != 6 and top.pdgId != -6:
                print("top hadronico trovato con pdgId:", top.pdgId, "e pt:", top.pt)
    jets = Collection(event, "Jet")
    nTopGenHadr = len(topgen)
    
    #Tutti i topreco
    topresolved = Collection(event, "TopResolved")
    topmixed = Collection(event, "TopMixed")
    topmerged = Collection(event, "FatJet")
    topMixedNoRes = removeResolved(topmixed)

    #### fill del pt dei top hadronic (pre emissione soft) posso farlo perchè ce n'è uno solo per evento#####
    h_GenTop_pt.Fill(topgen[0].pt)

    ####HISTO PT PER EFFICIENZA "RICOSTRUIBILI" ALMENO UN TOP RICOSTRUITO MATCHATO#####
    #quark match
    #lista dei top matchati secondo il criterio dei quark
    topResolvedQuarkMatch = matchingTopResGenPart(genpart, topresolved, jets)
    topMixedQuarkMatch = list(filter(lambda x : x.truth==1, topMixedNoRes)) #qui uso la truth per "almeno un quark matchato"
    topMergedQuarkMatch = matchingTopMerGenPart(genpart, topmerged)
    if len(topResolvedQuarkMatch) != 0:
        h_GenTop_pt_Reconstructable_QuarkMatch_Resolved.Fill(topgen[0].pt)
        h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Resolved.Fill(topgen[0].pt, len(topresolved))
        #h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Resolved.Fill(topgen[0].pt, len(topResolvedQuarkMatch))
        nEvRecoTopGenQuarktMatched += 1
    if len(topMixedQuarkMatch) != 0:
        h_GenTop_pt_Reconstructable_QuarkMatch_Mixed.Fill(topgen[0].pt)
        h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Mixed.Fill(topgen[0].pt, len(topmixed))
        #h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Mixed.Fill(topgen[0].pt, len(topMixedQuarkMatch))

    if len(topMergedQuarkMatch) != 0:
        h_GenTop_pt_Reconstructable_QuarkMatch_Merged.Fill(topgen[0].pt)
        h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Merged.Fill(topgen[0].pt, len(topmerged))
        #h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Merged.Fill(topgen[0].pt, len(topMergedQuarkMatch))
    
    topResolvedGenTopMatch_04 = matchingRecoTopGenTop(topgen, topresolved, 0.4)
    topMixedGenTopMatch_04 = matchingRecoTopGenTop(topgen, topMixedNoRes, 0.4)
    topMergedGenTopMatch_04 = matchingRecoTopGenTop(topgen, topmerged, 0.4)
    if len(topResolvedGenTopMatch_04) != 0:
        h_GenTop_pt_Reconstructable_GenTopMatch04_Resolved.Fill(topgen[0].pt)
        h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Resolved.Fill(topgen[0].pt, len(topresolved))
        nEvRecoTopGenTop04Matched += 1
    if len(topMixedGenTopMatch_04) != 0:
        h_GenTop_pt_Reconstructable_GenTopMatch04_Mixed.Fill(topgen[0].pt)
        h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Mixed.Fill(topgen[0].pt, len(topmixed))
    if len(topMergedGenTopMatch_04) != 0:
        h_GenTop_pt_Reconstructable_GenTopMatch04_Merged.Fill(topgen[0].pt)
        h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Merged.Fill(topgen[0].pt, len(topmerged))
    #gentop match dr=0.2
    topResolvedGenTopMatch_02 = matchingRecoTopGenTop(topgen, topresolved, 0.2)
    topMixedGenTopMatch_02 = matchingRecoTopGenTop(topgen, topMixedNoRes, 0.2)
    topMergedGenTopMatch_02 = matchingRecoTopGenTop(topgen, topmerged, 0.2)
    if len(topResolvedGenTopMatch_02) != 0:
        h_GenTop_pt_Reconstructable_GenTopMatch02_Resolved.Fill(topgen[0].pt)
        h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Resolved.Fill(topgen[0].pt, len(topresolved))
        nEvRecoTopGenTop02Matched += 1
    if len(topMixedGenTopMatch_02) != 0:
        h_GenTop_pt_Reconstructable_GenTopMatch02_Mixed.Fill(topgen[0].pt)
        h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Mixed.Fill(topgen[0].pt, len(topmixed))
    if len(topMergedGenTopMatch_02) != 0:
        h_GenTop_pt_Reconstructable_GenTopMatch02_Merged.Fill(topgen[0].pt)
        h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Merged.Fill(topgen[0].pt, len(topmerged))

    ####HISTO PT PER EFFICIENZA "DI SELEZIONE" E "REAL LIFE" IL MIGLIOR CANDIDATO TROTA è MATCHATO  #####
    #Lista dei topmixed non sovrapposti ordinati per score
    topResolvedSelect = selectTop(topresolved, resolved = True, year=2022, score_type  =score_type)
    #print("topResolvedSelect",isinstance(topResolvedSelect,list), topResolvedSelect[0].pt)
    #Lista dei topmixed senza resolved non sovrapposti ordinati per score
    topMixedSelect = selectTop(topMixedNoRes, resolved = False, year=2022, score_type= score_type)
    #lista dei topmerged ordinati per score
    if year == 2018:
        topMergedSelect = sorted(topmerged, key=lambda x: x.particleNet_TvsQCD, reverse=True)
    elif year == 2022:
        topMergedSelect = sorted(topmerged, key=lambda x: x.particleNetWithMass_TvsQCD, reverse=True)
    #Esiste almeno un candidato TROTA
    if len(topResolvedSelect) != 0:
        h_GenTop_pt_exist_resolved.Fill(topgen[0].pt)
    if len(topMixedSelect) != 0:
        h_GenTop_pt_exist_mixed.Fill(topgen[0].pt)
    if len(topMergedSelect) != 0:
        h_GenTop_pt_exist_merged.Fill(topgen[0].pt)
    
    
    if len(topResolvedSelect)!=0:
        h2_DeltaR_BestTop_GenTop_pt_Resolved.Fill(topgen[0].pt, deltaR(topResolvedSelect[0], topgen[0]))
        #Il miglior candidato TROTA è matchato con i quark
        if len(matchingTopResGenPart(genpart, [topResolvedSelect[0]], jets))!=0:
            h_GenTop_pt_Selection_QuarkMatch_Resolved.Fill(topgen[0].pt)
            h_GenTop_pt_RealLife_QuarkMatch_Resolved.Fill(topgen[0].pt)
            h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Resolved.Fill(topgen[0].pt, len(topresolved))
            #h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Resolved.Fill(topgen[0].pt, len(topResolvedSelect))

            nEvBestRecoTopGenQuarktMatched += 1
            top_resolved_selected_loose_QuarkMatch, top_resolved_selected_medium_QuarkMatch, top_resolved_selected_tight_QuarkMatch = thresholdTopScore([topResolvedSelect[0]], Top_Thr, 'Resolved', year, score_type)
            if len(top_resolved_selected_medium_QuarkMatch) != 0:
                h_GenTop_pt_TagMediumWP_QuarkMatch_Resolved.Fill(topgen[0].pt)
            if len(top_resolved_selected_tight_QuarkMatch) != 0:
                h_GenTop_pt_TagTightWP_QuarkMatch_Resolved.Fill(topgen[0].pt)
        else:
            h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Resolved.Fill(topgen[0].pt, len(topresolved))
        #Il miglior candidato TROTA è matchato con un topgen con dr = 0.4
        if len(matchingRecoTopGenTop(topgen, [topResolvedSelect[0]], 0.4))!=0:
            h_GenTop_pt_Selection_GenTopMatch04_Resolved.Fill(topgen[0].pt)
            h_GenTop_pt_RealLife_GenTopMatch04_Resolved.Fill(topgen[0].pt)
            h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Resolved.Fill(topgen[0].pt, len(topresolved))
            nEvBestRecoTopGenTop04Matched += 1
            top_resolved_selected_loose_GenTopMatch04_Resolved, top_resolved_selected_medium_GenTopMatch04_Resolved, top_resolved_selected_tight_GenTopMatch04_Resolved = thresholdTopScore([topResolvedSelect[0]], Top_Thr, 'Resolved', year, score_type)  
            if len(top_resolved_selected_medium_GenTopMatch04_Resolved) != 0:
                h_GenTop_pt_TagMediumWP_GenTopMatch04_Resolved.Fill(topgen[0].pt)
            if len(top_resolved_selected_tight_GenTopMatch04_Resolved) != 0:
                h_GenTop_pt_TagTightWP_GenTopMatch04_Resolved.Fill(topgen[0].pt)
        else:
            h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Resolved.Fill(topgen[0].pt, len(topresolved))
        #Il miglior candidato TROTA è matchato con un topgen con dr = 0.2
        if len(matchingRecoTopGenTop(topgen, [topResolvedSelect[0]], 0.2))!=0:
            h_GenTop_pt_Selection_GenTopMatch02_Resolved.Fill(topgen[0].pt)
            h_GenTop_pt_RealLife_GenTopMatch02_Resolved.Fill(topgen[0].pt)
            h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Resolved.Fill(topgen[0].pt, len(topresolved))
            nEvBestRecoTopGenTop02Matched += 1
            top_resolved_selected_loose_GenTopMatch02_Resolved, top_resolved_selected_medium_GenTopMatch02_Resolved, top_resolved_selected_tight_GenTopMatch02_Resolved = thresholdTopScore([topResolvedSelect[0]], Top_Thr, 'Resolved', year, score_type)
            if len(top_resolved_selected_medium_GenTopMatch02_Resolved) != 0:
                h_GenTop_pt_TagMediumWP_GenTopMatch02_Resolved.Fill(topgen[0].pt)
            if len(top_resolved_selected_tight_GenTopMatch02_Resolved) != 0:
                h_GenTop_pt_TagTightWP_GenTopMatch02_Resolved.Fill(topgen[0].pt)
            
        else:
            h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Resolved.Fill(topgen[0].pt, len(topresolved))


    if len(topMixedSelect) != 0:
        h2_DeltaR_BestTop_GenTop_pt_Mixed.Fill(topgen[0].pt, deltaR(topMixedSelect[0], topgen[0]))
        #Il miglior candidato TROTA è matchato con quark
        if topMixedSelect[0].truth == 1:
            h_GenTop_pt_Selection_QuarkMatch_Mixed.Fill(topgen[0].pt)
            h_GenTop_pt_RealLife_QuarkMatch_Mixed.Fill(topgen[0].pt)
            h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Mixed.Fill(topgen[0].pt, len(topmixed))
            #h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Mixed.Fill(topgen[0].pt, len(topMixedSelect))
            top_mixed_selected_loose_QuarkMatch, top_mixed_selected_medium_QuarkMatch, top_mixed_selected_tight_QuarkMatch = thresholdTopScore([topMixedSelect[0]], Top_Thr, 'Mixed', year, score_type)
            if len(top_mixed_selected_medium_QuarkMatch) != 0:
                h_GenTop_pt_TagMediumWP_QuarkMatch_Mixed.Fill(topgen[0].pt)
            if len(top_mixed_selected_tight_QuarkMatch) != 0:
                h_GenTop_pt_TagTightWP_QuarkMatch_Mixed.Fill(topgen[0].pt)
        else:
            h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Mixed.Fill(topgen[0].pt, len(topmixed))
        #Il miglior candidato TROTA è matchato con un topgen con dr = 0.4
        if len(matchingRecoTopGenTop(topgen, [topMixedSelect[0]], 0.4))!=0:
            h_GenTop_pt_Selection_GenTopMatch04_Mixed.Fill(topgen[0].pt)
            h_GenTop_pt_RealLife_GenTopMatch04_Mixed.Fill(topgen[0].pt)
            h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Mixed.Fill(topgen[0].pt, len(topmixed))
            top_mixed_selected_loose_GenTopMatch04_Mixed, top_mixed_selected_medium_GenTopMatch04_Mixed, top_mixed_selected_tight_GenTopMatch04_Mixed = thresholdTopScore([topMixedSelect[0]], Top_Thr, 'Mixed', year, score_type )
            if len(top_mixed_selected_medium_GenTopMatch04_Mixed) != 0:
                h_GenTop_pt_TagMediumWP_GenTopMatch04_Mixed.Fill(topgen[0].pt)
            if len(top_mixed_selected_tight_GenTopMatch04_Mixed) != 0:
                h_GenTop_pt_TagTightWP_GenTopMatch04_Mixed.Fill(topgen[0].pt)
        else:
            h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Mixed.Fill(topgen[0].pt, len(topmixed))
        #Il miglior candidato TROTA è matchato con un topgen con dr = 0.2
        if len(matchingRecoTopGenTop(topgen, [topMixedSelect[0]], 0.2))!=0:
            h_GenTop_pt_Selection_GenTopMatch02_Mixed.Fill(topgen[0].pt)
            h_GenTop_pt_RealLife_GenTopMatch02_Mixed.Fill(topgen[0].pt)
            h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Mixed.Fill(topgen[0].pt, len(topmixed))
            top_mixed_selected_loose_GenTopMatch02_Mixed, top_mixed_selected_medium_GenTopMatch02_Mixed, top_mixed_selected_tight_GenTopMatch02_Mixed = thresholdTopScore([topMixedSelect[0]], Top_Thr, 'Mixed', year, score_type )
            if len(top_mixed_selected_medium_GenTopMatch02_Mixed) != 0:
                h_GenTop_pt_TagMediumWP_GenTopMatch02_Mixed.Fill(topgen[0].pt)
            if len(top_mixed_selected_tight_GenTopMatch02_Mixed) != 0:
                h_GenTop_pt_TagTightWP_GenTopMatch02_Mixed.Fill(topgen[0].pt)
        else:
            h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Mixed.Fill(topgen[0].pt, len(topmixed))
    if len(topMergedSelect) != 0:
        h2_DeltaR_BestTop_GenTop_pt_Merged.Fill(topgen[0].pt, deltaR(topMergedSelect[0], topgen[0]))
        #Il miglior candidato TROTA è matchato con quark
        if len(matchingTopMerGenPart(genpart, [topMergedSelect[0]]))!=0:
            h_GenTop_pt_Selection_QuarkMatch_Merged.Fill(topgen[0].pt)
            h_GenTop_pt_RealLife_QuarkMatch_Merged.Fill(topgen[0].pt)
            h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Merged.Fill(topgen[0].pt, len(topmerged))
            #h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Merged.Fill(topgen[0].pt, len(topMergedSelect))
            top_merged_selected_loose_QuarkMatch, top_merged_selected_medium_QuarkMatch, top_merged_selected_tight_QuarkMatch = thresholdTopScore([topMergedSelect[0]], Top_Thr, 'Merged', year, score_type)
            if len(top_merged_selected_medium_QuarkMatch) != 0:
                h_GenTop_pt_TagMediumWP_QuarkMatch_Merged.Fill(topgen[0].pt)
            if len(top_merged_selected_tight_QuarkMatch) != 0:
                h_GenTop_pt_TagTightWP_QuarkMatch_Merged.Fill(topgen[0].pt)
        else:
            h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Merged.Fill(topgen[0].pt, len(topmerged))
        #Il miglior candidato TROTA è matchato con un topgen con dr = 0.4
        if len(matchingRecoTopGenTop(topgen, [topMergedSelect[0]], 0.4))!=0:
            h_GenTop_pt_Selection_GenTopMatch04_Merged.Fill(topgen[0].pt)
            h_GenTop_pt_RealLife_GenTopMatch04_Merged.Fill(topgen[0].pt)
            h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Merged.Fill(topgen[0].pt, len(topmerged))
            top_merged_selected_loose_GenTopMatch04_Merged, top_merged_selected_medium_GenTopMatch04_Merged, top_merged_selected_tight_GenTopMatch04_Merged = thresholdTopScore([topMergedSelect[0]], Top_Thr, 'Merged', year, score_type)
            if len(top_merged_selected_medium_GenTopMatch04_Merged) != 0:
                h_GenTop_pt_TagMediumWP_GenTopMatch04_Merged.Fill(topgen[0].pt)
            if len(top_merged_selected_tight_GenTopMatch04_Merged) != 0:
                h_GenTop_pt_TagTightWP_GenTopMatch04_Merged.Fill(topgen[0].pt)
        else:
            h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Merged.Fill(topgen[0].pt, len(topmerged))
        #Il miglior candidato TROTA è matchato con un topgen con dr = 0.2
        if len(matchingRecoTopGenTop(topgen, [topMergedSelect[0]], 0.2))!=0:
            h_GenTop_pt_Selection_GenTopMatch02_Merged.Fill(topgen[0].pt)
            h_GenTop_pt_RealLife_GenTopMatch02_Merged.Fill(topgen[0].pt)
            h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Merged.Fill(topgen[0].pt, len(topmerged))
            top_merged_selected_loose_GenTopMatch02_Merged, top_merged_selected_medium_GenTopMatch02_Merged, top_merged_selected_tight_GenTopMatch02_Merged = thresholdTopScore([topMergedSelect[0]], Top_Thr, 'Merged', year, score_type)
            if len(top_merged_selected_medium_GenTopMatch02_Merged) != 0:
                h_GenTop_pt_TagMediumWP_GenTopMatch02_Merged.Fill(topgen[0].pt)
            if len(top_merged_selected_tight_GenTopMatch02_Merged) != 0:
                h_GenTop_pt_TagTightWP_GenTopMatch02_Merged.Fill(topgen[0].pt)
        else:
            h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Merged.Fill(topgen[0].pt, len(topmerged))
        #il miglior candidato TROTA è matchato con quark e topgen dr=0.4


    if len(topResolvedSelect) !=0:
        #Il miglior candidato TROTA è matchato con i quark e topgen dr<0.4
        if len(matchingRecoTopGenTop(topgen, [topResolvedSelect[0]], 0.4))!=0 and len(matchingTopResGenPart(genpart, [topResolvedSelect[0]], jets))!=0:
            h_GenTop_pt_RealLife_OldMatch_Resolved.Fill(topgen[0].pt)
  
    if len(topMixedSelect) != 0:
        #Il miglior candidato TROTA è matchato con quark e topgen dr<0.4
        if topMixedSelect[0].truth == 1 and len(matchingRecoTopGenTop(topgen,[topMixedSelect[0]], 0.4))!=0:
            h_GenTop_pt_RealLife_OldMatch_Mixed.Fill(topgen[0].pt)

    if len(topMergedSelect) != 0:
        if len(matchingTopMerGenPart(genpart, [topMergedSelect[0]]))!=0 and len(matchingRecoTopGenTop(topgen, [topMergedSelect[0]], 0.4))!=0:
            h_GenTop_pt_RealLife_OldMatch_Merged.Fill(topgen[0].pt)

    
    
outfile.cd()
h_GenTop_pt.Write()
h_GenTop_pt_exist_resolved.Write()
h_GenTop_pt_exist_mixed.Write()
h_GenTop_pt_exist_merged.Write()
h_GenTop_pt_Reconstructable_QuarkMatch_Resolved.Write()
h_GenTop_pt_Reconstructable_QuarkMatch_Mixed.Write()
h_GenTop_pt_Reconstructable_QuarkMatch_Merged.Write()
h_GenTop_pt_Reconstructable_GenTopMatch02_Resolved.Write()
h_GenTop_pt_Reconstructable_GenTopMatch02_Mixed.Write()
h_GenTop_pt_Reconstructable_GenTopMatch02_Merged.Write()
h_GenTop_pt_Reconstructable_GenTopMatch04_Resolved.Write() 
h_GenTop_pt_Reconstructable_GenTopMatch04_Mixed.Write()
h_GenTop_pt_Reconstructable_GenTopMatch04_Merged.Write()
h_GenTop_pt_Selection_QuarkMatch_Resolved.Write()
h_GenTop_pt_Selection_QuarkMatch_Mixed.Write()
h_GenTop_pt_Selection_QuarkMatch_Merged.Write()
h_GenTop_pt_Selection_GenTopMatch02_Resolved.Write()
h_GenTop_pt_Selection_GenTopMatch02_Mixed.Write()
h_GenTop_pt_Selection_GenTopMatch02_Merged.Write()
h_GenTop_pt_Selection_GenTopMatch04_Resolved.Write()
h_GenTop_pt_Selection_GenTopMatch04_Mixed.Write()
h_GenTop_pt_Selection_GenTopMatch04_Merged.Write()
h_GenTop_pt_RealLife_QuarkMatch_Resolved.Write()
h_GenTop_pt_RealLife_QuarkMatch_Mixed.Write()
h_GenTop_pt_RealLife_QuarkMatch_Merged.Write()
h_GenTop_pt_RealLife_GenTopMatch02_Resolved.Write()
h_GenTop_pt_RealLife_GenTopMatch02_Mixed.Write()
h_GenTop_pt_RealLife_GenTopMatch02_Merged.Write()
h_GenTop_pt_RealLife_GenTopMatch04_Resolved.Write()
h_GenTop_pt_RealLife_GenTopMatch04_Mixed.Write()
h_GenTop_pt_RealLife_GenTopMatch04_Merged.Write()
h_GenTop_pt_TagMediumWP_QuarkMatch_Resolved.Write()
h_GenTop_pt_TagMediumWP_QuarkMatch_Mixed.Write()
h_GenTop_pt_TagMediumWP_QuarkMatch_Merged.Write()
h_GenTop_pt_TagMediumWP_GenTopMatch02_Resolved.Write()
h_GenTop_pt_TagMediumWP_GenTopMatch02_Mixed.Write()
h_GenTop_pt_TagMediumWP_GenTopMatch02_Merged.Write()
h_GenTop_pt_TagMediumWP_GenTopMatch04_Resolved.Write()
h_GenTop_pt_TagMediumWP_GenTopMatch04_Mixed.Write()
h_GenTop_pt_TagMediumWP_GenTopMatch04_Merged.Write()    
h_GenTop_pt_TagTightWP_QuarkMatch_Resolved.Write()
h_GenTop_pt_TagTightWP_QuarkMatch_Mixed.Write()
h_GenTop_pt_TagTightWP_QuarkMatch_Merged.Write()
h_GenTop_pt_TagTightWP_GenTopMatch02_Resolved.Write()
h_GenTop_pt_TagTightWP_GenTopMatch02_Mixed.Write()
h_GenTop_pt_TagTightWP_GenTopMatch02_Merged.Write()
h_GenTop_pt_TagTightWP_GenTopMatch04_Resolved.Write()
h_GenTop_pt_TagTightWP_GenTopMatch04_Mixed.Write()
h_GenTop_pt_TagTightWP_GenTopMatch04_Merged.Write()     
h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Resolved.Write()
h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Mixed.Write()
h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Merged.Write()
h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Resolved.Write()
h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Mixed.Write()       
h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Merged.Write()
h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Resolved.Write()
h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Mixed.Write()
h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Merged.Write()
h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Resolved.Write()
h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Mixed.Write()
h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Merged.Write()
h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Resolved.Write()
h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Mixed.Write()       
h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Merged.Write()
h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Resolved.Write()
h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Mixed.Write()
h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Merged.Write()
h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Resolved.Write()
h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Mixed.Write()   
h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Merged.Write()
h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Resolved.Write()
h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Mixed.Write()
h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Merged.Write()
h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Resolved.Write()
h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Mixed.Write()
h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Merged.Write()
h2_DeltaR_BestTop_GenTop_pt_Resolved.Write()
h2_DeltaR_BestTop_GenTop_pt_Mixed.Write()
h2_DeltaR_BestTop_GenTop_pt_Merged.Write() 
h_GenTop_pt_RealLife_OldMatch_Merged.Write()
h_GenTop_pt_RealLife_OldMatch_Mixed.Write()
h_GenTop_pt_RealLife_OldMatch_Resolved.Write()
outfile.Close()


