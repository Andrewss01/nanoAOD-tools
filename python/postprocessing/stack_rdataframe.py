import ROOT
import os
from samples.samples import *
import optparse
import copy
import math
from CMS_lumi import CMS_lumi
from variables import *

usage = 'python3 stack_rdataframe.py'
parser = optparse.OptionParser(usage)
parser.add_option('-p', '--plots', dest='plots', default = False, action='store_true', help='Default make no histos')
parser.add_option('-s', '--stack', dest='stack', default = False, action='store_true', help='Default make no stacks')
parser.add_option('-C', '--cut', dest='cut', type='string', default = '', help='Default no cut')
parser.add_option('-r', '--recreate', dest='recreate', default = False, action='store_true', help='Default append histos')
parser.add_option('-m', '--mergesamples', dest='mergesamples', default = False, action='store_true', help='Default do not create a single file for bkg datasets')
(opt, args) = parser.parse_args()

ROOT.gROOT.SetBatch()

def get_files_string(d):
    folder_files = "../../crab/macros/files/"
    infile_string = open(folder_files+d.label+".txt")
    strings = infile_string.readlines()
    for s in strings: s.replace('\n', '')
    return strings        

def makestack(datasets, var, cut):
    
    c_ =cut.replace(" ", "").replace("&&","_").replace(">","g").replace(".","_")
    #"lepveto"  #""#+"_isMerged"#+"_isMix"#+"_isResolved"
    var_name = var._name+"_"+c_#'mt_'+cut  #'BestTop_pt'#"mt"#"met_pt"#
    varlabel = var._title#'m_{T}'  #"m_{T}"#"MET_{p_{T}}"#
    print(var_name)
    stack = ROOT.THStack(var_name, var_name)
    leg_stack = ROOT.TLegend(0.45,0.88,0.9,0.75)
    leg_stack.SetNColumns(2)
    leg_stack.SetFillColor(0)
    leg_stack.SetFillStyle(0)
    leg_stack.SetTextFont(42)
    leg_stack.SetBorderSize(0)
    leg_stack.SetTextSize(0.03)
    
    h_sgn = []
    for d in datasets:
        if hasattr(d,"components"):
            samples = d.components
        else:
            samples= [d]
        for s in samples:
            infile = ROOT.TFile.Open(outfolder+s.label+'.root')
            h = copy.deepcopy(ROOT.TH1D(infile.Get(var_name)))
            h.GetXaxis().SetTitle(varlabel)
            #if 'mt_' in var._name : h.Rebin(4)
            #if 'MET_pt_' in var_name:  h.Rebin()
            #if 'Top_pt_' in var_name:  h.Rebin()
            h.SetName(s.leglabel)
            if not 'Tp' in s.label:
                h.SetLineColor(s.color)
                h.SetFillColor(s.color)
                stack.Add(h)
            else:
                h.SetLineColor(s.color)
                h_sgn.append(h)
                leg_stack.AddEntry(h, s.leglabel, "l")
            infile.Close()
        if not 'Tp' in d.label : leg_stack.AddEntry(h, d.leglabel, "f")
    
    c1 = ROOT.TCanvas("c_"+var_name,"c_"+var_name,50,50,700,600)
    c1.SetLogy()
    c1.SetFillColor(0)
    c1.SetBorderMode(0)
    c1.SetFrameFillStyle(0)
    c1.SetFrameBorderMode(0)
    c1.SetLeftMargin( 0.12 )
    c1.SetRightMargin( 0.9 )
    c1.SetTopMargin( 1 )
    c1.SetBottomMargin(-1)
    c1.SetTickx(1)
    c1.SetTicky(1)
    c1.cd()

    pad1= ROOT.TPad("pad1", "pad1", 0, 0.31 , 1, 1)
    pad1.SetTopMargin(0.1)
    pad1.SetBottomMargin(-0.9)
    pad1.SetLeftMargin(0.12)
    pad1.SetRightMargin(0.05)
    pad1.SetBorderMode(0)
    pad1.SetTickx(1)
    pad1.SetTicky(1)
    pad1.Draw()
    pad1.cd()
    pad1.SetLogy()
    c1.Draw()
    stack.Draw("HIST")
    #print(stack)
    stackmaximum = stack.GetHistogram().GetMaximum()#*10000
    stackminimum = stack.GetHistogram().GetMinimum()#10**(-7)#min([h.GetMinimum() for h in h_sgn])#*0.1
    print(stackminimum, stackmaximum)
    stack.SetMinimum(stackminimum*10**(-5))
    stack.SetMaximum(stackmaximum*10000)
    stack.GetYaxis().SetTitle("# Events")
    stack.GetXaxis().SetTitle(varlabel)
    #stack.GetXaxis().SetLabelOffset(0.0)
    stack.GetYaxis().SetTitleOffset(0.85)
    stack.GetXaxis().SetLabelSize(0.03)
    stack.GetYaxis().SetLabelSize(0.05)
    stack.GetYaxis().SetTitleSize(0.07)
    stack.GetXaxis().SetTitleSize(0.05)    
    stack.SetTitle("")

    stack.Draw("HIST")
    for h in h_sgn : 
        h.Draw("same")
    leg_stack.Draw("same")
    CMS_lumi.writeExtraText = 1
    CMS_lumi.extraText = ""
    lumi_sqrtS = "%s fb^{-1}  (13 TeV)"%(lumi)
     
    iPeriod = 0
    iPos = 10
    CMS_lumi(pad1, lumi_sqrtS, iPos, "")
    
    c1.Print(repostack+var_name+".png","png")
    c1.Print(repostack+var_name+".pdf","pdf")
    
