//#ifndef POST_H
//#define POST_H

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "TCanvas.h"
#include "TH1D.h"
#include "TFile.h"
#include "TH2D.h"
#include "TLatex.h"
#include "Math/Vector4D.h"
#include "TStyle.h"
#include <map>

#include "TDavixFile.h"

using namespace ROOT::VecOps;
using RNode = ROOT::RDF::RNode;
using rvec_f = const RVec<float> &;
using rvec_i = const RVec<int> &;
using rvec_b = const RVec<bool> &;

const float TopRes_minpt=  0.;
const float TopRes_maxpt=  300.;
const float TopMix_minpt=  300.;
const float TopMix_maxpt=  500.;
const float TopMer_minpt=  500.;
const float TopMer_maxpt=  10000.;
const float TopRes_trs=  0.5411276;
const float TopMix_trs=  0.39578277;
const float TopMer_trs=  0.99;
const float dR=  0.8;
const float btag_mediumWP = 0.2783;

// ########################################################
bool isMC(int SampleFlag){
  if (SampleFlag == 0) return false;
  else return true;
}

// ############### from skimtree_utils

float deltaPhi (float phi1, float phi2){
  float dphi = (phi1-phi2);
  while(dphi >  M_PI) dphi -= 2*M_PI;
  while(dphi < -M_PI) dphi += 2*M_PI;
  return dphi;
}

float deltaR(float eta1, float phi1, float eta2, float phi2){
  return hypot(eta1 - eta2, deltaPhi(phi1, phi2)); 
}

// ########################################################
// ############## Un/Ov flow bin ##########################
// ########################################################

float UnOvBin(float var, int bins, float xmin, float xmax){ 
  float fvar;
  float half_step = ((xmax-xmin)/float(bins))/2.; 

  if(var>=xmax) fvar = xmax-half_step;
  else if(var<=xmin) fvar = xmin+half_step;
  else fvar = var; 

  return fvar;
}

// ########################################################
// ############## Data2018 ################################
// ########################################################

bool hemveto(rvec_f Jet_eta, rvec_f Jet_phi, rvec_f Electron_eta, rvec_f Electron_phi){
  float hemvetoetaup = -3.05;
  float hemvetoetadown = -1.35;
  float hemvetophiup = -1.62;
  float hemvetophidown = -0.82;
  bool passesMETHEMVeto = true;

  for(size_t i = 0; i < Jet_eta.size(); i++){
    if(Jet_eta[i]>hemvetoetaup && Jet_eta[i]<hemvetoetadown && Jet_phi[i]>hemvetophiup && Jet_phi[i]<hemvetophidown){
      passesMETHEMVeto = false;
    }
  }
  for(size_t i = 0; i < Electron_eta.size(); i++){
    if(Electron_eta[i]>hemvetoetaup && Electron_eta[i]<hemvetoetadown && Electron_phi[i]>hemvetophiup && Electron_phi[i]<hemvetophidown){
      passesMETHEMVeto = false;
    }
  }
  return passesMETHEMVeto; 
}

int w_nominalhemveto(float w_nominal, bool HEMVeto){
  int w_nominal_update = w_nominal;
  if (HEMVeto == false){
    w_nominal_update = w_nominal * 0.354;
    // w_nominal_update = w_nominal * 0.932;
  }
  return w_nominal_update;
}

// ########################################################
// ############## TT correction ###########################
// ########################################################

bool tt_mtt_doublecounting(rvec_f GenPart_pdgId, rvec_f GenPart_pt, rvec_f GenPart_eta, rvec_f GenPart_phi, rvec_f GenPart_mass){ 
  TLorentzVector top;
  TLorentzVector antitop;
  bool pass = true;
  for(size_t i = 0; i<GenPart_pdgId.size(); i++){
    if(GenPart_pdgId[i]==6){
      top.SetPtEtaPhiM(GenPart_pt[i], GenPart_eta[i], GenPart_phi[i], GenPart_mass[i]);
      
    } else if(GenPart_pdgId[i]==-6){
      antitop.SetPtEtaPhiM(GenPart_pt[i], GenPart_eta[i], GenPart_phi[i], GenPart_mass[i]);
      
    }
  }
  float Mtt = (top+antitop).M();
  if(Mtt>=700){
    pass = false;
  }
  return pass;
}

// ########################################################
// ############## MET_HLT_filter ##########################
// ########################################################

