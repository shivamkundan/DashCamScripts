#!/usr/local/bin/python3

from geographiclib.geodesic import Geodesic


# This computes the geodesic from Wellington, New Zealand (41.32S 174.81E) to Salamanca, Spain (40.96N 5.50W).
# The distance is given by s12 (19959679 meters) and the initial azimuth (bearing) is given by azi1 (161.067... degrees clockwise from north).
print (Geodesic.WGS84.Inverse(37.73195556, -89.21577222, 37.73196111,-89.215525))

import math, numpy as np

def get_bearing(lat1,lon1,lat2,lon2):
    dLon = lon2 - lon1;
    y = math.sin(dLon) * math.cos(lat2);
    x = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dLon);
    brng = np.rad2deg(math.atan2(y, x));
    if brng < 0: brng+= 360
    return brng

print (get_bearing(37.73195556, -89.21577222, 37.73196111,-89.215525))