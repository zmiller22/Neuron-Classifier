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
import sklearn.manifold
from sklearn.feature_selection import SelectKBest, f_classif

import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import visualization_funcs

#%% Load and preprocess data and labels

NORMALIZE = True

K_PCA = 2

K_TSNE = 2
PCA_FIRST = True
NUM_PCA_COMP = 50
PERPLEXITY = 30

COLORS =  [(0,0,0,0.1), 'blue', 'green', 'red', 'cyan', 'magenta']


data_file_path = '/home/zack/Desktop/Lab_Work/Data/neuron_morphologies/Zebrafish/aligned_040120/zbrain_neuron_spatial_morphometrics_Zbrain_MECE_masks_reflected_x.csv'
lbl_file_path = '/home/zack/Desktop/Lab_Work/Data/neuron_morphologies/Zebrafish/aligned_040120/metadata.csv'

data_df = pd.read_csv(data_file_path, index_col=0)
lbl_df = pd.read_csv(lbl_file_path, index_col=0)

if NORMALIZE==True:
    idx_lbls = data_df.index.values
    col_lbls = data_df.columns

    # Standardize the data
    normalizer = sklearn.preprocessing.StandardScaler()
    norm_data_vals = normalizer.fit_transform(data_df.values)

    # Put standardized, combined data into a dataframe
    data_df = pd.DataFrame(norm_data_vals)
    data_df.index = idx_lbls
    data_df.columns = col_lbls
    
combined_df = pd.concat([lbl_df, data_df], axis=1, sort=False)
combined_df = visualization_funcs.convertNeurotransmitterLabels(combined_df)

combined_data = combined_df.values[:,2:]
combined_lbls = combined_df['gal4'].values.astype(int)

#%% Visualize soma locations
soma_data = data_df[['SomaX','SomaY','SomaZ']].values

# 3d plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(soma_data[:,0], soma_data[:,1], soma_data[:,2])
plt.show()

#%% Run PCA on the normalized data and plot 
pca = sklearn.decomposition.PCA()
pca.fit(combined_data)
combined_pca_data = pca.transform(combined_data)

if K_PCA==3:
    var_frac = np.sum(pca.explained_variance_ratio_[0:3])
    print("Fraction Explained Variance: ", var_frac)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(combined_pca_data[:,0], combined_pca_data[:,1], 
               combined_pca_data[:,2], c=combined_lbls, 
               cmap=matplotlib.colors.ListedColormap(COLORS))
    
    #ax.set_title('3d PCA Projection of All Neurons')
    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')
    ax.set_zlabel('PC3')
    
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.set_zticklabels([])
    
    plt.show()

elif K_PCA==2:
    var_frac = np.sum(pca.explained_variance_ratio_[0:2])
    print("Fraction Explained Variance: ", var_frac)
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(combined_pca_data[:,0], combined_pca_data[:,1], c=combined_lbls, 
               cmap=matplotlib.colors.ListedColormap(COLORS))
    
    ax.set_title('2d PCA Projection of All Neurons')
    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')

    ax.set_yticklabels([])
    ax.set_xticklabels([])
    
    plt.show()

#%% Run 2d or 3d TSNE on the normalized data

if PCA_FIRST==True: tsne_data = combined_pca_data[:,0:NUM_PCA_COMP]
elif PCA_FIRST==False: tsne_data = combined_data
    
if K_TSNE==3:
    tsne = sklearn.manifold.TSNE(n_components=3, perplexity=PERPLEXITY)
    combined_tsne_data = tsne.fit_transform(tsne_data)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(combined_tsne_data[:,0], combined_tsne_data[:,1], 
               combined_tsne_data[:,2], c=combined_lbls, 
               cmap=matplotlib.colors.ListedColormap(COLORS))
    
    ax.set_title('3d TSNE Projection of All Neurons')
    ax.set_xlabel('C1')
    ax.set_ylabel('C2')
    ax.set_zlabel('C3')
    
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.set_zticklabels([])
    
    plt.show()
    
elif K_TSNE==2:
    tsne = sklearn.manifold.TSNE(n_components=2, perplexity=PERPLEXITY)
    combined_tsne_data = tsne.fit_transform(tsne_data)
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(combined_tsne_data[:,0], combined_tsne_data[:,1], c=combined_lbls, 
               cmap=matplotlib.colors.ListedColormap(COLORS))
    
    ax.set_title('2d TSNE Projection of All Neurons')
    ax.set_xlabel('C1')
    ax.set_ylabel('C2')
    
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    
    plt.show()
    

