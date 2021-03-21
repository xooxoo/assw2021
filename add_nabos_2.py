#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 03:11:29 2021

@author: stanislav
"""


import pandas as pd
import glob
import xarray as xr

from seabird import fCNV


df = pd.read_csv('data/field_data.csv')

path = 'data/nabos_stations/cnv_110119/'
all_files = glob.glob(path + "*.cnv")
lst = []

for i, filename  in enumerate(all_files):
    print(f"\r{i+1}/{len(all_files)}", end='')
    seabird_stations = fCNV(filename)
    seabird_df = seabird_stations.as_DataFrame()
    if (seabird_stations['pumps'] == 1).all():
        seabird_df['station'] = seabird_stations.attributes['filename'][:5]
        seabird_df['date'] = seabird_stations.attributes['datetime']
        seabird_df = seabird_df.rename(columns={"DEPTH":"depth",
                                                "PSAL":"so",
                                                "TEMP":"temp",
                                                "LATITUDE":"lat",
                                                "LONGITUDE":"lon"})
        seabird_df['year'] = seabird_df['date'].dt.year
        seabird_df = seabird_df.query("depth <= 10")
        seabird_df = seabird_df[df.columns.to_list()]
        lst.append(seabird_df)      
        
nabos_df = pd.concat(lst, axis=0, ignore_index=True)

ds_temp = xr.load_dataset("data/nabos_stations/AT_ferrybox_temperature.nc")\
    .to_dataframe().reset_index()
ds_so = xr.load_dataset("data/nabos_stations/AT_ferrybox_salinity.nc")\
    .to_dataframe().reset_index()

df_ferrybox = ds_so.merge(ds_temp[['time','temperature']], on='time')
df_ferrybox = df_ferrybox.rename(columns={"time":"date", "latitude":'lat',
                                 "longitude":"lon", "salinity":"so",
                                 "temperature":"temp"})
df_ferrybox["station"] = "NABOS-ferrybox_"
df_ferrybox["ind"] = df_ferrybox.index
df_ferrybox["station"] = df_ferrybox.station + df_ferrybox.ind.astype(str)
df_ferrybox["year"] = df_ferrybox.date.dt.year
df_ferrybox["depth"] = 6
df_ferrybox = df_ferrybox[df.columns.to_list()]
df = pd.concat([df, nabos_df, df_ferrybox], axis=0, ignore_index=True)

df.to_csv("data/fdata_nabos.csv", index=False)


    
