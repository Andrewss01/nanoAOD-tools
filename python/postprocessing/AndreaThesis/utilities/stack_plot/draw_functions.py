#!/usr/local/bin/python
import os
from tqdm import tqdm
import numpy as np 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event, InputTree
import ROOT
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *

# no_files = ['nano_data2022CDE_229_20June_Selected.root', 'nano_data2022CDE_24_20June_Selected.root', 'nano_data2022CDE_355_20June_Selected.root', 
# 'nano_data2022CDE_404_20June_Selected.root']
# ', 'nano_data2022CDE_142_20June_Selected.root', 'nano_data2022CDE_188_20June_Selected.root', 
# 'nano_data2022CDE_397_20June_Selected.root', 'nano_data2022CDE_283_20June_Selected.root', 'nano_data2022CDE_315_20June_Selected.root', 'nano_data2022CDE_215_20June_Selected.root',
# 'nano_data2022CDE_276_20June_Selected.root', 'nano_data2022CDE_368_20June_Selected.root', 'nano_data2022CDE_61_20June_Selected.root']

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
no_files =[]

def get_pos_nums(num):
    pos_nums = []
    while num != 0:
        pos_nums.append(num % 10)
        num = num // 10
    return pos_nums 


def num_quark_match(top, jets, fatjets, resolved):
    
    if not resolved:
        
        idx_0,idx_1,idx_2,idx_fj = top.idxJet0, top.idxJet1, top.idxJet2, top.idxFatJet
        jet_0, jet_1 = jets[idx_0], jets[idx_1]
        if idx_2 != -1:
            jet_2 = jets[idx_2]
            fj = fatjets[idx_fj]
            flavs_j0, flavs_j1, flavs_j2, flavs_fj = jet_0.pdgId, jet_1.pdgId, jet_2.pdgId, fj.pdgId
            match_list = get_pos_nums(flavs_j0) + get_pos_nums(flavs_j1) + get_pos_nums(flavs_j2) + get_pos_nums(flavs_fj)

        elif idx_2 == -1:
            fj = fatjets[idx_fj]
            flavs_j0, flavs_j1, flavs_fj = jet_0.pdgId, jet_1.pdgId, fj.pdgId
            match_list = get_pos_nums(flavs_j0) + get_pos_nums(flavs_j1)  + get_pos_nums(flavs_fj)
        
        score_ft = top.TTScore/(top.FTScore + top.TTScore)
        score_qcd = top.TTScore/(top.QCDScore + top.TTScore)

        # print('match list is: ', len(np.unique(match_list)))
        len_match = len(np.unique(match_list))        
    
    else:
        idx_0,idx_1,idx_2 = top.idxJet0, top.idxJet1, top.idxJet2
        jet_0, jet_1, jet_2 = jets[idx_0], jets[idx_1], jets[idx_2]
        
        flavs_j0, flavs_j1, flavs_j2= jet_0.pdgId, jet_1.pdgId, jet_2.pdgId
        match_list = get_pos_nums(flavs_j0) + get_pos_nums(flavs_j1) + get_pos_nums(flavs_j2) 

        score_ft = top.TTScore/(top.FTScore + top.TTScore)
        score_qcd = top.TTScore/(top.QCDScore + top.TTScore)

        # print('match list is: ', len(np.unique(match_list)))
        len_match = len(np.unique(match_list))
        
    return len_match, score_ft, score_qcd


    


