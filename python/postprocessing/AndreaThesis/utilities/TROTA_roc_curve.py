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

'''
Vanno fatte delle roc curve prendendo il segnale e il fondo. Prendiamo per esempio il TT semileptonico. 
Per ogni top è possibilie definire l'FT score, inoltre, per ogni top abbiamo il vero label
'''


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





# file_sig = '/eos/user/a/apuglia/Master_Thesis/PostProcessed_Datasets/TT_semilep_2022/'
file_sig = '/eos/user/a/apuglia/Master_Thesis/PostProcessed_Datasets/TT_hadronic_2022/'
file_bkg_1 = '/eos/user/a/apuglia/Master_Thesis/PostProcessed_Datasets/QCD_HT100to200_2022/file_0/scores_model_lstm/file_0_lstm_model.root'
# file_bkg_2 = '/eos/user/a/apuglia/Master_Thesis/PostProcessed_Datasets/QCD_HT200to400_2022/file_0/scores_model_lstm/file_0_lstm_model.root'
file_bkg_3 = '/eos/user/a/apuglia/Master_Thesis/PostProcessed_Datasets/QCD_HT600to800_2022/file_0/scores_model_lstm/file_0_lstm_model.root'
file_bkg_4 = '/eos/user/a/apuglia/Master_Thesis/PostProcessed_Datasets/QCD_HT400to600_2022/file_0/scores_model_lstm/file_0_lstm_model.root'
# file_bkg_5 = '/eos/user/a/apuglia/Master_Thesis/PostProcessed_Datasets/ZJetsto2Nu_HT1500to2500_2022/file_0/scores_model_lstm/file_0_lstm_model.root'
# file_bkg_6 = '/eos/user/a/apuglia/Master_Thesis/PostProcessed_Datasets/ZJetsto2Nu_HT100to200_2022/file_0/scores_model_lstm/file_0_lstm_model.root'
chain1 = ROOT.TChain('Events')
# chain = ROOT.TChain('Events')

for fileName in tqdm(os.listdir(file_sig)):
    if  fileName == 'file_0' or fileName == 'file_1' or fileName == 'file_2' or fileName == 'file_3' :
        file = file_sig + fileName + '/' + 'scores_model_lstm_v2/' + fileName +'_lstm_model.root'
        chain1.Add(file)


# chain1.Add(file_sig_2)
tree_1 = InputTree(chain1)
print('num events is: ', tree_1.GetEntries())




pt_min = 600
# elif pt_max == :
pt_max = 100000

pred_false_mixed, pred_false_resolved, pred_false_merged = [], [], []
label_true_mixed, label_true_resolved, label_true_merged = [], [], []
pred_true_mixed, pred_true_resolved, pred_true_merged = [], [], []
label_false_mixed, label_false_resolved, label_false_merged = [], [], []


sig_mixed = ROOT.TH1F('scores_sig_mixed', 'scores_sig_mixed', 200,0,1)
sig_resolved = ROOT.TH1F('scores_sig_resolved', 'scores_sig_resolved', 200,0,1)
sig_merged = ROOT.TH1F('scores_sig_merged', 'scores_sig_merged', 200,0,1)
bkg_mixed = ROOT.TH1F('scores_bkg_mixed', 'scores_bkg_mixed', 200,0,1)
bkg_resolved = ROOT.TH1F('scores_bkg_resolved', 'scores_bkg_resolved', 200,0,1)
bkg_merged = ROOT.TH1F('scores_bkg_merged', 'scores_bkg_merged', 200,0,1)