def makehistos(samples, var, cut):
    for s in samples:
        c_ = cut
        print("... ", s.label)
        strings = get_files_string(s)
        chain = ROOT.TChain("Events")
        hist = ROOT.TH1F()
        ntot = 0 
        if len(strings)>5: strings = strings[:3]
        print("looping on strings: ", len(strings))
        for f in strings: 
            chain.Add(f)
            ifile = ROOT.TFile.Open(f)
            h_genweight = ROOT.TH1F(ifile.Get("plots/h_genweight"))
            #print("N event single file:", h_genweight.GetBinContent(1))
            ntot += h_genweight.GetBinContent(1)
            ifile.Close()
        print("N tot events:" , ntot)
        w = s.sigma*lumi/ntot
        if opt.recreate :
            ofile = ROOT.TFile.Open(outfolder+s.label+'.root', "RECREATE")
        else:
            ofile = ROOT.TFile.Open(outfolder+s.label+'.root', "UPDATE")
        Rdf = ROOT.RDataFrame(chain)
        
        s_cut = cut.replace(" ", "").replace("&&","_").replace(">","g").replace(".","_")
        print(s_cut)
        if 'leptonveto' in cut:
            Rdf = Rdf.Define("goodmuon", "Muon_pt>30 && Muon_eta<2.4 && Muon_looseId==1").Define("goodelectron", "Electron_pt>30 && Electron_mvaFall17V1Iso_WPL==1")
            Rdf = Rdf.Filter("ROOT::VecOps::Sum(goodelectron) == 0").Filter("ROOT::VecOps::Sum(goodmuon) == 0")
            
            if "&& leptonveto" in cut:
                c_ = c_.replace("&& leptonveto","")
            elif "leptonveto &&" in cut:
                c_ = c_.replace("leptonveto &&","")
        print("requirements: "+c_)
        Rdf = Rdf.Filter(c_).Define("mt", "sqrt(2 * BestTop_pt * MET_pt * (1 - cos(BestTop_phi - MET_phi)))")
        #h = []
        for v in var:
            h = (Rdf.Histo1D((v._name+"_"+s_cut," ;"+v._title+"", v._nbins, v._xmin, v._xmax), v._name).GetValue())
            h.Scale(w)
            h.Write()
        ofile.Close()
        print("Done "+s.label+" !")
        #h.SetLineColor(s.color)
        #h.SetFillColor(s.color)

def mergSamples(dataset, var, cut):
    c_ =cut.replace(" ", "").replace("&&","_").replace(">","g").replace(".","_")
    
    var_name = var._name+"_"+c_#'mt_'+cut  #'BestTop_pt'#"mt"#"met_pt"#
    varlabel = var._title#'m_{T}'  #"m_{T}"#"MET_{p_{T}}"#
    #print(var_name)
    
    
    for d in datasets:
        if hasattr(d,"components"):
            samples = d.components
            h_total = ROOT.TH1D(var_name, ";"+varlabel, var._nbins, var._xmin, var._xmax)
            for s in samples:
                infile = ROOT.TFile.Open(outfolder+s.label+'.root')
                h = copy.deepcopy(ROOT.TH1D(infile.Get(var_name)))
                h_total.Add(h)
                infile.Close()
            if not os.path.exists(outfolder+s.label+'.root') :
                outfile = ROOT.TFile.Open(outfolder+d.label+'.root', "RECREATE")
            else:
                outfile = ROOT.TFile.Open(outfolder+d.label+'.root', "UPDATE")
            h_total.Write()
            outfile.Close()
            h_total.Delete()
    
