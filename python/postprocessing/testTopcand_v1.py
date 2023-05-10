#!/usr/bin/env python3
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopcandidate_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoTopevaluate import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.nanoprepro_v2 import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.GenPart_MomFirstCp import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.preselection import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.topselection import *
import sys

#fnames = ["/eos/home-a/acagnott/DarkMatter/prepro/"+sys.argv[1]+".root"]
#fnames = ["/eos/home-a/acagnott/DarkMatter/prepro/"+sys.argv[1]+"_Skim.root"]
#fnames = ["/eos/home-a/acagnott/DarkMatter/topcandidate_file/"+sys.argv[1]+"_Skim_Skim.root"]
fnames = [sys.argv[1]]

#GenPart_MomFirstCp
# legend: w/o _Skim -> no matching
#         1 _Skim-> matching but no top collections
#         2 _Skim -> matching and top collections  
#         3 _Skim -> matching, top collections, and top evaluation
# NB: for QCD file no matching, so 1 SKim-> top collections, 2 _Skim-> top evaluation

#fnames=["/eos/home-a/acagnott/DarkMatter/prepro/tDM_mPhi1000_mChi1.root"]
#fnames=["/eos/home-a/acagnott/DarkMatter/prepro/TT_Mtt-1000toInf_2018.root"]
#fnames=["/eos/home-a/acagnott/DarkMatter/prepro/TT_Mtt-700to1000_2018.root"]
#fnames=["/eos/home-a/acagnott/DarkMatter/prepro/tDM_mPhi1000_mChi1_Skim.root"]
#fnames=["/eos/home-a/acagnott/DarkMatter/prepro/TT_Mtt-1000toInf_2018_Skim.root"]
#fnames=["/eos/home-a/acagnott/DarkMatter/prepro/TT_Mtt-700to1000_2018_Skim.root"]
#fnames=["/eos/home-a/acagnott/DarkMatter/prepro/QCD_HT1000.root"]
#fnames=["/eos/home-a/acagnott/DarkMatter/prepro/QCD-HT1500to2000_2018.root"]
#fnames=["/eos/home-a/acagnott/DarkMatter/prepro/QCD-HT2000toInf_2018.root"]
#fnames=["/eos/home-a/acagnott/DarkMatter/topcandidate_file/tDM_mPhi1000_mChi1_Skim_Skim.root"]
#fnames=["/eos/home-a/acagnott/DarkMatter/topcandidate_file/TT_Mtt-700to1000_2018_Skim_Skim.root"]
#fnames=["/eos/home-a/acagnott/DarkMatter/topcandidate_file/TT_Mtt-1000toInf_2018_Skim_Skim.root"]
#fnames=["/eos/home-a/acagnott/DarkMatter/topcandidate_file/QCD_HT1000_Skim.root"]
#fnames=["/eos/home-a/acagnott/DarkMatter/topcandidate_file/QCD-HT1500to2000_2018_Skim.root"]
#fnames=["/eos/home-a/acagnott/DarkMatter/topcandidate_file/QCD-HT2000toInf_2018_Skim.root"]

#fnames = ["root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv7/TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/110000/93A3DD37-635B-6649-91BC-279C75983C5B.root"]
#fnames = ["root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv7/TT_Mtt-1000toInf_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/110000/522E2902-0B1B-6644-AD2B-518A513F6778.root"]
#fnames = ["root://cms-xrd-global.cern.ch//store/mc/RunIIAutumn18NanoAODv7/QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8/NANOAODSIM/Nano02Apr2020_102X_upgrade2018_realistic_v21-v1/260000/EE305C43-E265-BB4A-B6FA-60B447464524.root"]

#p=PostProcessor(".",fnames,"Jet_pt>150","",[jetmetUncertainties2016(),exampleModuleConstr()],provenance=True)
#p=PostProcessor("/eos/home-a/acagnott/DarkMatter/prepro/",fnames,modules=[GenPart_MomFirstCp(flavour="-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24"),nanoprepro()],  provenance=True,  maxEntries = 30000)
#p=PostProcessor("/eos/home-a/acagnott/DarkMatter/topcandidate_file/",fnames,modules=[nanoTopcand()],  provenance=True,  maxEntries = 30000)


#p=PostProcessor("/eos/home-a/acagnott/DarkMatter/topcandidate_file/",fnames,modules=[GenPart_MomFirstCp(flavour="-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24"),nanoprepro(),nanoTopcand(), nanoTopevaluate()],  provenance=True,  maxEntries = 100)
if 'QCD' in fnames[0]:
    p=PostProcessor(".",fnames,modules=[preselection(), nanoTopcand(), nanoTopevaluate(), topselection()],  provenance=True)
else:
    p=PostProcessor(".",fnames,modules=[preselection(), GenPart_MomFirstCp(flavour="-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24"),nanoprepro(),nanoTopcand(), nanoTopevaluate(), topselection()], provenance=True)
p.run()

#dataset_label = sys.argv[2]+'_Skim.root'
#outname = sys.argv[3]+'_Skim.root'
#print(dataset_label, outname)
#os.replace('./'+outname, "root://eosuser.cern.ch///eos/home-a/acagnott/DarkMatter/topcandidate_file/"+dataset_label)
