# import ROOT 
import pickle as pkl
trs_file = open('/eos/user/a/apuglia/thesis/training_dataset/trainingSet_all.pkl', 'rb')
dataset = pkl.load(trs_file)
# print(dataset['zjets']['2j1fj'][5])

# components = dataset.keys()
# types = ['3j1fj','2j1fj','3j0fj']

# for c in components:
#     for t in types:
#         for i in dataset[c][t][5]:
#             if i ==1:

#                 print(i) 

print(dataset.keys())