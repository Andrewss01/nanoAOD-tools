import ROOT
import cmsstyle as CMS
def draw_stack_qcd ( histo, canv_name = "QCD shape FT scores" ,extraTest="", iPos=11, energy="", lumi = "",  addInfo="", ytitle = ""):
    CMS.SetExtraText(extraTest)
    iPos = iPos
    canv_name = canv_name
    CMS.SetLumi(lumi)
    
    CMS.SetEnergy(energy)
    CMS.ResetAdditionalInfo()
    CMS.AppendAdditionalInfo(addInfo)
    CMS.setCMSStyle()
    



    
    y_max= histo.GetMaximum()*1.2 # Aggiungi 20% di margine
    x_max = 1
    # x_max_stack = hs_ft.GetXaxis().GetXmax()

    # x_max = max(x_max_stack, x_max_data)
    x_min = 0
    # x_max = 1
    y_min = 1
    # y_max = 10**6
    if 'FT' in canv_name:
        x_axis_name = 'True Top vs False Top Scores'
    else:
        x_axis_name = 'True Top vs QCD Scores'
    ytitle = 'Events'

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

    CMS.cmsObjectDraw(histo,"HIST")


    return canv


file_ = '/eos/user/a/apuglia/Master_Thesis/Graphics/lstm/stack_plot_qcd_best_ptcut.root'
file =  ROOT.TFile.Open(file_, 'READ')
c_ft = file.Get('FT Scores qcd_best')
c_qcd = file.Get('QCD Scores qcd_best')

# c_ft.ls()
hs_ft = c_ft.GetPrimitive('hs_ft_scores')
h_ft_data = c_ft.GetPrimitive('ttvsft_scores')
hs_qcd = c_qcd.GetPrimitive('hs_qcd_scores')
h_qcd_data = c_qcd.GetPrimitive('ttvsqcd_scores')


# for hists in hs_ft.GetHists():
#     print(hists.FindBin(0)  )
#     print(hists.FindBin(1)  )

h_ft_tt = None
for hist in hs_ft.GetHists():
    if hist.GetName() == "histo_tt":
        h_ft_tt = hist
        break

h_qcd_tt = None
for hist in hs_qcd.GetHists():
    if hist.GetName() == "histo_tt":
        h_qcd_tt = hist
        break


h_diff = ROOT.TH1F('qcd shape ft score', 'qcd shape ft score', 50, 0,1)

for i in range(1,52):
    num_data = h_ft_data.GetBinContent(i)
    num_tt = h_ft_tt.GetBinContent(i)
    diff = num_data - num_tt

    h_diff.SetBinContent(i,diff)
# Plottare la differenza
canvas = draw_stack_qcd(h_diff)
# h_diff.Draw()

# if file.Get("QCD Shape FT Scores"):
#     file.Delete("QCD Shape FT Scores")
canvas.Draw()

file_save = ROOT.TFile.Open('/eos/user/a/apuglia/Master_Thesis/Graphics/qcd_shapes.root', 'RECREATE')
canvas.Write()


h_diff_qcd = ROOT.TH1F('qcd shape qcd score', 'qcd shape qcd score', 50, 0,1)

for i in range(1,52):

    num_data_qcd = h_qcd_data.GetBinContent(i)
    num_tt_qcd = h_qcd_tt.GetBinContent(i)
    diff = num_data_qcd - num_tt_qcd

    h_diff_qcd.SetBinContent(i,diff)
# Plottare la differenza


canvas_qcd = draw_stack_qcd(h_diff_qcd, 'QCD Shape QCD Scores')
canvas_qcd.Draw()
canvas_qcd.Write()