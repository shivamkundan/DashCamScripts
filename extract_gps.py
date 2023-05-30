#!/usr/local/opt/python@3.9/libexec/bin/python
import pandas as pd
import openpyxl

# need:
# valid bit        [RMC]
# epoch/Timestamp  [RMC]
# (lat, long)	   [RMC]
# speed kts -> mph [RMC]
# true heading (?) [RMC]
# num satellites   [GSV]

# HDOP,VDOP,PDOP   [GSA]

# ==== calc these ==== #
# trip start time
# gps sig start time
# trip end time
# total trip time
# total driving time
# total stopping/waiting time
# distance traveled -> calc from (lat, long)
# num of stops
# avg/median/min/max time stopped

# ==================================================================================================== #
# ==================================================================================================== #
# ----------------------------------------------------------------------------------------------------
# GPGLL
# 1    5133.81   Current latitude
# 2    N         North/South
# 3    00042.25  Current longitude
# 4    W         East/West
# 5    *75       checksum
GPGLL_headers=["epoch","code","latitude","N/S","longitude","E/W","timestamp","validity","","Checksum"]

# ----------------------------------------------------------------------------------------------------
# GPRMC
# KTS  to MPH: for an approximate result, multiply the speed value by 1.151
# KTS to KMPH: multiply the speed value by 1.852
# KMPH to MPH: for an approximate result, divide   the speed value by 1.609
# MPH to m/s: divide the speed value by 2.237


# 1   220516     Time Stamp
# 2   A          validity - A-ok, V-invalid
# 3   5133.82    current Latitude
# 4   N          North/South
# 5   00042.24   current Longitude
# 6   W          East/West
# 7   173.8      Speed in knots
# 8   231.8      True course
# 9   130694     Date Stamp
# 10  004.2      Variation
# 11  W          East/West
# 12  *70        checksum

# -------------
# $GPRMC,210230,A,3855.4487,N,09446.0071,W,0.0,076.2,130495,003.8,E*69
# The sentence contains the following fields:
# Epoch
# Code/The sentence type
# Current time (if available; UTC)
# Position status (A for valid, V for invalid)
# Latitude (in DDMM.MMM format)
# Latitude compass direction
# Longitude (in DDDMM.MMM format)
# Longitude compass direction
# Speed (in knots per hour)
# Heading
# Date (DDMMYY)
# Magnetic variation
# Magnetic variation direction
# The checksum validation value (in hexadecimal)

GPRMC_headers=["epoch","code","timestamp","validity","latitude","N/S","longitude","E/W",\
				"Speed (kts)","Heading","Date Stamp","Mag Variation","Mag Variation Dir","valid?","Checksum"]

# ----------------------------------------------------------------------------------------------------
# GPVTG
# 054.7,T      True track made good
# 034.4,M      Magnetic track made good
# 005.5,N      Ground speed, knots
# 010.2,K      Ground speed, Kilometers per hour
GPVTG_headers=["epoch","code","True track made good"," Magnetic track made good","Speed (kts)","Speed (kmph)"]

# ----------------------------------------------------------------------------------------------------
# GPGSV
# 1    = Total number of messages of this type in this cycle
# 2    = Message number
# 3    = Total number of SVs in view
# 4    = SV PRN number
# 5    = Elevation in degrees, 90 maximum
# 6    = Azimuth, degrees from true north, 000 to 359
# 7    = SNR, 00-99 dB (null when not tracking)
# 8-11 = Information about second SV, same as field 4-7
# 12-15= Information about third SV, same as field 4-7
# 16-19= Information about fourth SV, same as field 4-7

# -------------
# $GPGSV,2,1,08,02,74,042,45,04,18,190,36,07,67,279,42,12,29,323,36*77
# $GPGSV,2,2,08,15,30,050,47,19,09,158,,26,12,281,40,27,38,173,41*7B

# The GSV sentence contains the following fields:

# The sentence type
# The number of sentences in the sequence
# The number of this sentence
# The number of satellites
# The satellite number, elevation, azimuth, and signal to noise ratio for each satellite
# The checksum validation value (in hexadecimal)

GPGSV_headers=["epoch","code","#MSGS","MSG_NUM","#SVs","SV PRN#","ELV","AZM","SNR","","","","","","","","","","","","",""]


# ----------------------------------------------------------------------------------------------------
# GPGSA
# 1    = Mode:
#        M=Manual, forced to operate in 2D or 3D
#        A=Automatic, 3D/2D
# 2    = Mode:
#        1=Fix not available
#        2=2D
#        3=3D
# 3-14 = IDs of SVs used in position fix (null for unused fields)
# 15   = PDOP
# 16   = HDOP
# 17   = VDOP
GPGSA_headers=["epoch","code","manual/auto","mode"]


# ==================================================================================================== #
# ==================================================================================================== #
def print_summary(NMEA_codes_dict):
	for code in NMEA_codes_dict.keys():
		# print (f"code: {code}")
		print (f"#items[{code}]: {len(NMEA_codes_dict[code])}")
		# for item in NMEA_codes_dict[code]:
		# 	print (item)
		# print()
