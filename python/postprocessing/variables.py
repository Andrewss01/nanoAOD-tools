import math
class variable(object):
    def __init__(self, name, title, taglio=None, nbins=None, xmin=None, xmax=None, xarray=None):
        self._name = name
        self._title = title
        self._taglio = taglio
        self._nbins = nbins
        self._xmin = xmin
        self._xmax = xmax
        self._xarray = xarray
    def __str__(self):
        return  '\"'+str(self._name)+'\",\"'+str(self._title)+'\",\"'+str(self._taglio)+'\",'+str(self._nbins)+','+str(self._xmin)+','+str(self._xmax)

#variable("Top_pt", "Top p_T [GeV]", nbins = 50, xmin = 0 , xmax = 1000)

### Definition of requeriments for plots (cut), variables and regions

requirements = ""#"leptonveto" #"leptonveto && MET_pt>150 && MinDelta_phi>0.6"

vars = []

vars.append(variable(name = "MET_pt", title= "MET p_{T} [GeV]", nbins = 6, xmin = 200, xmax=800))
vars.append(variable(name = "MET_phi", title= "MET #phi", nbins = 6, xmin = -math.pi, xmax=math.pi))
vars.append(variable(name = "PuppiMET_pt", title= "p_{T}^{miss} [GeV]", nbins = 6, xmin = 200, xmax=800))

vars.append(variable(name = "LeadingJetPt_pt", title= "Leading Jet p_{T} [GeV]", nbins = 8, xmin = 50, xmax=850))
# vars.append(variable(name = "LeadingJetPt_eta", title= "Leading Jet #eta", nbins = 8, xmin = -4, xmax=4))
# vars.append(variable(name = "LeadingJetPt_phi", title= "Leading Jet #phi", nbins = 6, xmin = -math.pi, xmax=math.pi))
# vars.append(variable(name = "LeadingJetPt_mass", title= "Leading Jet mass [GeV]", nbins = 10, xmin = 50, xmax=550))

vars.append(variable(name = "LeadingFatJetPt_pt", title= "Leading FatJet p_{T} [GeV]", nbins = 8, xmin = 50, xmax=850))
# vars.append(variable(name = "LeadingFatJetPt_eta", title= "Leading FatJet #eta", nbins = 8, xmin = -4, xmax=4))
# vars.append(variable(name = "LeadingFatJetPt_phi", title= "Leading FatJet #phi", nbins = 6, xmin = -math.pi, xmax=math.pi))
# vars.append(variable(name = "LeadingFatJetPt_mass", title= "Leading FatJet mass [GeV]", nbins = 10, xmin = 50, xmax=550))
vars.append(variable(name = "LeadingMuonPt_pt", title= "Leading Muon p_{T} [GeV]", nbins = 30, xmin = 0, xmax=300))
# vars.append(variable(name = "LeadingMuonPt_eta", title= "Leading Muon #eta", nbins = 8, xmin = -4, xmax=4))
# vars.append(variable(name = "LeadingMuonPt_phi", title= "Leading Muon #phi", nbins = 6, xmin = -math.pi, xmax=math.pi))
vars.append(variable(name = "LeadingElectronPt_pt", title= "Leading Electron p_{T} [GeV]", nbins = 30, xmin = 0, xmax=300))
# vars.append(variable(name = "LeadingElectronPt_eta", title= "Leading Electron #eta", nbins = 8, xmin = -4, xmax=4))
# vars.append(variable(name = "LeadingElectronPt_phi", title= "Leading Electron #phi", nbins = 6, xmin = -math.pi, xmax=math.pi))
# vars.append(variable(name = "nTopHighPt", title= "# Top Candidate Mix", nbins = 80, xmin = -0.5, xmax=80.5))
# vars.append(variable(name = "nTopLowPt", title= "# Top Candidate Resolved", nbins = 50, xmin = -0.5, xmax=50.5))
vars.append(variable(name = "nJet", title= "# Jet", nbins = 10, xmin = -0.5, xmax=9.5))
vars.append(variable(name = "nJetBtag", title= "# b-Jet ", nbins = 5, xmin = -0.5, xmax=4.5))
vars.append(variable(name = "nFatJet", title= "# FatJet", nbins = 5, xmin = -0.5, xmax=4.5))
vars.append(variable(name = "MinDelta_phi", title= "min #Delta #phi", nbins = 18, xmin = 0, xmax = math.pi))
vars.append(variable(name = "MaxEta_jet", title= "max #eta jet", nbins = 5, xmin = 0, xmax = 5))
vars.append(variable(name = "HT_eventHT", title= "event HT", nbins = 20, xmin = 0, xmax = 2000))
# vars.append(variable(name = "run", title= "Run Number", nbins = 5142, xmin = 315251.5, xmax = 320393.5))
vars.append(variable(name = "PV_npvsGood", title= "Number of PV", nbins = 51, xmin = -0.5, xmax = 50.5))

