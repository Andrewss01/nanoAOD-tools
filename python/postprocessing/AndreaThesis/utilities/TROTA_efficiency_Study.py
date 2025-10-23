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

def check_same_top(topmixed1, topmixed2, resolved = False):

    '''
    Questa funzione prende due top in input e controlla se sono uguali o no
    In particolare restituisce True o se hanno anche solo un jet in comune
    oppure se entrambi hanno lo stesso fatjet (nel caso di top Mixed)
    se sono due top resolved confronta solo i jet normali, perchè il check sui fatjet è automaticamente False
    '''
    if not resolved:
        idx_fj_1, idx_j0_1, idx_j1_1, idx_j2_1 = topmixed1.idxFatJet, topmixed1.idxJet0, topmixed1.idxJet1, topmixed1.idxJet2
        idx_fj_2, idx_j0_2, idx_j1_2, idx_j2_2 = topmixed2.idxFatJet, topmixed2.idxJet0, topmixed2.idxJet1, topmixed2.idxJet2
    else:
        idx_fj_1, idx_j0_1, idx_j1_1, idx_j2_1 = -1, topmixed1.idxJet0, topmixed1.idxJet1, topmixed1.idxJet2
        idx_fj_2, idx_j0_2, idx_j1_2, idx_j2_2 = -1, topmixed2.idxJet0, topmixed2.idxJet1, topmixed2.idxJet2
    list_1 = [idx_j0_1, idx_j1_1, idx_j2_1]
    list_2 = [idx_j0_2, idx_j1_2, idx_j2_2]

    intersection = list(set(list_1) & set(list_2))
    check_jets = len(intersection) > 0
    check_fj = (idx_fj_1 == idx_fj_2) and (idx_fj_1 != -1 and idx_fj_2 != -1) 
    return check_jets or check_fj

def selectTop(topmixed, resolved = False, year = 2022):
    '''
    Questa funzione invece prende tutti i top e li ordina in base allo score
    dopodichè mette nella lista tutti i top, in ordine di score, ma prima controlla che siano diversi nel senso spiegato prima
    '''
    if len(topmixed) == 0: return []
    # print([top.TopScore for top in topmixed])
    if year == 2018:
        topmixed_sorted = sorted(topmixed, key=lambda x: x.TTScore, reverse=True)
    elif year == 2022:
        topmixed_sorted = sorted(topmixed, key=lambda x: (x.TTScore/(x.FTScore + x.TTScore)), reverse=True)  
    # print("sorted ", [top.TopScore for top in topmixed_sorted])
    topselected = []
    for i, top in enumerate(topmixed_sorted):
        if(i==0):
            if top.TTScore/(top.TTScore + top.FTScore) >= 0.92:
                topselected.append(top)
        else:
            same_top = False
            for bestTop in topselected:
                same_top = check_same_top(top, bestTop, resolved = resolved)
                if same_top: break
            if not same_top:
                if (top.TTScore)/(top.TTScore + top.FTScore) >= 0.92:
                    topselected.append(top)
    #print("starting number of tops", len(topmixed))
    #print("number of selected tops", len(topselected))
    return topselected

def sortTop(topmixed, resolved = False, year = 2022):
    if len(topmixed) == 0: return []
    # print([top.TopScore for top in topmixed])
    if year == 2018:
        topmixed_sorted = sorted(topmixed, key=lambda x: x.TTScore, reverse=True)
    elif year == 2022:
        topmixed_sorted = sorted(topmixed, key=lambda x: (x.TTScore/(x.FTScore + x.TTScore)), reverse=True)
    # print("sorted ", [top.TopScore for top in topmixed_sorted]
    topselected = []
    for i, top in enumerate(topmixed_sorted):
        if (top.TTScore/(top.FTScore + top.TTScore) >= 0.92):
            topselected.append(top)

    return topselected

def removeResolved(topmixed):
    '''
    Questa parte separa i top resolved 
    che si trovano all'interno dei top mixed
    '''
    if len(topmixed) == 0: return []
    topselected = []
    for top in topmixed:
        if top.idxFatJet != -1:
            topselected.append(top)
    return topselected

# def matchingTopResGenPart_first(genpart, top_res, jets):
#     top_res_matched_q = []

#     b  = None
#     q  = None
#     q_ = None
#     sign_w = 0
    
#     for part in genpart:
#         #se non è prompt(non generata dai gluoni) e prima copia 
#         if(part.genPartIdxMother_prompt>-1 and (part.statusFlags & (1<<12))): #la parte su statusFlag controlla se il 12esimo bit è 0 o 1 (1 << 12:Sposta il bit "1" di 12 posizioni verso sinistra & controlla bit a bit) il 12 slot indica se è la prima copia della particella
#             #se è un quark non top e la madre è un w e la nonna è un top
#             if(abs(part.pdgId)<6 and abs(genpart[part.genPartIdxMother_prompt].pdgId)==24 and abs(genpart[genpart[part.genPartIdxMother_prompt].genPartIdxMother_prompt].pdgId)==6):
#                 sign_w = genpart[part.genPartIdxMother_prompt].pdgId/24
#                 #assegna a q o q_ la particella selezionata (non importa quale a q o q_)
#                 if(q==None): q = part
#                 elif(q_==None): q_ = part
#                 else: continue
#     for part in genpart:
#         if(part.genPartIdxMother_prompt>-1 and (part.statusFlags & (1<<12))):
#             if(part.pdgId ==5*sign_w and abs(genpart[part.genPartIdxMother_prompt].pdgId)==6):
#                 b = part  

