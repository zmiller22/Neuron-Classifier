#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 15:29:34 2020

@author: zack
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed April 23 14:26:29 2020

@author: Zachary Miller
"""
#%% Import packages
import numpy as np
import pandas as pd
import sklearn
from sklearn.preprocessing import LabelEncoder, StandardScaler
import sklearn.manifold
from sklearn.feature_selection import SelectKBest, f_classif

import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import visualization_funcs

#%% Load and preprocess data and labels

STANDARDIZE = False
PCA_FIRST = True
NUM_PCA_COMP = 50
PERPLEXITY = 30

COLORS =  {0:'grey', 1:'red', 2:'green', 3:'blue', 4:'cyan', 5:'magenta'}
NT_DICT = {0:'Unlabeled', 1:'Gad1b', 2:'VGlut2a'}
CT_DICT = {0:'Unlabeled', 1:'Eurydendroid Cells', 2:'Retinal Ganglion Cells',
           3:'Mitral Cells'}

data_file_path = '/home/zack/Desktop/Lab_Work/Data/neuron_morphologies/Zebrafish/aligned_040120/zbrain_neuron_spatial_morphometrics_Zbrain_MECE_masks_reflected_x.csv'
lbl_file_path = '/home/zack/Desktop/Lab_Work/Data/neuron_morphologies/Zebrafish/aligned_040120/metadata.csv'

data_df = pd.read_csv(data_file_path, index_col=0)
lbl_df = pd.read_csv(lbl_file_path, index_col=0)

data_cols = data_df.columns
lbl_cols = lbl_df.columns

if STANDARDIZE==True:
    # Standardize the data
    scaler = StandardScaler()
    data_df[data_cols] = scaler.fit_transform(data_df[data_cols])
    
# Combine labels and data
combined_df = pd.concat([lbl_df, data_df], axis=1, sort=False)

# # Convert text labels to integers
# combined_df = visualization_funcs.convertCellTypeLabels(combined_df)
# combined_df = visualization_funcs.convertNeurotransmitterLabels(combined_df)

# # Get values out of combined_df
# data = combined_df.values[:,2:]
# nt_lbls = combined_df['gal4'].values
# ct_lbls = combined_df['cell_type'].values

#%% Run PCA and TSNE on the data 
pca = sklearn.decomposition.PCA()
pca.fit(data)
pca_data = pca.transform(data)
pca_var = pca.explained_variance_ratio_

if PCA_FIRST==True: tsne_data = pca_data[:,0:NUM_PCA_COMP]
elif PCA_FIRST==False: tsne_data = data
tsne_2 = sklearn.manifold.TSNE(n_components=2, perplexity=PERPLEXITY)
tsne_3 = sklearn.manifold.TSNE(n_components=3, perplexity=PERPLEXITY)

tsne_data_2 = tsne_2.fit_transform(tsne_data)
tsne_data_3 = tsne_3.fit_transform(tsne_data)

#%% Visualize soma locations
soma_data = data_df[['SomaX','SomaY','SomaZ']].values

# 3d plot fo soma locations
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(soma_data[:,0], soma_data[:,1], soma_data[:,2])
plt.show()

#%% Plot elbow plot of the explained PC variance
plt.plot(range(pca_var.shape[0]), pca_var, color='k', marker='.',
         markerfacecolor='r', markersize=8)
plt.title('Explained Variance Ratio of PCs')
plt.xlabel('PC #')
plt.ylabel('% Explained Variance')
plt.show()

#%% Create 2 component PCA plot for neurotransmitter labels
var_frac = np.sum(pca_var[0:2])
print("Fraction Explained Variance: ", var_frac)

fig = plt.figure()
ax = fig.add_subplot(111)
for g in np.unique(nt_lbls):
    idx = np.where(nt_lbls==g)
    if g == 0:
        ax.scatter(pca_data[idx,0], pca_data[idx,1], c=COLORS[g], alpha=0.4, 
                   label=NT_DICT[g])
        
    else: 
        ax.scatter(pca_data[idx,0], pca_data[idx,1], c=COLORS[g], alpha=0.6, 
                   label=NT_DICT[g])

ax.set_title('2d PCA Projection of All Neurons')
ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.legend()

plt.show()

#%% Create 2 component PCA plot for cell type labels
var_frac = np.sum(pca_var[0:2])
print("Fraction Explained Variance: ", var_frac)

fig = plt.figure()
ax = fig.add_subplot(111)
for g in np.unique(ct_lbls):
    idx = np.where(ct_lbls==g)
    if g == 0:
        ax.scatter(pca_data[idx,0], pca_data[idx,1], c=COLORS[g], alpha=0.4, 
                   label=CT_DICT[g])
        
    else:
        ax.scatter(pca_data[idx,0], pca_data[idx,1], c=COLORS[g], alpha=0.8, 
                   label=CT_DICT[g])

ax.set_title('2d PCA Projection of All Neurons')
ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.legend()

plt.show()

#%% Create 3 component PCA plot for neurotransmitter labels
var_frac = np.sum(pca_var[0:3])
print("Fraction Explained Variance: ", var_frac)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for g in np.unique(nt_lbls):
    idx = np.where(nt_lbls==g)
    if g == 0:
        ax.scatter(pca_data[idx,0], pca_data[idx,1], pca_data[idx,2], c=COLORS[g], 
                   alpha=0.3, label=NT_DICT[g])
        
    else:
        ax.scatter(pca_data[idx,0], pca_data[idx,1], pca_data[idx,2], c=COLORS[g], 
                   alpha=1, label=NT_DICT[g])

ax.set_title('3d PCA Projection of All Neurons')
ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.set_zlabel('PC3')
ax.legend()

plt.show()

#%% Create 3 component PCA plot for cell type labels
var_frac = np.sum(pca_var[0:3])
print("Fraction Explained Variance: ", var_frac)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for g in np.unique(ct_lbls):
    idx = np.where(ct_lbls==g)
    if g == 0:
        ax.scatter(pca_data[idx,0], pca_data[idx,1], pca_data[idx,2], c=COLORS[g], 
                   alpha=0.1, label=CT_DICT[g])
        
    else:
        ax.scatter(pca_data[idx,0], pca_data[idx,1], pca_data[idx,2], c=COLORS[g], 
                   alpha=1, label=CT_DICT[g])

ax.set_title('3d PCA Projection of All Neurons')
ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.set_zlabel('PC3')
ax.legend()

plt.show()

#%% Create 2 component tsne plot with neurotransmitter labels
fig = plt.figure()
ax = fig.add_subplot(111)
for g in np.unique(nt_lbls):
    idx = np.where(nt_lbls==g)
    if g == 0:
        ax.scatter(tsne_data_2[idx,0], tsne_data_2[idx,1], c=COLORS[g], alpha=0.4, 
                   label=NT_DICT[g])
    else:
        ax.scatter(tsne_data_2[idx,0], tsne_data_2[idx,1], c=COLORS[g], alpha=0.8, 
                   label=NT_DICT[g])

ax.set_title('2d TSNE Projection of All Neurons')
ax.set_xlabel('C1')
ax.set_ylabel('C2')
ax.legend()

plt.show()

#%% Create 2 component tsne plot with cell type labels
fig = plt.figure()
ax = fig.add_subplot(111)
for g in np.unique(ct_lbls):
    idx = np.where(ct_lbls==g)
    if g == 0:
        ax.scatter(tsne_data_2[idx,0], tsne_data_2[idx,1], c=COLORS[g], alpha=0.4, 
                   label=CT_DICT[g])
    else:
        ax.scatter(tsne_data_2[idx,0], tsne_data_2[idx,1], c=COLORS[g], alpha=0.8, 
                   label=CT_DICT[g])

ax.set_title('2d TSNE Projection of All Neurons')
ax.set_xlabel('C1')
ax.set_ylabel('C2')
ax.legend()

plt.show()