# vars.append(variable(name = "Top_mass", title= "Top mass [GeV]", nbins = 30, xmin = 100, xmax=250))
# vars.append(variable(name = "Top_pt", title= "Top p_{T} [GeV]", nbins = 30, xmin = 100, xmax=1000))

nocut = ""
hemveto = "(isMC || (year != 2018) || (HEMVeto || run<319077.))" 
met_filters = "(Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_ecalBadCalibFilter && Flag_eeBadScFilter)"
hlt_filters = "(HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60 || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight || HLT_Ele32_WPTight_Gsf || HLT_Ele115_CaloIdVT_GsfTrkIdT || HLT_Photon200 || HLT_IsoMu24)"
hlt2_filters = "(HLT_PFMET120_PFMHT120_IDTight || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight)"
hlt3_filters = "(HLT_PFMET140_PFMHT140_IDTight || HLT_PFMETNoMu140_PFMHTNoMu140_IDTight)"
metcut = "(MET_pt>250)"
hltmet_filters = "(HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60 || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight)"
hltmu_filters = "(HLT_IsoMu24)"

regions = {
    "NoCut"                             : nocut,
    # "HEMVeto"                         : hemveto,
    # "HEMVeto_MET_filters"             : hemveto +" && " + met_filters,
    "HEMVeto_HLTmet"                 : hemveto +" && " + hltmet_filters,
    "HEMVeto_HLTmu"                  : hemveto +" && " + hltmu_filters,
    "HEMVeto_HLT"                    : hemveto +" && (" + hltmet_filters +" && " + hltmu_filters + ")",
    "HEMVeto_HLTmet_METfilt"         : hemveto +" && " + met_filters +" && "+ hltmet_filters,
    "HEMVeto_HLTmu_METfilt"          : hemveto +" && " + met_filters +" && "+ hltmu_filters,
    "HEMVeto_HLT_METfilt"            : hemveto +" && " + met_filters +" && (" + hltmet_filters +" && " + hltmu_filters + ")",
    "HEMVeto_HLTmet_METcut"          : hemveto +" && " + hltmet_filters +" && "+ metcut,
    "HEMVeto_HLTmu_METcut"           : hemveto +" && " + hltmu_filters +" && "+ metcut,
    "HEMVeto_HLT_METcut"             : hemveto +" && (" + hltmet_filters +" && " + hltmu_filters + ") && "+ metcut,
    "AH_HLT"                         : hemveto +" && (" + hltmet_filters +" && " + hltmu_filters + ") && "+ metcut+" && "+"(nVetoMuon+nVetoElectron) == 0 && nJetBtag > 0 && nGoodJet>3",
    "AH1lWRmu_HLT"                   : hemveto +" && (" + hltmet_filters +" && " + hltmu_filters + ") && "+ metcut + " && " + "(nTightElectron == 0 && nVetoElectron == 0 && nTightMuon == 1 && nVetoMuon == 1) && nGoodJet>=3 && MT<=140 && nJetBtag == 0",
    "SL_HLT"                         : hemveto +" && (" + hltmet_filters +" && " + hltmu_filters + ") && "+ metcut + " && " + "((nTightElectron == 1 && nVetoElectron == 1 && nTightMuon == 0 && nVetoMuon == 0)||(nTightElectron == 0 && nVetoElectron == 0 && nTightMuon == 1 && nVetoMuon == 1)) && nJetBtag > 0",
    "AH_HLTmet"                      : hemveto +" && " + hltmet_filters +" && "+ metcut+" && "+"(nVetoMuon+nVetoElectron) == 0 && nJetBtag > 0 && nGoodJet>3",
    "AH1lWRmu_HLTmet"                : hemveto +" && " + hltmet_filters +" && "+ metcut + " && " + "(nTightElectron == 0 && nVetoElectron == 0 && nTightMuon == 1 && nVetoMuon == 1) && nGoodJet>=3 && MT<=140 && nJetBtag == 0",
    "SL_HLTmet"                      : hemveto +" && " + hltmet_filters +" && "+ metcut + " && " + "((nTightElectron == 1 && nVetoElectron == 1 && nTightMuon == 0 && nVetoMuon == 0)||(nTightElectron == 0 && nVetoElectron == 0 && nTightMuon == 1 && nVetoMuon == 1)) && nJetBtag > 0",
    "AH_HLTmu"                       : hemveto +" && " + hltmu_filters +" && "+ metcut+" && "+"(nVetoMuon+nVetoElectron) == 0 && nJetBtag > 0 && nGoodJet>3",
    "AH1lWRmu_HLTmu"                 : hemveto +" && " + hltmu_filters +" && "+ metcut + " && " + "(nTightElectron == 0 && nVetoElectron == 0 && nTightMuon == 1 && nVetoMuon == 1) && nGoodJet>=3 && MT<=140 && nJetBtag == 0",
    "SL_HLTmu"                       : hemveto +" && " + hltmu_filters +" && "+ metcut + " && " + "((nTightElectron == 1 && nVetoElectron == 1 && nTightMuon == 0 && nVetoMuon == 0)||(nTightElectron == 0 && nVetoElectron == 0 && nTightMuon == 1 && nVetoMuon == 1)) && nJetBtag > 0",

    # "HEMVeto_HLT_MET_filters"           : hemveto +" && " + met_filters +" && "+ hlt2_filters,
    # "HEMVeto_HLT3_MET_filters"        : hemveto +" && " + met_filters +" && "+ hlt3_filters,
    # "SMu"                               : hemveto +" && " + met_filters +" && "+ metcut+" && "+"(nTightElectron == 0 && nVetoElectron == 0 && nTightMuon == 1 && nVetoMuon == 1) && nJetBtag > 0",
    # "SEl"                               : hemveto +" && " + met_filters +" && "+ metcut+" && "+"(nTightElectron == 1 && nVetoElectron == 1 && nTightMuon == 0 && nVetoMuon == 0) && nJetBtag > 0",
    # "AH1lWR"                       : hemveto +" && " + metcut+" && "+"((nTightElectron == 1 && nVetoElectron == 1 && nTightMuon == 0 && nVetoMuon == 0)||(nTightElectron == 0 && nVetoElectron == 0 && nTightMuon == 1 && nVetoMuon == 1)) && nGoodJet>=3 && MT<=140 && nJetBtag == 0",
    
    # "all_regions" : "",  #### EventTopCategory!=0 fatto per fare selezione sui dati e comparare con MC18, da rimuovere il taglio qui",

    # "rA": "MET_pt>200 && MinDelta_phi>0.6 && MinDelta_phi<2.5",
    # "rB": "MET_pt>200 && MinDelta_phi>2.5",
    # "rC": "MET_pt>200 && MinDelta_phi>0.6 && MinDelta_phi<2.5 && nJetBtag > 0 ",
    # "rD": "MET_pt>200 && MinDelta_phi>2.5 && nJetBtag > 0",
    # "rE": "MET_pt>200 && MinDelta_phi>0.6 && MinDelta_phi<2.5 && nJetBtag == 0 ",
    # "rF": "MET_pt>200 && MinDelta_phi>2.5 && nJetBtag == 0",
    
    # "rA": "MET_pt>200 && MinDelta_phi>0.6 && MinDelta_phi<2.5 && nJet>3",
    # "rB": "MET_pt>200 && MinDelta_phi>2.5 && nJet>3",
    # "rC": "MET_pt>200 && MinDelta_phi>0.6 && MinDelta_phi<2.5 && nJet<4",
    # "rD": "MET_pt>200 && MinDelta_phi>2.5 && nJet<4",
    
    # "resolved_1fwjet": "EventTopCategory==3 && nForwardJet>0", 
    # "mixed_1fwjet": "EventTopCategory==2 && nForwardJet>0", 
    # "merged_1fwjet": "EventTopCategory==1 && nForwardJet>0",
    # "resolved_0fwjet": "EventTopCategory==3 && nForwardJet==0", 
    # "mixed_0fwjet": "EventTopCategory==2 && nForwardJet==0", 
    # "merged_0fwjet" : "EventTopCategory==1 && nForwardJet==0",
    # "noTopRegion" : "EventTopCategory==0"
}