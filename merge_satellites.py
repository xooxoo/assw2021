 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  4 23:35:05 2021

@author: stanislav
"""

import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import datetime as dt
import matplotlib.pyplot as plt

import geopandas

from scipy import spatial



smos = pd.read_csv("data/smos.csv").sort_values('date')
rems = pd.read_csv("data/rems.csv").sort_values('date')
nature = pd.read_csv("data/fdata_nabos.csv")

smos.date = pd.to_datetime(smos.date)
rems.date = pd.to_datetime(rems.date)
nature.date = pd.to_datetime(nature.date)

smos_q = smos.query('date.dt.month > 6 and date.dt.month <= 10')
rems_q = rems.query('date.dt.month > 6 and date.dt.month <= 10')
nature_q = nature.query('date.dt.month > 6 and date.dt.month <= 10 and so > 0 and temp > -10')
satellite = pd.merge(rems_q, smos_q, how='inner', 
                     on=["longitude", "latitude","date"])
satellite['year'] = satellite.date.dt.year
nature_q['year'] = nature_q.date.dt.year
satellite = satellite.groupby(["latitude", "longitude", "year"]).mean().reset_index()
nature_q = nature_q.groupby(["lat", "lon", "year"]).mean().reset_index()

nature_q = nature_q.rename(columns={'lat':'latitude', 'lon':'longitude'})

gp_nature = geopandas.GeoDataFrame(nature_q, 
                            geometry=geopandas.points_from_xy(nature_q.longitude, 
                                                              nature_q.latitude))
gp_satellite = geopandas.GeoDataFrame(satellite,
                             geometry=geopandas.points_from_xy(satellite.longitude, 
                                                               satellite.latitude))

gp_nature = gp_nature.set_crs("EPSG:4326")
gp_nature = gp_nature.to_crs("EPSG:3413")

gp_nature['x'] = gp_nature.geometry.x
gp_nature['y'] = gp_nature.geometry.y

gp_satellite = gp_satellite.set_crs("EPSG:4326")
gp_satellite = gp_satellite.to_crs("EPSG:3413")        

gp_satellite['x'] = gp_satellite.geometry.x
gp_satellite['y'] = gp_satellite.geometry.y

gp_nature['xy'] = gp_nature[['x', 'y']].apply(tuple, axis=1)
gp_satellite['xy'] = gp_satellite[['x', 'y']].apply(tuple, axis=1)

lst = list()
for year in range(2010,2020):
    sat_nat_dict = {"sat_node":[],
                    "longitude_sat":[],
                    "latitude_sat":[],
                    "longitude_n":[],
                    "latitude_n":[],
                    "year":[],
                    "temp_sat":[],
                    "so_sat":[],
                    "temp_n":[],
                    "so_n":[],
                    "depth":[],
                    }
    sat_node = 1
    gp_nature_yearly = gp_nature.query(f"year == {year}").reset_index(drop=True)
    gp_satellite_yearly = gp_satellite.query(f"year == {year}").reset_index(drop=True)
    tree = spatial.KDTree(gp_nature_yearly['xy'].to_list())
    a = tree.query_ball_point(gp_satellite_yearly.xy.to_list(), r = 50000)
    gp_satellite_yearly['a'] = a
    for index, row in gp_satellite_yearly.iterrows():
        if row.a:
            sat_node+=1
            for point in row.a:
                print(f"\r{year}: {index+1}/{len(gp_satellite_yearly)}", end='')
                sat_nat_dict["longitude_sat"].append(row.longitude)
                sat_nat_dict["latitude_sat"].append(row.latitude)
                sat_nat_dict["longitude_n"].append(gp_nature_yearly.iloc[point].longitude)
                sat_nat_dict["latitude_n"].append(gp_nature_yearly.iloc[point].latitude)
                sat_nat_dict["year"].append(row.year)
                sat_nat_dict["temp_sat"].append(row.sst_rss)
                sat_nat_dict["so_sat"].append(row.smos_sss_ave)
                sat_nat_dict["temp_n"].append(gp_nature_yearly.iloc[point].temp)
                sat_nat_dict["so_n"].append(gp_nature_yearly.iloc[point].so)
                sat_nat_dict["depth"].append(gp_nature_yearly.iloc[point].depth)
                sat_nat_dict['sat_node'].append(f"{sat_node}_{year}")
    temp_df = pd.DataFrame(sat_nat_dict)
    lst.append(temp_df)
sat_nat_df = pd.concat(lst)
sat_nat_df.to_csv("data/sat_nature.csv", index=False)    

fig, ax = plt.subplots(1, 1,
                       subplot_kw={'projection': ccrs.NorthPolarStereo()})


ax.add_feature(cfeature.NaturalEarthFeature("physical", 
                                            "land", 
                                            "50m",
                                            facecolor='#c1c8c7'))
ax.add_feature(cfeature.COASTLINE, edgecolor='#252b31')
ax.add_feature(cfeature.RIVERS, edgecolor='#f6fafb')
ax.set_extent([-180, 180, 65, 90], ccrs.PlateCarree())

gl = ax.gridlines(crs=ccrs.PlateCarree(), 
                  draw_labels=True,
                  linewidth=1.15, 
                  color='#5e6668', 
                  alpha=0.5, 
                  linestyle='--',
                  )
gl.right_labels = False
gl.xlabel_style = {'fontsize':13}
gl.ylabel_style = {'fontsize':13}

#спутники
ax.scatter(data=gp_satellite_yearly,
           x="longitude",
           y="latitude",
           transform=ccrs.PlateCarree(),
           s=0.5,
           color='#107dac')
#экспедиция
ax.scatter(data=gp_nature_yearly,
           x="longitude",
           y="latitude",
           transform=ccrs.PlateCarree(),
           s=4)
#совместные
ax.scatter(data=test_df,
           x="longitude_sat",
           y="latitude_sat",
           transform=ccrs.PlateCarree(),
           marker="o",
           facecolor='none',
           edgecolor='#107dac',
           s=4)
 