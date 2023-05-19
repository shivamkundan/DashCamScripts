#!/bin/bash

infolder="/Users/shivamkundan/Movies/Sep_6_trip/front" # NO slash at end
outfolder=$infolder

GPS_OUTFILE="$outfolder/extracted.gps"
SPEED_OUTFILE="$outfolder/speed.csv"

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

echo "extracting speed..."
more $GPS_OUTFILE | grep GPVTG | cut -d, -f 8 > $SPEED_OUTFILE
echo ""
echo "done"