import os
import sys
import ROOT
import math
from array import array
import numpy as np
import ROOT
import numpy as np
import pickle as pkl
import matplotlib.pyplot as plt
import mplhep as hep 
hep.style.use(hep.style.CMS)
ROOT.gROOT.SetBatch()

with open("/eos/home-a/acagnott/DarkMatter/cluster_studies/variables.pkl", "rb") as file: 
    variables = pkl.load(file)

tdm_ratio = np.array(variables['tDM_mPhi1000_mChi1_Skim_Skim.root']['ratio_clustovrtrs_clust'])
tdm_cluster = np.array(variables['tDM_mPhi1000_mChi1_Skim_Skim.root']['n_cluster'])
tdm_bestscore = np.array(variables['tDM_mPhi1000_mChi1_Skim_Skim.root']['best_score'])

qcd_ratio = np.array(variables['QCD_HT1000_Skim.root']['ratio_clustovrtrs_clust'])
qcd_cluster = np.array(variables['QCD_HT1000_Skim.root']['n_cluster'])
qcd_bestscore = np.array(variables['QCD_HT1000_Skim.root']['best_score'])

tt_ratio = np.array(variables['TT_Mtt_700to1000_Skim_Skim.root']['ratio_clustovrtrs_clust'])
tt_cluster = np.array(variables['TT_Mtt_700to1000_Skim_Skim.root']['n_cluster'])
tt_bestscore = np.array(variables['TT_Mtt_700to1000_Skim_Skim.root']['best_score'])

fig, ax = plt.subplots(ncols = 3, figsize = (30,10))
ax[0].hist(tdm_ratio, range= [0, 1], bins =50, density = True, histtype = 'step',  label ='tDM m=1000')
ax[0].hist(qcd_ratio, range= [0, 1], bins =50, density = True, histtype = 'step', label='QCD')
ax[0].set_xlabel('(#cluster>trs)/#cluster')
ax[0].legend()
ax[1].hist(tdm_cluster, range= [0, 500], bins =50, density = True, histtype = 'step', label ='tDM m=1000')
ax[1].hist(qcd_cluster, range= [0, 500], bins =50, density = True, histtype = 'step', label='QCD')
ax[1].set_xlabel('#cluster')
ax[1].legend()
ax[2].hist(tdm_bestscore, range= [0, 150], bins =50, density = True, histtype = 'step', label ='tDM m=1000')
ax[2].hist(qcd_bestscore, range= [0, 150], bins =50, density = True, histtype = 'step', label='QCD')
ax[2].set_xlabel('best_score')
#ax[2].set_yscale('Log')
ax[2].legend()
plt.savefig('/eos/home-a/acagnott/DarkMatter/cluster_studies/testfig.png')

print(len(tdm_ratio))
print(len(tdm_cluster))
fig, ax = plt.subplots(ncols = 3, figsize = (30,10))
h = ax[0].hist2d(tdm_ratio, tdm_cluster, 
                 range = np.array([(0, 1), (0, 500)]), cmin = 0.001, bins = [50,10], density = True,  label ='tDM m=1000') 
fig.colorbar(h[3], ax=ax[0])
h = ax[1].hist2d(qcd_ratio, qcd_cluster, 
                 range = np.array([(0, 1), (0, 500)]), cmin = 0.001,bins = [50,10], density = True, label='QCD')
fig.colorbar(h[3], ax=ax[2])
h = ax[2].hist2d(tt_ratio, tt_cluster, 
                 range = np.array([(0, 1), (0, 500)]), cmin = 0.001,bins = [50,10], density = True, label='QCD')
fig.colorbar(h[3], ax=ax[1])
ax[0].set_xlabel('(#cluster>trs)/#cluster')
ax[1].set_xlabel('(#cluster>trs)/#cluster')
ax[2].set_xlabel('(#cluster>trs)/#cluster')
ax[0].set_ylabel('#cluster')
ax[1].set_ylabel('#cluster')
ax[2].set_ylabel('#cluster')
ax[0].set_title('tDM_mPhi=1000')
ax[1].set_title('QCD_HT700to1000')
ax[2].set_title('TT_Mtt700to1000')
#ax.legend()
plt.savefig('/eos/home-a/acagnott/DarkMatter/cluster_studies/test2fig.png')


fig, ax = plt.subplots(ncols = 3, figsize = (20,10))
h = ax[0].hist2d(tdm_ratio, tdm_bestscore,
                 range = np.array([(0, 1), (0, 1)]), cmin = 0.001, bins = [50,20], density = True,  label ='tDM m=1000') 
fig.colorbar(h[3], ax=ax[0])
h = ax[1].hist2d(qcd_ratio, qcd_bestscore, 
                 range = np.array([(0, 1), (0, 1)]), cmin = 0.001,bins = [50,20], density = True, label='QCD')
fig.colorbar(h[3], ax=ax[1])
h = ax[2].hist2d(tt_ratio, tt_bestscore, 
                 range = np.array([(0, 1), (0, 1)]), cmin = 0.001,bins = [50,20], density = True, label='QCD')
fig.colorbar(h[3], ax=ax[2])

ax[0].set_xlabel('(#cluster>trs)/#cluster')
ax[1].set_xlabel('(#cluster>trs)/#cluster')
ax[2].set_xlabel('(#cluster>trs)/#cluster')
ax[0].set_ylabel('best score')
ax[1].set_ylabel('best score')
ax[2].set_ylabel('best score')
ax[0].set_title('tDM_mPhi=1000')
ax[1].set_title('QCD_HT700to1000')
ax[2].set_title('TT_Mtt700to1000')
#ax.legend()
plt.savefig('/eos/home-a/acagnott/DarkMatter/cluster_studies/test3fig.png')

x, y = [], []
for cut in np.arange(0.01, 1.01, 0.01):
    y.append(np.sum((tdm_ratio>0.2)+(tdm_bestscore>cut))/(len(tdm_ratio)))
    x.append(np.sum((qcd_ratio>0.2)+(qcd_bestscore>cut))/len(qcd_ratio))
fig, ax = plt.subplots()
ax.plot(x,y)
ax.set_xlabel("fpr")
ax.set_ylabel("tpr")
ax.set_ylim([0,1])
ax.set_xlim([0,1])
plt.savefig("/eos/home-a/acagnott/DarkMatter/cluster_studies/testRoc.png")
