# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 21:48:47 2022

@author: bkmcc
"""
""" module to load and clean the Crime data from Colorado """




import os
import requests
import pandas as pd
def clean_CO_precip_data(raw_DF):
    """function to clean raw precipitation data"""
    raw_DF["prcp"] = raw_DF["prcp"].fillna(0)
    raw_DF["snowfall"] = raw_DF["snowfall"].fillna(0)
    raw_DF["snowfallswe"] = raw_DF["snowfallswe"].fillna(0)
    raw_DF["snowdepth"] = raw_DF["snowdepth"].fillna(0)
    raw_DF["snowdepthswe"] = raw_DF["snowdepthswe"].fillna(0)
    raw_DF["xy"] = raw_DF[['lat', 'lng']].apply(tuple, axis=1)
    return raw_DF


def load_CO_precip_data(rprtYr):
    """function to load the CO precipitation data for a selected year"""
    pathName = os.getcwd()
    fileName = "Rain_hail_snow_in_CO_1999_to_2015.csv"

    files = [file for file in os.listdir(os.getcwd())]

    if fileName not in files:
        url = (
            "https://data.colorado.gov/api/views/mqid-8hv2/rows.csv?accessType=DOWNLOAD"
        )

        r = requests.get(url, stream=True)

        with open("Rain_hail_snow_in_CO_1999_to_2015.csv", "wb") as f:
            for chunk in r.iter_content(chunk_size=16 * 1024):
                f.write(chunk)
    chunk_size = 50000
    precip_DF = pd.DataFrame()
    dateStart = pd.Timestamp(rprtYr, 1, 1)
    dateEnd = pd.Timestamp(rprtYr, 12, 31)

    for chunk in pd.read_csv(
            os.path.join(pathName, fileName),
            chunksize=chunk_size,
            parse_dates=["obs_date"],
            keep_default_na=False,
            na_values=0,):
        tempDF = chunk[
            (chunk["obs_date"] >= dateStart) & (chunk["obs_date"] <= dateEnd)
        ]
        precip_DF = pd.concat([precip_DF, tempDF], ignore_index=True)
    out_precip_DF = clean_CO_precip_data(precip_DF)

    return out_precip_DF


# if __name__ == "__main__":
#     load_CO_precip_data()
