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
from PhysicsTools.NanoAODTools.postprocessing.examples.MCweight_writer import *
import sys

fnames = [sys.argv[1]]
label = sys.argv[4]

if 'QCD' in fnames[0]:
    p=PostProcessor(".",fnames,modules=[MCweight_writer(), preselection(), nanoTopcand(), nanoTopevaluate()],  provenance=True, histFileName="histOut.root", histDirName="plots", maxEntries=10)
else:
    p=PostProcessor(".",fnames,modules=[MCweight_writer(), preselection(), GenPart_MomFirstCp(flavour="-5,-4,-3,-2,-1,1,2,3,4,5,6,-6,24,-24"),nanoprepro(),nanoTopcand(), nanoTopevaluate()], provenance=True, histFileName="histOut"+label+".root", histDirName="plots", maxEntries=10)
p.run()

