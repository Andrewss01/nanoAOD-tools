import ROOT
from math import sqrt

model = 'lstm'
file_path = '/eos/user/a/apuglia/Master_Thesis/Graphics/' + model + '/stack_plot_best_single_top_ptcut.root'
file = ROOT.TFile.Open(file_path, 'READ')
# file.ls()ù
name_file = '/eos/user/a/apuglia/Master_Thesis/Graphics/' + model + '/scale_factors.txt'
canv_qcd = file.Get('QCD Scores best_single_top')

stack = canv_qcd.GetPrimitive("hs_qcd_scores")  # o FindObject()

hists = stack.GetHists()


num_sig_event_selected =0
num_sig_event = 0
num_bkg_event = 0
num_data_event =0

qcd_score_cnn = 0.94
qcd_bin_cnn = 24
end_bin_qcd_cnn =26

qcd_score_lstm = 0.95
qcd_bin_lstm = 24
end_bin_qcd_lstm = 26 

# stack.ls()
for hist in hists:
    name  = hist.GetName()
    if model == 'lstm':
        qcd_score = qcd_score_lstm
        qcd_bin = qcd_bin_lstm
        end_bin_qcd = end_bin_qcd_lstm
    elif model == 'cnn':
        qcd_score = qcd_score_cnn
        qcd_bin = qcd_bin_cnn
        end_bin_qcd = end_bin_qcd_cnn
    if 'wj' in name or 'QCD' in name or 'tw' in name or 'tt_dilep' in name:
        print('name is:', name)
        num_bkg_event += hist.Integral(qcd_bin,end_bin_qcd)
    elif name == 'histo_tt':
        num_sig_event_selected += hist.Integral(qcd_bin, end_bin_qcd)
        num_sig_event += hist.Integral(0, end_bin_qcd)

h_data = canv_qcd.GetPrimitive('ttvsqcd_scores')
num_data_event += h_data.Integral(qcd_bin, end_bin_qcd)


scale_fact_nominal = (num_data_event  - num_bkg_event)/(num_sig_event_selected)
bkg_error = sqrt(num_bkg_event)
sig_error = sqrt(num_sig_event_selected)
scale_fact_stat_error = (1/(num_sig_event_selected))*(bkg_error) + (num_bkg_event/(num_sig_event_selected**2))*(sig_error)

eff_signal_mc = num_sig_event_selected/num_sig_event
eff_signal_mc_error = sqrt(num_sig_event_selected)/num_sig_event

eff_data = scale_fact_nominal*eff_signal_mc
eff_data_error = scale_fact_nominal* eff_signal_mc_error +  scale_fact_stat_error * eff_signal_mc


scale_fact_up = (num_data_event - ((3/2)*num_bkg_event))/(num_sig_event_selected)
scale_fact_dw = (num_data_event - (num_bkg_event/2))/ (num_sig_event_selected)

eff_data_up = scale_fact_up * eff_signal_mc
eff_data_dw = scale_fact_dw * eff_signal_mc



with open(name_file, 'w') as file_wr:
    file_wr.write('QCD SCALE FACTORS LSTM MODEL')
    file_wr.write('sig: '+ str(int(num_sig_event))+ ' statistical error: '+ str(int(sig_error))+ '\n')
    file_wr.write('bkg: '+ str(int(num_bkg_event))+ ' statistical error: '+ str(int(bkg_error))+ '\n')
    file_wr.write('data: '+ str(int(num_data_event))+ '\n')
    file_wr.write('scale factor: '+ str(round(scale_fact_nominal,4)) + ' statistical error: '+ str(round(scale_fact_stat_error,4))+ '\n')
    file_wr.write('scale factor dw value: '+ str(round(scale_fact_dw,4))+ '\n')
    file_wr.write('scale factor up value: '+ str(round(scale_fact_up,4))+ '\n')
    file_wr.write('efficiency signal: '+ str(eff_signal_mc) + ' statistical error: ' + str(eff_signal_mc_error) + '\n')
    file_wr.write('efficiency data: ' + str(eff_data) + ' statistical error: ' + str(eff_data_error) + '\n')
    file_wr.write('sistematic up:' + str(eff_data_up) + ' sistematic down: ' + str(eff_data_dw))

