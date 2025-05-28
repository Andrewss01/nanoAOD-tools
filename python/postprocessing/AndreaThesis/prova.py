import ROOT
# import pickle as pkl


# file_pkl = '/eos/user/a/apuglia/thesis/training_dataset/pkls_19_05_2025/trainingSet_TT_semilep_file0.root.pkl'
# file = open(file_pkl, 'rb')
# data = pkl.load(file)
# categories = ['3j1fj', '2j1fj', '3j0fj']
# for key in data.keys():
#     for cat in categories:
#         print('key: ', key, 'cat: ', cat)
#         for i in range(6):
#             print('len is of num: ', i, ' ', len(data[key][cat][i]))

# print(len(data['TT_semilep_file0.root']['3j0fj'][3]))
# file = ROOT.TFile.Open('histOut.root')
# file.ls()

# directory= file.Get('plots')
# directory.ls()

file = ROOT.TFile.Open('prova.root')
file.ls()

tree = file.Get('Events')
print(tree.GetEntries())