#     #print(top_res)
#     for top in top_res:
#         j0 = jets[top.idxJet0]
#         j1 = jets[top.idxJet1]
#         j2 = jets[top.idxJet2]
#         top_jets = [j0, j1, j2]
#         #quarks = [b,q,q_]

#         #se tutti i quark sono stati trovati
#         if (b!=None and q!=None and q_!=None):
#             #!!qui sto introducendo una gerarchia intrinseca tra quark
#             bjet, drb    = closest(b, top_jets)
#             #print("pre remove bjet", top_jets)
#             top_jets.remove(bjet)
#             #print("post remove bjet", top_jets)
#             qjet, drq    = closest(q, top_jets)
#             top_jets.remove(qjet)
#             #print("post remove qjet", top_jets)
#             q_jet, drq_  = closest(q_, top_jets)
#             top_jets.remove(q_jet)
#             #print("post remove q_jet", top_jets
            
#         else:
#             drb, drq, drq_ = 1000, 1000, 1000
#         #se la distanza tra ogni quark e il proprio jet è minore di 0.4 ritorna i 3 oggetti

 
#         if(drb<0.4 and drq<0.4 and drq_<0.4) and len(top_jets)==0:
#             top_res_matched_q.append(top)
#             #print(bjet,qjet,q_jet)

#     return top_res_matched_q

# def matchingTopResGenPart_second(genpart, top_res, jets):
#     top_res_matched_q = []

#     b  = None
#     q  = None
#     q_ = None
#     sign_w = 0
    
#     for part in genpart:
#         #se non è prompt(non generata dai gluoni) e prima copia 
#         if(part.genPartIdxMother_prompt>-1 and (part.statusFlags & (1<<12))): #la parte su statusFlag controlla se il 12esimo bit è 0 o 1 (1 << 12:Sposta il bit "1" di 12 posizioni verso sinistra & controlla bit a bit) il 12 slot indica se è la prima copia della particella
#             #se è un quark non top e la madre è un w e la nonna è un top
#             if(abs(part.pdgId)<6 and abs(genpart[part.genPartIdxMother_prompt].pdgId)==24 and abs(genpart[genpart[part.genPartIdxMother_prompt].genPartIdxMother_prompt].pdgId)==6):
#                 sign_w = genpart[part.genPartIdxMother_prompt].pdgId/24
#                 #assegna a q o q_ la particella selezionata (non importa quale a q o q_)
#                 if(q==None): q = part
#                 elif(q_==None): q_ = part
#                 else: continue
#     for part in genpart:
#         if(part.genPartIdxMother_prompt>-1 and (part.statusFlags & (1<<12))):
#             if(part.pdgId ==5*sign_w and abs(genpart[part.genPartIdxMother_prompt].pdgId)==6):
#                 b = part  

#     #print(top_res)
#     for top in top_res:
#         j0 = jets[top.idxJet0]
#         j1 = jets[top.idxJet1]
#         j2 = jets[top.idxJet2]
#         top_jets = [j0, j1, j2]
#         #quarks = [b,q,q_]
#         matched_jets = []
        
#         j_duplicate = []
#         j_not_matched = []
#         #se tutti i quark sono stati trovati
#         if (b!=None and q!=None and q_!=None):
#             #!!qui sto introducendo una gerarchia intrinseca tra quark
#             bjet, drb    = closest(b, top_jets)
#             #print("pre remove bjet", top_jets)
#             #top_jets.remove(bjet)
#             matched_jets.append(bjet)
#             #print("post remove bjet", top_jets)
#             qjet, drq    = closest(q, top_jets)
#             #top_jets.remove(qjet)
#             matched_jets.append(qjet)
#             #print("post remove qjet", top_jets)
#             q_jet, drq_  = closest(q_, top_jets)
#             #top_jets.remove(q_jet)
#             matched_jets.append(q_jet)
#             #print("post remove q_jet", top_jets)
#             j_not_matched = list(set(top_jets) - set(matched_jets))
#             j_duplicate = [elem for elem, count in Counter(matched_jets).items() if count != 1]
#             #print(j_not_matched)
#             #print(j_duplicate)
#             i=0
#             selected_jets=matched_jets
#             while len(j_duplicate)!=0:
#                 i+=1
#                 #print("iterazione", i)
#                 matched_quarks_to_same_jet = []
#                 if j_duplicate[0] == selected_jets[0]:
#                     matched_quarks_to_same_jet.append(b)
#                     #print("b")
#                 if j_duplicate[0] == selected_jets[1]:
#                     matched_quarks_to_same_jet.append(q)
#                     #print("q")
#                 if j_duplicate[0] == selected_jets[2]:
#                     matched_quarks_to_same_jet.append(q_)   
#                     #print("q_")
#                 #print(matched_quarks_to_same_jet)
#                 for j in j_not_matched:
#                     closest_quark, dr = closest(j,matched_quarks_to_same_jet)
#                     if closest_quark == b:
#                         bjet = j
#                         drb=dr
#                     if closest_quark == q:
#                         qjet = j
#                         drq=dr
#                     if closest_quark == q_:
#                         q_jet = j
#                         drq_=dr
#                 selected_jets=[bjet,qjet,q_jet]
#                 #print("selected_jets",selected_jets)
#                 j_not_matched = list(set(top_jets) - set(selected_jets))
#                 #print("j_not_matched",j_not_matched)
#                 j_duplicate = [jet for jet, count in Counter(selected_jets).items() if count > 1]
#         else:
#             drb, drq, drq_ = 1000, 1000, 1000
#         #se la distanza tra ogni quark e il proprio jet è minore di 0.4 ritorna i 3 oggetti
#         selected_jets=[bjet,qjet,q_jet]
#         j_not_matched_2 = []
#         j_duplicate_2 = []
#         j_not_matched_2 = list(set(top_jets) - set(selected_jets))
#         j_duplicate_2 = [jet for jet, count in Counter(selected_jets).items() if count > 1]
#         if len(j_duplicate_2)!=0 :#and (drb<0.4 or drq<0.4 or drq_<0.4):
#                     print("\n CHE SUCCEDE \n")
#                     print("non match before",j_not_matched)
#                     print("non match",j_not_matched_2)
#                     print("match before",matched_jets)
#                     print("match",selected_jets)
#         if(drb<0.4 and drq<0.4 and drq_<0.4):
#             top_res_matched_q.append(top)
#             #print(bjet,qjet,q_jet)

