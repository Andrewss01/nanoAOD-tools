import ROOT
import numpy as np
import cmsstyle as CMS
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event
from PhysicsTools.NanoAODTools.postprocessing.tools import *
from sklearn.metrics import  roc_curve
# x_msd_t32 = np.array([0.0258964143426295, 0.045019920318725114, 0.0705179282868526, 0.10239043824701195, 0.14302788844621514, 0.19083665338645417, 0.23864541832669323, 0.2928286852589641, 0.33027888446215137, 0.013944223107569736, 0.017928286852589653, 0.035458167330677304, 0.056175298804780886, 0.0856573705179283, 0.1207171314741036, 0.1645418326693227, 0.2649402390438247, 0.21314741035856571, 0.035458167330677304])
x_msd_t32 = np.array([0.012350597609561767, 0.015537848605577706, 0.0203187250996016, 0.02509960159362551, 0.030677290836653395, 0.03944223107569722, 0.050597609561753, 0.06095617529880479, 0.07131474103585658, 0.08964143426294821, 0.10637450199203188, 0.1207171314741036, 0.14382470119521912, 0.16613545816733066, 0.18685258964143425, 0.21235059760956176, 0.2394422310756972, 0.2641434262948207, 0.28725099601593623, 0.3095617529880478, 0.33027888446215137])
y_msd_t32 = np.array([0.00011048957413047087, 0.0001566555726096109, 0.00024136343622617362, 0.00039089288159860726, 0.0006330587899870699, 0.0009434724909899058, 0.0014296662239690915, 0.002433781516179539, 0.0035673569774893063, 0.0054963224351931616, 0.008056328827945184, 0.01161400341661846, 0.017023424596426327, 0.021484733148877305, 0.02803195772977552, 0.035378259412695706, 0.04177713255853416, 0.05016040228087699, 0.05729579419317218, 0.06330587899870703, 0.06879313896675654])
# y_msd_t32 = np.array([0.00039089288159860726 ,0.0011710948139520582 ,0.0030715997313938968 ,0.007538003203664389 ,0.01566555726096109 ,0.028501889118902342 ,0.04318958801846273 ,0.05729579419317218 ,0.06654335495173698 ,0.00011234183573687349 ,0.00019771011142544198 ,0.0006994639610522263 ,0.0018966113244341676 ,0.004892498328108703 ,0.010866785210921978 ,0.021484733148877305 ,0.05016040228087699 ,0.034794952302021724 ,0.0006994639610522263])

x_hotvr = np.array([0.0203187250996016, 0.02509960159362551, 0.032270916334661365, 0.04103585657370519, 0.05219123505976097, 0.06414342629482073, 0.07928286852589642, 0.09760956175298806, 0.11354581673306774, 0.1302788844621514, 0.14621513944223108, 0.1653386454183267, 0.18127490039840638, 0.20119521912350596, 0.21872509960159361, 0.23864541832669323, 0.2593625498007968, 0.27609561752988043, 0.30079681274900394, 0.3199203187250996, 0.3374501992031872])
y_hotvr = np.array([0.00011234183573687349, 0.00014903394533218248, 0.00022211116861275984, 0.0003149161590661423, 0.0004247748984810421, 0.000643671469966306, 0.0008975705447453805, 0.001251621239071992, 0.0017165522985857155, 0.002277197624101913, 0.002922159862079623, 0.0038126543702379227, 0.004811832147490379, 0.005972735535321572, 0.007171263292167201, 0.009356623053315716, 0.01161400341661846, 0.013714630632654051, 0.017894006107035704, 0.02184490601268505, 0.028979698499021284])
# x_hotvr = np.array([0.04103585657370519, 0.06892430278884464, 0.14382470119521912, 0.200398406374502, 0.24661354581673306, 0.29203187250996016, 0.3334661354581673, 0.11274900398406375, 0.08406374501992032, 0.019521912350597623, 0.029880478087649417, 0.09840637450199204, 0.12709163346613547, 0.17649402390438246, 0.22669322709163345, 0.2697211155378486, 0.16135458167330677, 0.3087649402390438, 0.05378486055776893])

