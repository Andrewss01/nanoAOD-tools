
import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event, InputTree 
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
from PhysicsTools.NanoAODTools.postprocessing.tools import *
import numpy as np



def fill_histo(sv_list, var_name, histo, type_histo):
    # if object_type == 'top':
    if var_name != 'nsv':
        sv_values = []
        for sv_idx in sv_list: 
            sv = SVs[sv_idx] 
            # print(type(sv))
            sv_var  = getattr(sv,var_name)
            sv_values.append(sv_var)
        
        if len(sv_values) != 0:
            if type_histo == '_mean_':
                histo.Fill(np.mean(sv_values))
            elif type_histo == '_max_':
                histo.Fill(np.max(sv_values))
            elif type_histo == '_max-mean_':
                histo.Fill(np.max(sv_values)/np.mean(sv_values))

    else:
        sv_values = len(sv_list)

        histo.Fill(sv_values)



    

def top_matched(top,jets, fatjets):
    # to_print = ['no', 'no', 'no', 'no']
    idx_jet0 = top.idxJet0
    if idx_jet0 != -1:
        jet0 = jets[idx_jet0]
        if '5' in str(abs(jet0.pdgId)):
            return False
        # else:
        # to_print[0] = jet0.pdgId

    idx_jet1 = top.idxJet1
    if idx_jet1 != -1:
        jet1 = jets[idx_jet1]
        if '5' in str(abs(jet1.pdgId)):
            return False    
        # else:
        # to_print[1] = jet1.pdgId
        
    idx_jet2 = top.idxJet2
    if idx_jet2 != -1:
        jet2 = jets[idx_jet2]
        if '5' in str(abs(jet2.pdgId)):
            return False
        # else:
        # to_print[2] = jet2.pdgId
        
    idx_fatjet = top.idxFatJet
    if idx_fatjet != -1:
        fatjet = fatjets[idx_fatjet]
        
        if '5' in str(abs(fatjet.pdgId)):
            return False
        # else: 
        # to_print[3] = fatjet.pdgId
    

    
    return True


from argparse import ArgumentParser
parser                      = ArgumentParser()
parser.add_argument("-inFile_to_open",                      dest="inFile_to_open",                      default=None    ,       required=True      ,       type=str,       help="path to root file to run")
parser.add_argument("-type_plot"     ,                      dest="type_plot"     ,                      default="_max-mean_" ,       required=False     ,       type=str,       help="wite _mean_ or _max_ and it will fill histogram with means or max of the feautres")  
parser.add_argument("-out_file"      ,                      dest="out_file"      ,                      default=None    ,       required=True      ,       type=str,       help="path of root file in which store histograms")
parser.add_argument("-variabili"     ,                      dest="variabili"     ,                      default=None    ,       required=True      ,       type=str,       help="variables to plot") 
parser.add_argument("-verbose"       ,                      dest="verbose"       ,                      default=False   ,       action="store_true",                       help="Default do not print")
parser.add_argument("-dataset"       ,                      dest="dataset"       ,                      default=None    ,       required=True      ,       type=str,       help="Component name of the dataset") 
options                     = parser.parse_args()

usage  = "python3 Analysis_SVs.py -inFile_to_open /eos/user/a/apuglia/thesis/Datasets/nano_mcRun3_ttsl1_Skim_total.root -out_file /eos/user/a/apuglia/thesis/SV_analysis.root -variabili dlen,dxy,ntracks,mass,z,nsv -dataset ttsl"
### ARGS ###
inFile_to_open              = options.inFile_to_open
type_plot                   = options.type_plot
verbose                     = options.verbose
out_file                    = options.out_file
data_name                   = options.dataset
variabili                   = (options.variabili).split(',')

dict_variabili = {}
for index in range(len(variabili)):
    dict_variabili[index]  = variabili[index]

print(dict_variabili)


components = ['true_tops', 'no_b_false_tops', 'b_false_tops', 'b_jets', 'no_b_jets']