#     return top_res_matched_q


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
                    #questa cosa è fatta jet per jet e quark per quark, l'ordine dei quark rimane invariato, mentre quello dei jet varia a ogni permutazione risultando in tutte le possibili combinazioni
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

def matchingTopMerGenPart(genpart, top_mer, type):
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
            if type == 'Mixed':
                if (top.TTScore)/(top.TTScore + top.FTScore) >= 0.92:
                    top_mer_matched_q.append(top)
            else:
                top_mer_matched_q.append(top)

    return top_mer_matched_q

def matchingRecoTopGenTop(gentop, recotop, dR, type):
    # if len(gentop)==1:  top = gentop[0] # sempre vero per tt semilep
    top_reco_matched = []
    for top_r in recotop: 
        # Funziona solo per semilep
        dRGenTopRecoTop = deltaR(gentop[0].eta, gentop[0].phi, top_r.eta, top_r.phi) 
        if(dRGenTopRecoTop<dR): 
            if type == 'Mixed':
                if (top_r.TTScore)/(top_r.TTScore + top_r.FTScore) >= 0.92:
                    top_reco_matched.append(top_r)
            else:
                top_reco_matched.append(top_r)

    return top_reco_matched

def thresholdTopScore(topreco, Top_threshold, top_type, year):
    topselected_loose = []
    topselected_medium = []
    topselected_tight = []
    if top_type == 'Mixed' or top_type == 'Resolved':
        if year == 2018:
            attr_name = f"TTScore"
        elif year == 2022:
            attr_name = f"TTScore"
    elif top_type == 'Merged':
        if year == 2018:
            attr_name = f"particleNet_TvsQCD"
        elif year == 2022:
            attr_name = f"particleNetWithMass_TvsQCD"
    
    for i, t in enumerate(topreco):
        score = getattr(t, attr_name) 
        if score > float(Top_threshold[top_type]['WPloose']):
            topselected_loose.append(t)
        if score > float(Top_threshold[top_type]['WPmedium']):
            topselected_medium.append(t)
        if score > float(Top_threshold[top_type]['WPtight']):
            topselected_tight.append(t)
    return topselected_loose, topselected_medium, topselected_tight 

# with open("/afs/cern.ch/user/a/apuglia/CMSSW_14_1_7/src/PhysicsTools/NanoAODTools/python/postprocessing/AndreaThesis/samples/dict_samples_2022.json", "r") as f:
#     sample = json.load(f)


year = 2022
if year == 2018:    
    file = "root://cms-xrd-global.cern.ch//store/user/acagnott/Run3Analysis_Tprime/TT_semilep_2018/20240731_214516/tree_hadd_755.root"
    print(f"Using file: {file}")
    chain = ROOT.TChain('Events')
    chain.Add(file)
elif year == 2022:
    # file_dict = sample["TT_semilep_2022"]["TT_semilep_2022"] 
    # file_idx = file_dict["ntot"].index(max(file_dict["ntot"])) 
    # file = file_dict["strings"][file_idx]
    path = '/eos/user/a/apuglia/Master_Thesis/PostProcessed_Datasets/TT_semilep_2022/scores_model_lstm/'
    chain = ROOT.TChain('Events')

    for fileName in tqdm(os.listdir(path)):
        if fileName.endswith(".root") and not(fileName.startswith(".")):
            file = path + fileName
            # print(file)
            chain.Add(file)
    # for i in range(0,20):
    #     file=file_dict["strings"][i]
    #     print(f"Using file: {file}")
    #     chain.Add(file)


