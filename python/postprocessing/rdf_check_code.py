import ROOT
from tools import *
from samples.samples import *
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Event, Collection,Object
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
from datetime import datetime

def HEMveto(jets, electrons):
    hemvetoetaup = -3.05
    hemvetoetadown = -1.35
    hemvetophiup = -1.62
    hemvetophidown = -0.82;
    passesMETHEMVeto = True

    for jet in jets:
        if(jet.eta>hemvetoetaup and jet.eta<hemvetoetadown and jet.phi>hemvetophiup and jet.phi<hemvetophidown):
            passesMETHEMVeto = False

    for ele in electrons:
        if(ele.eta>hemvetoetaup and ele.eta<hemvetoetadown and ele.phi>hemvetophiup and ele.phi<hemvetophidown):
            passesMETHEMVeto = False
 
    return passesMETHEMVeto
    
def leptonveto(electron, muon):
    EleVetoPassed = 0
    MuVetoPassed = 0
    IsLepVetoPassed = True
  
    for el in electron: 
        if(el.cutBased>=1 and el.pt > 30. and abs(el.eta)<2.5): 
            EleVetoPassed+=1
    for mu in muon:
        if(mu.looseId == 1 and mu.pt > 30. and abs(mu.eta) < 2.4): 
            MuVetoPassed+=1
    if(EleVetoPassed+MuVetoPassed >0): 
        IsLepVetoPassed = False
    return IsLepVetoPassed

def atleast1Ak4good(jets):
    b = False
    for j in jets:
        if(j.pt>30 and abs(j.eta)<4 and j.jetId>1):
           b = True
    return b
def atleast1Ak8good(fatjets):
    b = False
    for j in fatjets:
        if(j.pt>200 and j.msoftdrop>40):
           b = True
    return b


file = "root://stormgf2.pi.infn.it//store/user/acagnott/DM_Run3_v0/MET/DataHTC_2018/230921_090909/0000/tree_hadd_118.root"
# inputFile = ROOT.TFile.Open(file)
chain = ROOT.TChain("Events")
chain.Add(file)

tree = InputTree(chain)
nevents = tree.GetEntries()
sample = sample_dict['DataHTC_2018']

passHLTMET = 0
passHEMveto = 0
passLepVeto = 0
passAK4 = 0
passAK8 = 0
passMET = 0

if 'Data' in sample.label: isMC = False
else: isMC = True

print("sample: ", sample.label, file)
print("isMC: ", isMC)
print("starting events loop : ", datetime.now().strftime("%H:%M:%S"))

for i in range(nevents):
    if i%100000==0: print(i)
    chain.GetEntry(i)
    event = Event(tree,i)
    jets = Collection(event, "Jet")
    fatjets = Collection(event, "FatJet")
    met = Object(event, "MET")
    electron = Collection(event, "Electron")
    muon = Collection(event, "Muon")
    HLT = Object(event, "HLT")
    flag = Object(event, "Flag")
    #run = Object(event, "run")
    nelectron = len(electron)
    nmuon = len(muon)

    passesMETHEMVeto = HEMveto(jets, electron)
    if(sample.year == 2018 and not passesMETHEMVeto):
        if(not isMC and chain.run > 319077.):
            continue
        elif(isMC):
            w_nominal_nominal[0] *= 0.354
    passHEMveto +=1

    good_HLT = HLT.PFMET120_PFMHT120_IDTight or HLT.PFMETNoMu120_PFMHTNoMu120_IDTight
    good_MET = flag.goodVertices and flag.globalSuperTightHalo2016Filter and flag.HBHENoiseFilter and flag.HBHENoiseIsoFilter and flag.EcalDeadCellTriggerPrimitiveFilter and flag.BadPFMuonFilter and flag.ecalBadCalibFilter and flag.eeBadScFilter #and flag.BadPFMuonDzFilter
    if not (good_HLT and good_MET):
        continue
    passHLTMET += 1

    if not leptonveto(electron, muon):
        continue
    passLepVeto += 1

    if not atleast1Ak4good(jets):
        continue
    passAK4 += 1

    if not atleast1Ak8good(fatjets):
        continue
    passAK8 += 1

    if not met.pt>200:
        continue
    passMET += 1

print("Ending events loop : ", datetime.now().strftime("%H:%M:%S"))
print("HLT and MET Efficiency: ", passHLTMET/nevents)
print("HEM Veto Efficiency: ", passHEMveto/passHLTMET)
print("Lepton Veto Efficiency: ", passLepVeto/passHEMveto)
print("AK4 Efficiency: ", passAK4/passLepVeto)
print("AK8 Efficiency: ", passAK8/passAK4)
print("MET Efficiency: ", passMET/passAK8)
print("Total Efficiency: ", passMET/nevents)

print("\n Total Events (start): ", nevents)
print("Total Events Select", passMET)