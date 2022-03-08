# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 21:06:38 2022

@author: bkmcc
"""
import FP_precip_load as rain
import FP_crime_load as crime
import FP_CO_county_load as cnty
import pandas as pd
import geopandas as gpd


def gpd_County(rain_DF, county_DF):
    """ function to assign county label to nearest Lat/Long precipitation data """
    gdf_rain = gpd.GeoDataFrame(
        rain_DF, geometry=gpd.points_from_xy(rain_DF['lat'], rain_DF['lng']))
    gdf_cnty = gpd.GeoDataFrame(county_DF, geometry=gpd.points_from_xy(
        county_DF['CENT_LAT'], county_DF['CENT_LONG']))

    return gdf_rain, gdf_cnty


def main():

    # replace tempYear with args input later
    tempYear = 2012
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
