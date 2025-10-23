import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, InputTree, Event
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.tools import *
import numpy as np

file_path = '/eos/user/a/apuglia/Master_Thesis/PostProcessed_Datasets/TT_semilep_2022/file_0/file_0.root'
file = ROOT.TFile(file_path, 'READ')

def get_pos_nums(num):
    pos_nums = []
    while num != 0:
        pos_nums.append(num % 10)
        num = num // 10
    return pos_nums 

tree = InputTree(file.Get('Events'))
for i in range(tree.GetEntries()):
    event=  Event(tree,i)
    topmixed = Collection(event, 'TopMixed')
    jets = Collection(event, 'Jet')
    fatjets = Collection(event, 'FatJet')
    

    for idx,top in enumerate(topmixed):
        if top.truth == 1:
            print('top num: ', idx, ' truth is: ', top.truth)

            top_idx0, top_idx1, top_idx2 = top.idxJet0, top.idxJet1, top.idxJet2
            top_idxfj = top.idxFatJet
            jet0, jet1, jet2, fatjet = jets[top_idx0], jets[top_idx1], jets[top_idx2], fatjets[top_idxfj]
            print(' jet 0 matching: ', jet0.matched, ' jet 0 pdgId: ', jet0.pdgId)
            print(' jet 1 matching: ', jet1.matched, ' jet 1 pdgId: ', jet1.pdgId)
            if top_idx2 != -1:
                print(' jet 2 matching: ', jet2.matched, ' jet 2 pdgId: ', jet2.pdgId)

            if top_idxfj != -1:
                print(' fatjet matching: ', fatjet.matched, ' fatjet pdgId: ', fatjet.pdgId)

            if top_idx2 == -1: 
                len_match = get_pos_nums(jet0.pdgId) + get_pos_nums(jet1.pdgId) + get_pos_nums(fatjet.pdgId)
            elif top_idxfj == -1:
                len_match = get_pos_nums(jet0.pdgId) + get_pos_nums(jet1.pdgId) + get_pos_nums(jet2.pdgId) 
            else:
                len_match = get_pos_nums(jet0.pdgId) + get_pos_nums(jet1.pdgId) + get_pos_nums(fatjet.pdgId) + get_pos_nums(jet2.pdgId)
                # print('len match is: ', len)
            if len(np.unique(len_match)) == 1 or len(np.unique(len_match)) == 2 or len(np.unique(len_match)) == 0:

                print('len match is: ', len_match, ' num quark matched is: ', len(np.unique(len_match)))
