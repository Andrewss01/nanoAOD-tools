import ROOT
from tqdm import tqdm
import os 
path  = '/eos/user/a/apuglia/Master_Thesis/PostProcessed_Datasets/'
directories = ['QCD_HT70to100_2022', 'QCD_HT100to200_2022', 'QCD_HT200to400_2022', 'QCD_HT400to600_2022', 
'QCD_HT600to800_2022', 'QCD_HT800to1000_2022', 'QCD_HT1000to1200_2022', 'QCD_HT1200to1500_2022', 'QCD_HT1500to2000_2022']

file_txt = open('/eos/user/a/apuglia/Master_Thesis/num_events.txt', 'w')

for fileName in tqdm(os.listdir(path)):
    print(fileName)
    
    # if fileName not in directories:
    file_txt.write('directory: ')
    file_txt.write(fileName)
    file_txt.write('\n')
    for directory in tqdm(os.listdir(path + fileName)):
        print('the directory is: ', directory)
        path_interno = path + fileName + '/' + directory + '/' + directory + '.root'
        
        if not (fileName == 'QCD_HT1000to1200_2022' and directory == 'file_9'):
            rfile = ROOT.TFile.Open(path_interno)
            tree = rfile.Get('Events')

            num_event = tree.GetEntries()

            len_top_mixed   = len(tree.TopMixed_pt)
            len_top_resolved = len(tree.TopResolved_pt)

            file_txt.write('file: ') 
            file_txt.write(directory)
            file_txt.write(' ')
            file_txt.write('num event: ') 
            file_txt.write(str(num_event))
            file_txt.write(' ')
            file_txt.write('num top mixed: ') 
            file_txt.write(str(len_top_mixed))
            file_txt.write(' ')
            file_txt.write('num top resolved: ') 
            file_txt.write(str(len_top_resolved))
            file_txt.write('\n')


            
        # , ' num events: ', num_event, ' num top Mixed: ', len_top_mixed, ' num top Resolved: ', len_top_resolved)
        