for i in tqdm(range(tree_1.GetEntries())):
    # print('Event: ', i)
    event = Event(tree_1,i)
    topmixed = Collection(event, 'TopMixed')
    topresolved = Collection(event, 'TopResolved')
    topmerged = Collection(event, 'FatJet')
    # print('n top merged:',len(topmerged))
    genpart = Collection(event, "GenPart")
    topMixedNoRes = removeResolved(topmixed)
    is_hadronic_top = np.zeros(len(genpart), dtype=int)
    hadronic_top_idx =[]
    quark_flavs = [int(1),int(2),int(3),int(4)]
    for particle in genpart:
        # print("la particella analizzata è", particle.pdgId, "con indice della madre:", particle.genPartIdxMother, "ed è:", genpart[0].pdgId)
        mom_id = particle.genPartIdxMother
        # se è un quark nella catena del top
        if abs(int(particle.pdgId)) in quark_flavs and mom_id!=-1: 
            # Print("è un quark")
            # se non è la propagazione di sè stessa
            if int(genpart[mom_id].pdgId) != int(particle.pdgId):
                mom = genpart[mom_id] 
                grandmom_id = mom.genPartIdxMother
                # Print("non è propagato e la madre è:",mom.pdgId)
                # se la madre è un w
                if abs(int(mom.pdgId))==24 and grandmom_id!=-1:
                    # Print("la madre è un w prodotto di decadimento")
                    grandmom = genpart[grandmom_id]
                    # Print("la nonna è:",grandmom.pdgId)
                    # se non è la propagazione di sè stessa
                    if int(grandmom.pdgId) != int(mom.pdgId):
                        # se la madre della w è un top
                        # print("non è propagato")
                        if abs(grandmom.pdgId) == 6:
                            # Print("la nonna è un top")
                            top = grandmom
                            top_id = grandmom_id
                            top_mom_id = top.genPartIdxMother
                            top_mom = genpart[top.genPartIdxMother]
                            # metti 1 nella posizione corrispondete al top
                            if genpart[top_id].pdgId!=6 and genpart[top_id].pdgId!=-6:
                                        print("1) il top è", top.pdgId, "e la madre del top è:",top_mom.pdgId)
                            is_hadronic_top[top_id]=int(1)
                            hadronic_top_idx.append(top_id)
                            # Print("salvato indice:",is_hadronic_top)
                            # fai lo stesso per i top da cui è stato propagato
                            while top_mom.pdgId==top.pdgId:
                                # print("1:",genpart[top_id].pdgId,genpart[top_mom_id].pdgId)
                                if genpart[top_id].pdgId!=6 and genpart[top_id].pdgId!=-6:
                                        print("2.0) il top è", top.pdgId, "e la madre del top è:",top_mom.pdgId)
                                top=top_mom
                                top_id = top_mom_id
                                top_mom_id = top_mom.genPartIdxMother
                                top_mom=genpart[top_mom.genPartIdxMother]
                                # print("2:",genpart[top_id].pdgId)
                                if genpart[top_id].pdgId!=6 and genpart[top_id].pdgId!=-6:
                                        print("2) il top è", top.pdgId, "e la madre del top è:",top_mom.pdgId)
                                is_hadronic_top[top_id]=int(1)
                                hadronic_top_idx.append(top_id)
                                # Print("salvato indice:",is_hadronic_top)

                    else:
                        # print("è propagato")
                        while (grandmom.pdgId==mom.pdgId): 
                            mom=grandmom
                            mom_id = grandmom_id
                            grandmom= genpart[mom.genPartIdxMother]  
                            grandmom_id = mom.genPartIdxMother
                            # Print("la nuova nonna è:",grandmom.pdgId)
                            # se la madre della w è un top
                            if abs(grandmom.pdgId) == 6:
                                top = grandmom
                                top_id = grandmom_id
                                top_mom_id = top.genPartIdxMother
                                top_mom = genpart[top.genPartIdxMother]
                                # print("la nonna era ", top.pdgId, "e la madre del top è:",top_mom.pdgId)
                                # metti 1 nella posizione corrispondete al top
                                if genpart[top_id].pdgId!=6 and genpart[top_id].pdgId!=-6:
                                        print("3) il top è", top.pdgId, "e la madre del top è:",top_mom.pdgId)
                                is_hadronic_top[top_id]=int(1)
                                hadronic_top_idx.append(top_id)
                                # Print("salvato indice:",is_hadronic_top)
                                # fai lo stesso per i top da cui è stato propagato
                                while top_mom.pdgId==top.pdgId:
                                    top=top_mom
                                    top_id = top_mom_id
                                    top_mom_id = top_mom.genPartIdxMother
                                    top_mom=genpart[top_mom.genPartIdxMother]
                                    if genpart[top_id].pdgId!=6 and genpart[top_id].pdgId!=-6:
                                        print("4) il top è", top.pdgId, "e la madre del top è:",top_mom.pdgId)
                                    is_hadronic_top[top_id]=int(1)
                                    hadronic_top_idx.append(top_id)
                                    # Print("salvato indice:",is_hadronic_top
    topgen = [particle for particle, is_hadr_top in zip(genpart, is_hadronic_top) if is_hadr_top==1]
    top_gen = topgen[0]
    if top_gen.pt <= pt_max and top_gen.pt >= pt_min:
    
        for t_m in topMixedNoRes:
            if t_m.truth ==1:
                true_top_prob = t_m.TTScore
                QCD_top_prob = t_m.QCDScore
        
                qcd_score = true_top_prob/(true_top_prob + QCD_top_prob)

                sig_mixed.Fill(qcd_score)
                label_true_mixed.append(t_m.truth)
                pred_true_mixed.append(qcd_score)


        topmerged_matched = matchingTopMerGenPart(genpart, topmerged)
        
        for top in topmerged: 
            # if top.pt < pt_max and top.pt > pt_min:
            if top in topmerged_matched:
                
                sig_merged.Fill(top.particleNetWithMass_TvsQCD)
                label_true_merged.append(1)
                pred_true_merged.append(top.particleNetWithMass_TvsQCD)
  

        for t_r in topresolved:

            if t_r.truth == 1:
                true_top_prob = t_r.TTScore
                QCD_top_prob = t_r.QCDScore

                qcd_score = true_top_prob/(true_top_prob + QCD_top_prob)
                
                sig_resolved.Fill(qcd_score)
                label_true_resolved.append(t_r.truth)
                pred_true_resolved.append(qcd_score)
    
   


