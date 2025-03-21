##### FIX SEED #####
seed_value= 0
import os
os.environ['PYTHONHASHSEED']=str(seed_value)

scram_arch = os.getenv('SCRAM_ARCH')
if scram_arch:
    print(f'SCRAM_ARCH is set to: {scram_arch}')
else:
    print('SCRAM_ARCH is not set')

import random
random.seed(seed_value)
import numpy as np
np.random.seed(seed_value)
from tensorflow import keras
import keras_tuner
import tensorflow as tf
tf.random.set_seed(12345)
session_conf = tf.compat.v1.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)
sess = tf.compat.v1.Session(graph=tf.compat.v1.get_default_graph(), config=session_conf)
from keras import backend as K
K.set_session(sess)



import os
import sys
from curses import keyname
#import tensorflow as tf
#from tensorflow import keras
import keras_tuner as kt
import pickle as pkl
# import random
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score, f1_score, confusion_matrix, auc, roc_curve
from tensorflow.keras.layers import Dense, Dropout, LSTM, concatenate, GRU,Masking, Activation, TimeDistributed, Conv1D, BatchNormalization, MaxPooling1D, Reshape, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import plot_model, to_categorical
from tensorflow.keras.backend import sigmoid
from tensorflow.keras import regularizers
#from keras.utils.generic_utils import get_custom_objects
from keras.utils import CustomObjectScope
import matplotlib.pyplot as plt
import ROOT
import json
import mplhep as hep
hep.style.use(hep.style.CMS)
from sklearn.utils import class_weight
import argparse


ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

### ADD ARGUMENTS

usage = 'python3 Training_MC.py -s TT,ZJ1,ZJ2 -i ./training_dataset/trainingSet_19k.pkl'
parser = argparse.ArgumentParser(usage)
parser.add_argument('-s', '--samples'  , dest = 'samples'   ,  required = True)
parser.add_argument('-i', '--inFile'   , dest = 'inFile'    ,  required = True)
parser.add_argument('-m', '--outModel' , dest = 'outModel'  ,  required = False, default = './models/model_prova.h5')
parser.add_argument('-j', '--outJson'  , dest = 'outJson'   ,  required = False, default = './trainings/score_tresholds_prova.json')
parser.add_argument('-g', '--graphics' , dest = 'graphics'  ,  required = False, default = './graphics/Multiclass_prova')
parser.add_argument('-v', '--verbose'  , dest = 'verbose'   ,  required = False, default = True)
parser.add_argument('-o', '--multiscore', dest = 'multiscore',  required = False, default = True)
args          = parser.parse_args()
samples       = args.samples.split(',')
inFile        = args.inFile
outModel      = args.outModel
path_outJson  = args.outJson
path_graphics = args.graphics
verbose = args.verbose
multiple_outputs = args.multiscore

### OPEN FILE

with open(inFile, 'rb') as fpkl:
    dataset = pkl.load(fpkl)
components = dataset.keys()
categories = ['3j1fj', '3j0fj', '2j1fj']

### REMOVE EMPTY COMPONENTS

components_todrop  = []
for c in components:
    for cat in categories:
        if dataset[c][cat] == 0 or c not in samples:  #Rimuove le componenti vuote o quelle non selezionate dall'utente
            components_todrop.append(c)
            break
for c_todrop in components_todrop:
    dataset.pop(c_todrop)

### DATASET BALANCING (remove some False Tops) 

for c in components:
    for cat in categories:
        idx_truetop  = [i for i, x in enumerate(dataset[c][cat][3]==1) if x==True]
        idx_falsetop = [i for i, x in enumerate(dataset[c][cat][3]==0) if x==True]
        print("stiamo selezionando i top per:",c,"",cat)
        if len(idx_truetop)==0:
            print('PROVA NO TRUE TOP')
            ids_todrop   = random.sample(idx_falsetop, int(len(idx_falsetop)*(0.9)))
        elif len(idx_falsetop)>2*len(idx_truetop):    
            ids_todrop   = random.sample(idx_falsetop, len(idx_falsetop)-2*len(idx_truetop))
        else:
            ids_todrop=[]
        dataset[c][cat][0] = np.delete(dataset[c][cat][0], ids_todrop, axis=0)
        dataset[c][cat][1] = np.delete(dataset[c][cat][1], ids_todrop, axis=0)
        dataset[c][cat][2] = np.delete(dataset[c][cat][2], ids_todrop, axis=0)
        dataset[c][cat][3] = np.delete(dataset[c][cat][3], ids_todrop, axis=0)

