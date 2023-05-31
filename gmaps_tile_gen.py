#!/usr/local/bin/python3
import pandas as pd

df=pd.read_csv("gps.csv")

i=0
for lat,longg in zip(df['lat_dec'],df['long_dec']):
	# print (lat,-1*longg)
	if (i%30==0):
		line=f"{lat},-{longg}|"
		print (line)
	i+=1
print (line.rstrip("|"))


# print (df)