# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 21:06:38 2022

@author: bkmcc, ebf
"""
import FP_precip_load as rain
import FP_crime_load as crime
import FP_CO_county_load as cnty
import CO_log_setup as cls_log
import FP_eda as eda
import pandas as pd
import argparse
from geopy import distance
import os


def parser_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int, choices=range(1999, 2016),  # change to Range(1999,2016)
                        help="four digit year from 1999 to 2015")
    parser.add_argument("--verbose", default=False)
    parser.add_argument("split", type=str, choices=['7d', '30d', '90d'], default='7d',
                        help="pick split time to capture crime in relation to weather")


# add_argument - verbose for different logging print / capture levels
    return parser.parse_args()

#     ****Version 1: Geopandas attempt****   (will add write up in final)
# def gpd_County(rain_DF, county_DF):
#     """ function to assign county label to nearest Lat/Long precipitation data """
#     logging.debug("DEBUG create geodataframes")
#     gdf_rain = gpd.GeoDataFrame(
#         rain_DF, geometry=gpd.points_from_xy(rain_DF['lat'], rain_DF['lng']))
#     gdf_cnty = gpd.GeoDataFrame(county_DF, geometry=gpd.points_from_xy(
#         county_DF['CENT_LAT'], county_DF['CENT_LONG']))

#     #colNameList = ['st_County', 'cnty_lat', 'cnty_long', 'cnty_geometry']
#     #gdf_cnty.columns = colNameList

#     return gdf_rain, gdf_cnty


def the_big_deal(df_rain, df_crime, split):
    if split == '7d':
        day_fence = 7
    elif split == '30d':
        day_fence = 30
    else:
        day_fence = 90

    df_rain['alt_prcp'] = df_rain['prcp'] + df_rain['snowfall']
    df_g_rain = df_rain.groupby(['county', 'obs_date', ])
    return df_g_rain

def min_dist_count(row, df_cnty):
    """ function to find the nearest CENT coord county to a weather station"""

    minCnty = ''
    row_xy = row

    df_cnty['xy'] = df_cnty[['CENT_LAT', 'CENT_LONG']].apply(tuple, axis=1)

    df_cnty['st_cnty_dist'] = df_cnty['xy'].apply(
        lambda xy: distance.distance(row_xy, xy).miles)

    minCnty = df_cnty['COUNTY'].loc[df_cnty['st_cnty_dist'].idxmin()]

    return(minCnty)


def main():
    """ central program for comparing weather and crime analysis """

    args = parser_config()
    logger = cls_log.Logger_FP_BE(args.verbose)

    logger.info('main function started')

    tempYear = args.year
    logger.debug(f'selected year is {args.year}')

    # load precipitation data for selected year
    df_Precip = rain.load_CO_precip_data(tempYear, logger)
    logger.debug(f" DF for precip called := {df_Precip.shape}")

    # load crime data for selected year
    df_Crime = crime.load_CO_crime_data(tempYear, logger)
    logger.debug(f" DF for crime called := {df_Crime.shape}")

    # load county geo data to match to precipitation data
    df_County = cnty.load_CO_county_data(logger)
    logger.debug(f" DF for county called := {df_County.shape}")
    logger.info(f"datasets loaded")

    # prep lat/long data of Precip & County to utilize geopy 'distance'  for merge prep
    df_unique_Precip = df_Precip.loc[:, [
        'st_num', 'lat', 'lng', 'xy']].drop_duplicates()
    df_unique_Precip['county'] = df_unique_Precip['xy'].apply(
        lambda row: min_dist_count(row, df_County))
    df_Precip = pd.merge(df_Precip, df_unique_Precip, how='left', on=[
                         'st_num', 'lat', 'lng', 'xy'])
    # df_Precip['county'] = df_Precip['county'].str.lower()
    logger.debug(f" DF for precip has county added := {df_Precip.shape}")
    logger.info(f"county classification added to precipitation data")

    # major join of crime data with weather data by split args value
    output_DF = the_big_deal(df_Precip, df_Crime, args.split)

    pathName = os.getcwd()
    csv_precip = 'CO_precip_data.csv'
    csv_crime = 'CO_crime_data.csv'

    df_Precip.to_csv(os.path.join(pathName, csv_precip))
    df_Crime.to_csv(os.path.join(pathName, csv_crime))
    logger.info(f"files refreshed")

    #EDA graphs, which use 2010 as default year
    # eda.crime_eda()
    # eda.rain_eda()

    #final graphs
    logger.info("graphing")


    return


if __name__ == "__main__":
    main()