chain2 = ROOT.TChain('Events')
chain2.Add(file_bkg_1)
# chain2.Add(file_bkg_2)
chain2.Add(file_bkg_3)
chain2.Add(file_bkg_4)
# chain2.Add(file_bkg_1)

tree_2 = InputTree(chain2)
print('num events is: ', tree_2.GetEntries())


for i in tqdm(range(tree_2.GetEntries())):
    # print('Event: ', i)
    event = Event(tree_2,i)
    topmixed = Collection(event, 'TopMixed')
    topresolved = Collection(event, 'TopResolved')
    topmerged = Collection(event, 'FatJet')
    genpart = Collection(event, "GenPart")
    topMixedNoRes = removeResolved(topmixed)
    is_hadronic_top = np.zeros(len(genpart), dtype=int)
    hadronic_top_idx =[]
    quark_flavs = [int(1),int(2),int(3),int(4)]
    
    
    
    for t_m in topMixedNoRes:
        
        if t_m.truth != 1:
            # n_mix +=1
            true_top_prob = t_m.TTScore
            QCD_top_prob = t_m.QCDScore
            # if t_m.truth ==1:
            qcd_score = true_top_prob/(true_top_prob + QCD_top_prob)

            bkg_mixed.Fill(qcd_score)
            label_false_mixed.append(t_m.truth)
            pred_false_mixed.append(qcd_score)


    topmerged_matched = matchingTopMerGenPart(genpart, topmerged)
   
    for top in topmerged: 
    
        # if top not in topmerged_matched:
            # n_mer += 1
        # print(top.particleNetWithMass_TvsQCD)
        bkg_merged.Fill(top.particleNetWithMass_TvsQCD)
        label_false_merged.append(0)
        pred_false_merged.append(top.particleNetWithMass_TvsQCD)
            
    
    for t_r in topresolved:
        # print(t_r.pt)
        # if t_r.pt < pt_max and t_r.pt > pt_min:
            # n_res += 1
        if t_r.truth != 1:
            # n_res += 1
            true_top_prob = t_r.TTScore
            QCD_top_prob = t_r.QCDScore

            qcd_score = true_top_prob/(true_top_prob + QCD_top_prob)

            bkg_resolved.Fill(qcd_score)
            label_false_resolved.append(t_r.truth)
            pred_false_resolved.append(qcd_score)
    # print('----------FINE EVENTO-----------')



