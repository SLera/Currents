import numpy as np
import backtrack
import read_currents as rc
import datetime
from matplotlib import pyplot as plt

start = datetime.datetime.now()
track = backtrack.backtrack_point( '/home/valeria/DATA/Currents/NH', 35, 160, datetime.datetime(2007,12,31), datetime.datetime(2007,8,28) )
print "time in sec = ", (datetime.datetime.now() - start).seconds

lat, lon, u, v = rc.read_currents( '/home/valeria/DATA/Currents/NH/2017/dt_global_allsat_phy_l4_20170101_20170530_NH.nc')

from mpl_toolkits.basemap import Basemap
(lats, lons) = np.meshgrid(lat,lon)
m = Basemap(projection='merc',llcrnrlat=lats[0,0],urcrnrlat=lats[-1,-1],\
            llcrnrlon=lons[0,0],urcrnrlon=180,lat_ts=lats[-1,-1],resolution='c')
m.drawcoastlines()

from mpl_toolkits.basemap import Basemap

(lons,lats) = np.meshgrid(lon, lat)
m = Basemap(projection='merc',llcrnrlat=lats[0,0],urcrnrlat=lats[-50,-50],\
            llcrnrlon=lons[0,0],urcrnrlon=lons[-50,-50],lat_ts=20,resolution='c')

m.pcolormesh(lons, lats, u, latlon = True)
m.drawcoastlines()

for i in range(len(track)):
    x,y = m(track[i][1],track[i][0], inverse = False)
    m.plot(x,y, 'bo')
print 'to', track[0][1],track[0][0]
print 'from', track[-1][1],track[-1][0]

x0,y0 = m(track[0][1],track[0][0], inverse = False)   
x1,y1 = m(track[-1][1],track[-1][0], inverse = False) 
plt.text(x0, y0, 'to',fontsize = 12)
plt.text(x1, y1, 'from',fontsize = 12)
plt.show()