x_image_top = np.array([0.03784860557768926, 0.04422310756972113, 0.049800796812749015, 0.059362549800796825, 0.06812749003984064, 0.07768924302788846, 0.08804780876494024, 0.09840637450199204, 0.11434262948207172, 0.1302788844621514, 0.14701195219123506, 0.16294820717131475, 0.17888446215139442, 0.19322709163346613, 0.20836653386454185, 0.22669322709163345, 0.24900398406374502, 0.2689243027888446, 0.28406374501992027, 0.29840637450199203, 0.3143426294820717, 0.3318725099601594, 0.33027888446215137])
y_image_top = np.array([0.00011422514889800926, 0.0001566555726096109, 0.00020782104806410425, 0.00030461726369111433, 0.000453983126241806, 0.0005729579419317218, 0.0007231123454746664, 0.0009434724909899058, 0.0013156294122130656, 0.0017453288048133347, 0.0022396518095649824, 0.0028265946844212024, 0.0035673569774893063, 0.004428018088232854, 0.005405700567067713, 0.0069367370913783226, 0.009513478700408475, 0.01262068805673068, 0.01619519873061116, 0.02184490601268505, 0.03149161590661423, 0.06879313896675654, 0.06879313896675654])

x_bdt = np.array([0.03705179282868527, 0.046613545816733076, 0.05697211155378487, 0.07131474103585658, 0.08486055776892432, 0.10159362549800798, 0.1199203187250996, 0.13745019920318724, 0.15258964143426296, 0.16852589641434262, 0.1884462151394422, 0.20677290836653386, 0.22749003984063745, 0.25219123505976093, 0.2752988047808765, 0.2936254980079681, 0.31673306772908366, 0.33665338645418325, 0.3565737051792829, 0.37569721115537846, 0.39641434262948205, 0.41633466135458164, 0.4370517928286852, 0.4569721115537848])
y_bdt = np.array([0.00011422514889800926, 0.0001619519873061115, 0.0002184490601268505, 0.0003255632528481172, 0.000453983126241806, 0.0006654335495173698, 0.0009279167733866198, 0.0012309848487932974, 0.0016061132809169186, 0.002095557775277597, 0.002779990560708306, 0.003687966807120607, 0.004974516807081604, 0.006599250056916111, 0.008056328827945184, 0.009672963895991604, 0.01161400341661846, 0.013488507536122527, 0.016466697150736738, 0.019124427696907795, 0.022962059095951007, 0.02711521150540814, 0.034221262600203084, 0.046933197634484364])


x_pn = np.array([0.1405152224824356, 0.1667447306791569, 0.18735362997658078, 0.2173302107728337, 0.2641686182669789, 0.2997658079625293, 0.33911007025761125, 0.38220140515222484, 0.4252927400468384, 0.477751756440281, 0.5227166276346604, 0.5733021077283372, 0.623887587822014, 0.6763466042154567, 0.7306791569086651, 0.7812646370023419, 0.818735362997658, 0.8562060889929742, 0.9011709601873537, 0.936768149882904, 0.9629976580796253, 0.985480093676815, 0.9967213114754099])*0.4

y_pn = np.array([0.00010731275413652415, 0.0001349796194000715, 0.00022916762119310944, 0.0003319500947418161, 0.00048083086443633194, 0.000649023670774234, 0.0008916441630011479, 0.0011215236318422607, 0.001596118510044297, 0.002154434690031882, 0.002959813643842183, 0.003925271777941393, 0.0052056515661918846, 0.007151647994711385, 0.010543589908346803, 0.015272426579169, 0.0198998853689599, 0.02639100559103041, 0.03890794687133388, 0.05537261313624339, 0.08163518751116162, 0.12467674075409112, 0.20433597178569418])


