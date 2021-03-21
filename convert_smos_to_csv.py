#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 05:26:39 2021

@author: stanislav
"""

import pandas as pd
import glob
import xarray as xr
import re
from os.path import basename
from datetime import datetime


path = "data/SMOS_monthly/netcdf_monthly/"
all_files = glob.glob(path + "*.nc")
lst = []
for i, file in enumerate(all_files):
    print(f"\r{i+1}/{len(all_files)}", end='')
    ds = xr.load_dataset(file)
    date = datetime.strptime(re.findall(r"\d{4}-\d", basename(file))[0],
                             "%Y-%m")
    ds = ds.to_dataframe()\
        .reset_index()\
        .dropna(axis=0)\
        .drop(["Latitude", "Longitude"], axis=1)
    ds['date'] = date 
    lst.append(ds)


df = pd.concat(lst)
df.to_csv('data/smos.csv', index=False)