canv_ft = file.Get('FT Scores best_single_top')

stack = canv_ft.GetPrimitive("hs_ft_scores")  # o FindObject()
stack.ls()
hists = stack.GetHists()

# Accedi agli istogrammi
num_sig_event_selected=0
num_sig_event = 0
num_bkg_event = 0
num_data_event =0

ft_score_cnn = 0.91
ft_bin_cnn = 23
end_bin_ft_cnn =26

ft_score_lstm = 0.94
ft_bin_lstm = 24
end_bin_ft_lstm = 26
for hist in hists:
    name  = hist.GetName()
    # print(name)
    if model == 'lstm':
        ft_score = ft_score_lstm
        ft_bin = ft_bin_lstm
        end_bin_ft = end_bin_ft_lstm
    elif model == 'cnn':
        ft_score = ft_score_cnn
        ft_bin = ft_bin_cnn
        end_bin_ft = end_bin_ft_cnn
    if 'wj' in name or 'qcd' in name or 'tw' in name or 'tt_dilep'in name:
        print('name is: ', name)
        # print('name is: ', name, ' integral is: ', hist.Integral(qcd_bin, end_bin_qcd))
        # qcd_bin = hist.FindBin(ft_score)
        # print('ft bin is: ', qcd_bin)
        num_bkg_event += hist.Integral(ft_bin,end_bin_ft)
    elif name == 'histo_tt':
        # print('name is: ', name, ' integral is: ', hist.Integral(ft_bin, end_bin_ft))
        num_sig_event_selected += hist.Integral(ft_bin, end_bin_ft)
        num_sig_event += hist.Integral(0, end_bin_ft)

h_data = canv_ft.GetPrimitive('ttvsft_scores')
num_data_event += h_data.Integral(ft_bin, end_bin_ft)


scale_fact_nominal = (num_data_event  - num_bkg_event)/(num_sig_event_selected)
bkg_error = sqrt(num_bkg_event)
sig_error = sqrt(num_sig_event_selected)
scale_fact_stat_error = (1/(num_sig_event_selected))*(bkg_error) + (num_bkg_event/(num_sig_event_selected**2))*(sig_error)

eff_signal_mc = num_sig_event_selected/num_sig_event
eff_signal_mc_error = sqrt(num_sig_event_selected)/num_sig_event

eff_data = eff_signal_mc * scale_fact_nominal
eff_data_error = eff_signal_mc_error*scale_fact_nominal + scale_fact_stat_error*eff_signal_mc

scale_fact_up = (num_data_event - ((3/2)*num_bkg_event))/(num_sig_event_selected)
scale_fact_dw = (num_data_event - (num_bkg_event/2)) / (num_sig_event_selected)

eff_data_up = scale_fact_up * eff_signal_mc
eff_data_dw = scale_fact_dw * eff_signal_mc


with open(name_file, 'a') as file:
    file.write('\nFT SCALE FACTORS LSTM MODEL\n')
    file.write('sig: '+ str(int(num_sig_event)) + ' statistical error: '+ str(int(sig_error)) + '\n')
    file.write('bkg: '+ str(int(num_bkg_event)) + ' statistical error: ' + str(int(bkg_error)) + '\n')
    file.write('data: '+ str(int(num_data_event)) + '\n')
    file.write('scale factor: '+ str(round(scale_fact_nominal,4)) + ' statistical error: '+ str(round(scale_fact_stat_error,4)) + '\n')
    file.write('scale factor up value: '+ str(round(scale_fact_up,4))+ '\n')
    file.write('scale factor dw value: '+ str(round(scale_fact_dw,4)) + '\n')
    file.write('efficiency signal MC: '+ str(eff_signal_mc) + ' statistical error: ' + str(eff_signal_mc_error) +'\n')
    file.write('efficiency data: ' + str(eff_data) + ' statistical error: '+ str(eff_data_error) +'\n')
    file.write('sistematic up: ' + str(eff_data_up) + 'sistematic down: ' + str(eff_data_dw))
