# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 21:48:47 2022

@author: bkmcc
"""

import os
import requests
import pandas as pd
import numpy as np


def clean_CO_precip_data(raw_DF, Logger):
    """function to clean raw precipitation data"""

    raw_DF[raw_DF['prcp'] == ""] = np.NaN
    raw_DF[raw_DF['snowfall'] == ""] = np.NaN

    raw_DF["prcp"] = raw_DF["prcp"].fillna(0)
    raw_DF.loc[(raw_DF.prcp < 0), 'prcp'] = 0

    raw_DF["snowfall"] = raw_DF["snowfall"].fillna(0)
    raw_DF["snowfall"] = raw_DF["snowfall"].astype("float")
    raw_DF.loc[(raw_DF.snowfall < 0), 'snowfall'] = 0

    raw_DF["snowfallswe"] = raw_DF["snowfallswe"].fillna(0)
    raw_DF["snowdepth"] = raw_DF["snowdepth"].fillna(0)
    raw_DF["snowdepthswe"] = raw_DF["snowdepthswe"].fillna(0)

    raw_DF['lat'] = raw_DF['lat'].fillna(0)
    raw_DF['lng'] = raw_DF['lng'].fillna(0)

    raw_DF["xy"] = raw_DF[['lat', 'lng']].apply(tuple, axis=1)

    Logger.debug(f"weather data BEFORE removing duplicates = {raw_DF.shape}")

    raw_DF = raw_DF[(raw_DF.prcp > 0) | (raw_DF.snowfall > 0)]
    raw_DF = raw_DF.reset_index()
    Logger.debug(f"weather data AFTER removing duplicates = {raw_DF.shape}")

    return raw_DF


def load_CO_precip_data(rprtYr, Logger):
    """function to load the CO precipitation data for a selected year"""
    pathName = os.getcwd()
    fileName = "Rain_hail_snow_in_CO_1999_to_2015.csv"
    Logger.info(f"CO weather data - start load")
    Logger.debug(f"filepath = {pathName}")

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
        Logger.debug(f"chunk loaded - {tempDF.shape}")

    Logger.debug(f"CO weather data - data loaded / start clean")
    out_precip_DF = clean_CO_precip_data(precip_DF, Logger)
    Logger.debug(f"CO weather data - data cleaned / return to MAIN")

    return out_precip_DF


# if __name__ == "__main__":
#     load_CO_precip_data()
