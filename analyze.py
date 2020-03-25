#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 14:26:29 2020

@author: Zachary Miller
"""
#%% Import packages
import numpy as np
import pandas as pd
import sklearn.decomposition
import sklearn.manifold
import sklearn.preprocessing

import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#%% Read in the data
output_file_dir = '/home/zack/Desktop/Lab_Work/Code/neuron_classifier/data'

gad_df = pd.read_csv(output_file_dir+'/gad.csv', index_col=0)
vglut_df = pd.read_csv(output_file_dir+'/vglut.csv', index_col=0)
unlabeled_df = pd.read_csv(output_file_dir+'/unlabeled.csv', index_col=0)
combined_df = pd.concat([unlabeled_df, gad_df, vglut_df], axis=0)

# Standardize the data
normalizer = sklearn.preprocessing.StandardScaler()
norm_combined_vals = normalizer.fit_transform(combined_df.values)
norm_combined_df = pd.DataFrame(norm_combined_vals)
norm_combined_df.index = combined_df.index.values
norm_combined_df.columns = combined_df.columns

norm_combined_df = pd.DataFrame(norm_combined_vals)
norm_combined_df.index = combined_df.index.values
norm_combined_df.columns = combined_df.columns

# Create lables and colomap for easy plotting
gad_lbls = np.zeros(gad_df.values.shape[0])
vglut_lbls = np.ones(vglut_df.values.shape[0])
unlabeled_lbls = 2*np.ones(unlabeled_df.values.shape[0])

lbls = np.concatenate((unlabeled_lbls, gad_lbls, vglut_lbls))
colors = ['red', 'green', 'grey']
#alphas = np.concatenate((gad_alpha, vglut_alpha, unlabeled_alpha))

#%% Run PCA on the Data
pca = sklearn.decomposition.PCA()
pca.fit(norm_combined_df.values)
combined_pca_data = pca.transform(combined_df.values)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(combined_pca_data[:,0], combined_pca_data[:,1], combined_pca_data[:,2],
           c=lbls, cmap=matplotlib.colors.ListedColormap(colors))
plt.show()

#%% Run PCA on the Data
tsne = sklearn.manifold.TSNE(n_components=3, perplexity=15)
combined_tsne_data = tsne.fit_transform(combined_pca_data[:,0:50])


fig = plt.figure(1)
ax = fig.add_subplot(111, projection='3d')
ax.scatter(combined_tsne_data[:,0], combined_tsne_data[:,1], combined_tsne_data[:,2],
           c=lbls, cmap=matplotlib.colors.ListedColormap(colors))
plt.show()

