#! /usr/bin/python
import os
import subprocess
import pandas as pd

import matplotlib.pyplot as plt
# plt.style.use('seaborn-whitegrid')
import numpy as np


DIR="/Users/shivamkundan/Movies/Sep_6_trip/"
df=pd.read_csv(DIR+'speed.csv')

TRIP_DATE="Sep 6"


start_nonzero=int(df.ne(0).idxmax())
end=len(df)

x=list(df['000.0'])

outlist=[]

for val in x[start_nonzero:end]:
	outlist.append(val*0.62)


out=pd.Series(outlist,name='Speed (MPH)')
out_pd=pd.DataFrame(out)

print out_pd.describe()


# out_pd.to_excel(DIR+'speed.xlsx')
# ----------------------------


plt.title(TRIP_DATE+" Speed (MPH)",fontsize=14)
# # plt.xlabel("x")
plt.ylabel("Speed (MPH)",fontsize=12);

# plt.xlim(10, 0)

if max(outlist)>90:
	max_y=max(outlist)+10
else:
	max_y=90

avg_speed=sum(outlist) / float(len(outlist))


plt.ylim(0, max_y);

ax = plt.axes()

x = [i for i in range(0,len(outlist))]
avg_speed_list=[avg_speed for i in range(0,len(outlist))]
avg_speed_label='Avg Speed ='+str(round(avg_speed,1))+' MPH'


ax.plot(x,outlist,linewidth=2,color='red');
ax.plot(x,avg_speed_list,linewidth=1,color='blue',label=avg_speed_label);

plt.legend()

# plt.show()

plt.savefig(DIR+TRIP_DATE+'_speed.jpg')



