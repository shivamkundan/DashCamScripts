# We translate the Swift implementation using the Python Math (trigonometry functions), NumPy (vectors) and PyQuaternion (quaternions) modules 

import math
import numpy as np
from pyquaternion import Quaternion

def calculateSatelliteLatLong (
	observers_latitude,
	observers_longitude,
	satellite_elevation,
	satellite_azimuth,
	satellite_altitude = 20200,    # distance of satellite above the planets surface in kilometers (default is GPS satellites)
	earth_radius       =  6371):   # Radius of planet in kilometers (default is Earth)

	r1 = earth_radius
	r2 = earth_radius + satellite_altitude

	elevation_angle = math.radians (satellite_elevation) + math.pi / 2
	inscribed_angle = math.asin (r1 * math.sin (elevation_angle) / r2)  # Applying the Sine Law
	central_angle   = math.pi - elevation_angle - inscribed_angle       # internal angle sum equals pi

	x_vector = np.array ([1.0, 0.0, 0.0])
	y_vector = np.array ([0.0, 1.0, 0.0])
	z_vector = np.array ([0.0, 0.0, 1.0])

	latitude_quaternion = Quaternion (angle = math.radians (-observers_latitude), axis = y_vector)
	lat_long_axis = latitude_quaternion.rotate (x_vector)

	longitude_quaternion = Quaternion (angle = math.radians (observers_longitude), axis = z_vector)
	lat_long_axis = longitude_quaternion.rotate (lat_long_axis)

	lat_long_z    = lat_long_axis[2]
	target_vector = np.subtract (np.array ([0.0, 0.0, 1.0 / lat_long_z]), lat_long_axis)
	target_axis   = target_vector / np.linalg.norm (target_vector)

	azimuth_quaternion = Quaternion (angle = math.pi + math.pi / 2.0 - math.radians (satellite_azimuth), axis = lat_long_axis)
	target_axis = azimuth_quaternion.rotate (target_axis)

	elevation_quaternion = Quaternion (angle = -central_angle, axis = target_axis)
	satellite_vector = elevation_quaternion.rotate (lat_long_axis)

	satellite_x = satellite_vector[0]
	satellite_y = satellite_vector[1]
	satellite_z = satellite_vector[2]

	satellite_latitude  = math.degrees (math.pi / 2 - math.acos (satellite_z))
	satellite_longitude = math.degrees (math.atan2 (satellite_y, satellite_x))

	return (satellite_latitude, satellite_longitude)