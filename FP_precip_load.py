# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 21:48:47 2022

@author: bkmcc
"""
""" module to load and clean the Crime data from Colorado """

#import csv
import os
import requests
import pandas as pd

def load_CO_crime_data():
   pathName = os.getcwd()
   fileName = 'Rain_hail_snow_in_CO_1999_to_2015.csv'
   
   files = [file for file in os.listdir(os.getcwd())]
   
   if fileName not in files:
       url = 'https://data.colorado.gov/api/views/mqid-8hv2/rows.csv?accessType=DOWNLOAD'
       
       r = requests.get(url, stream = True)
       
       with open("Rain_hail_snow_in_CO_1999_to_2015.csv", "wb") as f:
           for chunk in r.iter_content(chunk_size = 16*1024):
               f.write(chunk)

   test_DF = pd.read_csv(os.path.join(pathName, fileName), nrows=1000)


if __name__ == "__main__":
      load_CO_crime_data()
