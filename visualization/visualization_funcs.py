#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 20:04:05 2020

@author: zack
"""
import pandas as pd

# def convertPVPNLabels(df):
    #BROKEN nned to add back in more colors to color list
    # """Converts the PVPN labels to integers"""
    # lbl_dict = {
    #     'PVPN' : 1, 
    #     'PVPN Class 1' : 2, 
    #     'PVPN Class 2' : 3,
    #     'PVPN Class 3' : 4,
    #     'PVPN Class 4' : 5,
    #     'PVPN Class 5' : 6,
    #     'PVPN Class 6a' : 7,
    #     'PVPN Class 6b' : 8,
    #     'PVPN Class 8' : 9 }
    
    # df['cell_type'] = df['cell_type'].map(lbl_dict)
    # df['cell_type'] = pd.to_numeric(df['cell_type']).fillna(0)
    # df
    
    # return df

def convertCellTypeLabels(df):
    """Converts the cell type labels to integers"""
    lbl_dict = {
        'Eurydendroid Cells' : 1, 
        'Retinal Ganglion Cells' : 2, 
        'Mitral Cells' : 3 }
    
    df['cell_type'] = df['cell_type'].map(lbl_dict)
    df['cell_type'] = pd.to_numeric(df['cell_type']).fillna(0)
    df['cell_tyep'] = df['cell_type'].astype('int32')
    return df

def convertNeurotransmitterLabels(df):
    """Converts neurotransmitter lables to numbers"""
    lbl_dict = {
        'Gad1b (mpn155)' : 1, 
        'vGlut2a' : 2, 
        'vGut2a' : 2}
    
    df['gal4'] = df['gal4'].map(lbl_dict)
    df['gal4'] = pd.to_numeric(df['gal4']).fillna(0)
    df['gal4'] = df['gal4'].astype('int32')
    
    return df
    