print(len(label_true_merged))
print(len(label_false_merged))
print(len(pred_true_merged))
print(len(pred_false_merged))
label_resolved = label_true_resolved + label_false_resolved
pred_resolved = pred_true_resolved + pred_false_resolved


label_mixed = label_true_mixed + label_false_mixed
pred_mixed = pred_true_mixed + pred_false_mixed

label_merged = label_true_merged + label_false_merged
pred_merged = pred_true_merged + pred_false_merged

fpr_mixed, tpr_mixed, trs_mixed = roc_curve(label_mixed, pred_mixed)
fpr_resolved, tpr_resolved, trs_resolved = roc_curve(label_resolved, pred_resolved)
fpr_merged, tpr_merged, trs_merged = roc_curve(label_merged, pred_merged )


gr_mixed = ROOT.TGraph(len(fpr_mixed), fpr_mixed, tpr_mixed)
gr_resolved = ROOT.TGraph(len(fpr_resolved), fpr_resolved, tpr_resolved)
gr_merged = ROOT.TGraph(len(fpr_merged), fpr_merged, tpr_merged)
gr_mixed.SetTitle("Roc curve mixed")
gr_merged.SetTitle("Roc curve merged")
gr_resolved.SetTitle("Roc curve resolved")

gr_mixed.SetName("Roc_curve_mixed")
gr_merged.SetName("Roc_curve_merged")
gr_resolved.SetName("Roc_curve_resolved")
gr_mixed.GetXaxis().SetTitle("Background Efficiency")
gr_mixed.GetYaxis().SetTitle("Signal Efficiency")

sig_merged.Scale(1.0/(sig_merged.Integral()))
sig_mixed.Scale(1.0/(sig_mixed.Integral()))
sig_resolved.Scale(1.0/(sig_resolved.Integral()))

bkg_merged.Scale(1.0/(bkg_merged.Integral()))
bkg_mixed.Scale(1.0/(bkg_mixed.Integral()))
bkg_resolved.Scale(1.0/(bkg_resolved.Integral()))

# c1 = plotEfficiency(gr_merged, gr_mixed, gr_resolved)
# file_root_name = 'histos_roc_curve_200pt.root'
if pt_min == 0:
    file_root_name = 'histos_roc_curve_Pt'+str(pt_max)+'.root'
elif pt_max == 100000:
    file_root_name = 'histos_roc_curve_Pt'+str(pt_min)+'.root'
else:
    file_root_name = 'histos_roc_curve_Pt'+str(pt_min)+'to'+str(pt_max)+'.root'

file = ROOT.TFile(file_root_name, 'RECREATE')
gr_mixed.Write()
gr_merged.Write()
gr_resolved.Write()


sig_mixed.Write()
sig_merged.Write()
sig_resolved.Write()


bkg_mixed.Write()
bkg_merged.Write()
bkg_resolved.Write()
file.Close()
# c1.SetLogx()

# gr_mixed.SetLineColor(ROOT.kOrange)
# gr_merged.SetLineColor(ROOT.kRed)
# gr_resolved.SetLineColor(ROOT.kAzure)

# gr_mixed.SetLineStyle(1)
# gr_resolved.SetLineStyle(2)
# gr_merged.SetLineStyle(4)

# gr_merged.Draw()
# gr_mixed.Draw()
# gr_merged.Draw('SAME')
# gr_resolved.Draw('SAME')
# c1.Draw()
# c1.SaveAs('prova_roc.png')
# plt.savefig('prova_roc.png')