def best_top_candidate(topresolved, topmixed, pt_cut):
    best_score_ft, best_score_qcd = 0,0
    best_ft_idx, best_qcd_idx= 0,0
    best_ft, best_qcd = None, None
    for idx,top in enumerate(topmixed):
        if pt_cut:
            if top.pt >= 170:
                score_ft = top.TTScore/(top.FTScore + top.TTScore)
                score_qcd = top.TTScore/(top.QCDScore + top.TTScore)
                if score_ft > best_score_ft:
                    best_ft_idx = idx
                    best_score_ft = score_ft
                    best_ft = 'Mixed'
                if score_qcd > best_score_qcd:
                    best_qcd_idx = idx
                    best_score_qcd = score_qcd
                    best_qcd = 'Mixed'
        else:
            score_ft = top.TTScore/(top.FTScore + top.TTScore)
            score_qcd = top.TTScore/(top.QCDScore + top.TTScore)
            if score_ft > best_score_ft:
                best_ft_idx = idx
                best_score_ft = score_ft
                best_ft = 'Mixed'
            if score_qcd > best_score_qcd:
                best_qcd_idx = idx
                best_score_qcd = score_qcd
                best_qcd = 'Mixed'
    for idx,top in enumerate(topresolved):
        if pt_cut:
            # print('AHIA')
            if top.pt >= 170:
                score_ft = top.TTScore/(top.FTScore + top.TTScore)
                score_qcd = top.TTScore/(top.QCDScore + top.TTScore)
                if score_ft > best_score_ft:
                    best_ft_idx = idx
                    best_score_ft = score_ft
                    best_ft = 'Resolved'
                if score_qcd > best_score_qcd:
                    best_qcd_idx = idx
                    best_score_qcd = score_qcd
                    best_qcd = 'Resolved'
        else:
            score_ft = top.TTScore/(top.FTScore + top.TTScore)
            score_qcd = top.TTScore/(top.QCDScore + top.TTScore)
            if score_ft > best_score_ft:
                best_ft_idx = idx
                best_score_ft = score_ft
                best_ft = 'Resolved'
            if score_qcd > best_score_qcd:
                best_qcd_idx = idx
                best_score_qcd = score_qcd
                best_qcd = 'Resolved'

    # print(best_score_ft, best_score_qcd)
    if best_ft == 'Mixed':
        best_top_ft = topmixed[best_ft_idx]
    elif best_ft == 'Resolved':
        best_top_ft = topresolved[best_ft_idx]
    else:
        best_top_ft = None

    if best_qcd == 'Mixed':
        best_top_qcd = topmixed[best_qcd_idx]
    elif best_qcd == 'Resolved':
        best_top_qcd = topresolved[best_qcd_idx]
    else:
        best_top_qcd = None

    return best_top_ft, best_score_ft, best_top_qcd, best_score_qcd

