#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 20:04:05 2020

@author: zack
"""
import pandas as pd

def getPVPNLabels(df):
    """Gets the PVPN class labels from cell_type column and makes
    them numerical from 1, all non-numeric labels get set to 0"""
    lbl_dict = {
        'PVPN' : 1, 
        'PVPN Class 1' : 2, 
        'PVPN Class 2' : 3,
        'PVPN Class 3' : 4,
        'PVPN Class 4' : 5,
        'PVPN Class 5' : 6,
        'PVPN Class 6a' : 7,
        'PVPN Class 6b' : 8,
        'PVPN Class 8' : 9 }
    
    df['cell_type'] = df['cell_type'].map(lbl_dict)
    df['cell_type'] = pd.to_numeric(df['cell_type']).fillna(0)
    
    return df

def getCellTypeLabels(df):
    """Gets the named cell types as labels"""
    lbl_dict = {
        'Eurydendroid Cells' : 7, 
        'Retinal Ganglion Cells' : 8, 
        'Mitral Cells' : 9 }
    
    df['cell_type'] = df['cell_type'].map(lbl_dict)
    df['cell_type'] = pd.to_numeric(df['cell_type']).fillna(0)
    
    return df
    