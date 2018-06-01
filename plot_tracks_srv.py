import numpy as np
import backtrack
import read_currents as rc
import datetime
from matplotlib import pyplot as plt

start = datetime.datetime.now()
track = backtrack.backtrack_point( '/nfs0/valeria/Currents/Data_CMEMS/', 30, 140, datetime.datetime(2007,12,31), datetime.datetime(2007,1,1) )
print "time in sec = ", (datetime.datetime.now() - start).seconds

lat, lon, u, v = rc.read_currents( '/nfs0/valeria/Currents/Data_CMEMS/2017/dt_global_allsat_phy_l4_20170101_20170530_NH.nc')

from mpl_toolkits.basemap import Basemap
(lons,lats) = np.meshgrid(lon, lat)
m = Basemap(projection='merc',llcrnrlat=lats[0,0],urcrnrlat=lats[-50,-50],\
            llcrnrlon=lons[0,0],urcrnrlon=lons[-50,-50],lat_ts=20,resolution='c')

m.pcolormesh(lons, lats, u, latlon = True)
m.drawcoastlines()

for i in range(len(track)):
    x,y = m(track[i][1],track[i][0], inverse = False)
    m.plot(x,y, 'bo')
plt.show()
