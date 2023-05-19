strings *F.mp4 | grep -e GPRMC -e GPVTG -e GPGSA -e GPGSV -e GPGLL > ~/Desktop/extracted.gps

more extracted.gps | grep GPVTG | cut -d, -f 8 > speed.csv