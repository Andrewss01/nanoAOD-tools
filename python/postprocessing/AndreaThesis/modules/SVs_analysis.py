import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection, Event
from PhysicsTools.NanoAODTools.postprocessing.framework.treeReaderArrayTools import *
from PhysicsTools.NanoAODTools.postprocessing.tools import * 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import numpy as np

class SVs_dlen(Module):
    def __init__(self):
        self.writeHistFile = True


    def beginJob(self, histFile=None, histDirName=None):
        Module.beginJob(self, histFile, histDirName)
        
        self.h_dlen_true_top = ROOT.TH1F('dlen_sv_true_tops'  , 'dlen sv true tops' , 100, 0, 50)
        self.h_dlen_false_top = ROOT.TH1F('dlen_sv_false_tops', 'dlen sv false tops', 100, 0, 50)

        self.addObject(self.h_dlen_true_top)
        self.addObject(self.h_dlen_false_top)

    def analyze(self, event):
        tops    = Collection(event, 'TopMixed')
        SVs     = Collection(event, 'SV')
        indexes = Collection(event, 'IndexesSV')
        sv_indexes = []
        for sv_idx in indexes:
            sv_indexes.append(sv_idx.idxSV)

        for top_num, top in enumerate(tops):
            start_index = sv_indexes.index(-(top_num + 1))
            stop_index  = sv_indexes.index(-(top_num + 2))

            sv_to_append = sv_indexes[start_index + 1: stop_index]

            for sv_idx in sv_to_append:
                sv = SVs[sv_idx] 
                if top.truth == 1:
                    self.h_dlen_true_top.Fill(sv.dlen)
                else:
                    self.h_dlen_false_top.Fill(sv.dlen)

        return True 