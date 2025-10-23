import ROOT
import pickle as pkl
path_pkl = '/eos/user/a/apuglia/Master_Thesis/pkls/'
name_file = 'training_dataset_1.pkl'

path_to_file = path_pkl + name_file

with open(path_to_file, "rb") as f:
    data      = pkl.load(f)

print(data.keys())

string_components = ''
for c in data.keys():
    if string_components == '':
        string_components += c
        
    else:
        string_components += ','
        string_components += c

print(string_components)
print(len(data.keys()))