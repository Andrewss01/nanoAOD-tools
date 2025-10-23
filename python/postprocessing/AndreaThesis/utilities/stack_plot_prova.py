#!/usr/local/bin/python
import os
from tqdm import tqdm
import numpy as np 
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Object, Event, InputTree
import ROOT
from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *



hs = ROOT.THStack("hs","")
h1 = ROOT.TH1F("h1","test hstack",10,-4,4)
h1.FillRandom("gaus",20000)
h1.SetFillColor(ROOT.kRed)
h1.Scale(1.0/h1.Integral())
hs.Add(h1)
h2 = ROOT.TH1F("h2","test hstack",10,-4,4)
h2.FillRandom("gaus",15000)
h2.SetFillColor(ROOT.kBlue)
h2.Scale(1.0/h2.Integral())
hs.Add(h2)
h3 = ROOT.TH1F("h3","test hstack",10,-4,4)
h3.FillRandom("gaus",10000)
h3.SetFillColor(ROOT.kGreen)
h3.Scale(1.0/h3.Integral())
hs.Add(h3)
cs = ROOT.TCanvas("cs","cs",10,10,700,900)

hs.Draw('hist')
# h1.Draw('hist')
# h2.Draw('samehist')
# h3.Draw('samehist') 
cs.Draw()
cs.SaveAs('prova.png')