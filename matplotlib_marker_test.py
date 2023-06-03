#!/usr/local/bin/python3

# https://petercbsmith.github.io/marker-tutorial.html


import matplotlib as mpl
from svgpathtools import svg2paths
from svgpath2mpl import parse_path

import matplotlib.pyplot as plt
from matplotlib.markers import MarkerStyle
from matplotlib.transforms import Affine2D

marker_path, attributes = svg2paths('up_arrow.svg')
custom_marker = parse_path(attributes[0]['d'])
custom_marker.vertices -= custom_marker.vertices.mean(axis=0)

custom_marker = custom_marker.transformed(mpl.transforms.Affine2D().rotate_deg(0))
custom_marker = custom_marker.transformed(mpl.transforms.Affine2D().scale(1))



y=[2*i for i in range(10)]
x=[i for i in range(10)]




plt.plot(x,y,'o',marker=custom_marker,markersize=40)

plt.show()