bool MET_HLT_filter(bool HLT_PFMET120_PFMHT120_IDTight, bool HLT_PFMETNoMu120_PFMHTNoMu120_IDTight, bool flag_goodVertices, bool flag_globalSuperTightHalo2016Filter, bool flag_HBHENoiseFilter, bool flag_HBHENoiseIsoFilter, bool flag_EcalDeadCellTriggerPrimitiveFilter, bool flag_BadPFMuonFilter, bool flag_BadPFMuonDzFilter, bool flag_ecalBadCalibFilter, bool flag_eeBadScFilter){
  
  // bool good_HLT = HLT_PFMET120_PFMHT120_IDTight || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight;
  bool good_MET = flag_goodVertices && flag_globalSuperTightHalo2016Filter && flag_HBHENoiseFilter && flag_HBHENoiseIsoFilter && flag_EcalDeadCellTriggerPrimitiveFilter && flag_BadPFMuonFilter && flag_BadPFMuonDzFilter && flag_ecalBadCalibFilter && flag_eeBadScFilter; //  && flag_hfNoisyHitsFilter && flag_BadChargedCandidateFilter;
  
  return good_MET; //good_HLT
}

bool MET_filter(bool flag_goodVertices, bool flag_globalSuperTightHalo2016Filter, bool flag_HBHENoiseFilter, bool flag_HBHENoiseIsoFilter, bool flag_EcalDeadCellTriggerPrimitiveFilter, bool flag_BadPFMuonFilter, bool flag_BadPFMuonDzFilter, bool flag_ecalBadCalibFilter, bool flag_eeBadScFilter){
  bool good_MET = flag_goodVertices && flag_globalSuperTightHalo2016Filter && flag_HBHENoiseFilter && flag_HBHENoiseIsoFilter && flag_EcalDeadCellTriggerPrimitiveFilter && flag_BadPFMuonFilter && flag_BadPFMuonDzFilter && flag_ecalBadCalibFilter && flag_eeBadScFilter;
  return good_MET;
}

// ########################################################
// ########## PRESELECTION ################################
// ########################################################
int nTightElectron(rvec_f Electron_pt, rvec_f Electron_eta, rvec_f Electron_cutBased)
{
  int n=0;
  for(int i = 0; i<Electron_pt.size(); i++)
  {
    if(Electron_cutBased[i]>=4 && Electron_pt[i] > 35 && abs(Electron_eta[i])<2.1) n+=1;
  }
  return n;
}

RVec<int> TightElectron_idx(rvec_f Electron_pt, rvec_f Electron_eta, rvec_f Electron_cutBased)
{
  RVec<int> ids;
  for(int i = 0; i<Electron_pt.size(); i++)
  {
    if(Electron_cutBased[i]>=4 && Electron_pt[i] > 35 && abs(Electron_eta[i])<2.1) ids.emplace_back(i);
  }
  return ids;
}

int nTightMuon(rvec_f Muon_pt, rvec_f Muon_eta, rvec_f Muon_tightId)
{
  int n=0;
  for(int i = 0; i<Muon_pt.size(); i++)
  {
    if(Muon_tightId[i]==1 && Muon_pt[i] > 30 && abs(Muon_eta[i])<2.4) n+=1;
  }
  return n;
}

RVec<int> TightMuon_idx(rvec_f Muon_pt, rvec_f Muon_eta, rvec_f Muon_tightId)
{
  RVec<int> ids;
  for(int i = 0; i<Muon_pt.size(); i++)
  {
    if(Muon_tightId[i]==1 && Muon_pt[i] > 30 && abs(Muon_eta[i])<2.4) ids.emplace_back(i);
  }
  return ids;
}

int nVetoElectron(rvec_f Electron_pt, rvec_f Electron_cutBased)
{
  int n=0;
  for(int i = 0; i<Electron_pt.size(); i++)
  {
    if(Electron_cutBased[i]>=1 && Electron_pt[i] > 10) n+=1;
  }
  return n;
}

int nVetoMuon(rvec_f Muon_pt, rvec_f Muon_eta, rvec_f Muon_looseId)
{
  int n=0;
  for(int i = 0; i<Muon_pt.size(); i++)
  {
    if(Muon_looseId[i]==1 && Muon_pt[i] > 10) n+=1;
  }
  return n;
}

