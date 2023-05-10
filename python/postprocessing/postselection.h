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


float deltaPhi (float phi1, float phi2){
  float dphi = (phi1-phi2);
  while(dphi >  M_PI) dphi -= 2*M_PI;
  while(dphi < -M_PI) dphi += 2*M_PI;
  return dphi;
}

float deltaR(float eta1, float phi1, float eta2, float phi2){
  return hypot(eta1 - eta2, deltaPhi(phi1, phi2)); 
}

bool LepVeto(rvec_f Electron_pt, rvec_f Electron_eta, rvec_f Electron_mvaFall17V1Iso_WPL,rvec_f Muon_pt, rvec_f Muon_eta, rvec_b Muon_looseId )
{
  int EleVetoPassed = 0;
  int MuVetoPassed = 0;
  bool IsLepVetoPassed = true;
  
  for (size_t i = 0; i < Muon_pt.size(); i++) 
    {
      if(Electron_mvaFall17V1Iso_WPL[i]==1 && Electron_pt[i] > 30.) EleVetoPassed+=1;
    }
  for (size_t i = 0; i< Muon_pt.size(); i++)
    {
      if(Muon_looseId[i]==1 && Muon_pt[i] > 30. && abs(Muon_eta[i])<2.4) MuVetoPassed+=1;
    }
  if(EleVetoPassed+MuVetoPassed >0) IsLepVetoPassed = false;
  
  return IsLepVetoPassed;
}

RVec<int> select_TopMer(rvec_f FatJet_deepTag_TvsQCD, rvec_f FatJet_pt, rvec_f FatJet_eta, rvec_f FatJet_phi){
    RVec<int> ids;
    for (int i = 0; i < FatJet_deepTag_TvsQCD.size(); i++)
      {
	if(FatJet_deepTag_TvsQCD[i]>TopMer_trs && FatJet_pt[i]>TopMer_minpt && FatJet_pt[i]<TopMer_maxpt){
	  ids.emplace_back(i);
	}
      }
    return ids;
}

RVec<int> select_TopMix(rvec_f TopHighPt_score2, rvec_f TopHighPt_pt, rvec_f TopHighPt_eta, rvec_f TopHighPt_phi){
    RVec<int> ids;
    RVec<float> scores;
    for (int i = 0; i < TopHighPt_score2.size(); i++){
	if(TopHighPt_score2[i]>TopMix_trs && TopHighPt_pt[i]>TopMix_minpt && TopHighPt_pt[i]<TopMix_maxpt){
	  ids.emplace_back(i);
	  scores.emplace_back(TopHighPt_score2[i]);
	}
    }
    
    RVec<int> ids_ = ids;
    RVec<int> ids_select;
    RVec<float> scores_ = scores;
    int n_notzero = 0;
    
    for(int j=0; j<scores_.size(); j++){ 
      if(scores_[j]!=0){
	n_notzero += 1;
      }
      else {
	n_notzero += 0;
      }
    }

    while(n_notzero!=0){
      RVec<float> deltaRs;
      int bestTop_idx = ArgMax(scores_);
      
      for(int i = 0; i < ids_.size(); i++){
	if(i == bestTop_idx) continue;
	if(scores_[i]!=0 && deltaR(TopHighPt_eta[bestTop_idx], TopHighPt_phi[bestTop_idx], TopHighPt_eta[i], TopHighPt_phi[i])<dR)  scores_[i]=0;
     
      }
      ids_select.emplace_back(bestTop_idx);
      scores_[bestTop_idx]=0;
      n_notzero =0;
      for(int j=0; j<scores_.size(); j++){ 
	if(scores_[j]!=0){
	  n_notzero += 1;
	}
	else {
	  n_notzero += 0;
	}
      }
    }
    return ids_select;
}

RVec<int> select_TopRes(rvec_f TopLowPt_scoreDNN, rvec_f TopLowPt_pt, rvec_f TopLowPt_eta, rvec_f TopLowPt_phi){
    RVec<int> ids;
    RVec<float> scores;
    for (int i = 0; i < TopLowPt_scoreDNN.size(); i++){
	if(TopLowPt_scoreDNN[i]>TopRes_trs && TopLowPt_pt[i]>TopRes_minpt && TopLowPt_pt[i]<TopRes_maxpt){
	  ids.emplace_back(i);
	  scores.emplace_back(TopLowPt_scoreDNN[i]);
	}
    }
    
    RVec<int> ids_ = ids;
    RVec<float> ids_select;
    RVec<float> scores_ = scores;
    int n_notzero = 0;
    
    for(int j=0; j<scores_.size(); j++){ 
      if(scores_[j]!=0){
	n_notzero += 1;
      }
      else {
	n_notzero += 0;
      }
    }

    while(n_notzero!=0){
      RVec<float> deltaRs;
      int bestTop_idx = ArgMax(scores_);
      
      for(int i = 0; i < ids_.size(); i++){
	if(i == bestTop_idx) continue;
	if(scores_[i]!=0 && deltaR(TopLowPt_eta[bestTop_idx], TopLowPt_phi[bestTop_idx], TopLowPt_eta[i], TopLowPt_phi[i])<dR)  scores_[i]=0;
      }
      ids_select.emplace_back(bestTop_idx);
      scores_[bestTop_idx]=0;
      n_notzero =0;
      for(int j=0; j<scores_.size(); j++){ 
	if(scores_[j]!=0){
	  n_notzero += 1;
	}
	else {
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
  RVec<int> topselect ;
  int bestTop_idx;
  if (EventTopCategory==1){ 
    topselect = GoodTopMer_idx;
    bestTop_idx = ArgMax(FatJet_deepTag_TvsQCD);
  }
  else if (EventTopCategory==2){ 
    topselect = GoodTopMix_idx;
    bestTop_idx = ArgMax(TopHighPt_score2);
  }
  else if (EventTopCategory==3){ 
    topselect = GoodTopRes_idx;
    bestTop_idx = ArgMax(TopLowPt_scoreDNN);
  }
  else return -1;
  
  return bestTop_idx;
}

Float_t select_TopVar(Int_t EventTopCategory, Int_t Top_idx, rvec_f FatJet_pt, rvec_f TopHighPt_pt, rvec_f TopLowPt_pt){
  if (EventTopCategory==1) return FatJet_pt[Top_idx];
  else if (EventTopCategory==2) return TopHighPt_pt[Top_idx];
  else if (EventTopCategory==3) return TopLowPt_pt[Top_idx];
  else return -1000;
}
