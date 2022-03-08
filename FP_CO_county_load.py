# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 19:21:28 2022

@author: bkmcc
"""


import os
import requests
import pandas as pd


def load_CO_county_data():
    """function to load county lat / long data """

    co_pathName = os.getcwd()
    co_fileName = "Colorado_County_Boundaries.csv"

    files = [file for file in os.listdir(os.getcwd())]

    if co_fileName not in files:
        print(f"Colorado County file not in folder.  Please remedy!!")
        raise AttributeError
    co_DF = pd.read_csv(os.path.join(co_pathName, co_fileName))
    co_DF = co_DF[["COUNTY", "CENT_LAT", "CENT_LONG"]]

    return co_DF
