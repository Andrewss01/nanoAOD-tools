import ROOT 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event, InputTree 
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
from PhysicsTools.NanoAODTools.postprocessing.tools import *
import numpy as np
import pickle as pkl

file_pkl = open('/eos/user/a/apuglia/thesis/training_dataset/pkls_3/trainingSet_TT_mini.pkl', 'rb')
pkl_tt  = pkl.load(file_pkl)

file_tt = ROOT.TFile("/eos/user/a/apuglia/thesis/Datasets/nano_mcRun3_ttsl1_mini.root")
# # file_tt = ROOT.TFile("/eos/user/a/apuglia/thesis/Datasets/ZtoNu_4Jets_800to1500_Skim.root")
tree_tt = file_tt.Get('Events')
tree_tt = InputTree(tree_tt)

number_tops = {'2j1fj':0, '3j1fj': 0 ,'3j0fj':0}
# num_true_tops = 0
# num_tot_tops = 0
for i in range(5):
    event = Event(tree_tt,i)

    tops = Collection(event, 'TopMixed')
    jets = Collection(event, 'Jet')
    fatjets = Collection(event, 'FatJet')
    print(' ------------------ Event ', i, ' ------------------')
    
    for index in range(len(tops)):
        # num_tot_tops +=1

        top = tops[index]
        print('___ top ', index, ' ___')
        
        
        # print('true tops: ', num_true_tops)


        
        idx_fatjet, idx_jet0, idx_jet1, idx_jet2 = top.idxFatJet, top.idxJet0, top.idxJet1, top.idxJet2
        jet0, jet1 = jets[idx_jet0], jets[idx_jet1]
        if idx_jet2 == -1:
            if idx_fatjet == -1:
                print('ERRORE')
            
            fatjet = fatjets[idx_fatjet]
            c = '2j1fj'
            number_tops[c] += 1
        elif idx_fatjet == -1:
            c = '3j0fj'
            number_tops[c] +=1
            jet2 = jets[idx_jet2]
        else:
            c = '3j1fj'
            number_tops[c] +=1
        # print('FILE ROOT')
        num_top = number_tops[c]
        print('component: ', c, 'num tops: ', num_top)
        print('file root top pt : '   , top.pt    , ' file pkl top pt: '    , pkl_tt['TT_mini'][c][2][num_top -1 ,2])
        print('file root top truth: ' , top.truth , ' file pkl top truth: ' , pkl_tt['TT_mini'][c][3][num_top -1 ])
        print('file root top mass: '  , top.mass  , ' file pkl top mass: ' , pkl_tt['TT_mini'][c][2][num_top -1 ,1])

        print('file root jet0 btagPNetB: '   , jet0.btagPNetB   , ' file pkl jet0 btagPNetB '    , pkl_tt['TT_mini'][c][0][num_top -1 , 0,1])
        print('file root jet0 area: '   , jet0.area   , ' file pkl jet0 area '    , pkl_tt['TT_mini'][c][0][num_top -1 , 0,0])
        print('file root jet0 mass: '   , jet0.mass   , ' file pkl jet0 mass '    , pkl_tt['TT_mini'][c][0][num_top -1 , 0,3])
        print('file root jet0 pt: '   , jet0.pt   , ' file pkl jet0 pt '    , pkl_tt['TT_mini'][c][0][num_top -1 , 0,5])
        print('file root jet1 btagPNetB: '   , jet1.btagPNetB   , ' file pkl jet1 btagPNetB '    , pkl_tt['TT_mini'][c][0][num_top -1 , 1,1])
        print('file root jet1 area: '   , jet1.area   , ' file pkl jet1 area '    , pkl_tt['TT_mini'][c][0][num_top -1 , 1,0])
        print('file root jet1 mass: '   , jet1.mass   , ' file pkl jet1 mass '    , pkl_tt['TT_mini'][c][0][num_top -1 , 1,3])
        print('file root jet1 pt: '   , jet1.pt   , ' file pkl jet1 pt '    , pkl_tt['TT_mini'][c][0][num_top -1 , 1,5])

        if c == '3j0fj' or c == '3j1fj':
            print('file root jet2 btagPNetB: '   , jet2.btagPNetB   , ' file pkl jet2 btagPNetB '    , pkl_tt['TT_mini'][c][0][num_top -1 , 2,1])
            print('file root jet2 area: '   , jet2.area   , ' file pkl jet2 area '    , pkl_tt['TT_mini'][c][0][num_top -1 , 2,0])
            print('file root jet2 mass: '   , jet2.mass   , ' file pkl jet2 mass '    , pkl_tt['TT_mini'][c][0][num_top -1 , 2,3])
            print('file root jet2 pt: '   , jet2.pt   , ' file pkl jet2 pt '    , pkl_tt['TT_mini'][c][0][num_top -1 , 2,5])
        elif c == '2j1fj' or c == '3j1fj':
            
            print('file root fatjet area: ' ,      fatjet.area, 'file pkl fatjet area: ' , pkl_tt['TT_mini'][c][1][num_top -1, 0])
            print('file root fatjet btagDeepB: ' , fatjet.btagDeepB, 'file pkl fatjet btagDeepb: ' , pkl_tt['TT_mini'][c][1][num_top -1, 1])
            print('file root fatjet particleNetWithMass_QCD: ' , fatjet.particleNetWithMass_QCD, 'file pkl fatjet particleNetWithMass_QCD: ' , pkl_tt['TT_mini'][c][1][num_top -1, 2])
            print('file root fatjet particleNetWithMass_TvsQCD: ', fatjet.particleNetWithMass_TvsQCD,  'file pkl fatjet particleNetWithMass_TvsQCD: ' , pkl_tt['TT_mini'][c][1][num_top -1, 3])
            print('file root fatjet particleNetWithMass_WvsQCD: ', fatjet.particleNetWithMass_WvsQCD,  'file pkl fatjet particleNetWithMass_WvsQCD: ' , pkl_tt['TT_mini'][c][1][num_top -1, 4])
            print('file root fatjet eta: ', fatjet.eta, ' file pkl fatjet eta: ', pkl_tt['TT_mini'][c][1][num_top -1, 5] )
            print('file root fatjet mass: '  , fatjet.mass,    ' file pkl fatjet mass:   ',   pkl_tt['TT_mini'][c][1][num_top -1, 6])
            print('file root fatjet phi: '  , fatjet.phi,    ' file pkl fatjet phi:   ',   pkl_tt['TT_mini'][c][1][num_top -1, 7])
            print('file root fatjet pt: ' , fatjet.pt, 'file pkl fatjet pt: ' , pkl_tt['TT_mini'][c][1][num_top -1, 8])
        

        