y_TROTA = np.array([0.021601562499999998, 0.047705078125, 0.070908203125, 0.09701171874999999, 0.125048828125, 0.152119140625, 0.175322265625, 0.202392578125, 0.233330078125, 0.264267578125, 0.293271484375, 0.326142578125, 0.36384765625, 0.397685546875, 0.4315234375, 0.461494140625, 0.494365234375, 0.52626953125, 0.5591406250000001, 0.587177734375, 0.620048828125, 0.649052734375, 0.682890625, 0.7176953125, 0.741865234375, 0.767001953125, 0.794072265625, 0.82984375, 0.8646484375, 0.886884765625, 0.906220703125, 0.938125, 0.958427734375])
x_TROTA = np.array([0.6729064039408866, 0.6847290640394088, 0.6945812807881773, 0.696551724137931, 0.7103448275862069, 0.716256157635468, 0.7261083743842365, 0.7359605911330049, 0.7399014778325123, 0.747783251231527, 0.747783251231527, 0.7596059113300493, 0.7635467980295566, 0.767487684729064, 0.7793103448275862, 0.787192118226601, 0.787192118226601, 0.7931034482758621, 0.7990147783251231, 0.8029556650246306, 0.8068965517241379, 0.8068965517241379, 0.8088669950738916, 0.8147783251231526, 0.8147783251231526, 0.8147783251231526, 0.8167487684729063, 0.81871921182266, 0.8206896551724138, 0.8206896551724138, 0.8206896551724138, 0.8167487684729063, 0.81871921182266])

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


def draw_stack_qcd ( canv_name = "QCD Scores" ,extraTest="", iPos=11, energy="", lumi = "",  addInfo="", ytitle = ""):
    CMS.SetExtraText(extraTest)
    iPos = iPos
    canv_name = canv_name
    CMS.SetLumi(lumi)
    
    CMS.SetEnergy(energy)
    CMS.ResetAdditionalInfo()
    CMS.AppendAdditionalInfo(addInfo)
    CMS.setCMSStyle()
    



    
    y_max= 1 # Aggiungi 20% di margine
    x_max = 1
    # x_max_stack = hs_ft.GetXaxis().GetXmax()

    # x_max = max(x_max_stack, x_max_data)
    x_min = 0
    # x_max = 1
    y_min = 10**(-4)
    # y_max = 10**6
    x_axis_name = 'Signal Efficiency'
    ytitle = 'Background Efficiency '

    canv = CMS.cmsCanvas(canv_name,x_min,x_max, y_min ,y_max,x_axis_name,ytitle,square=CMS.kRectangular, extraSpace=20.0, iPos=iPos)
    hdf = CMS.GetcmsCanvasHist(canv)
    hdf.GetYaxis().SetMaxDigits(1)
    hdf.GetYaxis().SetLabelOffset(0.001)
    hdf.GetYaxis().SetLabelSize(0.045)
    hdf.GetYaxis().SetTitleOffset(1.1)
    hdf.GetYaxis().SetTitleSize(0.045)
    hdf.GetXaxis().SetLabelOffset(0.001)
    hdf.GetXaxis().SetLabelSize(0.045)
    hdf.GetXaxis().SetTitleOffset(1.1)
    hdf.GetXaxis().SetTitleSize(0.045)


    return canv

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

file_sig = '/eos/user/a/apuglia/Master_Thesis/PostProcessed_Datasets/TT_semilep_2022/'
file_bkg = '/eos/user/a/apuglia/Master_Thesis/PostProcessed_Datasets/QCD_HT70to100_2022/'
chain_lstm = ROOT.TChain('Events')
chain_cnn = ROOT.TChain('Events')

chain_lstm_bkg = ROOT.TChain('Events')
chain_cnn_bkg = ROOT.TChain('Events')


for fileName in (os.listdir(file_sig)):
    if  fileName == 'file_0':
        file_lstm = file_sig + fileName + '/' + 'scores_model_lstm_v2/' + fileName +'_lstm_model.root'
        chain_lstm.Add(file_lstm)
        file_cnn = file_sig +fileName + '/' + 'scores_model_cnn/' + fileName + '_cnn_model.root'
        chain_cnn.Add(file_cnn)


tree_lstm = InputTree(chain_lstm)
tree_cnn = InputTree(chain_cnn)
# file = ROOT.TFile.Open(file_lstm, 'READ')