histo_list = []
list_top, list_jet, list_fat_jet = [], [], []
for var_name in dict_variabili.values():
    
    for num,c in enumerate(components):
        #tt_true_tops_max_dlen
        #h_true_tops_max_dlen_ttsl
        histo = ROOT.TH1F(data_name+"_"+c+type_plot+var_name, data_name+"_"+c+type_plot+var_name, 100, 0 ,30)
        if num <= 2:
            list_top.append(histo) 
        elif num in range(3,5):
            list_jet.append(histo)
        # elif num in range(4,6):
        #     list_fat_jet.append(histo)
histo_list.append(list_top)
histo_list.append(list_jet)
    # histo_list.append(list_fat_jet)




rfile         = ROOT.TFile.Open(inFile_to_open)
tree          = InputTree(rfile.Get("Events"))

for i in range(tree.GetEntries()):
    event = Event(tree,i)
    SVs     = Collection(event, 'SV')
    jets    = Collection(event, 'Jet')
    fatjets = Collection(event, 'FatJet')
    tops    = Collection(event, 'TopMixed')
    indexes = Collection(event, 'IndexesSV')
    goodjets, goodfatjets = presel(jets, fatjets)
    N_SVs   = len(SVs)

    verbose = False
    if verbose:
        print('good jets is', len(goodjets), 'good fat jets is', len(goodfatjets))
        print('number of secondary vertexes is:' , len(SVs))
        print('number of jets is: ', len(jets), ' number of fat jets is ', len(fatjets))
        print('number of tops is: ', len(tops))

    sv_indexes = []
    for sv_idx in indexes:
        sv_indexes.append(sv_idx.idxSV) #qua prendiamo per ogni evento la lista degli indici sv

    
    for top_num, top in enumerate(tops):
        start_idx = sv_indexes.index(-(top_num + 1))
        stop_idx  = sv_indexes.index(-(top_num + 2))
        sv_to_append = sv_indexes[start_idx + 1: stop_idx]
        if top.truth == 1:
            # top_matched(top,jets,fatjets)
            for histo_idx in range(len(histo_list[0])):
                if histo_idx % 3 == 0: 
                    fill_histo(sv_list= sv_to_append, var_name= dict_variabili[histo_idx//3], type_histo= type_plot, histo = histo_list[0][histo_idx])
        else:
            if top_matched(top, jets, fatjets) :
                
                for histo_idx in range(len(histo_list[0])):
                    if histo_idx %3 == 1:
                        fill_histo(sv_list= sv_to_append, var_name= dict_variabili[histo_idx//3], type_histo= type_plot, histo= histo_list[0][histo_idx])

            if not top_matched(top,jets,fatjets):

                for histo_idx in range(len(histo_list[0])):
                    if histo_idx % 3 == 2:
                        fill_histo(sv_list= sv_to_append, var_name= dict_variabili[histo_idx//3], type_histo= type_plot, histo= histo_list[0][histo_idx])
            
    goodjets_idx, goodfatjets_idx = [], []
    for goodjet in goodjets:
        goodjets_idx.append(goodjet.jetIdx)
    for goodfatjet in goodfatjets:
        goodfatjets_idx.append(goodfatjet.fatjetIdx)

    jets_sv_index, fatjet_sv_index = list(np.zeros(len(jets))), list(np.zeros(len(fatjets)))
    
    for sv in SVs:
        jet_idx = sv.JetIdx
        fj_idx  = sv.FatJetIdx
        sv_idx = sv.Idx
        if jet_idx != -1 and jet_idx in goodjets_idx:
            if jets_sv_index[jet_idx] == 0.0:
                jets_sv_index[jet_idx] = [sv_idx]
            else:
                jets_sv_index[jet_idx].append(sv_idx)
        
        if fj_idx != -1 and fj_idx in goodfatjets_idx:
            if fatjet_sv_index[fj_idx] == 0.0:
                fatjet_sv_index[fj_idx] = [sv_idx]
            else: 
                fatjet_sv_index[fj_idx].append(sv_idx)
    # print(jets_sv_index)
#Adesso prendiamo per ogni jet 

    for jet_idx in range(len(jets_sv_index)):
        sv_index_jet = jets_sv_index[jet_idx]
        jet = jets[jet_idx]
        jet_pdgid = jet.pdgId

        if type(jets_sv_index[jet_idx]) == list:
            if '5' in str(abs(jet_pdgid)):
                for histo_idx in range(len(histo_list[1])):
                    if histo_idx %2 == 0:
                        fill_histo(sv_list= sv_index_jet, var_name= dict_variabili[histo_idx//2], type_histo= type_plot, histo = histo_list[1][histo_idx])
            else:
                for histo_idx in range(len(histo_list[1])):
                    if histo_idx %2 != 0:
                        fill_histo( sv_list= sv_index_jet, var_name= dict_variabili[histo_idx//2], type_histo= type_plot, histo= histo_list[1][histo_idx])
    
    # for jet_idx in range(len(jets_svs)):
    #     jet = jets[jet_idx]
    #     jet_pdgid = jet.pdgId
    #     if '5' in str(abs(jet_pdgid)):
    #         fill_dict(dict = SVs_bmatch_jets, object_type = 'jet', lista = jets_svs, obj_idx= jet_idx)
        
    #     else:
    #         fill_dict(dict = SVs_no_bmatch_jets, object_type= 'jet', lista=  jets_svs, obj_idx= jet_idx)

    
        # if len(sv_to_append) == 0:
        #     print('EVNTO', i, 'TOP NUMERO', top_num,  'NON CI SONO SVS')
        #     print(sv_indexes[start_idx - 1: stop_idx +1])
        
            # fill_dict(dict = SVs_true_tops, lista = indexes, obj_idx= top_num, histo = h_len_true_tops)
        # elif top.truth == 0 and top_num <= 5:
        #     fill_dict(dict = SVs_false_tops, object_type= 'top', lista = indexes, obj_idx= top_num, histo= h_len_false_tops)


           
    # for fatjet_idx in range(len(fatjets_svs)):
    #     fatjet = fatjets[fatjet_idx]
    #     fatjet_pdgId = fatjet.pdgId
    #     if '5' in str(abs(fatjet_pdgId)):
    #         SVs_bmatch_fatjets['nsv'] += 1
    #         SVs_bmatch_fatjets['dlen'].append(sv.dlen)
    #         SVs_bmatch_fatjets['dxy'].append(sv.dxy)
    #         SVs_bmatch_fatjets['ntracks'].append(sv.ntracks)
    #     else:
    #         SVs_no_bmatch_fatjets['nsv'] +=1 
    #         SVs_no_bmatch_fatjets['dlen'].append(sv.dlen)
    #         SVs_no_bmatch_fatjets['dxy'].append(sv.dxy)
    #         SVs_no_bmatch_fatjets['ntracks'].append(sv.ntracks)


 
# print(SVs_bmatch_jets['nobj'])
# print('media delle dl sul numero di jets:', len(SVs_bmatch_jets['dlen'])/SVs_bmatch_jets['njets'])
# print('JET B MATCHED')
# print('media delle dl', np.mean(SVs_bmatch_jets['dlen']))
# print('media del n tracks', np.mean(SVs_bmatch_jets['ntracks']))
# print('media del dxy', np.mean(SVs_bmatch_jets['dxy']))
# print('numero medio di secondary vertexes per jet', SVs_bmatch_jets['nsv']/SVs_bmatch_jets['nobj'])

# print('JET NO B MATCHED')
# print('media delle dl', np.mean(SVs_no_bmatch_jets['dlen']))
# print('media del n tracks', np.mean(SVs_no_bmatch_jets['ntracks']))
# print('media del dxy', np.mean(SVs_no_bmatch_jets['dxy']))
# print('numero medio di secondary vertexes per jet', SVs_no_bmatch_jets['nsv']/SVs_no_bmatch_jets['nobj'])


# print(SVs_true_tops['nobj'])
# print('media delle dl sul numero di jets:', len(SVs_true_tops['dlen'])/SVs_true_tops['njets'])
# print('TRUE TOPS')
# print('media delle dl', np.mean(SVs_true_tops['dlen']), 'valore massimo dlen', np.max(SVs_true_tops['dlen']))
# print('media del n tracks', np.mean(SVs_true_tops['ntracks']), 'valore massimo ntracks', np.max(SVs_true_tops['ntracks']))
# print('media del dxy', np.mean(SVs_true_tops['dxy']), 'valore massimo dxy', np.max(SVs_true_tops['dxy']))
# print('numero medio di secondary vertexes per true top', SVs_true_tops['nsv']/SVs_true_tops['nobj'])

# print('FALSE TOPS')
# print('media delle dl', np.mean(SVs_false_tops['dlen']), 'valore massimo dlen', np.max(SVs_false_tops['dlen']))
# print('media del n tracks', np.mean(SVs_false_tops['ntracks']), 'valore massimo n tracks', np.max(SVs_false_tops['ntracks']))
# print('media del dxy', np.mean(SVs_false_tops['dxy']), 'valore massimo dxy', np.max(SVs_false_tops['dxy']))
# print('numero medio di secondary vertexes per false top', SVs_false_tops['nsv']/SVs_false_tops['nobj'])



# h_len_false_tops.SetLineColor(3)
# h_len_false_tops.Scale(1.0/h_len_false_tops.Integral())
# h_len_false_tops.Draw('hist')
# h_len_true_tops.Scale(1.0/h_len_true_tops.Integral())
# h_len_true_tops.Draw('SAMEhist')
# c1.Draw()
# c1.SaveAs('/eos/user/a/apuglia/thesis/true_top_dlen.png')
    
   

# mean_SVs = mean_SVs_per_event/(tree.GetEntries())
# mean_SVs_per_bjet = mean_SVs_per_bjet/num_bjet
# mean_SVs_per_nobjet = mean_SVs_per_nobjet/num_nobjet
# mean_SVs_per_bfatjet = mean_SVs_per_bfatjet/num_bfatjet
# print('numero medio di sv per evento:'                        , mean_SVs           )
# print('numero medio di sv per jets matchati con il bottom'    , mean_SVs_per_bjet/num_bjet  )
# print('numero medio di sv per jets non matchati con il bottom', mean_SVs_per_nobjet/num_nobjet)
# print('numero medio di sv per fatjet matchati con bottom ', mean_SVs_per_bfatjet/num_bfatjet)
# print('numero medio di sv per fatjet non matchati con il bottom ', mean_SVs_per_nobfatjet/num_nobfatjet )
# print('jets pfcs is', jets_pfcs)
# print('jets sv is: ', jets_svs)
# # mean_svs_b = sv_jet_b/(tree.GetEntries())
# mean_svs_no_b = sv_jet_no_b/(tree.GetEntries())
# print('numero medio di sv per i jet con un bottom: ', mean_svs_b)
# print('numero medio di sv per i jet senza bottom: ', mean_svs_no_b)

# print(jetsv_max_jet, jetsv_min_jet)
# print(jetsv_max_sv, jetsv_min_sv)
# print(jetpfc_max_jet, jetpfc_min_jet)
# print(jetpfc_max_pfc, jetpfc_min_pfc)
# print('SVS jets b matched', SVs_bmatch_jets['dlen'])
# print('SVS no b match jets', SVs_no_bmatch_jets)
# SVs_bmatch_jets['dlen'] = np.mean(SVs_bmatch_jets['dlen'])
# print(SVs_bmatch_jets['dlen'])
# print(SVs_bmatch_jets['nsv'])

if type_plot == '_mean_':
    file_tops = ROOT.TFile('/eos/user/a/apuglia/thesis/tops_histos'+type_plot+ '.root'   , 'UPDATE')
    file_jets = ROOT.TFile('/eos/user/a/apuglia/thesis/jet_histos' + type_plot + '.root' , 'UPDATE')

elif type_plot == '_max_': 
    file_tops = ROOT.TFile('/eos/user/a/apuglia/thesis/tops_histos'+type_plot+ '.root'   , 'UPDATE')
    file_jets = ROOT.TFile('/eos/user/a/apuglia/thesis/jet_histos' + type_plot + '.root' , 'UPDATE')

elif type_plot == '_max-mean_':
    file_tops = ROOT.TFile('/eos/user/a/apuglia/thesis/tops_histos_'+type_plot+ '.root'   , 'RECREATE')
    file_jets = ROOT.TFile('/eos/user/a/apuglia/thesis/jet_histos_' +type_plot+ '.root' , 'RECREATE')
file_tops.cd()

for histo in histo_list[0]:
    histo.Write()


file_tops.Close()

file_jets.cd()
for histo in histo_list[1]:
    histo.Write()

file_jets.Close()