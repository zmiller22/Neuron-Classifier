#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 23:27:11 2019

@author: Zachary Miller
"""
import os
import numpy as np
import pandas as pd

#TODO add option to strip file extensions
def getFilenames(dir_path):
    """Returns a list of filesnames within a directory
    
    Args: 
        dir_path (str): path to the directory
        
    Returns:
        list: list containing the filenames as strings
    """
    filename_list = []
    dir_obj = os.fsencode(dir_path)
    for file in os.listdir(dir_obj):
        filename = os.fsdecode(file)
        file_path = os.path.join(dir_path, filename)
        if os.path.isdir(file_path) == False:
            filename_list.append(filename)
            
    return filename_list
    
def getSomaLoc(file_path):
    """Returns the (x,y,z) coordinate for the soma of a swc file
    
    Args:
        file_path (str): path to the swc file

    Returns:
        list: list formatted as [x,y,z]
    
    """
    # Read in the swc file as a dataframe
    nrn_df = pd.read_csv(file_path, header=None, comment="#",
                         delim_whitespace=True)
    
    # Get all rows containing soma points and find the average of the points
    soma_rows = nrn_df.loc[nrn_df.iloc[:,1] == 1].values
    soma_point = np.mean(soma_rows, axis=0)[2:5]
    
    return list(soma_point)