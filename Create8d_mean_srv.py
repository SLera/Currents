#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 14:04:59 2017

@author: valeria
"""
#from osgeo import gdal
import netCDF4
import numpy as np
import os
import glob
#import matplotlib
#matplotlib.use('Agg')
from matplotlib import pyplot as plt
import datetime


INDIR_cur = '/nfs0/valeria/Currents/Data_CMEMS'
INDIR_ref_dates= '/nfs0/RSF2017_PozdnyakovDV/data/gridded/spectra_mask'

##creater list of 8-days mean reference dates (1 day of 8-days intrval)
def extract_ref_dates(INDIR_ref_dates,y):
    ref_dates= []
    for root, dirs, files in os.walk(INDIR_ref_dates):
        for cfile in files:
            if cfile.endswith('.npy'):
                fpath = os.path.join(root, cfile)
                ref_date = datetime.strptime(fpath[-18:-10], '%Y%m%d')
                if str(ref_date.year) == str(y): 
                    ref_dates.append(ref_date)
    return ref_dates 
    
##find files fitting to an 8-days interval
def extract_dates_cur(INDIR_cur, year):
    flist_cur = []
    dates_cur = []
    for root, dirs, files in os.walk(INDIR_cur+'/'+str(year)):
        for cfile in files:
            fpath = os.path.join(root, cfile)
            if cfile.endswith('.nc'):
                flist_cur.append(fpath)
                date_cur = datetime.strptime(fpath[-23:-15], '%Y%m%d')
    
                dates_cur.append(date_cur)
    return flist_cur, dates_cur

def read_current_CMEMS(FILENAME):
    data_set = netCDF4.Dataset(FILENAME)
    time = data_set.variables['time'][:][0]
    date = datetime.date(1950,1,1)+datetime.timedelta(int(time))
    lat = data_set.variables['latitude'][:]
    lon = data_set.variables['longitude'][:]
    
    u = data_set.variables['ugos'][:].data[0,:,:]
    u_mask = data_set.variables['ugos'][:].mask[0,:,:]
    ind = np.where(u_mask==True)
    u[ind]=np.nan
    
    v = data_set.variables['vgos'][:].data[0,:,:]
    v_mask = data_set.variables['vgos'][:].mask[0,:,:]
    ind = np.where(v_mask==True)
    v[ind]=np.nan
    return date, lat, lon, u, v

#def read_ifremer_sic_daily(FILENAME):
#     """Returns np.array with 0-100 sea ice concentration, (%)
#     Parameters:
#     -----------
#     FILENAME
#     """
#     data_set = netCDF4.Dataset(FILENAME)
#     sic = filter_array(data_set, filter1)
#     return sic
#
    

def find_8d_files(ref_date,dates_cur,fpath_cur):
    ls_cur_8days = []
    for i in range(len(dates_cur)):
        timedif = dates_cur[i]-ref_date
        if (timedif.days>=0 and timedif.days<8):
            ls_cur_8days.append(fpath_cur[i])
    return ls_cur_8days

def calculate_8d_mean(ls_cur_8days):
    ls_u = []  
    ls_v = []             
    for i in range(len(ls_cur_8days)):
        date, lat, lon, daily_u, daily_v = read_current_CMEMS(ls_cur_8days[i])
        ls_u.append(daily_u)
        ls_v.append(daily_v)
    u_array = np.array(ls_u)
    u_mean = np.nanmean(u_array,axis=0)
    v_array = np.array(ls_v)
    v_mean = np.nanmean(v_array,axis=0)
    #nnan = np.isnan(sic_mean)
    #ind = np.where(nnan==1)
    #sic_mean[ind]=-999
    return u_mean, v_mean




INDIR_cur = '/nfs0/data_sonarc/data/heap/ice_concentration/raw'
INDIR_ref_dates= '/nfs0/RSF2017_PozdnyakovDV/data/gridded/spectra_mask'
OUTDIR ='/nfs0/data_sonarc/data/heap/ice_concentration/processed_ocolor_v2'
years = np.arrange(1998,2016)
for y in years:
    fpath_cur,dates_cur = extract_dates_cur(INDIR_cur + '/' + str(y),y)
    ref_dates = extract_ref_dates(INDIR_ref_dates,y)
    for i in range(len(ref_dates)):
        ref_date=ref_dates[i]

        fname = ref_date.strftime('%Y%m%d')
        print 'processing %s...' % fname
        ls_cur_8days = find_8d_files(ref_date,dates_cur)
        u_mean,v_mean = calculate_8d_mean(ls_cur_8days)
        u_mean.dump('u_8days_'+fname)
        v_mean.dump('v_8days_'+fname)
