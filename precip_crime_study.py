# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 21:06:38 2022

@author: bkmcc, ebf
"""
import FP_precip_load as rain
import FP_crime_load as crime
import FP_CO_county_load as cnty
import pandas as pd
import geopandas as gpd
import logging
import argparse


def log_config():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # i.e. everything

    fh = logging.FileHandler("precip_crime_logs.log", 'w')
    fh.setLevel(logging.DEBUG)  # everything prints to log file
    logger.addHandler(fh)

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)  # only INFO and greater print to console
    logger.addHandler(sh)


def parser_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int, choices=[1999, 2000, 2001, 2002, 2003, 2004, 2005,
                        2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015],
                        help="four digit year from 1999 to 2015")
    return parser.parse_args()


def gpd_County(rain_DF, county_DF):
    """ function to assign county label to nearest Lat/Long precipitation data """
    logging.debug("DEBUG create geodataframes")
    gdf_rain = gpd.GeoDataFrame(
        rain_DF, geometry=gpd.points_from_xy(rain_DF['lat'], rain_DF['lng']))
    gdf_cnty = gpd.GeoDataFrame(county_DF, geometry=gpd.points_from_xy(
        county_DF['CENT_LAT'], county_DF['CENT_LONG']))

    return gdf_rain, gdf_cnty


def main():
    log_config()
    args = parser_config()
    
    tempYear = args.year
    # load precipitation data for selected year
    df_Precip = rain.load_CO_precip_data(tempYear)
    # load crime data for selected year
    df_Crime = crime.load_CO_crime_data(tempYear)
    # load county geo data to match to precipitation data
    df_County = cnty.load_CO_county_data()

    # create GeoDataFrames of Precip & County data for merge prep
    df_Precip_A = gpd_County(df_Precip, df_County)

    return group_St_Number


# if __name__ == "__main__":
#     main()
