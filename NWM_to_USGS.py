#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# import necessary packages 
import pandas as pd
import numpy as np
import os, s3fs, pyproj, warnings
import xarray as xr
import geopandas as gpd
import matplotlib.pyplot as plt

# Suppressing all warnings for clearer output
warnings.filterwarnings("ignore")

# define path for csv spreadsheet where NWM feature ids and USGS gages ids are stored
# if path of the spread sheet is different than the current working directory call file by giving full path
path1 = (r'C:\Users\stiwar44.ASURITE\Dropbox (ASU)\Hydrology_Mascaro_Lab\Suraj\Python_supporting_file'
        r'\gage_id_nwm_feature_id_crosswalk.csv')

# read the csv file
nws = pd.read_csv(path1)
print(f"Total USGS and NWM corresponding data: {len(nws)}")

# define a target CRS to work on same coordinate system
target_crs = "EPSG:4269"

# Define the path to the shapefile containing USGS streamflow data
shapefile_path = r'D:\\1._Ph.D._Research_work\\ArcGIS_works\\GageLoc\\GageLoc.shp'
# read shapefile of USGS gages as geopandas dataframe
gages = gpd.read_file(shapefile_path)

# read shapefile of river network
reaches_conus = gpd.read_file(r'D:\1._Ph.D._Research_work\ArcGIS_works\shape_files\nwm_reaches_conus_NAD1983.shp')

# read the USA state map's shapefile and project it to the target crs.
US_boundary = gpd.read_file(r"C:\Users\stiwar44.ASURITE\Dropbox (ASU)\Hydrology_Mascaro_Lab\Suraj\GIS_files\US_territory"
                           r"\CONUS_territory.shp")
# project the US boundary shapefile to target CRS
US_boundary = US_boundary.to_crs(target)

# clip the gages by CONUS_boundary 
gages = gpd.clip(gages, boundary)

# buffer to any specific value you like, less is the buffer distance more accurately gages align with stream segments
buffer_distance = 0.00001

# make a copy of gages for buffering
gages_new = gages.copy()

# add geometry to copied geodataframe of gages
gages_new['geometry'] = gages.buffer(buffer_distance)

# spatial join the buffered USGS gages to NWM stream network shapefile
gages_with_NWM_id = gpd.sjoin(gages_new, reaches[['geometry','feature_id']], how = 'left', op = 'intersects')

# set USGS gages id as index
gages_with_NWM_id = gages_with_NWM_id.set_index("SOURCE_FEA")

# remove the nan values by applying dropna
gages_with_NWM_id = gages_with_NWM_id.dropna(subset=['feature_id'])

# convert the NWM feature id values to integer type
gages_with_NWM_id['feature_id'] = gages_with_NWM_id['feature_id'].astype(int)

# convert the UGSG gages as string format type
gages_with_NWM_id.index = gages_with_NWM_id.index.astype(str)

# make a dataframe with USGS gages and NWM feature id only and save as text file
gages_vs_NWM = gages_with_NWM_id[['feature_id']]
gages_vs_NWM = gages_vs_NWM.rename_axis("USGS_gages")

# save the dataframe as a csv
gages_vs_NWM.to_csv(r"C:\Users\stiwar44.ASURITE\Dropbox (ASU)\Hydrology_Mascaro_Lab\Suraj\Python_output_files"
                    r"\USGS_gages_corresponding_NWM.txt")