bool LepVeto(rvec_f Electron_pt, rvec_f Electron_eta, rvec_f Electron_cutBased, rvec_f Muon_pt, rvec_f Muon_eta, rvec_b Muon_looseId )
{
  int EleVetoPassed = 0;
  int MuVetoPassed = 0;
  bool IsLepVetoPassed = true;
  
  for (size_t i = 0; i < Electron_pt.size(); i++) 
    {
      if(Electron_cutBased[i]>=1 && Electron_pt[i] > 30. && abs(Electron_eta[i])<2.4) EleVetoPassed+=1;
    }
  for (size_t i = 0; i< Muon_pt.size(); i++)
    {
      if(Muon_looseId[i]==1 && Muon_pt[i] > 30. && abs(Muon_eta[i])<2.4) MuVetoPassed+=1;
    }
  if(EleVetoPassed+MuVetoPassed >0) IsLepVetoPassed = false;
  
  return IsLepVetoPassed;
}

RVec<int> GetGoodJet(rvec_f Jet_pt, rvec_f Jet_eta, rvec_i Jet_jetId)
{
  RVec<int> ids;
  for(int i = 0; i<Jet_pt.size(); i++)
  {
      if (Jet_pt[i]>30 && abs(Jet_eta[i])<2.4 && Jet_jetId[i]>1)
      {
        ids.emplace_back(i);
      }
  }
  return ids;
}

int nGoodJet(rvec_i GoodJet_idx)
{
  return GoodJet_idx.size();
}

bool atLeast1verygoodjet(rvec_i GoodJet_idx, rvec_f Jet_pt, rvec_f Jet_eta)
{
  bool pass = false;
  for(int i = 0; i < GoodJet_idx.size(); i++)
  {
    if (Jet_pt[GoodJet_idx[i]]>30 && abs(Jet_eta[GoodJet_idx[i]])<4) 
    {
      pass = true;
    }
  }
  return pass;
}

bool atLeast1verygoodfatjet(rvec_f FatJet_pt, rvec_f FatJet_msoftdrop)
{
  bool pass = false;
  for(int i = 0; i < FatJet_pt.size(); i++)
  {
    if (FatJet_pt[i]>200 && FatJet_msoftdrop[i]>40) 
    {
      pass = true;
    }
  }
  return pass;
}

// ########################################################
// ########## New functions for deb #######################
// ########################################################

bool atLeast1jet_setparams(rvec_f Jet_pt, rvec_f Jet_eta, rvec_f Jet_mass, rvec_i Jet_jetId, float minpt, float maxeta, float minmass, int jetId)
{
  bool pass = false;
  for(int i = 0; i < Jet_pt.size(); i++)
  {
    if (Jet_pt[i]>minpt && abs(Jet_eta[i])<maxeta && Jet_mass[i]>minmass && Jet_jetId[i]>=jetId) 
    {
      pass = true;
    }
  }
  return pass;
}

bool atLeast1fatjet_setparams(rvec_f FatJet_pt, rvec_f FatJet_msoftdrop, rvec_f FatJet_eta, rvec_i FatJet_jetId, float minpt, float maxeta, float minmsoftdrop, int jetId)
{
  bool pass = false;
  for(int i = 0; i < FatJet_pt.size(); i++)
  {
    if (FatJet_pt[i]>minpt && abs(FatJet_eta[i])<maxeta && FatJet_msoftdrop[i]>minmsoftdrop && FatJet_jetId[i]>=jetId) 
    {
      pass = true;
    }
  }
  return pass;
}

Int_t GetLeadingPtJet(rvec_f Jet_pt)
{
  RVec<float> pt;
  for(int i = 0; i < Jet_pt.size(); i++)
  {
    pt.emplace_back(Jet_pt[i]);
  }
  return ArgMax(pt);
}

Int_t GetLeadingPtLep(rvec_f Lep_pt, rvec_f Lep_eta, rvec_i Lep_looseId)
{
  RVec<float> pt;
  for(int i = 0; i < Lep_pt.size(); i++)
  {
    if (Lep_looseId[i]>0 && Lep_pt[i]>30 && abs(Lep_eta[i])<2.4)
    {
      pt.emplace_back(Lep_pt[i]);
    }
    else
    {
      pt.emplace_back(-10);
    }
  }
  if (pt.size() == 0) return -1;
  else return ArgMax(pt);
}

Float_t GetLeadingJetVar(int LeadingJet_idx, rvec_f Jet_var)
{
  if (LeadingJet_idx == -1) return 0;
  else return Jet_var[LeadingJet_idx];
}

