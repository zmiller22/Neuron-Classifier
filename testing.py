#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 20:42:37 2020

@author: zack
"""

import neurom as nm
from neurom import check
import numpy as np
import os
import functions as my_func

# Set up directory paths
reg_gad_dir = "/home/zack/Desktop/Lab_Work/Data/neuron_morphologies/Zebrafish/unlabeled_kunst_data_unaligned/data/"
unreg_gad_dir = "/home/zack/Desktop/Lab_Work/Data/neuron_morphologies/Zebrafish/labeled_kunst_data_unaligned/data/Gad1b/"

# get a list of the neuron filenames in each directory
unreg_gad_nrn_filename_list = my_func.getFilenames(unreg_gad_dir)
reg_gad_nrn_filename_list = my_func.getFilenames(reg_gad_dir)

# %%
# Iterate over all neurons

unreg_nrn_list = []
for filename in unreg_gad_nrn_filename_list:
    #com = "morph_check " + unreg_gad_dir + filename
    #os.system(com)
    
    nrn_path = unreg_gad_dir + filename

    try:
        nrn = nm.load_neuron(nrn_path)
        unreg_nrn_list.append(nrn)
        
        
    except nm.exceptions.SomaError:
        print("Neuron", filename, "did not contain a soma")
        
print()
        
reg_nrn_list = []
for filename in reg_gad_nrn_filename_list:
    #com = "morph_check " + unreg_gad_dir + filename
    #os.system(com)
    
    nrn_path = reg_gad_dir + filename

    try:
        nrn = nm.load_neuron(nrn_path)
        reg_nrn_list.append(nrn)
        
        
    except nm.exceptions.SomaError:
        print("Neuron", filename, "did not contain a soma")

        
test = map(lambda nrn : nm.get("number_of_forking_points", nrn), reg_nrn_list)
test_2 = map(lambda nrn : nm.get("number_of_forking_points", nrn), unreg_nrn_list)