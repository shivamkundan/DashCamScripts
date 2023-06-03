#!/usr/local/bin/python3
from math import sin, cos, sqrt, atan2, radians


# Decimal Degrees = degrees + (minutes/60) + (seconds/3600)



def calc_distance(point2,point1):
	lat2=radians(point2[0])
	lon2=radians(point2[1])

	lat1=radians(point1[0])
	lon1=radians(point1[1])

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	# Approximate radius of earth in km
	R = 6373.0
	distance = R * c

	print("Result: ", distance,"km")
	# print("Should be: ", 278.546, "km")

if __name__ == '__main__':
	calc_distance((37.72024021471334,-89.2162186017107),(37.72089997172164,-89.21630259924612))
	print()
	calc_distance((37.72089997172164,-89.21630259924612),(37.72024021471334,-89.2162186017107))