tree = InputTree(chain)
print('num events: ', tree.GetEntries())

if year == 2018: 
    dir_path = "/eos/user/f/fsalerno/Evaluation/TROTA_2018_studies/Histo_files"
    if not os.path.exists(dir_path):  
        os.makedirs(dir_path)   
    outfile = ROOT.TFile(f"{dir_path}/output_TROTA_efficiency_Study_ttsemilep_noResinMix.root","RECREATE")

elif year == 2022:
    dir_path = "/eos/user/a/apuglia/Thesis/Evaluation/TROTA_2022_studies/FT_Score_cut/Histo_files"
    if not os.path.exists(dir_path):  
        os.makedirs(dir_path)   
    outfile = ROOT.TFile(f"{dir_path}/output_TROTA_efficiency_Study_ttsemilep_noResinMix.root","RECREATE")


###############!!! DA CONTROLLARE I WORKING POINTS 2022!!!#############

if year == 2018:
    Top_threshold = {"Resolved" :{'WPloose': "0.24193972", 'WPmedium': "0.5411276", 'WPtight': "0.77197933"},
                    "Mixed"    :{'WPloose': "0.2957885265350342", 'WPmedium': "0.7584613561630249", 'WPtight': "0.9129540324211121"},
                    "Merged"   :{'WPloose': "0.79", 'WPmedium': "0.91", 'WPtight': "0.97"}}

elif year == 2022:
    Top_threshold = {"Resolved" :{'WPloose': "0.1422998", 'WPmedium': "0.59264845", 'WPtight': "0.86580896"},
                    "Mixed"    :{'WPloose': "0.7780495285987854", 'WPmedium': "0.8904699683189392", 'WPtight': "0.9797756671905518"},
                    "Merged"   :{'WPloose': "0.79", 'WPmedium': "0.8", 'WPtight': "0.97"}}

###############!!! DA CONTROLLARE I WORKING POINTS 2022 !!!#############
 

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
# h2_Num_cand_DeltaR_GenTop_pt_QuarkMatch_Mixed          = ROOT.TH1D("h2_Num_cand_DeltaR_GenTop_pt_QuarkMatch_Mixed","; num candidates vs genTop pT matched with top mixed with quark", 20, 0, 1000, 10, 0, 100)
# h2_Num_cand_DeltaR_GenTop_pt_QuarkMatch_Merged         = ROOT.TH1D("h2_Num_cand_DeltaR_GenTop_pt_QuarkMatch_Merged","; num candidates vs genTop pT matched with top merged with quark", 20, 0, 1000, 10, 0, 100)
# h2_Num_cand_DeltaR_GenTop_pt_GenTopMatch02_Resolved    = ROOT.TH1D("h2_Num_cand_DeltaR_GenTop_pt_GenTopMatch02_Resolved","; num candidates vs genTop pT matched with top resolved with dr 0.2", 20, 0, 1000, 10, 0, 100)
# h2_Num_cand_DeltaR_GenTop_pt_GenTopMatch02_Mixed       = ROOT.TH1D("h2_Num_cand_DeltaR_GenTop_pt_GenTopMatch02_Mixed","; num candidates vs genTop pT matched with top mixed with dr 0.2", 20, 0, 1000, 10, 0, 100)
# h2_Num_cand_DeltaR_GenTop_pt_GenTopMatch02_Merged      = ROOT.TH1D("h2_Num_cand_DeltaR_GenTop_pt_GenTopMatch02_Merged","; num candidates vs genTop pT matched with top merged with dr 0.2", 20, 0, 1000, 10, 0, 100)
# h2_Num_cand_DeltaR_GenTop_pt_GenTopMatch04_Resolved    = ROOT.TH1D("h2_Num_cand_DeltaR_GenTop_pt_GenTopMatch04_Resolved","; num candidates vs genTop pT matched with top resolved with dr 0.4", 20, 0, 1000, 10, 0, 100)
# h2_Num_cand_DeltaR_GenTop_pt_GenTopMatch04_Mixed       = ROOT.TH1D("h2_Num_cand_DeltaR_GenTop_pt_GenTopMatch04_Mixed","; num candidates vs genTop pT matched with top mixed with dr 0.4", 20, 0, 1000, 10, 0, 100)
# h2_Num_cand_DeltaR_GenTop_pt_GenTopMatch04_Merged      = ROOT.TH1D("h2_Num_cand_DeltaR_GenTop_pt_GenTopMatch04_Merged","; num candidates vs genTop pT matched with top merged with dr 0.4", 20, 0, 1000, 10, 0, 100)