// ########################################################
// ########## AH1lWR control region #######################
// ########################################################
int Lepton_flavour(int nTightElectron, int nTightMuon)
{
  int flav=0;
  if (nTightElectron == 1) flav = 1;
  else if (nTightMuon == 1) flav = 2;
  return flav;
}

float Lepton_var(int Lepton_flavour, rvec_f Electron_var, rvec_i tightElectron_idx, rvec_f Muon_var, rvec_i tightMuon_idx)
{
  float var=0;
  if (Lepton_flavour == 1) var = Electron_var[tightElectron_idx[0]];
  else if (Lepton_flavour == 2) var = Muon_var[tightMuon_idx[0]];
  else var = -1000;
  return var;
}

// ########################################################
// ############## MC/data comparison vars #################
// ########################################################

Float_t LeadingJetPt(rvec_i GoodJet_idx, rvec_f Jet_pt)
{
  RVec<float> GoodJet_pt;
  for(int i = 0; i < GoodJet_idx.size(); i++)
  {
    GoodJet_pt.emplace_back(Jet_pt[GoodJet_idx[i]]);
  }
  return Max(GoodJet_pt);
}

Float_t LeadingFatJetPt(rvec_f FatJet_pt)
{
  
  RVec<float> fj_pt;
  for(int i = 0; i < FatJet_pt.size(); i++)
  {
    fj_pt.emplace_back(FatJet_pt[i]);
  }
  return Max(fj_pt);
}

Int_t nForwardJet(rvec_i GoodJet_idx, rvec_f Jet_eta)
{
  int nfwdjet = 0;
  for(int i = 0; i < GoodJet_idx.size(); i++)
  {
    if (Jet_eta[GoodJet_idx[i]]>2.5)
    {
      nfwdjet += 1;
    }
  }
  return nfwdjet;
}

Int_t njetbtag(rvec_i GoodJet_idx, rvec_f Jet_btagDeepFlavB)
{
  int nbjet = 0;
  for(int i = 0; i < GoodJet_idx.size(); i++)
  {
    if (Jet_btagDeepFlavB[GoodJet_idx[i]] > btag_mediumWP)
    {
      nbjet += 1;
    }
  }
  return nbjet;
}

// ########################################################
// ############## TopSelection ############################
// ########################################################

RVec<int> select_TopMer(rvec_f FatJet_deepTag_TvsQCD, rvec_f FatJet_pt, rvec_f FatJet_eta, rvec_f FatJet_phi)
{
  RVec<int> ids;
  for (int i = 0; i < FatJet_deepTag_TvsQCD.size(); i++)
  {
  	if(FatJet_deepTag_TvsQCD[i]>TopMer_trs && FatJet_pt[i]>TopMer_minpt && FatJet_pt[i]<TopMer_maxpt){
      ids.emplace_back(i);
	  }
  }
  return ids;
}

RVec<int> select_TopMix(rvec_f TopHighPt_score2, rvec_f TopHighPt_pt, rvec_f TopHighPt_eta, rvec_f TopHighPt_phi)
{
  RVec<int> ids;
  RVec<float> scores;
  for (int i = 0; i < TopHighPt_score2.size(); i++)
  {
  	if(TopHighPt_score2[i]>TopMix_trs && TopHighPt_pt[i]>TopMix_minpt && TopHighPt_pt[i]<TopMix_maxpt)
    {
      ids.emplace_back(i);
	    scores.emplace_back(TopHighPt_score2[i]);
	  }
  }
    
  RVec<int> ids_ = ids;
  RVec<int> ids_select;
  RVec<float> scores_ = scores;
  int n_notzero = 0;
    
  for(int j=0; j<scores_.size(); j++)
  { 
    if(scores_[j]!=0)
    {
	    n_notzero += 1;
    }
    else 
    {
	    n_notzero += 0;
    }
  }

  while(n_notzero!=0)
  {
    RVec<float> deltaRs;
    int bestTop_idx = ArgMax(scores_);
      
    for(int i = 0; i < ids_.size(); i++)
    {
	    if(i == bestTop_idx) continue;
	    if(scores_[i]!=0 && deltaR(TopHighPt_eta[bestTop_idx], TopHighPt_phi[bestTop_idx], TopHighPt_eta[i], TopHighPt_phi[i])<dR)  scores_[i]=0;
     
    }
    ids_select.emplace_back(bestTop_idx);
    scores_[bestTop_idx]=0;
    n_notzero =0;
    for(int j=0; j<scores_.size(); j++)
    { 
	    if(scores_[j]!=0)
      {
	      n_notzero += 1;
	    }
	    else 
      {
	      n_notzero += 0;
	    }
    }
  }
  return ids_select;
}

