# import ROOT
# from PhysicsTools.NanoAODTools.postprocessing.get_file_fromdas import *
# from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event, InputTree
# import numpy as np 
# from samples import *
# from PhysicsTools.NanoAODTools.postprocessing.tools import *

# # list_files = get_files_string(TT_semilep_2024, option = 'phys03')


# # file_path = 'root://cms-xrd-global.cern.ch/' +'/store/mc/RunIII2024Summer24NanoAODv15/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/NANOAODSIM/150X_mcRun3_2024_realistic_v2-v2/2520000/004eb958-f042-48a7-b7a3-2f1cd5185215.root'
# file_path = '/eos/user/a/apuglia/TROTA_2024/PostProcessed_Datasets/TT_dilep_2024/file_0/file_0.root'
# file = ROOT.TFile.Open(file_path, 'READ')
# tree = file.Get('Events')

# # print('file_path is: ', file_path)


# # # tree.Print('SV*')
# tree = InputTree(tree)

# tree.Print("Indexes*")
# # break_ = False
# # # err = 0
# for i in range(5):
# # # #     errore = False
#     event = Event(tree,i)
#     print('########event: ', i, '######')
#     pfc = Collection(event, 'PFCand')
#     idxs_pfc = Collection(event, 'IndexesPFC')
#     tops = Collection(event, 'TopMixed')

#     print('n top is: ', len(tops))
#     print('n idx is :', len(idxs_pfc))
     
#     for idx in idxs_pfc:
#         print(idx.idxPFC)
# #     for fj in fatjets:
# #         print(fj.jetId)
#     if i ==1: 
#         break

#     PFCs = Collection(event, 'Jet')
#     SVs = Collection(event, 'SV')
# #     nsv = len(SVs)
#     print('---------------------EVENTO',i,'-----------------------------------------------------------')
# #     print('event: ', i, ' n svs: ', len(SVs))
#     for pf in PFCs:

#         print('pt is: ', pf.pt)
#     for sv in SVs:
#         print('n tracks is: ', sv.ntracks)


# #         print('jet index: ', idx, ' number of sv: ', jet.nSVs)
        
# #         if jet.svIdx1 != -1 or jet.svIdx2 != -1:
            
# #             if jet.svIdx1 != -1 and jet.svIdx1 < nsv:
# #                 sv_particle_1 = SVs[jet.svIdx1]
# #                 print('delta R is :', deltaR(sv_particle_1, jet))
# #                 print('SV 1:  eta: ', sv_particle_1.eta, ' phi: ', sv_particle_1.phi, ' chi2: ', sv_particle_1.chi2)
# #                 print('jet: eta: ', jet.eta, ' phi: ', jet.phi)
# #             if jet.svIdx2 != -1 and jet.svIdx2 < nsv:
# #                 sv_particle_2 = SVs[jet.svIdx2]
# #                 print('delta R is :', deltaR(sv_particle_2, jet))
# #                 print('SV 2:  eta: ', sv_particle_2.eta, ' phi: ', sv_particle_2.phi, ' chi2: ', sv_particle_2.chi2)
# #                 print('jet: eta: ', jet.eta, ' phi: ', jet.phi)
# #             if jet.svIdx1 >= nsv or jet.svIdx2 >= nsv:
# #                 print('ERRORE: indice sv1 ', jet.svIdx1, ' indice sv2: ', jet.svIdx2, ' numero di sv: ', nsv)
# #                 errore = True
# #     if errore : 
# #         err +=1
       
# # print('numeor di eventi: ', tree.GetEntries(), 'errori : ', err)
    


        

# # # #     n_sv = len(tree.SV_eta)
# # # #     for sv_idx_1, sv_idx_2 in zip(tree.Jet_svIdx1, tree.Jet_svIdx2):
# # # #         # print('sv idx 1: ', sv_idx_1)
# # # #         # print('sv idx 2: ', sv_idx_2)
# # # #         if sv_idx_1 > n_sv:
# # # #             print('sv idx 1 is: ', sv_idx_1, ' n sv is: ', n_sv)
# # # #         if sv_idx_2 > n_sv:
# # #             print('sv idx 2 is: ', sv_idx_2, ' n sv is: ', n_sv)

import pickle as pkl
path = "/eos/user/a/apuglia/TROTA/pkls/training_dataset_1.pkl"

with open(path, 'rb') as file:
    dict_pkl  =pkl.load(file)
# p_bkg_test
print(dict_pkl.keys())