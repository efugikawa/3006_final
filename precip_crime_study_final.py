# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 21:06:38 2022

@author: bkmcc
"""
import FP_precip_load as rain
import FP_crime_load as crime
import FP_CO_county_load as cnty
import CO_log_setup as cls_log
import pandas as pd
import numpy as np
import argparse
from geopy import distance
import os
import time
import matplotlib as plt


def parser_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int, choices=range(1999, 2016),  # change to Range(1999,2016)
                        help="four digit year from 1999 to 2015")
    parser.add_argument("--verbose", "-v", default=False)
    parser.add_argument("--split", type=str, choices=['7d', '30d', '90d'], default='7d',
                        help="pick split time to capture crime in relation to weather")

    return parser.parse_args()


def plotting_the_end(df_rain, df_crime, df_g_rain, Logger):

    pathName = os.getcwd()

    # plot of county sum of rain by date's - graph1
    Logger.info(f"first graph started - rain by county by quarter")
    df_rain_graph1 = df_rain.groupby(['county', 'obs_date'])[
        'prcp'].sum().reset_index()
    df_rain_graph1['quarters'] = df_rain_graph1['obs_date'].dt.quarter

    df_pivot1 = pd.pivot_table(
        df_rain_graph1, values="prcp", index="quarters", columns="county", aggfunc=np.sum)
    graph1 = df_pivot1.plot(kind='bar')
    graph1.legend(bbox_to_anchor=(1, 1), loc='upper left', title='Counties',
                  borderpad=3, labelspacing=1)
    graph1.set_xlabel("Quarters")
    graph1.set_ylabel("Precipitation")
    out_graph1 = graph1.get_figure()
    out_graph1.savefig("graph1_rain_by_quarter.png")

    # plot of county sum of rain for year - graph2
    Logger.info(f"second graph started - rain by county for the year")
    df_rain_graph2 = df_rain.groupby(['county'])['prcp'].sum().reset_index()

    df_pivot2 = pd.pivot_table(
        df_rain_graph2, values='prcp', index='county', columns='county', aggfunc=np.sum)
    graph2 = df_pivot2.plot(kind='bar')
    graph2.legend(bbox_to_anchor=(1, 1), loc='upper left', title='Counties',
                  borderpad=3, labelspacing=1)
    graph2.set_xlabel("Counties")
    graph2.set_ylabel("Annual Precipitation")
    out_graph2 = graph2.get_figure()
    out_graph2.savefig("graph2_annual_rain_by_county.png")

    return


def the_big_deal(df_rain, df_crime, split, Logger):
    if split == '7d':
        day_fence = 7
    elif split == '30d':
        day_fence = 30
    else:
        day_fence = 90
    Logger.debug(f"time split fence length := {day_fence}")

    # summarize weather data by average prcp by county / date
    df_rain['alt_prcp'] = df_rain['prcp'] + df_rain['snowfall']
    df_rain = df_rain.loc[:, ['st_num', 'county', 'obs_date', 'alt_prcp']]
    df_g_rain = df_rain.groupby(['st_num', 'county', 'obs_date'])[
        'alt_prcp'].sum().reset_index()
    df_g_rain = df_g_rain.groupby(['county', 'obs_date'])[
        'alt_prcp'].mean().reset_index()

    timedelta_str = str(day_fence) + ' day'
    df_g_rain['end_date_fence1'] = df_g_rain['obs_date'] + \
        pd.Timedelta(timedelta_str)
    df_g_rain['end_date_fence2'] = df_g_rain['end_date_fence1'] + \
        pd.Timedelta(timedelta_str)

    Logger.debug(
        f"Grouped rain DF data : Shape = {df_g_rain.shape} / Columns = {list(df_g_rain)}")

    # summarize crime data by number of offenses by county / date
    df_crime = df_crime.loc[:, [
        'primary_county', 'incident_date', 'offense_name']]
    df_g_crime = df_crime.groupby(['primary_county', 'incident_date'])[
        'offense_name'].count().reset_index()
    df_g_crime = df_g_crime[df_g_crime['primary_county'] != '']

    Logger.debug(
        f"Grouped crime DF data : Shape = {df_g_crime.shape} / Columns = {list(df_g_crime)}")

    # add in sum of crimes inside and outside of time fence
    df_g_rain['crime_in'] = df_g_rain.apply(lambda x: df_g_crime.loc[(df_g_crime.incident_date >= x.obs_date) & (
        df_g_crime.incident_date < x.end_date_fence1) & (df_g_crime.primary_county == x.county), 'offense_name'].sum(), axis=1)
    df_g_rain['crime_out'] = df_g_rain.apply(lambda x: df_g_crime.loc[(df_g_crime.incident_date >= x.end_date_fence1) & (
        df_g_crime.incident_date < x.end_date_fence2) & (df_g_crime.primary_county == x.county), 'offense_name'].sum(), axis=1)

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
    startTime = time.time()
    args = parser_config()

    Logger = cls_log.Logger_FP_BE()
    #Logger = cls_log.Logger_FP_BE(args.verbose)
    Logger.info(f"MAIN PROGRAM START : {startTime}")
    Logger.info(f'main function started')

    time_split = args.split
    tempYear = args.year

    Logger.debug(f"selected time split is {args.split}")
    Logger.debug(f'selected year is {args.year}')

    # load precipitation data for selected year
    df_Precip = rain.load_CO_precip_data(tempYear, Logger)
    Logger.debug(f" DF for precip called := {df_Precip.shape}")

    # load crime data for selected year
    df_Crime = crime.load_CO_crime_data(tempYear, Logger)
    Logger.debug(f" DF for crime called := {df_Crime.shape}")

    # load county geo data to match to precipitation data
    df_County = cnty.load_CO_county_data(Logger)
    Logger.debug(f" DF for county called := {df_County.shape}")
    Logger.info(f"datasets loaded")

    # prep lat/long data of Precip & County to utilize geopy 'distance'  for merge prep
    df_unique_Precip = df_Precip.loc[:, [
        'st_num', 'lat', 'lng', 'xy']].drop_duplicates()
    df_unique_Precip['county'] = df_unique_Precip['xy'].apply(
        lambda row: min_dist_count(row, df_County))
    df_Precip = pd.merge(df_Precip, df_unique_Precip, how='left', on=[
                         'st_num', 'lat', 'lng', 'xy'])
    # df_Precip['county'] = df_Precip['county'].str.lower()
    Logger.debug(f" DF for precip has county added := {df_Precip.shape}")
    Logger.info(f"county classification added to precipitation data")

    # major join of crime data with weather data by split args value
    output_DF = the_big_deal(df_Precip, df_Crime, time_split, Logger)

    # call the plotting function
    plotting_the_end(df_Precip, df_Crime, output_DF, Logger)

    pathName = os.getcwd()
    csv_precip = 'CO_precip_data.csv'
    csv_crime = 'CO_crime_data.csv'
    csv_rain_sum = 'CO_rain_crime.csv'

    df_Precip.to_csv(os.path.join(pathName, csv_precip))
    df_Crime.to_csv(os.path.join(pathName, csv_crime))
    output_DF.to_csv(os.path.join(pathName, csv_rain_sum))
    Logger.info(f"files refreshed")

    endTime = time.time()
    Logger.info(f'MAIN PROGRAM END: {endTime}')
    Logger.info(f"TOTAL PROGRAM RUNTIME: {endTime-startTime}")
    return


if __name__ == "__main__":
    main()