def make_plot_scores_data(path_, color_ = ROOT.kBlack, style_ = ROOT.kCircle, file_options = 'best_single_top', pt_cut = True, model = 'lstm'):
    # histo1_ = ROOT.TH1F('ttvsft_scores' , 'ttvsft_scores' , 100,0,1)
    # histo2_ = ROOT.TH1F('ttvsqcd_scores', 'ttvsqcd_scores', 100,0,10)
    if file_options == 'best_single_top' or file_options == 'all_tops' or file_options == 'qcd_best' or file_options == 'qcd_all':
        bins , start, end = 100,0,1
    elif file_options == 'pt_best_top':
        bins, start, end = 300, 50, 850
    elif file_options == 'pt_top':
        bins,start,end = 300, 0 , 800
    elif file_options == 'met':
        bins, start,end = 200, 50,300
    elif file_options == 'mass_best_top':
        bins, start,end = 300,0,500

    histo1_ = ROOT.TH1F('ttvsft_scores', 'ttvsft_scores', bins, start, end)
    histo2_ = ROOT.TH1F('ttvsqcd_scores', 'ttvsqcd_scores', bins, start, end)


    for fileName in tqdm(os.listdir(path_)):
        
        if fileName.endswith('.root') and not fileName.startswith('.') and model in fileName:
            print('file name is: ',  fileName)

            file = ROOT.TFile.Open(path_+ fileName, 'READ')
 
            tree = InputTree(file.Get('Events'))

            if file_options == 'best_single_top':
                for i in range(tree.GetEntries()):
                    event = Event(tree,i)
                    tops = Collection(event, 'TopMixed')
                    topmixed = removeResolved(tops)
                    topresolved = Collection(event,'TopResolved')
                    # met = Object(event, 'MET')
                    # print('topmixed: ', len(topmixed))
                    # print('top resolved; ', len(topresolved))
                    # if met.pt >= 75:
                    best_top_ft, best_score_ft, best_top_qcd, best_score_qcd = best_top_candidate(topresolved, topmixed, pt_cut)
                    # print(best_score_ft, best_score_qcd)
                    if best_top_ft != None:
                        histo1_.Fill(best_score_ft)
                    if best_top_qcd != None:
                        histo2_.Fill(best_score_qcd)
                                
                
            elif file_options == 'all_tops':
                for i in range(tree.GetEntries()):
                    event = Event(tree,i)
                    tops  = Collection(event, 'TopMixed')
                    topmixed = removeResolved(tops)
                    topresolved = Collection(event,'TopResolved')
                    for top in topmixed:
                        if pt_cut:
                            if top.pt >= 170:
                                score_ft = top.TTScore/(top.FTScore + top.TTScore)
                                score_qcd = top.TTScore/(top.QCDScore + top.TTScore)

                                histo1_.Fill(score_ft)
                                histo2_.Fill(score_qcd)
                        else:
                            score_ft = top.TTScore/(top.FTScore + top.TTScore)
                            score_qcd = top.TTScore/(top.QCDScore + top.TTScore)

                            histo1_.Fill(score_ft)
                            histo2_.Fill(score_qcd)
                    
                    for top in topresolved:
                        if pt_cut:
                            if top.pt >= 160:
                                score_ft = top.TTScore/(top.FTScore + top.TTScore)
                                score_qcd = top.TTScore/(top.QCDScore + top.TTScore)

                                histo1_.Fill(score_ft)
                                histo2_.Fill(score_qcd)
                        else:
                            score_ft = top.TTScore/(top.FTScore + top.TTScore)
                            score_qcd = top.TTScore/(top.QCDScore + top.TTScore)

                            histo1_.Fill(score_ft)
                            histo2_.Fill(score_qcd)

            elif file_options == 'pt_best_top':
                for i in range(tree.GetEntries()):
                    event = Event(tree,i)
                    tops = Collection(event, 'TopMixed')
                    topmixed = removeResolved(tops)
                    topresolved = Collection(event,'TopResolved')
                    
                    best_top_ft, best_score_ft, best_top_qcd, best_score_qcd = best_top_candidate(topresolved, topmixed, pt_cut)
                    
                    if best_top_ft != None:
                        histo1_.Fill(best_top_ft.pt)
                    if best_top_qcd != None:
                        histo2_.Fill(best_top_qcd.pt)

                    

            elif file_options == 'mass_best_top':
            
                for i in range(tree.GetEntries()):
                    event = Event(tree,i)
                    tops = Collection(event, 'TopMixed')
                    topmixed = removeResolved(tops)
                    topresolved = Collection(event,'TopResolved')
                    
                    best_top_ft, best_score_ft, best_top_qcd, best_score_qcd = best_top_candidate(topresolved, topmixed, pt_cut)
                    
                    if best_top_ft != None:
                        histo1_.Fill(best_top_ft.mass)
                    if best_top_qcd != None:
                        histo2_.Fill(best_top_qcd.mass)



            elif file_options == 'met':
                for i in range(tree.GetEntries()):
                    event = Event(tree,i)
                    met = Object(event, 'MET')

                    histo1_.Fill(met.pt)
                    histo2_.Fill(met.phi)
            elif file_options == 'pt_top':
                for i in range(tree.GetEntries()):
                    event = Event(tree,i)
                    tops = Collection(event, 'TopMixed')

                    for top in tops:
                        if pt_cut:
                            if top.pt >= 160:
                                histo1_.Fill(top.pt)
                            if top.pt >= 160:
                                histo2_.Fill(top.pt)
                        else:
                            histo1_.Fill(top.pt)
                            histo2_.Fill(top.pt)
    
            elif file_options == 'qcd_best':
                for i in range(tree.GetEntries()):
                    event = Event(tree,i)
                    met = Object(event, 'MET')
                    tops = Collection(event, 'TopMixed')
                    topresolved = Collection(event, 'TopResolved')
                    topmixed = removeResolved(tops)     
                    # print(len(topresolved))
                    if met.pt >=   75: 
                    

                        # if len(topresolved) != 0:
                        #     print(len(topresolved))
                        # print('top resolved: ', len(topresolved))
                        # print('top mixed: ', len(topmixed))
                        # prin

                        best_top_ft, best_score_ft, best_top_qcd, best_score_qcd = best_top_candidate(topresolved, topmixed, pt_cut)
                    # # print(best_score_ft, best_score_qcd)
                        if best_top_ft != None:
                            histo1_.Fill(best_score_ft)
                        if best_top_qcd != None:
                            histo2_.Fill(best_score_qcd)

            elif file_options == 'qcd_all':
                for i in range(tree.GetEntries()):
                    event = Event(tree,i)
                    met = Object(event, 'MET')
                    tops = Collection(event, 'TopMixed')
                    topresolved = Collection(event, 'TopResolved')
                    topmixed = removeResolved(tops)     
                    # print(len(topresolved))
                    if met.pt <=   60: 
                        for top in topmixed:
                            score_qcd = top.TTScore/(top.TTScore + top.QCDScore)
                            score_ft = top.TTScore/(top.TTScore + top.FTScore)
                            if top.pt <= 100:
                                histo1_.Fill(score_ft)
                                histo2_.Fill(score_qcd)
                        for top in topresolved:
                            score_qcd = top.TTScore/(top.TTScore + top.QCDScore)
                            score_ft = top.TTScore/(top.TTScore + top.FTScore)
                            if top.pt <= 100:
                                histo1_.Fill(score_ft)
                                histo2_.Fill(score_qcd)

                            
                        

    
    histo1_.SetMarkerStyle(style_)
    histo1_.SetMarkerColor(color_)
    histo2_.SetMarkerStyle(style_)
    histo2_.SetMarkerColor(color_)
    return histo1_, histo2_


