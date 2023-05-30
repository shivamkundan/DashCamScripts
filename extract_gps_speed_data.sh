#!/bin/bash

# ====================================================================== #
# DOCS
# http://aprs.gids.nl/nmea/
# https://exiftool.org/forum/index.php?topic=10058.0
# https://github.com/bartbroere/blackvue-acc
# https://en.wikipedia.org/wiki/NMEA_0183
# ====================================================================== #

infolder="/Users/shivamkundan/Movies/Drive_to_Stews_May28/Front" # NO slash at end
outfolder=$infolder

GPS_OUTFILE="$outfolder/extracted.gps"
SPEED_OUTFILE="$outfolder/speed.csv"
POS_TIME_OUTFILE="$outfolder/pos_time.csv"

echo ""
echo "working directory:"
echo "$infolder" 
echo ""
echo "mapping gps position..."


# while true;do echo -n .;sleep 1;done &
# # sleep 10 # or do something else here
strings $infolder/*F.mp4 | grep -e GPRMC -e GPVTG -e GPGSA -e GPGSV -e GPGLL > $GPS_OUTFILE
# wait
# kill $!; trap 'kill $!' SIGTERM
# echo done

# ---------------------------------------------------------------
echo "extracting speed..."
more $GPS_OUTFILE | grep GPVTG | cut -d, -f 8 > $SPEED_OUTFILE
echo ""
echo "done"

# ---------------------------------------------------------------
echo "extracting position lat/long and UTC timestamp hhmmss.ss ..."
more $GPS_OUTFILE | grep GPGLL | cut -d, -f 2,4,6,7 > $POS_TIME_OUTFILE
echo ""
echo "done"

# ---------------------------------------------------------------
echo "extracting Recommended minimum specific GPS/Transit data..."
more $GPS_OUTFILE | grep GPRMC | cut -d, -f 2-13 > $outfolder/GPRMC_OUTFILE.csv
echo ""
echo "done"

# ---------------------------------------------------------------
echo "extracting GPS Satellites in view..."
more $GPS_OUTFILE | grep GPGSV | cut -d, -f 4 > $outfolder/GPGSV_OUTFILE.csv
echo ""
echo "done"

# ---------------------------------------------------------------
# DOP can be expressed as a number of separate measurements:
# 	HDOP
# 		Horizontal dilution of precision
# 	VDOP
# 		Vertical dilution of precision
# 	PDOP
# 		Position (3D) dilution of precision

# DOP val	|	Rating		| Description
# ---------- --------------- -------------
# <1		|	Ideal		| Highest possible confidence level to be used for applications demanding the highest possible precision at all times.
# 1–2		|	Excellent	| At this confidence level, positional measurements are considered accurate enough to meet all but the most sensitive applications.
# 2–5		|	Good		| Represents a level that marks the minimum appropriate for making accurate decisions. Positional measurements could be used to make reliable in-route navigation suggestions to the user.
# 5–10		|	Moderate	| Positional measurements could be used for calculations, but the fix quality could still be improved. A more open view of the sky is recommended.
# 10–20		|	Fair		| Represents a low confidence level. Positional measurements should be discarded or used only to indicate a very rough estimate of the current location.
# >20		|	Poor		| At this level, measurements should be discarded.
echo "extracting DOP [Dilution of precision]..."
more $GPS_OUTFILE | grep GPGSA | cut -d, -f 2,3,16-18 > $outfolder/GPGSA_OUTFILE.csv
echo ""
echo "done"