nEvRecoTopGenQuarktMatched = 0
nEvRecoTopGenTop02Matched = 0
nEvRecoTopGenTop04Matched = 0
nEvBestRecoTopGenQuarktMatched = 0
nEvBestRecoTopGenTop02Matched = 0
nEvBestRecoTopGenTop04Matched = 0
# print('a')
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
    # print('topgen is: ', topgen)
    # if len(topgen) != 2:
    print("numero di top hadronici trovati:", len(topgen))
    tot_top = []
    for particle in genpart:
        if abs(particle.pdgId) ==6:
            particle.append(tot_top)
    print('numero totale di top: ', len(tot_top))
    # print("top hadronici trovati:", [top.pdgId for top in topgen])
    # print("hadronic top idx:", hadronic_top_idx)
    # print("i top sono:", [genpart[idx].pdgId for idx in hadronic_top_idx])
    # for i,part in enumerate(genpart):
    #     print(i,"part pdgId:", part.pdgId, "e idx madre:", part.genPartIdxMother)
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
    # if (top.TTScore/(top.ZJScore + top.TTScore) >= 0.79):
    topMixedQuarkMatch = list(filter(lambda x : x.truth==1 and (x.TTScore/(x.TTScore + x.FTScore)) >= 0.92, topMixedNoRes)) #qui uso la truth per "almeno un quark matchato"
    topMergedQuarkMatch = matchingTopMerGenPart(genpart, topmerged, type = 'Merged')
    # if len(topResolvedQuarkMatch) != 0:
        # h_GenTop_pt_Reconstructable_QuarkMatch_Resolved.Fill(topgen[0].pt)
        #print(len(topResolvedQuarkMatch))
        # h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Resolved.Fill(topgen[0].pt, len(topresolved))
        #h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Resolved.Fill(topgen[0].pt, len(topResolvedQuarkMatch))
        # nEvRecoTopGenQuarktMatched += 1
    if len(topMixedQuarkMatch) != 0:
        h_GenTop_pt_Reconstructable_QuarkMatch_Mixed.Fill(topgen[0].pt)
        h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Mixed.Fill(topgen[0].pt, len(topmixed))
        #h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Mixed.Fill(topgen[0].pt, len(topMixedQuarkMatch))

    if len(topMergedQuarkMatch) != 0:
        h_GenTop_pt_Reconstructable_QuarkMatch_Merged.Fill(topgen[0].pt)
        h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Merged.Fill(topgen[0].pt, len(topmerged))
        #h2_Num_cand_GenTop_pt_ExistsMatched_QuarkMatch_Merged.Fill(topgen[0].pt, len(topMergedQuarkMatch))
    #gentop match dr=0.4
    # topResolvedGenTopMatch_04 = matchingRecoTopGenTop(topgen, topresolved, 0.4)
    topMixedGenTopMatch_04 = matchingRecoTopGenTop(topgen, topMixedNoRes, 0.4, type = 'Mixed')
    topMergedGenTopMatch_04 = matchingRecoTopGenTop(topgen, topmerged, 0.4, type = 'Merged')
    # if len(topResolvedGenTopMatch_04) != 0:
    #     h_GenTop_pt_Reconstructable_GenTopMatch04_Resolved.Fill(topgen[0].pt)
    #     h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Resolved.Fill(topgen[0].pt, len(topresolved))
    #     nEvRecoTopGenTop04Matched += 1
    if len(topMixedGenTopMatch_04) != 0:
        h_GenTop_pt_Reconstructable_GenTopMatch04_Mixed.Fill(topgen[0].pt)
        h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Mixed.Fill(topgen[0].pt, len(topmixed))
    if len(topMergedGenTopMatch_04) != 0:
        h_GenTop_pt_Reconstructable_GenTopMatch04_Merged.Fill(topgen[0].pt)
        h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch04_Merged.Fill(topgen[0].pt, len(topmerged))
    #gentop match dr=0.2
    # topResolvedGenTopMatch_02 = matchingRecoTopGenTop(topgen, topresolved, 0.2)
    topMixedGenTopMatch_02 = matchingRecoTopGenTop(topgen, topMixedNoRes, 0.2, type = 'Mixed')
    topMergedGenTopMatch_02 = matchingRecoTopGenTop(topgen, topmerged, 0.2, type = 'Merged')
    # if len(topResolvedGenTopMatch_02) != 0:
    #     h_GenTop_pt_Reconstructable_GenTopMatch02_Resolved.Fill(topgen[0].pt)
    #     h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Resolved.Fill(topgen[0].pt, len(topresolved))
    #     nEvRecoTopGenTop02Matched += 1
    if len(topMixedGenTopMatch_02) != 0:
        h_GenTop_pt_Reconstructable_GenTopMatch02_Mixed.Fill(topgen[0].pt)
        h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Mixed.Fill(topgen[0].pt, len(topmixed))
    if len(topMergedGenTopMatch_02) != 0:
        h_GenTop_pt_Reconstructable_GenTopMatch02_Merged.Fill(topgen[0].pt)
        h2_Num_cand_GenTop_pt_ExistsMatched_GenTopMatch02_Merged.Fill(topgen[0].pt, len(topmerged))

    ####HISTO PT PER EFFICIENZA "DI SELEZIONE" E "REAL LIFE" IL MIGLIOR CANDIDATO TROTA è MATCHATO  #####
    #Lista dei topmixed non sovrapposti ordinati per score
    # topResolvedSelect = selectTop(topresolved, resolved = True, year=year)
    #print("topResolvedSelect",isinstance(topResolvedSelect,list), topResolvedSelect[0].pt)
    #Lista dei topmixed senza resolved non sovrapposti ordinati per score
    topMixedSelect = selectTop(topMixedNoRes, resolved = False, year=year)
    #lista dei topmerged ordinati per score
    if year == 2018:
        topMergedSelect = sorted(topmerged, key=lambda x: x.particleNet_TvsQCD, reverse=True)
    elif year == 2022:
        topMergedSelect = sorted(topmerged, key=lambda x: x.particleNetWithMass_TvsQCD, reverse=True)
    #Esiste almeno un candidato TROTA
    # if len(topResolvedSelect) != 0:
    #     h_GenTop_pt_exist_resolved.Fill(topgen[0].pt)
    if len(topMixedSelect) != 0:
        h_GenTop_pt_exist_mixed.Fill(topgen[0].pt)
    if len(topMergedSelect) != 0:
        h_GenTop_pt_exist_merged.Fill(topgen[0].pt)
    
    
    # if len(topResolvedSelect) !=0:
    #     h2_DeltaR_BestTop_GenTop_pt_Resolved.Fill(topgen[0].pt, deltaR(topResolvedSelect[0], topgen[0]))
    #     #Il miglior candidato TROTA è matchato con i quark
    #     if len(matchingTopResGenPart(genpart, [topResolvedSelect[0]], jets))!=0:
    #         h_GenTop_pt_Selection_QuarkMatch_Resolved.Fill(topgen[0].pt)
    #         h_GenTop_pt_RealLife_QuarkMatch_Resolved.Fill(topgen[0].pt)
    #         h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Resolved.Fill(topgen[0].pt, len(topresolved))
    #         #h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Resolved.Fill(topgen[0].pt, len(topResolvedSelect))

    #         nEvBestRecoTopGenQuarktMatched += 1
    #         top_resolved_selected_loose_QuarkMatch, top_resolved_selected_medium_QuarkMatch, top_resolved_selected_tight_QuarkMatch = thresholdTopScore([topResolvedSelect[0]], Top_threshold, 'Resolved', year)
    #         if len(top_resolved_selected_medium_QuarkMatch) != 0:
    #             h_GenTop_pt_TagMediumWP_QuarkMatch_Resolved.Fill(topgen[0].pt)
    #     else:
    #         h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Resolved.Fill(topgen[0].pt, len(topresolved))
    #     #Il miglior candidato TROTA è matchato con un topgen con dr = 0.4
    #     if len(matchingRecoTopGenTop(topgen, [topResolvedSelect[0]], 0.4))!=0:
    #         h_GenTop_pt_Selection_GenTopMatch04_Resolved.Fill(topgen[0].pt)
    #         h_GenTop_pt_RealLife_GenTopMatch04_Resolved.Fill(topgen[0].pt)
    #         h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Resolved.Fill(topgen[0].pt, len(topresolved))
    #         nEvBestRecoTopGenTop04Matched += 1
    #         top_resolved_selected_loose_GenTopMatch04_Resolved, top_resolved_selected_medium_GenTopMatch04_Resolved, top_resolved_selected_tight_GenTopMatch04_Resolved = thresholdTopScore([topResolvedSelect[0]], Top_threshold, 'Resolved', year)  
    #         if len(top_resolved_selected_medium_GenTopMatch04_Resolved) != 0:
    #             h_GenTop_pt_TagMediumWP_GenTopMatch04_Resolved.Fill(topgen[0].pt)
    #     else:
    #         h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Resolved.Fill(topgen[0].pt, len(topresolved))
    #     #Il miglior candidato TROTA è matchato con un topgen con dr = 0.2
    #     if len(matchingRecoTopGenTop(topgen, [topResolvedSelect[0]], 0.2))!=0:
    #         h_GenTop_pt_Selection_GenTopMatch02_Resolved.Fill(topgen[0].pt)
    #         h_GenTop_pt_RealLife_GenTopMatch02_Resolved.Fill(topgen[0].pt)
    #         h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Resolved.Fill(topgen[0].pt, len(topresolved))
    #         nEvBestRecoTopGenTop02Matched += 1
    #         top_resolved_selected_loose_GenTopMatch02_Resolved, top_resolved_selected_medium_GenTopMatch02_Resolved, top_resolved_selected_tight_GenTopMatch02_Resolved = thresholdTopScore([topResolvedSelect[0]], Top_threshold, 'Resolved', year)
    #         if len(top_resolved_selected_medium_GenTopMatch02_Resolved) != 0:
    #             h_GenTop_pt_TagMediumWP_GenTopMatch02_Resolved.Fill(topgen[0].pt)

    #     else:
    #         h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Resolved.Fill(topgen[0].pt, len(topresolved))

    if len(topMixedSelect) != 0:
        h2_DeltaR_BestTop_GenTop_pt_Mixed.Fill(topgen[0].pt, deltaR(topMixedSelect[0], topgen[0]))
        #Il miglior candidato TROTA è matchato con quark
        if topMixedSelect[0].truth == 1:
            h_GenTop_pt_Selection_QuarkMatch_Mixed.Fill(topgen[0].pt)
            h_GenTop_pt_RealLife_QuarkMatch_Mixed.Fill(topgen[0].pt)
            h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Mixed.Fill(topgen[0].pt, len(topmixed))
            #h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Mixed.Fill(topgen[0].pt, len(topMixedSelect))
            top_mixed_selected_loose_QuarkMatch, top_mixed_selected_medium_QuarkMatch, top_mixed_selected_tight_QuarkMatch = thresholdTopScore([topMixedSelect[0]], Top_threshold, 'Mixed', year)
            if len(top_mixed_selected_medium_QuarkMatch) != 0:
                h_GenTop_pt_TagMediumWP_QuarkMatch_Mixed.Fill(topgen[0].pt)
        else:
            h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Mixed.Fill(topgen[0].pt, len(topmixed))
        #Il miglior candidato TROTA è matchato con un topgen con dr = 0.4
        if len(matchingRecoTopGenTop(topgen, [topMixedSelect[0]], 0.4, type = 'Mixed'))!=0:
            h_GenTop_pt_Selection_GenTopMatch04_Mixed.Fill(topgen[0].pt)
            h_GenTop_pt_RealLife_GenTopMatch04_Mixed.Fill(topgen[0].pt)
            h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Mixed.Fill(topgen[0].pt, len(topmixed))
            top_mixed_selected_loose_GenTopMatch04_Mixed, top_mixed_selected_medium_GenTopMatch04_Mixed, top_mixed_selected_tight_GenTopMatch04_Mixed = thresholdTopScore([topMixedSelect[0]], Top_threshold, 'Mixed', year)
            if len(top_mixed_selected_medium_GenTopMatch04_Mixed) != 0:
                h_GenTop_pt_TagMediumWP_GenTopMatch04_Mixed.Fill(topgen[0].pt)
        else:
            h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Mixed.Fill(topgen[0].pt, len(topmixed))
        #Il miglior candidato TROTA è matchato con un topgen con dr = 0.2
        if len(matchingRecoTopGenTop(topgen, [topMixedSelect[0]], 0.2, type = 'Mixed'))!=0:
            h_GenTop_pt_Selection_GenTopMatch02_Mixed.Fill(topgen[0].pt)
            h_GenTop_pt_RealLife_GenTopMatch02_Mixed.Fill(topgen[0].pt)
            h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Mixed.Fill(topgen[0].pt, len(topmixed))
            top_mixed_selected_loose_GenTopMatch02_Mixed, top_mixed_selected_medium_GenTopMatch02_Mixed, top_mixed_selected_tight_GenTopMatch02_Mixed = thresholdTopScore([topMixedSelect[0]], Top_threshold, 'Mixed', year)
            if len(top_mixed_selected_medium_GenTopMatch02_Mixed) != 0:
                h_GenTop_pt_TagMediumWP_GenTopMatch02_Mixed.Fill(topgen[0].pt)
        else:
            h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Mixed.Fill(topgen[0].pt, len(topmixed))
    if len(topMergedSelect) != 0:
        h2_DeltaR_BestTop_GenTop_pt_Merged.Fill(topgen[0].pt, deltaR(topMergedSelect[0], topgen[0]))
        #Il miglior candidato TROTA è matchato con quark
        if len(matchingTopMerGenPart(genpart, [topMergedSelect[0]], type= 'Merged'))!=0:
            h_GenTop_pt_Selection_QuarkMatch_Merged.Fill(topgen[0].pt)
            h_GenTop_pt_RealLife_QuarkMatch_Merged.Fill(topgen[0].pt)
            h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Merged.Fill(topgen[0].pt, len(topmerged))
            #h2_Num_cand_GenTop_pt_BestMatched_QuarkMatch_Merged.Fill(topgen[0].pt, len(topMergedSelect))
            top_merged_selected_loose_QuarkMatch, top_merged_selected_medium_QuarkMatch, top_merged_selected_tight_QuarkMatch = thresholdTopScore([topMergedSelect[0]], Top_threshold, 'Merged', year)
            if len(top_merged_selected_medium_QuarkMatch) != 0:
                h_GenTop_pt_TagMediumWP_QuarkMatch_Merged.Fill(topgen[0].pt)
        else:
            h2_Num_cand_GenTop_pt_NotMatched_QuarkMatch_Merged.Fill(topgen[0].pt, len(topmerged))
        #Il miglior candidato TROTA è matchato con un topgen con dr = 0.4
        if len(matchingRecoTopGenTop(topgen, [topMergedSelect[0]], 0.4, type = 'Merged'))!=0:
            h_GenTop_pt_Selection_GenTopMatch04_Merged.Fill(topgen[0].pt)
            h_GenTop_pt_RealLife_GenTopMatch04_Merged.Fill(topgen[0].pt)
            h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch04_Merged.Fill(topgen[0].pt, len(topmerged))
            top_merged_selected_loose_GenTopMatch04_Merged, top_merged_selected_medium_GenTopMatch04_Merged, top_merged_selected_tight_GenTopMatch04_Merged = thresholdTopScore([topMergedSelect[0]], Top_threshold, 'Merged', year)
            if len(top_merged_selected_medium_GenTopMatch04_Merged) != 0:
                h_GenTop_pt_TagMediumWP_GenTopMatch04_Merged.Fill(topgen[0].pt)
        else:
            h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch04_Merged.Fill(topgen[0].pt, len(topmerged))
        #Il miglior candidato TROTA è matchato con un topgen con dr = 0.2
        if len(matchingRecoTopGenTop(topgen, [topMergedSelect[0]], 0.2, type = 'Merged'))!=0:
            h_GenTop_pt_Selection_GenTopMatch02_Merged.Fill(topgen[0].pt)
            h_GenTop_pt_RealLife_GenTopMatch02_Merged.Fill(topgen[0].pt)
            h2_Num_cand_GenTop_pt_BestMatched_GenTopMatch02_Merged.Fill(topgen[0].pt, len(topmerged))
            top_merged_selected_loose_GenTopMatch02_Merged, top_merged_selected_medium_GenTopMatch02_Merged, top_merged_selected_tight_QuarkMatch02_Merged = thresholdTopScore([topMergedSelect[0]], Top_threshold, 'Merged', year)
            if len(top_merged_selected_medium_GenTopMatch02_Merged) != 0:
                h_GenTop_pt_TagMediumWP_GenTopMatch02_Merged.Fill(topgen[0].pt)
        else:
            h2_Num_cand_GenTop_pt_NotMatched_GenTopMatch02_Merged.Fill(topgen[0].pt, len(topmerged))
        #il miglior candidato TROTA è matchato con quark e topgen dr=0.4


    # if len(topResolvedSelect) !=0:
    #     #Il miglior candidato TROTA è matchato con i quark e topgen dr<0.4
    #     if len(matchingRecoTopGenTop(topgen, [topResolvedSelect[0]], 0.4))!=0 and len(matchingTopResGenPart(genpart, [topResolvedSelect[0]], jets))!=0:
    #         h_GenTop_pt_RealLife_OldMatch_Resolved.Fill(topgen[0].pt)
  
    if len(topMixedSelect) != 0:
        #Il miglior candidato TROTA è matchato con quark e topgen dr<0.4
        if topMixedSelect[0].truth == 1 and len(matchingRecoTopGenTop(topgen,[topMixedSelect[0]], 0.4, type = 'Mixed'))!=0:
            h_GenTop_pt_RealLife_OldMatch_Mixed.Fill(topgen[0].pt)

    if len(topMergedSelect) != 0:
        if len(matchingTopMerGenPart(genpart, [topMergedSelect[0]], type = 'Merged'))!=0 and len(matchingRecoTopGenTop(topgen, [topMergedSelect[0]], 0.4, type = 'Merged'))!=0:
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


