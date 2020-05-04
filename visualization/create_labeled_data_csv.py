#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 29 17:27:29 2020

@author: zack
"""

import numpy as np
import pandas as pd

import visualization_funcs

data_file_path = '/home/zack/Desktop/Lab_Work/Data/neuron_morphologies/Zebrafish/aligned_040120/zbrain_neuron_spatial_morphometrics_Zbrain_MECE_masks.csv'
lbl_file_path = '/home/zack/Desktop/Lab_Work/Data/neuron_morphologies/Zebrafish/aligned_040120/metadata.csv'

data_df = pd.read_csv(data_file_path, index_col=0)
lbl_df = pd.read_csv(lbl_file_path, index_col=0)

    
# Combine labels and data
combined_df = pd.concat([lbl_df, data_df], axis=1, sort=False)

