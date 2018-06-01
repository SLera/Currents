import read_currents as rc
import pyproj
import math
import os
import datetime

def move_point_az( lon, lat, l, az ):
    g = pyproj.Geod(ellps='WGS84')
    return g.fwd(lon, lat, az, l)

def move_point( lon, lat, du, dv ):
    angle = 90 - math.atan2( dv, du ) / math.pi * 180
    length = math.sqrt( du**2 + dv**2 )
    return move_point_az(lon, lat, length, angle)

def transform_lon(lon):
    if lon < 0:
        lon = lon +360
    return lon

def list_dir( dir ):
    onlyfiles = [os.path.join(dir, f) for f in os.listdir(dir) \
                 if os.path.isfile(os.path.join(dir, f)) and f.startswith("dt_global_allsat_msla_h_")]
    return onlyfiles

def extract_date( path ):
    return datetime.datetime.strptime(path[-23:-15], '%Y%m%d')

def check_file_path(path, first_date, last_date):
    date = extract_date(path)
    return date >= first_date and date <= last_date

def filter_by_date( list, first_date, last_date ):
    filtered = [f for f in list if check_file_path(f, first_date, last_date)]
    return filtered

def list_needed_files( dir, lat, lon, last_day, first_day ):
    if last_day.year == first_day.year:
        lst = list_dir( os.path.join(dir, str(last_day.year)) )
        file_list = filter_by_date( lst, first_day, last_day )
        return file_list
    else:
        assert last_day.year-1 == first_day.year
        lst0 = list_dir(os.path.join(dir, str(first_day.year)))
        file_list = filter_by_date(lst0, first_day, last_day)
        lst1 = list_dir(os.path.join(dir, str(last_day.year)))
        file_list += filter_by_date(lst1, first_day, last_day)
        return file_list

def get_point_index( lats, lons, lat, lon ):
    lon = transform_lon(lon)
    assert lat >= lats[0] and lat < lats[-1]
    assert lon >= 0 and lon <= 360
    #assert lon >= lons[0] and lon < lons[-1]
    lat_step = lats[1] - lats[0]
    lon_step = lons[1] - lons[0]
    lat_idx = int((lat - lats[0]) / lat_step)
    lon_idx = int((lon - lons[0]) / lon_step)
    if lon <= lons[0]:
        lon_idx = 0
    if lon >= lons[-1]:
        lon_idx = len(lons)-1
    return  lat_idx, lon_idx

def backtrack_point( dir, lat, lon, last_day, first_day ):
    file_list = list_needed_files( dir, lat, lon, last_day, first_day )
    file_list.sort()
    file_list.reverse()

    #file_list = [ os.path.join(dir, f) for f in file_list ]

    print "Start"
    res = [(lat,lon)]

    for i in range( len(file_list)-1 ):
        lats, lons, us, vs = rc.read_currents( file_list[i] )
        lat_idx, lon_idx = get_point_index( lats, lons, lat, lon )
        u = us[lat_idx, lon_idx]
        v = vs[lat_idx, lon_idx]
        if math.isnan(u) or math.isnan(v):
            print "we are in nan region"
            print "lat lon = ",lat, lon, "date = ", extract_date( file_list[i] )
            return res
        days_diff = (extract_date( file_list[i] ) - extract_date( file_list[i+1] )).days
        dt = days_diff * 24 * 60 * 60
        lon, lat, _ = move_point(lon, lat, -u*dt, -v*dt)
        lon = transform_lon(lon)
        assert lon>=0 and lon<=360
        res.append( (lat, lon) )

    return res

def backtrack_point_totxt( dir, lat, lon, last_day, first_day ):
    file_list = list_needed_files( dir, lat, lon, last_day, first_day )
    file_list.sort()
    file_list.reverse()

    #file_list = [ os.path.join(dir, f) for f in file_list ]

    print "Start"
    res = [['lat', 'lon', 'year', 'month', 'day']]
    res.append([str(lat), str(lon), str(last_day.year), str(last_day.month), str(last_day.day)])

    for i in range( len(file_list)-1 ):
        lats, lons, us, vs = rc.read_currents( file_list[i] )
        lat_idx, lon_idx = get_point_index( lats, lons, lat, lon )
        u = us[lat_idx, lon_idx]
        v = vs[lat_idx, lon_idx]
        if math.isnan(u) or math.isnan(v):
            print "we are in nan region"
            print "lat lon = ",lat, lon, "date = ", extract_date( file_list[i] )
            return res
        days_diff = (extract_date( file_list[i] ) - extract_date( file_list[i+1] )).days
        dt = days_diff * 24 * 60 * 60
        lon, lat, _ = move_point(lon, lat, -u*dt, -v*dt)
        lon = transform_lon(lon)
        assert lon>=0 and lon<=360
        cur_day = extract_date( file_list[i+1] )
        res.append( [str(lat), str(lon), str(cur_day.year), str(cur_day.month), str(cur_day.day)] )

    return res   

#a = backtrack_point( '/home/valeria/DATA/Currents/NH', 30, 140, datetime.datetime(2007,12,31), datetime.datetime(2007,1,1) )
#print a