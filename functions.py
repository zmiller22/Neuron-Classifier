#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 19 23:27:11 2019

@author: Zachary Miller
"""
import os

def get_filenames(dir_path, strip_ext):
    """Given a directory, returns a list of all file names within that path. If
    strip_ext is set to True, the filenames will not have their extensions. 
    (strip_ext not implimented yet)"""
    #TODO add option to strip
    filename_list = []
    dir_obj = os.fsencode(dir_path)
    for file in os.listdir(dir_obj):
        filename = os.fsdecode(file)
        file_path = os.path.join(dir_path, filename)
        if os.path.isdir(file_path) == False:
            filename_list.append(filename)
            
    return filename_list

# def fix_neurom_json_df(df):
#     """When reading using pandas load_json(json_file, orient='index') to load 
#     a json file created using NeuroM's morph_stats with my config file, the first
#     column ends up holding the dict values"""