def make_plot_scores_mc(path_, dataset_, data_name, file_options = 'best_single_top', pt_cut = True, model = 'lstm'):
    num_tot_events  = 0
    
    data_name_ = data_name
    color_ = dataset_.color
    sigma_ = dataset_.sigma
    name_1 = 'ttvsft_scores_' + data_name_
    name_2 = 'ttvsqcd_scores_'+data_name_

    if file_options == 'best_single_top' or file_options == 'all_tops' or file_options == 'qcd_best' or file_options == 'qcd_all':
        bins , start, end = 100,0,1
    elif file_options == 'pt_best_top':
        bins, start, end = 300, 50, 850
    elif file_options == 'pt_top':
        bins,start,end = 300, 0 , 800
    elif file_options == 'met':
        bins, start,end = 200, 50,300
    elif file_options == 'mass_best_top':
        bins, start,end = 300,0,500

    histo1_ = ROOT.TH1F(name_1, name_1, bins, start, end)
    histo2_ = ROOT.TH1F(name_2, name_2, bins, start, end)
    

    print('dataset name is: ',  data_name_ ,' sigma is: ', sigma_,' color is: ', color_, 'model is: ', model)
    if data_name_ == 'WtoLNu_4Jets_2022' or data_name_ == 'WtoLNu_4Jets_2J_2022' or data_name_ == 'WtoLNu_4Jets_3J_2022':
        file_list = ['file_1', 'file_2', 'file_3', 'file_4', 'file_5', 'file_6','file_7', 'file_8', 'file_9', 'file_10', 'file_0' ]
    elif 'QCD_HT' in data_name_ :
        file_list = ['file_0', 'file_1', 'file_2', 'file_3', 'file_4', 'file_5', 'file_6', 'file_7', 'file_8', 'file_9', 'file_10', 'file_11', 'file_12', 'file_13', 'file_14', 'file_15', 'file_16', 'file_17', 'file_18', 'file_19', 'file_20', 'file_21', 'file_22', 'file_23', 'file_24', 'file_25', 'file_26', 'file_27', 'file_28', 'file_29']
    elif 'WtoLNu_4Jets_4J' in data_name_:
        file_list = ['file_1', 'file_2', 'file_3', 'file_4', 'file_5', 'file_6','file_7', 'file_0']
    elif data_name_ == 'TWmins_1L_2022' or data_name_ == 'TbarWplus_1L_2022' or data_name == 'TT_dilep_2022':
        file_list = ['file_0', 'file_1', 'file_2', 'file_3', 'file_4', 'file_5']
    else:
        file_list = ['file_0', 'file_1', 'file_2', 'file_3']

    for fileName in tqdm(os.listdir(path_ + data_name_)):
        
        
        if fileName  in file_list:

            
            file_events_name = 'histOut_'+fileName+'.root'
            file_event = ROOT.TFile.Open(path_+ data_name + '/' + fileName + '/'+file_events_name)
            if model == 'lstm':
                file_  =ROOT.TFile.Open(path_ + data_name_ + '/'+ fileName +'/'+ fileName+ '_'+model+'_model_sel_one_muon.root')
            else:
                file_  =ROOT.TFile.Open(path_ + data_name_ + '/'+ fileName +'/' + fileName+ '_'+model+'_model_sel_one_muon.root')
            # print('file path is: ', file)
            dir_plot = file_event.Get('plots')
            h_gen  =dir_plot.Get('h_genweight')
            num_tot_events += int(h_gen.GetBinContent(1))

            print('file name is: ', fileName, ' num_tot_events is: ', num_tot_events)
            # file = ROOT.TFile.Open(path_ + data_name_ + '/Scores/' + fileName, 'READ')
            tree = InputTree(file_.Get('Events'))
            
            print('num entries: ', tree.GetEntries())
            if file_options == 'best_single_top':
                for i in range(tree.GetEntries()):
                    event = Event(tree,i)
                    tops = Collection(event, 'TopMixed')
                    # print(len(tops))
                    topmixed = removeResolved(tops)
                    topresolved = Collection(event,'TopResolved')
                    # print('topmixed: ', len(topmixed))
                    # print('top resolved; ', len(topresolved))
                    # met = Object(event, 'MET')
                    
                    # if data_name == 'TT_hadronic_2022':
                        # print(len(topmixed), len(topresolved))
                    # if met.pt >= 75:
                    best_top_ft, best_score_ft, best_top_qcd, best_score_qcd = best_top_candidate(topresolved, topmixed, pt_cut)
                    # if data_name == 'TT_hadronic_2022':
                        # print(best_score_ft, best_score_qcd)
                    if best_top_ft != None:
                        histo1_.Fill(best_score_ft)
                    if best_top_qcd != None:
                        histo2_.Fill(best_score_qcd)

                    
                
            elif file_options == 'all_tops':
                for i in range(tree.GetEntries()):
                    event = Event(tree,i)
                    tops  = Collection(event, 'TopMixed')
                    topmixed = removeResolved(tops)
                    topresolved = Collection(event,'TopResolved')

                    
                    for top in topmixed:
                        if pt_cut:
                            if top.pt >= 170:
                                score_ft = top.TTScore/(top.FTScore + top.TTScore)
                                score_qcd = top.TTScore/(top.QCDScore + top.TTScore)

                                histo1_.Fill(score_ft)
                                histo2_.Fill(score_qcd)
                        else:
                            score_ft = top.TTScore/(top.FTScore + top.TTScore)
                            score_qcd = top.TTScore/(top.QCDScore + top.TTScore)

                            histo1_.Fill(score_ft)
                            histo2_.Fill(score_qcd)
                    
                    for top in topresolved:
                        if pt_cut:
                            if top.pt >= 160:
                                score_ft = top.TTScore/(top.FTScore + top.TTScore)
                                score_qcd = top.TTScore/(top.QCDScore + top.TTScore)

                                histo1_.Fill(score_ft)
                                histo2_.Fill(score_qcd)
                        else:
                            score_ft = top.TTScore/(top.FTScore + top.TTScore)
                            score_qcd = top.TTScore/(top.QCDScore + top.TTScore)

                            histo1_.Fill(score_ft)
                            histo2_.Fill(score_qcd)

            elif file_options == 'pt_best_top':
                for i in range(tree.GetEntries()):
                    event = Event(tree,i)
                    tops = Collection(event, 'TopMixed')
                    topmixed = removeResolved(tops)
                    topresolved = Collection(event,'TopResolved')
                    
                    best_top_ft, best_score_ft, best_top_qcd, best_score_qcd = best_top_candidate(topresolved, topmixed, pt_cut)
                    
                    if best_top_ft != None:
                        histo1_.Fill(best_top_ft.pt)
                    if best_top_qcd != None:
                        histo2_.Fill(best_top_qcd.pt)
            elif file_options == 'mass_best_top':
            
                for i in range(tree.GetEntries()):
                    event = Event(tree,i)
                    tops = Collection(event, 'TopMixed')
                    topmixed = removeResolved(tops)
                    topresolved = Collection(event,'TopResolved')


                    best_top_ft, best_score_ft, best_top_qcd, best_score_qcd = best_top_candidate(topresolved, topmixed, pt_cut)
                    
                    if best_top_ft != None:
                        histo1_.Fill(best_top_ft.mass)
                    if best_top_qcd != None:
                        histo2_.Fill(best_top_qcd.mass)



            elif file_options == 'met':
                for i in range(tree.GetEntries()):
                    event = Event(tree,i)
                    met = Object(event, 'MET')
                    # tops = Collection(tree, 'TopMixed')
                    # topresolved = Collection(tree, 'TopResolved')
                    # topmixed = removeResolved(tops)
                    histo1_.Fill(met.pt)
                    histo2_.Fill(met.phi)
            elif file_options == 'pt_top':
                for i in range(tree.GetEntries()):
                    event = Event(tree,i)
                    tops = Collection(event, 'TopMixed')

                    for top in tops:
                        if pt_cut:
                            if top.pt >= 160:
                                histo1_.Fill(top.pt)
                            if top.pt >= 160:
                                histo2_.Fill(top.pt)
                        else:
                            histo1_.Fill(top.pt)
                            histo2_.Fill(top.pt)            
            

            elif file_options == 'qcd_best':
                for i in range(tree.GetEntries()):
                    event = Event(tree,i)
                    tops = Collection(event, 'TopMixed')
                    topmixed = removeResolved(tops)
                    topresolved = Collection(event,'TopResolved')
                    
                    met = Object(event, 'MET')
                    # print('dataset: ', data_name)
                    if met.pt >= 75: 
                        # print('event passes')
                        # print('tm: ', len(topmixed))
                        # print('tr: ', len(topresolved))
                        best_top_ft, best_score_ft, best_top_qcd, best_score_qcd = best_top_candidate(topresolved, topmixed, pt_cut)
                    # print(best_score_ft, best_score_qcd)
                        if best_top_ft != None:
                            histo1_.Fill(best_score_ft)
                        if best_top_qcd != None:
                            histo2_.Fill(best_score_qcd)

            elif file_options == 'qcd_all':
                for i in range(tree.GetEntries()):
                    event = Event(tree,i)
                    tops = Collection(event, 'TopMixed')
                    topmixed = removeResolved(tops)
                    topresolved = Collection(event,'TopResolved')
                    
                    met = Object(event, 'MET')
                    # print('dataset: ', data_name)
                    if met.pt <= 60: 

                        for top in topmixed:
                            score_qcd = top.TTScore/(top.TTScore + top.QCDScore)
                            score_ft = top.TTScore/(top.TTScore + top.FTScore)
                            if top.pt <= 100:
                                histo1_.Fill(score_ft)
                                histo2_.Fill(score_qcd)
                        for top in topresolved:
                            score_qcd = top.TTScore/(top.TTScore + top.QCDScore)
                            score_ft = top.TTScore/(top.TTScore + top.FTScore)
                            if top.pt <= 100:
                                histo1_.Fill(score_ft)
                                histo2_.Fill(score_qcd)
                          
                    
            
    # histo1_.Scale((sigma_)/num_tot_events)
    # histo2_.Scale((sigma_)/num_tot_events)
    histo1_.SetFillColor(color_)
    histo2_.SetFillColor(color_)
    histo1_.SetLineColor(color_)
    histo2_.SetLineColor(color_)
    return histo1_, histo2_, num_tot_events, sigma_