def convert_coords_dms_to_decimal(lat,long):
	# Decimal Degrees = degrees + (minutes/60) + (seconds/3600)
	pass
# ==================================================================================================== #
# ==================================================================================================== #

outfile="gps_data.xlsx"
infile="out.txt"

# Main data struct
NMEA_codes_dict={"GPRMC":[],
				 "GPVTG":[],
				 "GPGSA":[],
				 "GPGSV":[],
				 "GPGLL":[],
				}

if __name__=="__main__":

	# Read file
	inlist=[]
	with open(infile,'r') as f:
		inlist=f.readlines()
	f.close()
	print (f"#Input lines: {len(inlist)}")

	# Basic parse each line
	# $	0x24	36	Start delimiter
	# *	0x2a	42	Checksum delimiter
	# ,	0x2c	44	Field delimiter
	for line in inlist:
		l=line.replace("$",",").replace("*",",").replace("[","").replace("]","").replace("\n","")
		l=l.split(",")
		l[0]=l[0].replace("gps","").replace(" ","")

		curr_code=l[1]
		if (curr_code=="GPGSV"):
			if ( l[3]=="1"):
				NMEA_codes_dict[curr_code].append(l)
		else:
			NMEA_codes_dict[curr_code].append(l)
	# Print details
	print_summary(NMEA_codes_dict)

	# Convert to dataframes
	df_GPRMC = pd.DataFrame(NMEA_codes_dict["GPRMC"], columns=GPRMC_headers)
	df_GPGLL = pd.DataFrame(NMEA_codes_dict["GPGLL"], columns=GPGLL_headers)
	df_GPVTG = pd.DataFrame(NMEA_codes_dict["GPVTG"])#, columns=GPVTG_headers)
	df_GPGSV = pd.DataFrame(NMEA_codes_dict["GPGSV"], columns=GPGSV_headers)
	df_GPGSA = pd.DataFrame(NMEA_codes_dict["GPGSA"])#, columns=GPVTG_headers)

	# Typecasting
	df_GPGLL["latitude_adj"]=pd.to_numeric(df_GPGLL["latitude"])#, errors='raise', downcast="float")#, dtype_backend=_NoDefault.no_default)
	df_GPGLL["longitude_adj"]=pd.to_numeric(df_GPGLL["longitude"])#, errors='raise', downcast="float")#, dtype_backend=_NoDefault.no_default)


	df_GPRMC["Speed (kts)"]=pd.to_numeric(df_GPRMC["Speed (kts)"])
	df_GPRMC["Heading"]=pd.to_numeric(df_GPRMC["Heading"])
	df_GPRMC["latitude"]=pd.to_numeric(df_GPRMC["latitude"])
	df_GPRMC["longitude"]=pd.to_numeric(df_GPRMC["longitude"])

	# GSV
	df_GPGSV["#SVs"]=pd.to_numeric(df_GPGSV["#SVs"])
	df_GPGSV["#MSGS"]=pd.to_numeric(df_GPGSV["#MSGS"])
	df_GPGSV["MSG_NUM"]=pd.to_numeric(df_GPGSV["MSG_NUM"])


	# df1.merge(df2, left_on='objectdesc', right_on='objdescription')[['Content', 'objectdesc', 'TS_id', 'idname']]


	df_3 = df_GPRMC.merge(df_GPGSV[['epoch', '#SVs']], left_on='epoch',right_on='epoch',how="outer").drop(["code","timestamp","N/S","E/W","Date Stamp","Speed (kts)","Mag Variation","Mag Variation Dir","valid?","Checksum"], axis='columns')


	df_3["Speed (kts)"]=df_GPRMC["Speed (kts)"]
	df_3["Speed (MPH)"]=df_GPRMC["Speed (kts)"]*1.151
	df_3["Speed (MPH)"]=df_3["Speed (MPH)"].round(decimals=1)
	# df_3["#SVs"]=df_3["#SVs"].multiply(1, fill_value=0)


	# Convert from unix epoch to readable date time
	for df in [df_GPRMC,df_GPGLL,df_GPGSV,df_3]:
		# try:
		df["epoch"]=pd.to_datetime(df["epoch"], errors="raise", unit="ms", origin="unix")
		# except:

	# # create a excel writer object
	# with pd.ExcelWriter(outfile) as writer:
	# 	df_GPRMC.to_excel(writer, sheet_name="GPRMC", index=False)
	# 	df_GPGLL.to_excel(writer, sheet_name="GPGLL", index=False)
	# 	df_GPVTG.to_excel(writer, sheet_name="GPVTG", index=False)
	# 	df_GPGSV.to_excel(writer, sheet_name="GPGSV", index=False)
	# 	df_GPGSA.to_excel(writer, sheet_name="GPGSA", index=False)
	# 	df_3.to_excel(writer, sheet_name="Summary", index=False)


	lat=df_GPGLL["latitude_adj"]
	lon=df_GPGLL["longitude_adj"]

	print (len(lat))


	for i in range (1,len(lat)):
		lat1=lat[i]
		lat2=lat[i-1]

		lon1=lon[i]
		lon2=lon[i-1]

		print (f"({lat2},{lon2}) - ({lat1},{lon1})")
	# for item in x:
	# 	print (item)