label_lstm, predictions_lstm = [],[]
label_resolved, predictions_resolved = [],[]
for i in range(tree_lstm.GetEntries()):
    event = Event(tree_lstm,i)
    topmixed = Collection(event, 'TopMixed')
    # topmixed = removeResolved(tops)
    topresolved = Collection(event, 'TopResolved')
    genpart = Collection(event,'GenPart')
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
    if top_gen.pt <= 500 and top_gen.pt >= 300:

        for top in topmixed:
            if top.truth == 1:
                label_lstm.append(top.truth)
                qcdscore= top.TTScore/(top.TTScore + top.QCDScore)
                predictions_lstm.append(qcdscore)

        for top in topresolved:
            if top.truth == 1:
                label_resolved.append(top.truth)
                qcdscore = top.TTScore/(top.TTScore + top.QCDScore)
                predictions_resolved.append(qcdscore)

    
for fileName in (os.listdir(file_bkg)):
    if  fileName == 'file_0':
        file_lstm = file_bkg + fileName + '/' + 'scores_model_lstm_v2/' + fileName +'_lstm_model.root'
        chain_lstm_bkg.Add(file_lstm)
        file_cnn = file_bkg +fileName + '/' + 'scores_model_cnn/' + fileName + '_cnn_model.root'
        chain_cnn_bkg.Add(file_cnn)

tree_lstm_bkg = InputTree(chain_lstm_bkg)
tree_cnn_bkg = InputTree(chain_cnn_bkg)

for i in range(tree_lstm_bkg.GetEntries()):
    event = Event(tree_lstm_bkg,i)
    topmixed = Collection(event, 'TopMixed')
    # topmixed = removeResolved(tops)
    topresolved = Collection(event, 'TopResolved')
   
    
    for top in topmixed:
        label_lstm.append(top.truth)
        qcdscore= top.TTScore/(top.TTScore + top.QCDScore)
        predictions_lstm.append(qcdscore)

    for top in topresolved:
        label_resolved.append(top.truth)
        qcdscore = top.TTScore/(top.TTScore + top.QCDScore)
        predictions_resolved.append(qcdscore)
        



fpr_lstm, tpr_lstm, trs_lstm = roc_curve(label_lstm, predictions_lstm)
tpr_lstm = tpr_lstm * 0.7
graph_lstm = ROOT.TGraph(len(fpr_lstm), tpr_lstm, fpr_lstm)
graph_lstm.SetLineColor(ROOT.kBlue -6)
graph_lstm.SetLineWidth(2)


fpr_resolved, tpr_resolved, trs_resolved = roc_curve(label_resolved, predictions_resolved)
tpr_resolved = tpr_resolved * 0.5
graph_resolved = ROOT.TGraph(len(fpr_resolved), tpr_resolved, fpr_resolved)
graph_resolved.SetLineColor(ROOT.kCyan +3)
graph_resolved.SetLineWidth(2)


# file_cnn = '/eos/user/a/apuglia/Master_Thesis/PostProcessed_Datasets/TT_semilep_2022/file_0/scores_model_cnn/file_0_cnn_model.root'
# file = ROOT.TFile.Open(file_cnn, 'READ')
# tree_cnn = InputTree(file.Get('Events'))

label_cnn, predictions_cnn = [],[]
for i in range(tree_cnn.GetEntries()):
    event = Event(tree_cnn,i)
    topmixed= Collection(event, 'TopMixed')
    # topmixed = removeResolved(tops)
    topresolved = Collection(event, 'TopResolved')
    genpart = Collection(event, "GenPart")
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
    if top_gen.pt <= 500 and top_gen.pt >= 300:
        for top in topmixed:
            if top.truth == 1:
                label_cnn.append(top.truth)
                qcdscore= top.TTScore/(top.TTScore + top.QCDScore)
                predictions_cnn.append(qcdscore)

        # for top in topresolved:
        #     if top.truth == 1:
        #         label_cnn.append(top.truth)
        #         qcdscore = top.TTScore/(top.TTScore + top.QCDScore)
        #         predictions_cnn.append(qcdscore)