def make_plot_tt(path_, dataset_, data_name,  pt_cut, model = 'lstm'):
    num_tot_events  = 0
    histo_0q_ft = ROOT.TH1F('ttvsft_scores_0quark_'+data_name, 'ttvsft_scores_0quark_'+data_name, 100, 0, 1)
    histo_0q_qcd = ROOT.TH1F('ttvsqcd_scores_0quark_'+data_name, 'ttvsqcd_scores_0quark_'+data_name, 100, 0, 1)
    histo_1q_ft = ROOT.TH1F('ttvsft_scores_1quark_'+data_name, 'ttvsft_scores_1quark_'+data_name, 100, 0, 1)
    histo_1q_qcd = ROOT.TH1F('ttvsqcd_scores_1quark_'+data_name, 'ttvsqcd_scores_1quark_'+data_name, 100, 0, 1)
    histo_2q_ft = ROOT.TH1F('ttvsft_scores_2quark_'+data_name, 'ttvsft_scores_2quark_'+data_name, 100, 0, 1)
    histo_2q_qcd = ROOT.TH1F('ttvsqcd_scores_2quark_'+data_name, 'ttvsqcd_scores_2quark_'+data_name, 100, 0, 1)
    histo_3q_ft = ROOT.TH1F('ttvsft_scores_3quark_'+data_name, 'ttvsft_scores_3quark_'+data_name, 100, 0, 1)
    histo_3q_qcd = ROOT.TH1F('ttvsqcd_scores_3quark_'+data_name, 'ttvsqcd_scores_3quark_'+data_name, 100, 0, 1)

    sigma_ = dataset_.sigma
    if data_name == 'TT_semilep_2022' or data_name == 'TT_hadronic_2022' :
    
        for fileName in tqdm(os.listdir(path_ + data_name)):
            if fileName == 'file_0' or fileName == 'file_1' or fileName == 'file_2' or fileName == 'file_3':
                file_events_name = 'histOut_'+fileName+'.root'
                file_event = ROOT.TFile.Open(path_+ data_name + '/' + fileName + '/'+file_events_name)
                if model == 'lstm':
                    file_  =ROOT.TFile.Open(path_ + data_name + '/'+ fileName +'/'+ fileName+ '_'+model+'_model_sel_one_muon.root')
                else:
                    file_  =ROOT.TFile.Open(path_ + data_name + '/'+ fileName +'/'+ fileName+ '_'+model+'_model_sel_one_muon.root')
                dir_plot = file_event.Get('plots')
                h_gen  =dir_plot.Get('h_genweight')
                num_tot_events += int(h_gen.GetBinContent(1))

                print('file name is: ', fileName, ' num_tot_events is: ', num_tot_events, 'model is: ', model, ' sigma is: ', sigma_)
                # file = ROOT.TFile.Open(path_ + data_name_ + '/Scores/' + fileName, 'READ')
                tree = InputTree(file_.Get('Events'))

                for i in range(tree.GetEntries()):
                    event = Event(tree,i)
                    tops = Collection(event, 'TopMixed')
                    topmixed = removeResolved(tops)
                    topresolved = Collection(event,'TopResolved')
                    jets = Collection(event, 'Jet')
                    fatjets = Collection(event, 'FatJet')

                    for top in topmixed:
                        num_quark, ft_score, qcd_score = num_quark_match(top, jets, fatjets,  resolved = False)

                        if num_quark == 1:
                            if pt_cut:
                                if top.pt >= 160: 
                                    histo_1q_ft.Fill(ft_score)
                                    histo_1q_qcd.Fill(qcd_score)
                            else: 
                                histo_1q_ft.Fill(ft_score)
                                histo_1q_qcd.Fill(qcd_score)
                        
                        elif num_quark == 2:
                            if pt_cut:
                                if top.pt >= 160: 
                                    histo_2q_ft.Fill(ft_score)
                                    histo_2q_qcd.Fill(qcd_score)
                            else: 
                                histo_2q_ft.Fill(ft_score)
                                histo_2q_qcd.Fill(qcd_score)

                        elif num_quark == 3:
                            if pt_cut:
                                if top.pt >= 160: 
                                    histo_3q_ft.Fill(ft_score)
                                    histo_3q_qcd.Fill(qcd_score)
                            else: 
                                histo_3q_ft.Fill(ft_score)
                                histo_3q_qcd.Fill(qcd_score)


                        elif num_quark == 0:
                            if pt_cut:
                                if top.pt >= 160: 
                                    histo_0q_ft.Fill(ft_score)
                                    histo_0q_qcd.Fill(qcd_score)
                            else: 
                                histo_0q_ft.Fill(ft_score)
                                histo_0q_qcd.Fill(qcd_score)
                    for top in topresolved:
                        num_quark, ft_score, qcd_score = num_quark_match(top, jets, fatjets,  resolved = True)

                        if num_quark == 1:
                            if pt_cut:
                                if top.pt >= 160: 
                                    histo_1q_ft.Fill(ft_score)
                                    histo_1q_qcd.Fill(qcd_score)
                            else: 
                                histo_1q_ft.Fill(ft_score)
                                histo_1q_qcd.Fill(qcd_score)
                        
                        elif num_quark == 2:
                            if pt_cut:
                                if top.pt >= 160: 
                                    histo_2q_ft.Fill(ft_score)
                                    histo_2q_qcd.Fill(qcd_score)
                            else: 
                                histo_2q_ft.Fill(ft_score)
                                histo_2q_qcd.Fill(qcd_score)

                        elif num_quark == 3:
                            if pt_cut:
                                if top.pt >= 160: 
                                    histo_3q_ft.Fill(ft_score)
                                    histo_3q_qcd.Fill(qcd_score)
                            else: 
                                histo_3q_ft.Fill(ft_score)
                                histo_3q_qcd.Fill(qcd_score)
                        elif num_quark == 0:
                            if pt_cut:
                                if top.pt >= 160: 
                                    histo_0q_ft.Fill(ft_score)
                                    histo_0q_qcd.Fill(qcd_score)
                            else: 
                                histo_0q_ft.Fill(ft_score)
                                histo_0q_qcd.Fill(qcd_score)
                        
    return histo_1q_ft, histo_1q_qcd, histo_2q_ft, histo_2q_qcd, histo_3q_ft, histo_3q_qcd, histo_0q_ft, histo_0q_qcd, sigma_, num_tot_events


