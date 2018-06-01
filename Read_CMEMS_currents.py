#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 13:52:41 2018

@author: valeria
"""

import netCDF4
import numpy as np
import datetime
fname = '/home/valeria/NIERSC/Scripts/Currents/test_data/dt_global_allsat_msla_h_19951220_20170110_NH.nc'

data_set = netCDF4.Dataset(fname)
time = data_set.variables['time'][:][0]
date = datetime.date(1950,1,1)+datetime.timedelta(int(time))
lat = data_set.variables['latitude'][:]
lon = data_set.variables['longitude'][:]

uanom = data_set.variables['ugosa'][:].data[0,:,:]
uanom_mask = data_set.variables['ugosa'][:].mask[0,:,:]
ind = np.where(uanom_mask==True)
uanom[ind]=np.nan
vanom = data_set.variables['vgosa'][:].data[0,:,:]
vanom_mask = data_set.variables['vgosa'][:].mask[0,:,:]
ind = np.where(vanom_mask==True)
vanom[ind]=np.nan

u = data_set.variables['ugos'][:].data[0,:,:]
u_mask = data_set.variables['ugos'][:].mask[0,:,:]
ind = np.where(u_mask==True)
u[ind]=np.nan


v = data_set.variables['vgos'][:].data[0,:,:]
v_mask = data_set.variables['vgos'][:].mask[0,:,:]
ind = np.where(v_mask==True)
v[ind]=np.nan

from matplotlib import pyplot as plt

plt.figure()
plt.imshow(uanom, origin ='lower')
plt.colorbar()
plt.title('uanom')
plt.show()

plt.figure()
plt.imshow(vanom, origin ='lower')
plt.colorbar()
plt.title('vanom')
plt.show()

plt.figure()
plt.imshow(u, origin ='lower')
plt.title('u')
plt.colorbar()
plt.show()

plt.figure()
plt.imshow(v, origin ='lower')
plt.title('v')
plt.colorbar()
plt.show()