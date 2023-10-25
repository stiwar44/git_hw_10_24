#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import os
import xarray as xr
import geopandas as gpd
import s3fs
import pyproj
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
path1 = (r'C:\Users\stiwar44.ASURITE\Dropbox (ASU)\Hydrology_Mascaro_Lab\Suraj\Python_supporting_file'
        r'\gage_id_nwm_feature_id_crosswalk.csv')
x = pd.read_csv(path1)
print(f"Total USGS and NWM corresponding data: {len(x)}")
target = "EPSG:4269"
path2 = r'D:\\1._Ph.D._Research_work\\ArcGIS_works\\GageLoc\\GageLoc.shp'
gages = gpd.read_file(shapefile_path)
reaches = gpd.read_file(r'D:\1._Ph.D._Research_work\ArcGIS_works\shape_files\nwm_reaches_conus_NAD1983.shp')
boundary = gpd.read_file(r"C:\Users\stiwar44.ASURITE\Dropbox (ASU)\Hydrology_Mascaro_Lab\Suraj\GIS_files\US_territory"
                           r"\CONUS_territory.shp")
boundary = boundary.to_crs(target)
gages = gpd.clip(gages, boundary)
y = 0.00001
gages_new = gages.copy()
gages_new['geometry'] = gages.buffer(buffer_distance)
gages_with_NWM_id = gpd.sjoin(gages_new, reaches[['geometry','feature_id']], how = 'left', op = 'intersects')
gages_with_NWM_id = gages_with_NWM_id.set_index("SOURCE_FEA")
gages_with_NWM_id = gages_with_NWM_id.dropna(subset=['feature_id'])
gages_with_NWM_id['feature_id'] = gages_with_NWM_id['feature_id'].astype(int)
gages_with_NWM_id.index = gages_with_NWM_id.index.astype(str)
gages_vs_NWM = gages_with_NWM_id[['feature_id']]
gages_vs_NWM = gages_vs_NWM.rename_axis("USGS_gages")
gages_vs_NWM.to_csv(r"C:\Users\stiwar44.ASURITE\Dropbox (ASU)\Hydrology_Mascaro_Lab\Suraj\Python_output_files"
                    r"\USGS_gages_corresponding_NWM.txt")