RVec<int> select_TopRes(rvec_f TopLowPt_scoreDNN, rvec_f TopLowPt_pt, rvec_f TopLowPt_eta, rvec_f TopLowPt_phi)
{
  RVec<int> ids;
  RVec<float> scores;
  for (int i = 0; i < TopLowPt_scoreDNN.size(); i++)
  {
	  if(TopLowPt_scoreDNN[i]>TopRes_trs && TopLowPt_pt[i]>TopRes_minpt && TopLowPt_pt[i]<TopRes_maxpt)
    {
	    ids.emplace_back(i);
	    scores.emplace_back(TopLowPt_scoreDNN[i]);
	  }
  }
    
  RVec<int> ids_ = ids;
  RVec<float> ids_select;
  RVec<float> scores_ = scores;
  int n_notzero = 0;
    
  for(int j=0; j<scores_.size(); j++)
  { 
    if(scores_[j]!=0)
    {
	    n_notzero += 1;
    }
    else 
    {
	    n_notzero += 0;
    }
  }

  while(n_notzero!=0)
  {
    RVec<float> deltaRs;
    int bestTop_idx = ArgMax(scores_);
      
    for(int i = 0; i < ids_.size(); i++)
    {
	    if(i == bestTop_idx) continue;
	    if(scores_[i]!=0 && deltaR(TopLowPt_eta[bestTop_idx], TopLowPt_phi[bestTop_idx], TopLowPt_eta[i], TopLowPt_phi[i])<dR)  scores_[i]=0;
    }
    ids_select.emplace_back(bestTop_idx);
    scores_[bestTop_idx]=0;
    n_notzero =0;
    for(int j=0; j<scores_.size(); j++)
    { 
      if(scores_[j]!=0)
      {
	      n_notzero += 1;
	    }
	    else 
      {
	      n_notzero += 0;
	    }
    }
  }
  return ids_select;
}

Int_t select_TopCategory(rvec_i GoodTopMer_idx, rvec_i GoodTopMix_idx, rvec_i GoodTopRes_idx){
  //return:  0- no top sel, 1- top merged, 2- top mix, 3- top resolved
  int nRes = GoodTopRes_idx.size();
  int nMix = GoodTopMix_idx.size();
  int nMer = GoodTopMer_idx.size();
  
  if (nRes>0 && nMix==0 && nMer==0){
    return 3;
  }
  else if (nRes<2 && nMix>0 && nMer==0){
    return 2;
  }
  else if (nRes==0 && nMix<2 && nMer>0){
    return 1;
  }
  else return 0;
}

Int_t select_bestTop(int EventTopCategory, rvec_i GoodTopMer_idx, rvec_i GoodTopMix_idx, rvec_i GoodTopRes_idx, rvec_f FatJet_deepTag_TvsQCD, rvec_f TopHighPt_score2, rvec_f TopLowPt_scoreDNN){
  //RVec<int> topselect ;
  //int bestTop_idx;
  RVec<float> scores;
  if (EventTopCategory==1){ 
    //topselect = GoodTopMer_idx;
    for(int i = 0; i < GoodTopMer_idx.size(); i++)
    {
      scores.emplace_back(FatJet_deepTag_TvsQCD[i]);
    }
  }
  else if (EventTopCategory==2){
    for(int i = 0; i < GoodTopMix_idx.size(); i++)
    {
      scores.emplace_back(TopHighPt_score2[i]);
    } 
  }
  else if (EventTopCategory==3){ 
    for(int i = 0; i < GoodTopRes_idx.size(); i++)
    {
      scores.emplace_back(TopLowPt_scoreDNN[i]);
    } 
  }
  else return -1;

  return ArgMax(scores);
}

Float_t select_TopVar(Int_t EventTopCategory, Int_t Top_idx, rvec_f FatJet_pt, rvec_f TopHighPt_pt, rvec_f TopLowPt_pt){
  if (EventTopCategory==1) return FatJet_pt[Top_idx];
  else if (EventTopCategory==2) return TopHighPt_pt[Top_idx];
  else if (EventTopCategory==3) return TopLowPt_pt[Top_idx];
  else return -1000;
}