for i in range(tree_cnn_bkg.GetEntries()):
    event = Event(tree_cnn_bkg,i)
    topmixed = Collection(event, 'TopMixed')
    # topmixed = removeResolved(tops)
    topresolved = Collection(event, 'TopResolved')
    genpart = Collection(event, "GenPart")
    is_hadronic_top = np.zeros(len(genpart), dtype=int)
    hadronic_top_idx =[]
    quark_flavs = [int(1),int(2),int(3),int(4)]
    
    for top in topmixed:
        # if top.truth == 1:
        label_cnn.append(top.truth)
        qcdscore= top.TTScore/(top.TTScore + top.QCDScore)
        predictions_cnn.append(qcdscore)

    # for top in topresolved:
    #     # if top.truth == 1:
    #     label_cnn.append(top.truth)
    #     qcdscore = top.TTScore/(top.TTScore + top.QCDScore)
    #     predictions_cnn.append(qcdscore)


fpr_cnn, tpr_cnn, trs_cnn = roc_curve(label_cnn, predictions_cnn)
tpr_cnn = tpr_cnn * 0.7
graph_cnn = ROOT.TGraph(len(fpr_cnn), tpr_cnn, fpr_cnn)
graph_cnn.SetLineColor(ROOT.kGreen-6)
graph_cnn.SetLineWidth(2)


graph_mt = ROOT.TGraph(len(x_msd_t32), x_msd_t32, y_msd_t32)
graph_hotvr = ROOT.TGraph(len(x_hotvr), x_hotvr, y_hotvr)
graph_bdt = ROOT.TGraph(len(x_bdt), x_bdt, y_bdt)
graph_image_top = ROOT.TGraph(len(x_image_top), x_image_top, y_image_top)
graph_pn = ROOT.TGraph(len(x_pn), x_pn, y_pn)
graph_trota = ROOT.TGraph(len(x_TROTA), x_TROTA, y_TROTA)

canv = draw_stack_qcd()
graph_mt.Sort()
graph_hotvr.Sort()
graph_image_top.Sort()
graph_bdt.Sort()
graph_pn.Sort()
graph_trota.Sort()
# graph_lstm.Sort()
# graph_cnn.Sort()

graph_mt.SetLineColor(ROOT.kRed-6)
graph_mt.SetLineWidth(2)
graph_mt.Draw()

graph_hotvr.SetLineColor(ROOT.kGray)
graph_hotvr.SetLineWidth(2)
graph_hotvr.Draw('SAME')

graph_image_top.SetLineColor(ROOT.kMagenta-6)
graph_image_top.SetLineWidth(2)
graph_image_top.Draw('SAME')

graph_bdt.SetLineColor(ROOT.kOrange-3)
graph_bdt.SetLineWidth(2)
graph_bdt.Draw('SAME')

graph_pn.SetLineColor(ROOT.kCyan-3)
graph_pn.SetLineWidth(2)
graph_pn.Draw('SAME')

graph_trota.SetLineColor(ROOT.kBlue -3)
graph_trota.SetLineWidth(2)
graph_trota.Draw('SAME')

graph_lstm.Draw('SAME')
graph_cnn.Draw('SAME')
graph_resolved.Draw('SAME')

legend = ROOT.TLegend(0.7, 0.2, 0.9, 0.5)  # Posizione (x1, y1, x2, y2)
# legend.SetBorderSize(1)  
legend.SetFillColor(0)  
legend.SetTextSize(0.03) 

legend.AddEntry(graph_mt, "m_{SD} + #tau_{32}", 'l')
legend.AddEntry(graph_hotvr, "HOTVR", 'l')
legend.AddEntry(graph_image_top, "Image-Top", 'l')
legend.AddEntry(graph_bdt, "N_3 - BDT", 'l')
legend.AddEntry(graph_lstm, "TROTA 2D-LSTM", 'l')
legend.AddEntry(graph_cnn, "TROTA 2D-CNN", 'l')
legend.AddEntry(graph_pn, 'Particle-Net', 'l')
legend.AddEntry(graph_resolved, 'TROTA-resolved','l')
legend.AddEntry(graph_trota, 'TROTA standard', 'l')
legend.Draw()
canv.SetLogy()
canv.Draw()
canv.SaveAs('comparison_performance.png')