class trainer:
    def __init__(self, X_jet, X_fatjet, X_top, y):
        self.X_jet = X_jet
        self.X_fatjet = X_fatjet
        self.X_top = X_top
        self.y = y
        self.best_hyperparameters = None
        self.history  = None
        self.model = None


    def split(self, test_size):
        self.X_jet_train, self.X_jet_test, self.X_fatjet_train, self.X_fatjet_test, self.X_top_train, self.X_top_test, self.y_train, self.y_test= train_test_split(self.X_jet, self.X_fatjet, self.X_top, self.y,
                                                                                                                                         stratify = self.y, shuffle = True, test_size = test_size)

    def model_builder(self, hp):
        InputShape_FatJet = self.X_fatjet_train.shape[1]
        InputShape_Jet = self.X_jet_train.shape[2]
        InputShape_Top  = self.X_top_train.shape[1]
        
        fj_inputs   = tf.keras.Input(shape=(InputShape_FatJet,),   name="fatjet")    #x
        jet_inputs  = tf.keras.Input(shape=(None,InputShape_Jet,), name="jet")       #y
        top_inputs  = tf.keras.Input(shape=(InputShape_Top,),      name="top")       #z

        ## Fatjet inputs
        
        x = BatchNormalization()(fj_inputs)
        fj_units              = hp.Int('fj_units', min_value = 1, max_value = 10, step = 1)
        fj_activation         = hp.Choice("fj_activation", values=["relu", "sigmoid", "tanh"])
        fj_kernel_initializer = hp.Choice('fj_kernel_initializer', values = ['random_uniform' , 'random_normal'])
        x = Dense(units = fj_units, activation =  fj_activation, kernel_initializer = fj_kernel_initializer)(x)

        #Jets inputs

        y = Masking(mask_value = 0.)(jet_inputs) 
        y = BatchNormalization()(y)

        j_units = hp.Int('j_units', min_value = 1, max_value = 10, step = 1)
        j_activation = hp.Choice("j_activation", values= ['relu', 'sigmoid', 'tanh'])
        j_kernel_initializer = hp.Choice('j_kernel_initializer', values = ['random_uniform', 'random_normal'])

        y = keras.layers.LSTM(units = j_units,
                              activation = j_activation, 
                              kernel_initializer = j_kernel_initializer, 
                              dropout = 0.0)(y)
        
        #top inputs

        z = Dense(1, activation = 'relu')(top_inputs)

        ### jets+fatjets

        x = concatenate([x,y])
        x = concatenate([x,z])
        x = Dense(5, activation = 'relu', kernel_initializer = 'random_normal')(x)

        outputs = Dense(3, activation = 'softmax')(x)

        self.model = tf.keras.Model(inputs = [fj_inputs, jet_inputs, top_inputs], outputs = outputs)


        trainer = tf.keras.optimizers.Nadam(learning_rate = 0.001)
        loss = tf.keras.losses.SparseCategoricalCrossentropy()
        self.model.compile(optimizer = trainer, loss = loss, metrics = ['accuracy'])
        
        return self.model
    
    def callbacks(self):
        early_stop = keras.callbacks.EarlyStopping(monitor="val_accuracy",
                                                   mode="max", # quantity that has to be monitored(to be minimized in this case)
                                                   patience=40, # number of epochs with no improvement after which training will be stopped.
                                                   min_delta=1e-5,
                                                   restore_best_weights=True) # update the model with the best-seen weights

        # Reduce learning rate when a metric has stopped improving
        reduce_LR = keras.callbacks.ReduceLROnPlateau(monitor="val_accuracy",
                                                      mode="max",# quantity that has to be monitored
                                                      min_delta=1e-5,
                                                      factor=0.1, # factor by which LR has to be reduced...
                                                      patience=10, #...after waiting this number of epochs with no improvements on monitored quantity
                                                      min_lr=1e-15) 
        self.callback_list=[early_stop, reduce_LR]

    def tune_hps(self, max_epochs = 1000, batch_size = 250, factor = 3, project_name = 'hps_tuning'):
        if not hasattr(self, 'X_jet_train'):
            self.split(test_size= 0.3)
        objective = kt.Objective('val_accuracy', direction = 'max')
        tuner = kt.Hyperband(self.model_builder, objective=objective, factor=factor, project_name=project_name)
        tuner.search_space_summary()
        self.callbacks()
        
        tuner.search({'fatjet': self.X_fatjet_train, 'jet': self.X_jet_train, 'top': self.X_top_train},
                     self.y_train, validation_split = 0.3, shuffle = True, callbacks = self.callback_list, 
                     epochs = max_epochs, 
                     batch_size = batch_size, verbose = 1)

        self.best_hyperparameters = tuner.get_best_hyperparameters(num_trials=1)
        #self.model = tuner.hypermodel.build(self.best_hyperparameters)
        print(f'best hps found: \n {self.best_hyperparameters[0].values}')
        #return self.best_hyperparameters
    
    def training(self, validation_split = 0.3, epochs = 50, batch_size = 1, verbose = True, save_model = False, path_to_model = './models/model_prova.h5'):
        if self.model == None and self.best_hyperparameters == None:
            print('no model avaible')
        
        if not hasattr(self, 'X_jet_train'):
            self.split(test_size= 0.3)
        
        weights = class_weight.compute_class_weight(class_weight= 'balanced', classes = np.unique(self.y_train), y = np.concatenate(self.y_train))
        class_weights = {0: weights[0], 1: weights[1], 2: weights[2]}
        self.history = self.model.fit({"fatjet": self.X_fatjet_train, "jet": self.X_jet_train, "top": self.X_top_train}, self.y_train,
                                       callbacks=self.callback_list, validation_split=validation_split, epochs=epochs, batch_size=batch_size, verbose=verbose,
                                       class_weight=class_weights)
        
        if save_model:
            self.model.save(path_to_model)

    def load_model(self, model_to_load):
        self.model = tf.keras.model.load_model(model_to_load)

    def evaluate(self, X_jet_test = None, X_fatjet_test = None, X_top_test = None, y_test = None):
        if (X_jet_test is None) and (X_fatjet_test is None) and (X_top_test is None) and (y_test is None):
            self.eval_result = self.model.evaluate({"fatjet": self.X_fatjet_test, "jet": self.X_jet_test, "top": self.X_top_test}, self.y_test)
            return self.eval_result
        else:
            eval_result      = self.model.evaluate({"fatjet": X_fatjet_test, "jet": X_jet_test, "top": X_top_test}, y_test)
            return eval_result
        
    def predict(self, X_jet_train = None, X_fatjet_train = None, X_top_train = None, X_jet_test = None, X_fatjet_test = None, X_top_test = None):
        if (X_jet_train is None) and (X_fatjet_train is None) and (X_top_train is None) and (X_jet_test is None) and (X_fatjet_test is None) and (X_top_test is None):
            self.y_pred_train = self.model.predict({"fatjet": self.X_fatjet_train, "jet": self.X_jet_train, "top": self.X_top_train})
            self.y_pred_test  = self.model.predict({"fatjet": self.X_fatjet_test, "jet": self.X_jet_test, "top": self.X_top_test})
        else:
            y_pred_train      = self.model.predict({"fatjet": X_fatjet_train, "jet": X_jet_train, "top": X_top_train})
            y_pred_test       = self.model.predict({"fatjet": X_fatjet_test, "jet": X_jet_test, "top": X_top_test})
            return y_pred_train, y_pred_test
    