f = "/eos/home-a/acagnott/DarkMatter/nosynch/v1/"
if not os.path.exists(f):
    os.mkdir(f)
outfolder = f+"plots/"
if not os.path.exists(outfolder):
    os.mkdir(outfolder)
repostack = f+"stacks/"
if not os.path.exists(repostack):
    os.mkdir(repostack)
lumi = 1
datasets = [QCD_2018, ZJetsToNuNu_2018, 
            TT_2018,
            TprimeToTZ_700_2018, TprimeToTZ_1000_2018,TprimeToTZ_1800_2018]
cut = opt.cut #lepveto && isMerged==1 && MET_pt>50 
var = []

if "Merged" in cut:
    var.append(variable(name = "BestTop_pt", title= "Top p_{T} [GeV]", taglio = cut, nbins = 10, xmin = 500, xmax=1000))
    var.append(variable(name = "BestTop_score", title= "Top score", taglio = cut, nbins = 10, xmin = 0.8, xmax=1))
elif "Mix" in cut:
    #var.append(variable(name = "BestTop_pt", title= "Top p_{T} [GeV]", taglio = cut, nbins = 30, xmin = 400, xmax=500))
    var.append(variable(name = "BestTop_pt", title= "Top p_{T} [GeV]", taglio = cut, nbins = 4, xmin = 300, xmax=500))
    var.append(variable(name = "BestTop_score", title= "Top score", taglio = cut, nbins = 8, xmin = 0.3, xmax=1))
elif "Resolved" in cut:
    #var.append(variable(name = "BestTop_pt", title= "Top p_{T} [GeV]", taglio = cut, nbins = 30, xmin = 0, xmax=400))
    var.append(variable(name = "BestTop_pt", title= "Top p_{T} [GeV]", taglio = cut, nbins = 6, xmin = 0, xmax=300))
    var.append(variable(name = "BestTop_score", title= "Top score", taglio = cut, nbins = 6, xmin = 0.5, xmax=1))
else:
    #var.append(variable(name = "BestTop_pt", title= "Top p_{T} [GeV]", taglio = cut, nbins = 30, xmin = 0, xmax=1000))
    var.append(variable(name = "BestTop_pt", title= "Top p_{T} [GeV]", taglio = cut, nbins = 20, xmin = 0, xmax=1000))
    var.append(variable(name = "BestTop_score", title= "Top score", taglio = cut, nbins = 8, xmin = 0.3, xmax=1))

var.append(variable(name = "BestTop_score", title= "Top score", taglio = cut, nbins = 30, xmin = 0, xmax=1))
var.append(variable(name = "MET_pt", title= "MET p_{T} [GeV]", taglio = cut, nbins = 30, xmin = 150, xmax=1000))
var.append(variable(name = "MET_phi", title= "MET #phi [GeV]", taglio = cut, nbins = 6, xmin = -math.pi, xmax=math.pi))
var.append(variable(name = "mt", title="M_{T} [GeV]", taglio = cut, nbins = 30, xmin = 0, xmax=2000))
var.append(variable(name = "BestTop_phi", title= "Top #phi", taglio = cut, nbins = 6, xmin = -math.pi, xmax=math.pi))
var.append(variable(name = "BestTop_eta", title= "Top #eta", taglio = cut, nbins = 9, xmin = -4, xmax=4))
var.append(variable(name = "BestTop_mass", title= "Top mass [GeV]", taglio = cut, nbins = 15, xmin = 0, xmax=500))

#if "isMerged" in cut:

if opt.plots:
    for d in datasets:
        print("Launching "+d.label)
        if not 'Tp' in d.label:
            samples = d.components
        else:
            samples = [d]
        c = opt.cut
        makehistos(samples, var, c)
cut = opt.cut #lepveto && isMerged==1 && MET_pt>50 
if opt.stack:
    for v in var:
        makestack(datasets, v , cut)
if opt.recreate:
    for d in datasets:
        if hasattr(d, "components"):
            os.popen("rm "+outfolder+d.label+".root")

if opt.mergesamples:
    for v in var:
        mergSamples(datasets, v, cut)
