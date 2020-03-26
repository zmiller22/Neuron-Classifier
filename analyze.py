#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 14:26:29 2020

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

#%% Load and preprocess data
output_file_dir = '/home/zack/Desktop/Lab_Work/Code/neuron_classifier/data'

gad_df = pd.read_csv(output_file_dir+'/gad.csv', index_col=0)
vglut_df = pd.read_csv(output_file_dir+'/vglut.csv', index_col=0)
unlabeled_df = pd.read_csv(output_file_dir+'/unlabeled.csv', index_col=0)
combined_df = pd.concat([unlabeled_df, gad_df, vglut_df], axis=0)
gad_glut_df = pd.concat([gad_df, vglut_df], axis=0)

idx_lbls = combined_df.index.values
col_lbls = combined_df.columns

# Standardize the data
normalizer = sklearn.preprocessing.StandardScaler()
norm_combined_vals = normalizer.fit_transform(combined_df.values)
norm_combined_df = pd.DataFrame(norm_combined_vals)
norm_combined_df.index = combined_df.index.values
norm_combined_df.columns = combined_df.columns

# Put standardized, combined data into a dataframe
norm_combined_df = pd.DataFrame(norm_combined_vals)
norm_combined_df.index = idx_lbls
norm_combined_df.columns = col_lbls

# Create lables and colomap for easy plotting
gad_lbls = np.zeros(gad_df.values.shape[0])
vglut_lbls = np.ones(vglut_df.values.shape[0])
unlabeled_lbls = 2*np.ones(unlabeled_df.values.shape[0])
combined_lbls = np.concatenate((unlabeled_lbls, gad_lbls, vglut_lbls))
gad_glut_lbls = np.concatenate((gad_lbls, vglut_lbls))

colors = ['red', 'green', 'grey']

# Perform feature selection using ANOVA F-value 
feature_selector = SelectKBest(f_classif, k=50).fit(norm_combined_df.values[unlabeled_lbls.shape[0]:],
                                                   combined_lbls[unlabeled_lbls.shape[0]:])
selected_features = feature_selector.get_support()
norm_filtered_df = gad_glut_df.loc[:,selected_features]

#%% Visualize soma locations
soma_data = combined_df[['somaX','somaY','somaZ']].values

# 3d plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(soma_data[:,0], soma_data[:,1], soma_data[:,2],
           c=combined_lbls, cmap=matplotlib.colors.ListedColormap(colors))
plt.show()

#%% Run PCA on the Data
pca = sklearn.decomposition.PCA()
pca.fit(norm_combined_df.values)
combined_pca_data = pca.transform(norm_combined_df.values)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(combined_pca_data[:,0], combined_pca_data[:,1], combined_pca_data[:,2],
           c=combined_lbls, cmap=matplotlib.colors.ListedColormap(colors))
plt.show()

#%% Run TSNE on the Data
tsne = sklearn.manifold.TSNE(n_components=3, perplexity=20)
combined_tsne_data = tsne.fit_transform(combined_pca_data[:,0:50])


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(combined_tsne_data[:,0], combined_tsne_data[:,1], combined_tsne_data[:,2],
           c=combined_lbls, cmap=matplotlib.colors.ListedColormap(colors))
plt.show()

#%% Run PCA on the filtered data
pca = sklearn.decomposition.PCA()
pca.fit(norm_filtered_df.values)
filtered_pca_data = pca.transform(norm_filtered_df.values)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(filtered_pca_data[:,0], filtered_pca_data[:,1], filtered_pca_data[:,2],
           c=gad_glut_lbls, cmap=matplotlib.colors.ListedColormap(colors))
plt.show()

#%% Run TSNE on the filtered data
tsne = sklearn.manifold.TSNE(n_components=3, perplexity=20)
filtered_tsne_data = tsne.fit_transform(norm_filtered_df.values[:,0:50])


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(filtered_tsne_data[:,0], filtered_tsne_data[:,1], filtered_tsne_data[:,2],
           c=gad_glut_lbls, cmap=matplotlib.colors.ListedColormap(colors))
plt.show()