## DATASET DI INPUT
X_jet                     = np.concatenate([dataset[c][cat][0] for c in samples for cat in categories]) # here we use only the samples selected by the user
X_fatjet                  = np.concatenate([dataset[c][cat][1] for c in samples for cat in categories]) # here we use only the samples selected by the user
X_top                     = np.concatenate([dataset[c][cat][2] for c in samples for cat in categories]) # here we use only the samples selected by the user
y                         = np.concatenate([dataset[c][cat][3] for c in samples for cat in categories]) # here we use only the samples selected by the user
  
## CASO MULTISCORE
def Multi_score(data):
    a = []
    for c in samples:
        for cat in categories:
            for j in data[c][cat][3]:
                if j== 0 and c == 'TT': #Se un fondo TT aggiunge 1 
                    a.append([1])
                elif j == 1 and c == 'TT': #Se è segnale aggunge 0 
                    a.append([0])
                elif 'ZJ' in c:
                    a.append([2])
    y = np.concatenate([a])
    return y

#multiple_outputs=  True
if multiple_outputs:
    y = Multi_score(dataset)

data = X_jet, X_fatjet, X_top, y

trainer1 = trainer(*data)
trainer1.split(0.3)
trainer1.tune_hps(max_epochs= 1000, batch_size = 250, project_name = 'tuning_jets_fatjets')

best_hps = trainer1.best_hyperparameters
#tuner.get_best_hyperparameters(num_trials=1)
print(f"BEST HPS FOUND:\n{best_hps[0].values}")

# Save best_hps to json file
#path_to_model_folder = '/eos/user/a/apuglia/SWAN_projects/thesis/CMSSW_14_1_7/src/' 
path_to_model_folder = '/afs/cern.ch/user/a/apuglia/CMSSW_14_1_7/src/PhysicsTools/NanoAODTools/python/postprocessing/ML' 
''
with open(f"{path_to_model_folder}/best_hps_jets_fatjets.json", "w") as jsFile:
    # f.write(best_hps[0].values)
    json.dump(best_hps[0].values, jsFile, indent=4)
    
        

        