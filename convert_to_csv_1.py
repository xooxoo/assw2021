#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 18:57:05 2021

@author: stanislav
"""
# =============================================================================
# this script reads and converts field observations 
# from 2010 to 2020 into .csv format
# =============================================================================

import pandas as pd
from datetime import datetime

filepath = "data/export-01.o4x"

with open(filepath,  encoding="utf8", errors='ignore') as file:
    header = [next(file).strip() for x in range(10)]
    content = file.read().splitlines()

station_number = 0
st_dict = {"station":[],
           "date":[],
           "lon":[],
           "lat":[],
           "depth":[],
           "temp":[],
           "so":[]}


for line in content:
    if line[0] == "#":
        line_list = line.split()
        date = datetime.strptime(line.split()[4], '%m/%d/%Y')
        lon = line_list[5]
        lat = line_list[6]
        station_number += 1
    elif len(line.split()) > 3:
        line_data = line.split()
        st_dict["station"].append(station_number)
        st_dict["date"].append(date)
        st_dict["lon"].append(lon)
        st_dict["lat"].append(lat)
        st_dict["depth"].append(line_data[0])
        st_dict["temp"].append(line_data[2])
        st_dict["so"].append(line_data[4])
        


df = pd.DataFrame(st_dict)

df.to_csv("data/field_data.csv", index=False)