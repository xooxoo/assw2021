#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 06:06:24 2021

@author: stanislav
"""
#%%
import pandas as pd

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import seaborn as sns
import matplotlib.colors as mcolors
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.serif'] = ["Montserrat", "Ubuntu", "Fira"]
#%%

# =============================================================================
# read and select first horizon on each station
# =============================================================================
df = pd.read_csv("data/fdata_nabos.csv", low_memory=False)
df['date'] =  pd.to_datetime(df.date)
df['year'] = df.date.dt.year
df = df.query('date.dt.month > 6 and date.dt.month <= 10 and so > 0 and temp > -10')
df = df.sort_values(['station', 'depth'])
df_first = df.groupby("station").first().reset_index()

#%%

# =============================================================================
# draws maps of the station distribution for each year. 
# color bar - the depth of the first horizon
# =============================================================================

for year in range(2010,2021):
    print(f"\r{year}", end="")
    plt.rcParams['font.family'] = 'serif'
    
    #filter df for each year, create an axis object, 
    # set a projection, draw a grid, coast and rivers
    df_yearly = df_first.query("year == @year")
    fig, ax = plt.subplots(1, 1,
                           subplot_kw={'projection': ccrs.NorthPolarStereo()})
    
    #ax.add_feature(cfeature.OCEAN, facecolor='#f6fafb') 
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
    
# =============================================================================
#     in 2018 we have observations from ferrybox. 
#     This block of code is only needed to show this track with a thin line.
# =============================================================================
    if year == 2018:
        df_nabos = df_yearly.query("station.str.contains('NABOS', na=False)")
        df_yearly = df_yearly.query("~station.str.contains('NABOS', na=False)")
        
        ax.scatter(df_nabos.lon, df_nabos.lat, c=df_nabos.depth, 
           cmap = 'tab10',
           transform=ccrs.PlateCarree(), 
           s = 1, 
           alpha=0.5,
           vmin=0, vmax=10,)
        deep_points = ax.scatter(df_yearly.lon, 
                             df_yearly.lat, 
                             c=df_yearly.depth, 
                             cmap = 'tab10',
                             transform=ccrs.PlateCarree(), 
                             s = 15, 
                             alpha=0.8,
                             vmin=0, vmax=10,
                             edgecolor='#252b31',
                             linewidth=0.05)

    deep_points = ax.scatter(df_yearly.lon, 
                             df_yearly.lat, 
                             c=df_yearly.depth, 
                             cmap = 'tab10',
                             transform=ccrs.PlateCarree(), 
                             s = 15, 
                             alpha=0.8,
                             vmin=0, vmax=10,
                             edgecolor='#252b31',
                             linewidth=0.05)
    # very important thing to place colorbar in a right place
    divider = make_axes_locatable(ax)
    ax_cb = divider.new_horizontal(size="5%", pad=0.1, axes_class=plt.Axes)
    
    fig.add_axes(ax_cb)
    cbar = plt.colorbar(deep_points, cax=ax_cb)
    cbar.ax.invert_yaxis()
    cbar.set_label("Depth, m", fontsize=16, color='#252b31')
    
    ax.annotate(year,
                xy=(1, 1), xycoords='axes fraction',
                xytext=(-20, -40), textcoords='offset pixels',
                horizontalalignment='right',
                verticalalignment='top',
                fontsize=30,
                color = '#252b31')
    plt.savefig(f"graphs_assw/first_hor_maps/first_hor_{year}.png", dpi=300,
                bbox_inches = 'tight',
                pad_inches = 0)
    plt.close()
# =============================================================================
#   First horizon depth distribution histogram
# =============================================================================
    plt.rcParams['font.family'] = 'serif'
    
    fig, ax = plt.subplots()
    ax.hist(df_yearly.depth, 
        bins=range(0,11, 1),
        color='#f15a29', 
        alpha=0.9, linewidth=1.2,
        edgecolor="black",
        align='left')
    
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    plt.xlabel("Depth", fontsize=16)
    plt.ylabel('Count', fontsize=16)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid()

    ax.annotate(year, xy = (1,1),
                xycoords='axes fraction',
                xytext=(-10, -20), 
                textcoords='offset pixels',
                horizontalalignment='right',
                verticalalignment='top',
                fontsize=20)
    plt.savefig(f'graphs_assw/hist_first_depth/hist_{year}.png', dpi=300,
                bbox_inches = 'tight',
                pad_inches = 0)
    plt.close()
#%%

   
plt.rcParams['font.family'] = 'serif'

fig, ax = plt.subplots()
ax.hist(df_first.depth, 
    bins=range(0,11, 1),
    color='#f15a29', 
    alpha=0.9, linewidth=1.2,
    edgecolor="black",
    align='left')

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.xlabel("Depth", fontsize=16)
plt.ylabel('Count', fontsize=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid()

ax.annotate("2010 - 2020", xy = (1,1),
            xycoords='axes fraction',
            xytext=(-10, -20), 
            textcoords='offset pixels',
            horizontalalignment='right',
            verticalalignment='top',
            fontsize=20)