# print("Reconstructable efficiency quark criterion resolved: %.4f" %(nEvRecoTopGenQuarktMatched/tree.GetEntries()))
# print("Reconstructable efficiency dr=0.4 criterion resolved: %.4f" %(nEvRecoTopGenTop04Matched/tree.GetEntries()))
# print("Reconstructable efficiency dr=0.2 criterion resolved: %.4f" %(nEvRecoTopGenTop02Matched/tree.GetEntries()))
# print("Selection efficiency quark criterion resolved: %.4f" %(nEvBestRecoTopGenQuarktMatched/nEvRecoTopGenQuarktMatched))
# print("Selection efficiency dr=0.4 criterion resolved: %.4f" %(nEvBestRecoTopGenTop04Matched/nEvRecoTopGenTop04Matched))
# print("Selection efficiency dr=0.2 criterion resolved: %.4f" %(nEvBestRecoTopGenTop02Matched/nEvRecoTopGenTop02Matched))
# print("Real Life efficiency quark criterion resolved: %.4f" %(nEvBestRecoTopGenQuarktMatched/tree.GetEntries()))
# print("Real Life efficiency dr=0.4 criterion resolved: %.4f" %(nEvBestRecoTopGenTop04Matched/tree.GetEntries()))
# print("Real Life efficiency dr=0.2 criterion resolved: %.4f" %(nEvBestRecoTopGenTop02Matched/tree.GetEntries()))




