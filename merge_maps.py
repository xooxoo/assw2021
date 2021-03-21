#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 17:20:35 2021

@author: stanislav
"""
#%%
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import cmocean
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable

import datetime as dt
import matplotlib.ticker as ticker

import math
import matplotlib.colors as mcolors
from matplotlib import rcParams
import numpy as np
rcParams['font.family'] = 'sans-serif'
rcParams['font.serif'] = ["Montserrat", "Ubuntu", "Fira"]


df = pd.read_csv("data/sat_nature.csv")
df_sat = pd.read_csv("data/satellite_data.csv")
df_nat = pd.read_csv("data/fdata_nabos.csv")
df_nat.date = pd.to_datetime(df_nat.date)
df_nat['year'] = df_nat.date.dt.year
df_nat = df_nat.query('6 < date.dt.month <= 10 and so > 0 and temp > -10')

df_avg = df.groupby(["longitude_sat", "latitude_sat", "year"]).mean()\
    .reset_index()
    
df_avg['temp_dif'] = df_avg.temp_sat - df_avg.temp_n
df_avg['so_dif'] = df_avg.so_sat - df_avg.so_n

#Температура натурные
plt.rcParams['font.family'] = 'serif'

for year in range(2010, 2020):
    bck_c = "#252b31"
    light_c ='#f6fafb'
    land_c = '#c1c8c7'
    df_avg_yearly = df_avg.query("year == @year")
    
    plt.rcParams['font.family'] = 'serif'
    
    fig, ax = plt.subplots(1, 1,
                           subplot_kw={'projection': ccrs.NorthPolarStereo()})
        
    ax.add_feature(cfeature.NaturalEarthFeature("physical", 
                                                "land", 
                                                "50m",
                                                facecolor='#e8e8e8'))
    ax.add_feature(cfeature.COASTLINE, edgecolor=light_c)
    ax.add_feature(cfeature.RIVERS, edgecolor=bck_c)
    ax.set_extent([-180, 180, 65, 90], ccrs.PlateCarree())
    
    gl = ax.gridlines(crs=ccrs.PlateCarree(), 
                      draw_labels=True,
                      linewidth=1.15, 
                      color='#6e6e6e', 
                      alpha=0.5, 
                      linestyle='--')
    gl.right_labels = False
    gl.xlabel_style, gl.ylabel_style = {'fontsize':13, 'color':bck_c}, {'fontsize':13, 'color':'#6e6e6e'}
    
    nat_points = ax.scatter(df_avg_yearly.longitude_sat, 
                            df_avg_yearly.latitude_sat, 
                            c=df_avg_yearly.temp_n,
                            cmap = cmocean.cm.thermal,
                            transform=ccrs.PlateCarree(), 
                            s = 20, 
                            # alpha=0.8,
                            # edgecolor='#252b31',
                            linewidth=0.05,
                            marker='s',
                            vmin = min(df_avg.temp_n),
                            vmax = max(df_avg.temp_n))
    # very important thing to place colorbar in a right place
    divider = make_axes_locatable(ax)
    ax_cb = divider.new_horizontal(size="3%", pad=0.1, axes_class=plt.Axes)
    
    fig.add_axes(ax_cb)
    cbar = plt.colorbar(nat_points, cax=ax_cb, extend="both",
                        drawedges=True, format="%d",
                        boundaries=np.arange(math.floor(min(df_avg.temp_n)), 
                                             math.ceil(max(df_avg.temp_n)), 
                                             1))
    cbar.ax.tick_params(labelsize=13)
    cbar.set_label("In-situ temperature, $^\circ$C", fontsize=16)
    
    
    ax.annotate(year,
                xy=(1, 1), xycoords='axes fraction',
                xytext=(-20, -40), textcoords='offset pixels',
                horizontalalignment='right',
                verticalalignment='top',
                fontsize=30,
                color = '#252b31',
                )
    ax.set(facecolor=bck_c)
    plt.savefig(f"graphs_assw/temp_maps/in-situ_yearly_{year}.png", dpi=300,
                bbox_inches='tight', pad_inches=0.1)
    plt.close()


#Температура спутник

plt.rcParams['font.family'] = 'serif'

for year in range(2010, 2020):
    bck_c = "#252b31"
    light_c ='#f6fafb'
    land_c = '#c1c8c7'
    df_avg_yearly = df_avg.query("year == @year")
    
    plt.rcParams['font.family'] = 'serif'
    
    fig, ax = plt.subplots(1, 1,
                           subplot_kw={'projection': ccrs.NorthPolarStereo()})
        
    ax.add_feature(cfeature.NaturalEarthFeature("physical", 
                                                "land", 
                                                "50m",
                                                facecolor='#e8e8e8'))
    ax.add_feature(cfeature.COASTLINE, edgecolor=light_c)
    ax.add_feature(cfeature.RIVERS, edgecolor=bck_c)
    ax.set_extent([-180, 180, 65, 90], ccrs.PlateCarree())
    
    gl = ax.gridlines(crs=ccrs.PlateCarree(), 
                      draw_labels=True,
                      linewidth=1.15, 
                      color='#6e6e6e', 
                      alpha=0.5, 
                      linestyle='--')
    gl.right_labels = False
    gl.xlabel_style, gl.ylabel_style = {'fontsize':13, 'color':bck_c}, {'fontsize':13, 'color':'#6e6e6e'}
    
    nat_points = ax.scatter(df_avg_yearly.longitude_sat, 
                            df_avg_yearly.latitude_sat, 
                            c=df_avg_yearly.temp_sat,
                            cmap = cmocean.cm.thermal,
                            transform=ccrs.PlateCarree(), 
                            s = 20, 
                            # alpha=0.8,
                            # edgecolor='#252b31',
                            linewidth=0.05,
                            marker='s',
                            vmin = min(df_avg.temp_sat),
                            vmax = max(df_avg.temp_sat))
    # very important thing to place colorbar in a right place
    divider = make_axes_locatable(ax)
    ax_cb = divider.new_horizontal(size="3%", pad=0.1, axes_class=plt.Axes)
    
    fig.add_axes(ax_cb)
    cbar = plt.colorbar(nat_points, cax=ax_cb, extend="both",
                        drawedges=True, format="%d",
                        boundaries=np.arange(math.floor(min(df_avg.temp_sat)), 
                                             math.ceil(max(df_avg.temp_sat)), 
                                             1))
    cbar.ax.tick_params(labelsize=13)
    cbar.set_label("Sea surface temperature, $^\circ$C", fontsize=16)
    
    
    ax.annotate(year,
                xy=(1, 1), xycoords='axes fraction',
                xytext=(-20, -40), textcoords='offset pixels',
                horizontalalignment='right',
                verticalalignment='top',
                fontsize=30,
                color = '#252b31',
                )
    ax.set(facecolor=bck_c)
    plt.savefig(f"graphs_assw/temp_maps/sst_yearly_{year}.png", dpi=300,
                bbox_inches='tight', pad_inches=0.1)
    plt.close()



#Разница температур
for year in range(2010, 2020):
    plt.rcParams['font.family'] = 'serif'
    
    bck_c = "#252b31"
    light_c ='#f6fafb'
    land_c = '#c1c8c7'
    df_avg_yearly = df_avg.query("year == @year")
    
    plt.rcParams['font.family'] = 'serif'
    
    fig, ax = plt.subplots(1, 1,
                           subplot_kw={'projection': ccrs.NorthPolarStereo()})
        
    ax.add_feature(cfeature.NaturalEarthFeature("physical", 
                                                "land", 
                                                "50m",
                                                facecolor='#e8e8e8'))
    ax.add_feature(cfeature.COASTLINE, edgecolor=light_c)
    ax.add_feature(cfeature.RIVERS, edgecolor=bck_c)
    ax.set_extent([-180, 180, 65, 90], ccrs.PlateCarree())
    
    gl = ax.gridlines(crs=ccrs.PlateCarree(), 
                      draw_labels=True,
                      linewidth=1.15, 
                      color='#6e6e6e', 
                      alpha=0.5, 
                      linestyle='--')
    gl.right_labels = False
    gl.xlabel_style, gl.ylabel_style = {'fontsize':13, 'color':bck_c}, {'fontsize':13, 'color':'#6e6e6e'}
    
    offset = mcolors.TwoSlopeNorm(vmin=-3, 
                                  vcenter=0, 
                                  vmax=3)
    
    satellite_points = ax.scatter(df_avg_yearly.longitude_sat, 
                             df_avg_yearly.latitude_sat, 
                             c=df_avg_yearly.temp_dif,                       
                             transform=ccrs.PlateCarree(), 
                             s = 5,
                             marker='s',
    #                         alpha=0.8,
    #                         edgecolor='#252b31',
    #                         linewidth=0.05,
                             cmap=cmocean.cm.balance,
                             norm=offset)
    # very important thing to place colorbar in a right place
    divider = make_axes_locatable(ax)
    ax_cb = divider.new_horizontal(size="3%", pad=0.1, axes_class=plt.Axes)
    
    fig.add_axes(ax_cb)
    cbar = plt.colorbar(satellite_points, cax=ax_cb, extend="both",
                        drawedges=True,
                        boundaries=np.arange(-3, 
                                             3.5, 
                                             0.5))
    cbar.ax.tick_params(labelsize=13)
    cbar.set_label('Difference, $^\circ$C', fontsize=16)
    
    
    ax.annotate(year,
                xy=(1, 1), xycoords='axes fraction',
                xytext=(-20, -40), textcoords='offset pixels',
                horizontalalignment='right',
                verticalalignment='top',
                fontsize=30,
                color = '#252b31',
                )
    ax.set(facecolor=bck_c)
    plt.savefig(f"graphs_assw/temp_maps/temp_dif_{year}.png", dpi=300,
                bbox_inches='tight', pad_inches=0.1)
    plt.close()



#Соленость натурные

plt.rcParams['font.family'] = 'serif'

for year in range(2010, 2020):
    bck_c = "#252b31"
    light_c ='#f6fafb'
    land_c = '#c1c8c7'
    df_avg_yearly = df_avg.query("year == @year")
    
    plt.rcParams['font.family'] = 'serif'
    
    fig, ax = plt.subplots(1, 1,
                           subplot_kw={'projection': ccrs.NorthPolarStereo()})
        
    ax.add_feature(cfeature.NaturalEarthFeature("physical", 
                                                "land", 
                                                "50m",
                                                facecolor='#e8e8e8'))
    ax.add_feature(cfeature.COASTLINE, edgecolor=light_c)
    ax.add_feature(cfeature.RIVERS, edgecolor=bck_c)
    ax.set_extent([-180, 180, 65, 90], ccrs.PlateCarree())
    
    gl = ax.gridlines(crs=ccrs.PlateCarree(), 
                      draw_labels=True,
                      linewidth=1.15, 
                      color='#6e6e6e', 
                      alpha=0.5, 
                      linestyle='--')
    gl.right_labels = False
    gl.xlabel_style, gl.ylabel_style = {'fontsize':13, 'color':bck_c}, {'fontsize':13, 'color':'#6e6e6e'}
    
    nat_points = ax.scatter(df_avg_yearly.longitude_sat, 
                            df_avg_yearly.latitude_sat, 
                            c=df_avg_yearly.so_n,
                            cmap = cmocean.cm.haline,
                            transform=ccrs.PlateCarree(), 
                            s = 20, 
                            # alpha=0.8,
                            # edgecolor='#252b31',
                            linewidth=0.05,
                            marker='s',
                            vmin = min(df_avg.so_n),
                            vmax = max(df_avg.so_n))
    # very important thing to place colorbar in a right place
    divider = make_axes_locatable(ax)
    ax_cb = divider.new_horizontal(size="3%", pad=0.1, axes_class=plt.Axes)
    
    fig.add_axes(ax_cb)
    cbar = plt.colorbar(nat_points, cax=ax_cb, extend="both",
                        drawedges=True, format="%d",
                        boundaries=np.arange(math.floor(min(df_avg.so_n)), 
                                             math.ceil(max(df_avg.so_n)), 
                                             1))
    cbar.ax.tick_params(labelsize=13)
    cbar.set_label("In-situ salinity, ‰", fontsize=16)
    
    
    ax.annotate(year,
                xy=(1, 1), xycoords='axes fraction',
                xytext=(-20, -40), textcoords='offset pixels',
                horizontalalignment='right',
                verticalalignment='top',
                fontsize=30,
                color = '#252b31',
                )
    ax.set(facecolor=bck_c)
    plt.savefig(f"graphs_assw/so_maps/in-situ_yearly_{year}.png", dpi=300,
                bbox_inches='tight', pad_inches=0.1)
    plt.close()



#Соленость спутник

plt.rcParams['font.family'] = 'serif'

for year in range(2010, 2020):
    bck_c = "#252b31"
    light_c ='#f6fafb'
    land_c = '#c1c8c7'
    df_avg_yearly = df_avg.query("year == @year")
    
    plt.rcParams['font.family'] = 'serif'
    
    fig, ax = plt.subplots(1, 1,
                           subplot_kw={'projection': ccrs.NorthPolarStereo()})
        
    ax.add_feature(cfeature.NaturalEarthFeature("physical", 
                                                "land", 
                                                "50m",
                                                facecolor='#e8e8e8'))
    ax.add_feature(cfeature.COASTLINE, edgecolor=light_c)
    ax.add_feature(cfeature.RIVERS, edgecolor=bck_c)
    ax.set_extent([-180, 180, 65, 90], ccrs.PlateCarree())
    
    gl = ax.gridlines(crs=ccrs.PlateCarree(), 
                      draw_labels=True,
                      linewidth=1.15, 
                      color='#6e6e6e', 
                      alpha=0.5, 
                      linestyle='--')
    gl.right_labels = False
    gl.xlabel_style, gl.ylabel_style = {'fontsize':13, 'color':bck_c}, {'fontsize':13, 'color':'#6e6e6e'}
    
    nat_points = ax.scatter(df_avg_yearly.longitude_sat, 
                            df_avg_yearly.latitude_sat, 
                            c=df_avg_yearly.so_sat,
                            cmap = cmocean.cm.haline,
                            transform=ccrs.PlateCarree(), 
                            s = 20, 
                            # alpha=0.8,
                            # edgecolor='#252b31',
                            linewidth=0.05,
                            marker='s',
                            vmin = min(df_avg.so_sat),
                            vmax = max(df_avg.so_sat))
    # very important thing to place colorbar in a right place
    divider = make_axes_locatable(ax)
    ax_cb = divider.new_horizontal(size="3%", pad=0.1, axes_class=plt.Axes)
    
    fig.add_axes(ax_cb)
    cbar = plt.colorbar(nat_points, cax=ax_cb, extend="both",
                        drawedges=True, format="%d",
                        boundaries=np.arange(math.floor(min(df_avg.so_sat)), 
                                             math.ceil(max(df_avg.so_sat)), 
                                             1))
    cbar.ax.tick_params(labelsize=13)
    cbar.set_label("Sea surface salinity, ‰", fontsize=16)
    
    
    ax.annotate(year,
                xy=(1, 1), xycoords='axes fraction',
                xytext=(-20, -40), textcoords='offset pixels',
                horizontalalignment='right',
                verticalalignment='top',
                fontsize=30,
                color = '#252b31',
                )
    ax.set(facecolor=bck_c)
    plt.savefig(f"graphs_assw/so_maps/sss_yearly_{year}.png", dpi=300,
                bbox_inches='tight', pad_inches=0.1)
    plt.close()

#Разница соленость
for year in range(2010, 2020):
    plt.rcParams['font.family'] = 'serif'
    
    bck_c = "#252b31"
    light_c ='#f6fafb'
    land_c = '#c1c8c7'
    df_avg_yearly = df_avg.query("year == @year")
    
    plt.rcParams['font.family'] = 'serif'
    
    fig, ax = plt.subplots(1, 1,
                           subplot_kw={'projection': ccrs.NorthPolarStereo()})
        
    ax.add_feature(cfeature.NaturalEarthFeature("physical", 
                                                "land", 
                                                "50m",
                                                facecolor='#e8e8e8'))
    ax.add_feature(cfeature.COASTLINE, edgecolor=light_c)
    ax.add_feature(cfeature.RIVERS, edgecolor=bck_c)
    ax.set_extent([-180, 180, 65, 90], ccrs.PlateCarree())
    
    gl = ax.gridlines(crs=ccrs.PlateCarree(), 
                      draw_labels=True,
                      linewidth=1.15, 
                      color='#6e6e6e', 
                      alpha=0.5, 
                      linestyle='--')
    gl.right_labels = False
    gl.xlabel_style, gl.ylabel_style = {'fontsize':13, 'color':bck_c}, {'fontsize':13, 'color':'#6e6e6e'}
    
    offset = mcolors.TwoSlopeNorm(vmin=-3, 
                                  vcenter=0, 
                                  vmax=3)
    
    satellite_points = ax.scatter(df_avg_yearly.longitude_sat, 
                             df_avg_yearly.latitude_sat, 
                             c=df_avg_yearly.so_dif,                       
                             transform=ccrs.PlateCarree(), 
                             s = 5,
                             marker='s',
    #                         alpha=0.8,
    #                         edgecolor='#252b31',
    #                         linewidth=0.05,
                             cmap=cmocean.cm.balance,
                             norm=offset)
    # very important thing to place colorbar in a right place
    divider = make_axes_locatable(ax)
    ax_cb = divider.new_horizontal(size="3%", pad=0.1, axes_class=plt.Axes)
    
    fig.add_axes(ax_cb)
    cbar = plt.colorbar(satellite_points, cax=ax_cb, extend="both",
                        drawedges=True,
                        boundaries=np.arange(-3, 
                                             3.5, 
                                             0.5))
    cbar.ax.tick_params(labelsize=13)
    cbar.set_label('Difference, ‰', fontsize=16)
    
    
    ax.annotate(year,
                xy=(1, 1), xycoords='axes fraction',
                xytext=(-20, -40), textcoords='offset pixels',
                horizontalalignment='right',
                verticalalignment='top',
                fontsize=30,
                color = '#252b31',
                )
    ax.set(facecolor=bck_c)
    plt.savefig(f"graphs_assw/so_maps/so_dif_{year}.png", dpi=300,
                bbox_inches='tight', pad_inches=0.1)
    plt.close()


# Сомещенные карты
for year in range(2010, 2020):
    plt.rcParams['font.family'] = 'serif'
    df_yearly = df.query("year == @year")
    df_sat_yearly = df_sat.query("year == @year")
    df_nat_yearly = df_nat.query('year == @year and 6 < date.dt.month <= 10 and so > 0 and temp > -10')
    
    
    s_nat_yearly = df_nat_yearly[['lon', 'lat']].apply(tuple, axis=1)
    s_sat_yearly = df_sat_yearly[['longitude', 'latitude']].apply(tuple, axis=1)
    s_yearly_n = df_yearly[['longitude_n', 'latitude_n']].apply(tuple, axis=1)
    s_yearly_s = df_yearly[['longitude_sat', 'latitude_sat']].apply(tuple, axis=1)
    
    
    df_sat_out = df_sat_yearly[~s_sat_yearly.isin(s_yearly_s)]
    df_nat_out = df_nat_yearly[~s_nat_yearly.isin(s_yearly_n)]
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
    gl.xlabel_style = {'fontsize':13}
    gl.ylabel_style = {'fontsize':13}
    
    # спутники не вошедшие
    ax.scatter(data=df_sat_out,
                x="longitude",
                y="latitude",
                transform=ccrs.PlateCarree(),
                s=0.3,
                color='#65737e')
    # натурные не вошедшие
    ax.scatter(data=df_nat_out,
                x="lon",
                y="lat",
                transform=ccrs.PlateCarree(),
                s=7,
                color='#c75643',
    #            facecolor='none'
                )
    # спутники вошедшие
    ax.scatter(data=df_yearly,
                x="longitude_sat",
                y="latitude_sat",
                transform=ccrs.PlateCarree(),
                color='#11698e',
                s=1)
    # натурные вошедшие
    ax.scatter(data=df_yearly,
                x="longitude_n",
                y="latitude_n",
                transform=ccrs.PlateCarree(),
                color='#11698e',
                s=3)
    ax.annotate(year,
            xy=(1, 1), xycoords='axes fraction',
            xytext=(-20, -40), textcoords='offset pixels',
            horizontalalignment='right',
            verticalalignment='top',
            fontsize=30,
            color = '#252b31',
            )
    plt.savefig(f"graphs_assw/interaction_maps/interaction_{year}.png")



#Гистограмма
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ['Montserrat'],                    # use latex default serif font
    "font.sans-serif": ["Montserrat"],  # use a specific sans-serif font
})

c_df = (df.groupby('year').agg({'so_n': 'count'})/100000).reset_index()

fig, ax = plt.subplots()

ax.bar(c_df.year, c_df.so_n,
       color='#f15a29', alpha=0.9, linewidth=1.2,
       edgecolor="black",
       align='center',
       width=0.9)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.set_xticks(range(2010,2021, 1))
plt.xlabel("Years", fontsize=16)
plt.ylabel(r'Count $\cdot 10^5$', fontsize=16)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid()
plt.savefig("graphs_assw/count_by_year.png", dpi=300,
                bbox_inches = 'tight',
                pad_inches = 0.1)


# Скаттерплот температура/температура
for year in range(2010, 2020):
    plt.rcParams['font.family'] = 'serif'
    df_avg_yearly = df_avg.query('year == @year')
    fig, ax = plt.subplots(1 ,1)
    
    offset = mcolors.TwoSlopeNorm(vmin=-3, 
                              vcenter=0, 
                              vmax=3)
    
    sc = ax.scatter(data = df_avg_yearly, 
                    x='temp_n',
                    y='temp_sat',
                    c='temp_dif',
                    cmap=cmocean.cm.balance,
                    s=20,
                    edgecolor='#e0e0e0',
                    linewidth=0.05,
                    norm=offset)
    ax.plot([math.floor(min(df_avg[["temp_n", "temp_sat"]].min())), 
             math.ceil(max(df_avg[["temp_n", "temp_sat"]].max()))],
            [math.floor(min(df_avg[["temp_n", "temp_sat"]].min())), 
             math.ceil(max(df_avg[["temp_n", "temp_sat"]].max()))],
            c='#e0e0e0',
            linewidth=4)
    
    
    plt.grid(color='#e0e0e0',
             linewidth=0.5)
    divider = make_axes_locatable(ax)
    ax_cb = divider.new_horizontal(size="2.5%", pad=0.1, axes_class=plt.Axes)
    
    fig.add_axes(ax_cb)
    
    cbar = plt.colorbar(sc, cax=ax_cb, extend="both",
                        drawedges=True, format="%d",
                        boundaries=np.arange(-3, 3.5, 0.5)) 
                                        
    
    cbar.outline.set_edgecolor('#e0e0e0')
    cbar.dividers.set_edgecolor('#e0e0e0')
    cbar.ax.tick_params(labelsize=13, 
                        labelcolor='#e0e0e0',
                        color='#e0e0e0')
    cbar.set_label('Difference, $^\circ$C',
                   color='#e0e0e0', 
                   fontsize=16)
    
    
    ax.set(facecolor='#424242')
    fig.set(facecolor='#424242')
    
    ax.set_xlim([math.floor(min(df_avg[["temp_n", "temp_sat"]].min())),
              math.ceil(max(df_avg[["temp_n", "temp_sat"]].max()))])
    ax.set_ylim([math.floor(min(df_avg[["temp_n", "temp_sat"]].min())),
              math.ceil(max(df_avg[["temp_n", "temp_sat"]].max()))])
    
    
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_edgecolor('#e0e0e0')
    ax.spines['left'].set_edgecolor('#e0e0e0')
    
    ax.set_xlabel("In-situ temperature, $^\circ$C", fontsize=16, c='#e0e0e0')
    ax.set_ylabel("Sea surface temperature, $^\circ$C", fontsize=16, c='#e0e0e0')
    
    ax.annotate(year,
                xy=(0, 1), xycoords='axes fraction',
                xytext=(30, -120), textcoords='offset pixels',
                horizontalalignment='left',
                verticalalignment='top',
                fontsize=25,
                color = '#e0e0e0',
                bbox=dict(fc='#424242', pad=0.2, ec='#424242'))
    
    sc.axes.tick_params(color='#e0e0e0', 
                        labelcolor='#e0e0e0', 
                        labelsize=12)
    plt.savefig(f"graphs_assw/sat-vs-insitu/temp/sst_v_Tinsitu_{year}.png", dpi=300,
                bbox_inches = 'tight',
                pad_inches = 0.1)
    plt.close()

# Скаттерплот соленость/соленость
for year in range(2010, 2020):
    plt.rcParams['font.family'] = 'serif'
    df_avg_yearly = df_avg.query('year == @year')
    fig, ax = plt.subplots(1 ,1)
    
    offset = mcolors.TwoSlopeNorm(vmin=-3, 
                              vcenter=0, 
                              vmax=3)
    
    sc = ax.scatter(data = df_avg_yearly, 
                    x='so_n',
                    y='so_sat',
                    c='so_dif',
                    cmap=cmocean.cm.balance,
                    s=20,
                    edgecolor='#e0e0e0',
                    linewidth=0.05,
                    norm=offset)
    
    ax.plot([math.floor(min(df_avg[["so_n", "so_sat"]].min())), 
             math.ceil(max(df_avg[["so_n", "so_sat"]].max()))],
            [math.floor(min(df_avg[["so_n", "so_sat"]].min())), 
             math.ceil(max(df_avg[["so_n", "so_sat"]].max()))],
             c='#e0e0e0',
             linewidth=4)
    
    
    plt.grid(color='#e0e0e0',
             linewidth=0.5)
    divider = make_axes_locatable(ax)
    ax_cb = divider.new_horizontal(size="2.5%", pad=0.1, axes_class=plt.Axes)
    
    fig.add_axes(ax_cb)
    
    cbar = plt.colorbar(sc, cax=ax_cb, extend="both",
                        drawedges=True, format="%d",
                        boundaries=np.arange(-3, 3.5, 0.5)) 
                                        
    
    cbar.outline.set_edgecolor('#e0e0e0')
    cbar.dividers.set_edgecolor('#e0e0e0')
    cbar.ax.tick_params(labelsize=13, 
                        labelcolor='#e0e0e0',
                        color='#e0e0e0')
    cbar.set_label('Difference, ‰',
                   color='#e0e0e0', 
                   fontsize=16)
    
    
    ax.set(facecolor='#424242')
    fig.set(facecolor='#424242')
    
    ax.set_xlim([math.floor(min(df_avg[["so_n", "so_sat"]].min())),
              math.ceil(max(df_avg[["so_n", "so_sat"]].max()))])
    ax.set_ylim([math.floor(min(df_avg[["so_n", "so_sat"]].min())),
              math.ceil(max(df_avg[["so_n", "so_sat"]].max()))])
        
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_edgecolor('#e0e0e0')
    ax.spines['left'].set_edgecolor('#e0e0e0')
    
    ax.set_xlabel("In-situ salinity, ‰", fontsize=16, c='#e0e0e0')
    ax.set_ylabel("Sea surface sality, ‰", fontsize=16, c='#e0e0e0')
    
    ax.annotate(year,
                xy=(0, 1), xycoords='axes fraction',
                xytext=(30, -120), textcoords='offset pixels',
                horizontalalignment='left',
                verticalalignment='top',
                fontsize=25,
                color = '#e0e0e0',
                bbox=dict(fc='#424242', pad=0.2, ec='#424242'))
    
    sc.axes.tick_params(color='#e0e0e0', 
                        labelcolor='#e0e0e0', 
                        labelsize=12)
    plt.savefig(f"graphs_assw/sat-vs-insitu/sal/sss_v_Sinsitu_{year}.png", dpi=300,
                bbox_inches = 'tight',
                pad_inches = 0.1)
    plt.close()
    


#Вариант для разной цветовой схемы и сетки для каждого года
# =============================================================================
# for year in range(2010, 2020):
#     plt.rcParams['font.family'] = 'serif'
#     df_avg_yearly = df_avg.query('year == @year')
#     fig, ax = plt.subplots(1 ,1)
#     
#     offset = mcolors.TwoSlopeNorm(vmin=min(df_avg_yearly.so_dif), 
#                               vcenter=0, 
#                               vmax=max(df_avg_yearly.so_dif))
#     
#     sc = ax.scatter(data = df_avg_yearly, 
#                     x='so_n',
#                     y='so_sat',
#                     c='so_dif',
#                     cmap=cmocean.cm.balance,
#                     s=20,
#                     edgecolor='#e0e0e0',
#                     linewidth=0.05,
#                     norm=offset)
#     
#     ax.plot([math.floor(min(df_avg_yearly[["so_n", "so_sat"]].min())), 
#              math.ceil(max(df_avg_yearly[["so_n", "so_sat"]].max()))],
#             [math.floor(min(df_avg_yearly[["so_n", "so_sat"]].min())), 
#              math.ceil(max(df_avg_yearly[["so_n", "so_sat"]].max()))],
#              c='#e0e0e0',
#              linewidth=4)
#     
#     
#     plt.grid(color='#e0e0e0',
#              linewidth=0.5)
#     divider = make_axes_locatable(ax)
#     ax_cb = divider.new_horizontal(size="2.5%", pad=0.1, axes_class=plt.Axes)
#     
#     fig.add_axes(ax_cb)
#     
#     cbar = plt.colorbar(sc, cax=ax_cb, extend="both",
#                         drawedges=True, format="%d",
#                         boundaries=np.arange(math.floor(min(df_avg_yearly.so_dif)), 
#                                              math.ceil(max(df_avg_yearly.so_dif)), 1)) 
#                                         
#     
#     cbar.outline.set_edgecolor('#e0e0e0')
#     cbar.dividers.set_edgecolor('#e0e0e0')
#     cbar.ax.tick_params(labelsize=13, 
#                         labelcolor='#e0e0e0',
#                         color='#e0e0e0')
#     cbar.set_label('Difference, ‰',
#                    color='#e0e0e0', 
#                    fontsize=16)
#     
#     
#     ax.set(facecolor='#424242')
#     fig.set(facecolor='#424242')
#     
#     ax.set_xlim([math.floor(min(df_avg_yearly[["so_n", "so_sat"]].min())),
#               math.ceil(max(df_avg_yearly[["so_n", "so_sat"]].max()))])
#     ax.set_ylim([math.floor(min(df_avg_yearly[["so_n", "so_sat"]].min())),
#               math.ceil(max(df_avg_yearly[["so_n", "so_sat"]].max()))])
#     
#     ax.set_xticks(np.arange(math.floor(min(df_avg_yearly[["so_n", "so_sat"]].min())),
#               math.ceil(max(df_avg_yearly[["so_n", "so_sat"]].max())), 
#               round((math.ceil(max(df_avg_yearly[["so_n", "so_sat"]].max())) -
#               math.floor(min(df_avg_yearly[["so_n", "so_sat"]].min())))/100*12)))
#     ax.set_yticks(np.arange(math.floor(min(df_avg_yearly[["so_n", "so_sat"]].min())),
#               math.ceil(max(df_avg_yearly[["so_n", "so_sat"]].max())),
#               round((math.ceil(max(df_avg_yearly[["so_n", "so_sat"]].max())) -
#               math.floor(min(df_avg_yearly[["so_n", "so_sat"]].min())))/100*12)))
#     
#     ax.spines['right'].set_visible(False)
#     ax.spines['top'].set_visible(False)
#     ax.spines['bottom'].set_edgecolor('#e0e0e0')
#     ax.spines['left'].set_edgecolor('#e0e0e0')
#     
#     ax.set_xlabel("In-situ salinity, ‰", fontsize=16, c='#e0e0e0')
#     ax.set_ylabel("Sea surface sality, ‰", fontsize=16, c='#e0e0e0')
#     
#     ax.annotate(year,
#                 xy=(0, 1), xycoords='axes fraction',
#                 xytext=(30, -120), textcoords='offset pixels',
#                 horizontalalignment='left',
#                 verticalalignment='top',
#                 fontsize=25,
#                 color = '#e0e0e0',
#                 bbox=dict(fc='#424242', pad=0.2, ec='#424242'))
#     
#     sc.axes.tick_params(color='#e0e0e0', 
#                         labelcolor='#e0e0e0', 
#                         labelsize=12)
#     plt.savefig(f"graphs_assw/sat-vs-insitu/sal/sss_v_Sinsitu_{year}.png", dpi=300,
#                 bbox_inches = 'tight',
#                 pad_inches = 0.1)
#     plt.close()
# =============================================================================
