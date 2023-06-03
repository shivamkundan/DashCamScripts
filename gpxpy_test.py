#!/usr/local/bin/python3

# https://nbviewer.org/github/FlorianWilhelm/gps_data_with_python/blob/master/talk.ipynb

import sys
import gpxpy
import math
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle
from matplotlib.transforms import Affine2D
from matplotlib.text import TextPath
from svgpathtools import svg2paths
from svgpath2mpl import parse_path

plt.rcParams['axes.xmargin'] = 0.1
plt.rcParams['axes.ymargin'] = 0.1
import seaborn as sns
sns.set_style("whitegrid")
sns.set_context("talk")
import warnings # to suppress warnings of Seaborn's deprecated usage of Matplotlib
warnings.filterwarnings("ignore")

from distance_calc import calc_distance


# ============================================= #
def get_bearing(lat1,lon1,lat2,lon2):
    dLon = lon2 - lon1;
    y = math.sin(dLon) * math.cos(lat2);
    x = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dLon);
    brng = np.rad2deg(math.atan2(y, x));
    if brng < 0: brng+= 360
    return brng

def print_gpx_details(gpx_file):
    print(gpx_file.get_bounds().max_latitude)
    print(gpx_file.get_bounds().max_longitude)
    print(gpx_file.get_bounds().min_latitude)
    print(gpx_file.get_bounds().min_longitude)
    print ()
    print(gpx_file.get_duration())
    print(gpx_file.get_time_bounds())

    print(gpx_file.has_elevations())
    print(gpx_file.has_times())

    print(gpx_file.length_2d())
    print(gpx_file.length_3d())

    moving_data = gpx_file.get_moving_data(raw=True)
    print (moving_data)

def create_report(gpx_file):
    indentation = '   '
    info_display = ""
    length_2d = gpx_file.length_2d()
    length_3d = gpx_file.length_3d()
    info_display += "\n%sLength 2D: %s" % (indentation, format_long_length(length_2d))
    info_display += "\n%sLength 3D: %s" % (indentation, format_long_length(length_3d))

    moving_time, stopped_time, moving_distance, stopped_distance, max_speed = gpx_file.get_moving_data()
    info_display += "\n%sMoving time: %s" %(indentation, format_time(moving_time))
    info_display += "\n%sStopped time: %s" %(indentation, format_time(stopped_time))
    info_display += "\n%sMax speed: %s" % (indentation, format_speed(max_speed))
    info_display += "\n%sAvg speed: %s" % (indentation, format_speed(moving_distance / moving_time) if moving_time > 0 else "?")
    uphill, downhill = gpx_file.get_uphill_downhill()
    info_display += "\n%sTotal uphill: %s" % (indentation, format_short_length(uphill))
    info_display += "\n%sTotal downhill: %s" % (indentation, format_short_length(downhill))
    info_display += "\n\n\n"
    print(info_display)

# ============================================= #
def format_time(time_s):
    if not time_s:
        return 'n/a'
    else:
        minutes = math.floor(time_s / 60.)
        hours = math.floor(minutes / 60.)
        return '%s:%s:%s' % (str(int(hours)).zfill(2), str(int(minutes % 60)).zfill(2), str(int(time_s % 60)).zfill(2))

def format_long_length(length):
    return '{:.3f} miles'.format((length / 1000.)/1.609)

def format_short_length(length):
    return '{:.1f}m'.format(length)

def format_speed(speed):
    if not speed:
        speed = 0
    else:
        return '{:.0f}m/s = {:.0f} MPH'.format(speed, speed * 2.237)

# ============================================= #

with open('stews.gpx') as fh:
    gpx_file = gpxpy.parse(fh)

print (dir(gpx_file))

# --- Print a report --- #
print_gpx_details(gpx_file)
create_report(gpx_file)


# ----- Make dataframe from raw data ----- #
segment = gpx_file.tracks[0].segments[0]
coords = pd.DataFrame([
        {'lat': p.latitude,
         'lon': p.longitude,
         'speed': p.speed,
         'time': p.time} for p in segment.points])
coords.set_index('time', drop=True, inplace=True)
coords["speed"]=coords["speed"]*2.237


# ----- Calculate compass headings ----- #
total_len=len(coords['lon'])
coords["heading"]=pd.Series([-1 for i in range(0,total_len)])
for i in range(1,total_len):
    C1=(coords['lat'][i-1],coords['lon'][i-1])
    C2=(coords['lat'][i],coords['lon'][i])

    head=get_bearing(C1[0], C1[1], C2[0], C2[1])
    coords["heading"][i]=head

print (coords)




# # ----- Write to CSV ----- #
# coords.to_csv("ouput.csv")

# exit()

verts = [[-1, -1], [1, -1], [1, 1], [-1, -1]]

# ----- Plot the track and position markers ----- #

marker_path, attributes = svg2paths('up_arrow.svg')




i=0
out_dir="/Users/shivamkundan/Developer/DashCamScripts/tracks_pngs/"

for i in range(1000,total_len):

    if (i%50==0):
        print (i)

    fig = plt.figure(frameon=False)

    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    # ax = fig.gca()
    # plt.axis('off')
    # plt.grid(False)

    fig.add_axes(ax)
    ax.set_xticks([])
    ax.set_yticks([])
    plt.box(False)

    custom_marker = parse_path(attributes[0]['d'])
    custom_marker.vertices -= custom_marker.vertices.mean(axis=0)

    # Plot the 'track'
    plt.plot(coords['lon'].values, coords['lat'].values,color="red")


    try:
        h=round(coords['heading'].values[i],0)


        custom_marker = custom_marker.transformed(mpl.transforms.Affine2D().rotate_deg(180-h))
        custom_marker = custom_marker.transformed(mpl.transforms.Affine2D().scale(1))


        # print (f"h:{h}")
        # t = Affine2D().scale(3).rotate_deg(360-h)
        # m = MarkerStyle(SUCCESS_SYMBOLS[0], transform=t)
    except:
        # t = Affine2D().scale(3)#.rotate_deg(round(coords['heading'].values[i]),0)
        # m = MarkerStyle(SUCCESS_SYMBOLS[2], transform=t)
        custom_marker = custom_marker.transformed(mpl.transforms.Affine2D().scale(1))





    # Plot current location marker
    plt.plot(coords['lon'].values[i], coords['lat'].values[i],'o',marker=custom_marker,color="yellow",markersize=20)

    # Save file
    fig.canvas.print_png(f"{out_dir}{i}.png")