# Fraction of Events where at least 1 genquark is not matched with a jet: 0.13580660613000511
# Fraction of Events where gentop is not matched with the jet sum: 0.8004777695317077
#first
# Reconstructable efficiency quark criterion resolved: 0.3616
# Reconstructable efficiency dr=0.4 criterion resolved: 0.5860
# Reconstructable efficiency dr=0.2 criterion resolved: 0.3889
# Selection efficiency quark criterion resolved: 0.2880
# Selection efficiency dr=0.4 criterion resolved: 0.3813
# Selection efficiency dr=0.2 criterion resolved: 0.3307
# Real Life efficiency quark criterion resolved: 0.1042
# Real Life efficiency dr=0.4 criterion resolved: 0.2234
# Real Life efficiency dr=0.2 criterion resolved: 0.1286
#newest
# Reconstructable efficiency quark criterion resolved: 0.3619
# Reconstructable efficiency dr=0.4 criterion resolved: 0.5860
# Reconstructable efficiency dr=0.2 criterion resolved: 0.3889
# Selection efficiency quark criterion resolved: 0.2880
# Selection efficiency dr=0.4 criterion resolved: 0.3813
# Selection efficiency dr=0.2 criterion resolved: 0.3307
# Real Life efficiency quark criterion resolved: 0.1042
# Real Life efficiency dr=0.4 criterion resolved: 0.2234
# Real Life efficiency dr=0.2 criterion resolved: 0.1286