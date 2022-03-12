# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 21:48:47 2022

@author: bkmcc
"""
""" module to load and clean the Crime data from Colorado """




import os
import requests
import pandas as pd
def clean_CO_crime_data(raw_DF, Logger):
    """ function to clean up missing data and create an Age group"""
    raw_DF['age_num'] = pd.to_numeric(raw_DF['age_num'])
    raw_DF['age_num'] = raw_DF['age_num'].fillna(1000)
    raw_DF['age_grp'] = 10 * (raw_DF['age_num']//10)

    Logger.debug(f"CO crime data : clean complete")
    return raw_DF


def load_CO_crime_data(rprtYr, Logger):
    """ function to load the crime data, either from a file or the source site """
    pathName = os.getcwd()
    fileName = "Crimes_in_Colorado_1997_to_2015.csv"

    Logger.info(f"CO crime data - start load")
    Logger.debug(f"filepath = {pathName}")

    files = [file for file in os.listdir(pathName)]

    if fileName not in files:
        url = (
            "https://data.colorado.gov/api/views/6vnq-az4b/rows.csv?accessType=DOWNLOAD"
        )

        r = requests.get(url, stream=True)

        with open("Crimes_in_Colorado_1997_to_2015.csv", "wb") as f:
            for chunk in r.iter_content(chunk_size=16 * 1024):
                f.write(chunk)

    chunk_size = 50000
    crime_DF = pd.DataFrame()
    dateStart = pd.Timestamp(rprtYr, 1, 1)
    dateEnd = pd.Timestamp(rprtYr, 12, 31)

    for chunk in pd.read_csv(
            os.path.join(pathName, fileName),
            chunksize=chunk_size,
            parse_dates=["incident_date"],
            keep_default_na=False,
            na_values=0):
        tempDF = chunk[
            (chunk["incident_date"] >= dateStart) & (
                chunk["incident_date"] <= dateEnd)
        ]
        crime_DF = pd.concat([crime_DF, tempDF], ignore_index=True)
        Logger.debug(f"chunk loaded - {tempDF.shape}")

    Logger.debug(f"CO crime data - data loaded / start clean")
    out_crime_DF = clean_CO_crime_data(crime_DF, Logger)
    Logger.debug(f"CO crime data - data cleaned / return to MAIN")

    return out_crime_DF


# if __name__ == "__main__":
#       load_CO_crime_data()
