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
reg_gad_dir = '/home/zack/Desktop/Lab_Work/Data/neuron_morphologies/Zebrafish/labeled_kunst_data_aligned/data/Gad1b'
reg_vglut_dir = '/home/zack/Desktop/Lab_Work/Data/neuron_morphologies/Zebrafish/labeled_kunst_data_aligned/data/VGlut2a'
reg_unlabeled_dir = '/home/zack/Desktop/Lab_Work/Data/neuron_morphologies/Zebrafish/unlabeled_kunst_data_aligned/data/Original'

# path to the directory you want you csv file to be outputted to
output_file_dir = '/home/zack/Desktop/Lab_Work/Code/neuron_classifier/data'


#%% Extract morphometrics and store in json files

# NOTE: I was origionally going to put these directly into a csv file, but some of the neurons throw errors that stop the data from
# bseing stored. However, this bug is not a problem with the JSON format for some reason
reg_gad_com = 'morph_stats ' + reg_gad_dir + ' -I \'SomaError\' -C ' + config_file_path + ' -o ' + output_file_dir + '/reg_gad.json' 
reg_vglut_com = 'morph_stats ' + reg_vglut_dir + ' -I \'SomaError\' -C ' + config_file_path + ' -o ' + output_file_dir + '/reg_vglut.json' 
reg_unlabeled_com = 'morph_stats ' + reg_unlabeled_dir + ' -I \'SomaError\' -C ' + config_file_path + ' -o ' + output_file_dir + '/reg_unlabeled.json' 

#TODO get location information
os.system(reg_gad_com)
os.system(reg_vglut_com)
os.system(reg_unlabeled_com)

#%% Handle the json file issues with pandas and save to CSV

# Read morphometry data from json files into a dataframe
reg_gad_mm_df = pd.read_json(output_file_dir + '/reg_gad.json', orient="index")
reg_vglut_mm_df = pd.read_json(output_file_dir + '/reg_vglut.json', orient="index")
reg_unlabeled_mm_df = pd.read_json(output_file_dir + '/reg_unlabeled.json', orient="index")

# Unpack the column containing a dict and drop any rows containing NaN
reg_gad_mm_df = reg_gadmm_df.iloc[:,0].apply(pd.Series).dropna()
reg_vglut_mm_df = reg_vglut_mm_df.iloc[:,0].apply(pd.Series).dropna()
reg_unlabeled_mm_df = reg_unlabeled_mm_df.iloc[:,0].apply(pd.Series).dropna()

<<<<<<< Updated upstream
df_list = [reg_gad_mm_df, reg_vglut_mm_df, reg_mm_unlabeled_df]
csv_name_list = ['/reg_gad.csv', '/reg_vglut.csv', '/reg_unlabeled.csv']

# Check for any remaining non-numeric values, save to csv if there are none
=======
# Check for any remaining non-numeric values
>>>>>>> Stashed changes
non_numeric = False
for df in df_list:
    if np.sum(~df.applymap(np.isreal).values) != 0: 
        non_numeric=True

if non_numeric == True: 
    print("Non-numeric values present")

elif non_numeric == False:
    gad_nn_list = reg_gad_df.index.values
    vglut_nn_list = reg_vglut_df.index.values
    unlabeled_nn_list = reg_unlabeled_df.index.values
    
    good_gad_paths_list = [reg_gad_dir+"/"+fn+".swc" for fn in gad_nn_list]
    good_vglut_paths_list = [reg_vglut_dir+"/"+fn+".swc" for fn in vglut_nn_list]
    good_unlabeled_paths_list = [reg_unlabeled_dir+"/"+fn+".swc" for fn in unlabeled_nn_list]
    
    gad_somas_df = pd.DataFrame([my_func.getSomaLoc(path) for path in good_gad_paths_list])
    vglut_somas_df = pd.DataFrame([my_func.getSomaLoc(path) for path in good_vglut_paths_list])
    unlabeled_somas_df = pd.DataFrame([my_func.getSomaLoc(path) for path in good_unlabeled_paths_list])
    
    soma_col_names = ["somaX", "somaY", "somaZ"]
    gad_somas_df.columns = soma_col_names
    vglut_somas_df.columns = soma_col_names
    unlabeled_somas_df.columns = soma_col_names
    
    # Combine the morphometric data with the spatial data
    reg_gad_df = pd.concat([reg_gad_df.reset_index(drop=True), gad_somas_df],
                           axis=1)
    reg_gad_df.index = gad_nn_list
    
    reg_vglut_df = pd.concat([reg_vglut_df.reset_index(drop=True), vglut_somas_df],
                           axis=1)
    reg_vglut_df.index = vglut_nn_list
    
    reg_unlabeled_df = pd.concat([reg_unlabeled_df.reset_index(drop=True), unlabeled_somas_df],
                           axis=1)
    reg_unlabeled_df.index = unlabeled_nn_list
    
    
    df_list = [reg_gad_df, reg_vglut_df, reg_unlabeled_df]
    csv_name_list = ['/reg_gad.csv', '/reg_vglut.csv', '/reg_unlabeled.csv']
    print("No non-numeric values present, saving data to CSV...")
    for idx, df in enumerate(df_list):
        path = output_file_dir+csv_name_list[idx]
        df.to_csv(path)
            
    