#        prepare_nsidc_ic_filtered (sic_mean, OUTDIR+'/IFREMER_IceConcentration_8day_'+fname +'.tif')






#def gdalwarp (input_file, target_file, epsg,xmin,xmax,ymin,ymax,x_size,y_size):
#    #print 'gdalwarp -t_srs %s -te %s %s %s %s -tr %s %s -overwrite -of GTiff %s %s' % (epsg, xmin, ymin, xmax, ymax, x_size, y_size, input_file, target_file)
#    os.system('gdalwarp --config GDAL_DATA "/home/valeria/Programs/miniconda/share/gdal" -r near -t_srs %s -te %s %s %s %s -tr %s %s -overwrite -of GTiff %s %s -et 0.01 -dstnodata -999' % (epsg, xmin, ymin, xmax, ymax, x_size, y_size, input_file, target_file))
#
#def prepare_nsidc_ic_filtered (sic_mean, output_tiff):
##    dataset = netCDF4.Dataset(input_nc)
###   ice_concentration = dataset.variables['concentration'][:][0]
##    sic = filter_array(dataset, filter1)
#    ice_concentration = sic_mean
##    print ice_concentration
#    
#    driver = gdal.GetDriverByName('GTiff')
#    outData = driver.Create('temp.tif', ice_concentration.shape[1], ice_concentration.shape[0], 1, gdal.GDT_Int16)
#    outData.GetRasterBand(1).WriteArray(ice_concentration)
#    outData.SetGeoTransform(geotransform_opt)
#    outData.SetProjection(NSIDC_WKT)
#    outData.FlushCache()
#    del outData
#    
#    gdalwarp('temp.tif', output_tiff, target_epsg, target_xmin, target_xmax, target_ymin, target_ymax, taget_xsize, target_ysize)
#
###### CONSTS
#xSize = 12500
#ySize = -12500
#xCorner = -3850074.56
#yCorner = 5850046.72
#geotransform_opt = [xCorner, xSize, 0, yCorner, 0, ySize]
##NSIDC_WKT = 'PROJCS["NSIDC Sea Ice Polar Stereographic North",GEOGCS["Unspecified datum based upon the Hughes 1980 ellipsoid",DATUM["Not_specified_based_on_Hughes_1980_ellipsoid",SPHEROID["Hughes 1980",6378273,298.279411123064,AUTHORITY["EPSG","7058"]],AUTHORITY["EPSG","6054"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4054"]],PROJECTION["Polar_Stereographic"],PARAMETER["latitude_of_origin",70],PARAMETER["central_meridian",-45],PARAMETER["scale_factor",1],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["X",EAST],AXIS["Y",NORTH],AUTHORITY["EPSG","3411"]]'
#NSIDC_WKT = 'PROJCS["WGS 84 / NSIDC EASE-Grid North (deprecated)",GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]],PROJECTION["Lambert_Azimuthal_Equal_Area"],PARAMETER["latitude_of_center",90],PARAMETER["longitude_of_center",0],PARAMETER["false_easting",0],PARAMETER["false_northing",0],UNIT["metre",1,AUTHORITY["EPSG","9001"]],AXIS["X",EAST],AXIS["Y",NORTH],AUTHORITY["EPSG","3973"]]'
## Domain
##EPSG:3973 -te -5000000 -5000000 5000000 5000000 -tr 4000 4000
#target_epsg = 'EPSG:3973'
#target_xmin = -5000000
#target_ymin = -5000000
#target_xmax = 5000000
#target_ymax = 5000000
#taget_xsize = 4000
#target_ysize = 4000
######
#
#
#INDIR_sic = '/nfs0/data_sonarc/data/heap/ice_concentration/raw'
#INDIR_ref_dates= '/nfs0/RSF2017_PozdnyakovDV/data/gridded/spectra_mask'
#OUTDIR ='/nfs0/data_sonarc/data/heap/ice_concentration/processed_ocolor_v2'
#years = np.arrange(1998,2016)
##years = range(2011,2017,1)
#for y in years:
#    fpath_sic,dates_sic = extract_dates_sic(INDIR_sic + '/' + str(y),y)
#    ref_dates = extract_ref_dates(INDIR_ref_dates,y)
#    for i in range(len(ref_dates)):
#        ref_date=ref_dates[i]
#
#        fname = ref_date.strftime('%Y%m%d')
#        print 'processing %s...' % fname
#        ls_sic_8days = find_8d_files(ref_date,dates_sic)
#        sic_mean = calculate_8d_mean(ls_sic_8days)
#        
#        prepare_nsidc_ic_filtered (sic_mean, OUTDIR+'/IFREMER_IceConcentration_8day_'+fname +'.tif')
