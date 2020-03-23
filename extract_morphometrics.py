#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 14:29:07 2020

@author: zack


"""

import numpy as np
import os
import pandas as pd
import functions as my_func

#%% Set paths

# Path to morph_stats config file
config_file_path = '/home/zack/Desktop/Lab_Work/Code/neuron_classifier/neurom-config.yaml'

# Paths to directories containing the data
gad_dir = '/home/zack/Desktop/Lab_Work/Data/neuron_morphologies/Zebrafish/labeled_kunst_data_aligned/data/Gad1b'
vglut_dir = '/home/zack/Desktop/Lab_Work/Data/neuron_morphologies/Zebrafish/labeled_kunst_data_aligned/data/VGlut2a'
unlabeled_dir = '/home/zack/Desktop/Lab_Work/Data/neuron_morphologies/Zebrafish/unlabeled_kunst_data_aligned/data/Original'

# path to the directory you want you csv file to be outputted to
output_file_dir = '/home/zack/Desktop/Lab_Work/Code/neuron_classifier/data'


#%% Extract morphometrics and store in json files

# NOTE: I was origionally going to put these directly into a csv file, but some of the neurons throw errors that stop the data from
# bseing stored. However, this bug is not a problem with the JSON format for some reason
gad_com = 'morph_stats ' + gad_dir + ' -I \'SomaError\' -C ' + config_file_path + ' -o ' + output_file_dir + '/gad.json' 
vglut_com = 'morph_stats ' + vglut_dir + ' -I \'SomaError\' -C ' + config_file_path + ' -o ' + output_file_dir + '/vglut.json' 
unlabeled_com = 'morph_stats ' + unlabeled_dir + ' -I \'SomaError\' -C ' + config_file_path + ' -o ' + output_file_dir + '/unlabeled.json' 

#TODO get location information
os.system(gad_com)
os.system(vglut_com)
os.system(unlabeled_com)

#%% Handle the json file issues with pandas and save to CSV

# Read morphometry data from json files into a dataframe
gad_df = pd.read_json(output_file_dir + '/gad.json', orient="index")
vglut_df = pd.read_json(output_file_dir + '/vglut.json', orient="index")
unlabeled_df = pd.read_json(output_file_dir + '/unlabeled.json', orient="index")

# Unpack the column containing a dict and drop any rows containing NaN
gad_df = gad_df.iloc[:,0].apply(pd.Series).dropna()
vglut_df = vglut_df.iloc[:,0].apply(pd.Series).dropna()
unlabeled_df = unlabeled_df.iloc[:,0].apply(pd.Series).dropna()

# Check for any remaining non-numeric values
df_list = [gad_df, vglut_df, unlabeled_df]
non_numeric = False
for df in df_list:
    if np.sum(~df.applymap(np.isreal).values) != 0: 
        non_numeric=True

if non_numeric == True: 
    print("Non-numeric values present")

elif non_numeric == False:
    gad_nn_list = gad_df.index.values
    vglut_nn_list = vglut_df.index.values
    unlabeled_nn_list = unlabeled_df.index.values
    
    good_gad_paths_list = [gad_dir+"/"+fn+".swc" for fn in gad_nn_list]
    good_vglut_paths_list = [vglut_dir+"/"+fn+".swc" for fn in vglut_nn_list]
    good_unlabeled_paths_list = [unlabeled_dir+"/"+fn+".swc" for fn in unlabeled_nn_list]
    
    gad_somas_df = pd.DataFrame([my_func.getSomaLoc(path) for path in good_gad_paths_list])
    vglut_somas_df = pd.DataFrame([my_func.getSomaLoc(path) for path in good_vglut_paths_list])
    unlabeled_somas_df = pd.DataFrame([my_func.getSomaLoc(path) for path in good_unlabeled_paths_list])
    
    soma_col_names = ["somaX", "somaY", "somaZ"]
    gad_somas_df.columns = soma_col_names
    vglut_somas_df.columns = soma_col_names
    unlabeled_somas_df.columns = soma_col_names
    
    # Combine the morphometric data with the spatial data
    gad_df = pd.concat([gad_df.reset_index(drop=True), gad_somas_df],
                           axis=1)
    gad_df.index = gad_nn_list
    
    vglut_df = pd.concat([vglut_df.reset_index(drop=True), vglut_somas_df],
                           axis=1)
    vglut_df.index = vglut_nn_list
    
    unlabeled_df = pd.concat([unlabeled_df.reset_index(drop=True), unlabeled_somas_df],
                           axis=1)
    unlabeled_df.index = unlabeled_nn_list
    
    
    csv_name_list = ['/gad.csv', '/vglut.csv', '/unlabeled.csv']
    print("No non-numeric values present, saving data to CSV...")
    for idx, df in enumerate(df_list):
        path = output_file_dir+csv_name_list[idx]
        df.to_csv(path)
            
    


