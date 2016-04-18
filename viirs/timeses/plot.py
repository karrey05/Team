import matplotlib.pyplot as plt
from matplotlib import colors, ticker, cm
import matplotlib as mpl                                #Loads map plotting library
import numpy as np                                      #Loads functions for array, linear algebra, array operations
import glob
import gc
import datetime as dt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
#import json

read_dict=np.load('lights.npy').item()
ct_t=read_dict['ct_t']
light_t=read_dict['light_t']

read_dict2=np.load('cf.npy').item()
cf_t=read_dict2['cf_t']
time_t=read_dict2['time_t']
ticks=np.arange(len(time_t))
#labels=np.asarray(time_t[::2])
labels=[" " for x in range(len(time_t))]
for x in range(0,len(time_t),2):
	labels[x]=time_t[x]

#dates=time_t
#x = [dt.datetime.strptime(d,'%y/%m').date() for d in dates]
x=ticks
color_sq=['#1f77b4','#aec7e8', '#ff7f0e']
#exit()

with plt.style.context('fivethirtyeight'):
    plt.plot(x, light_t,color=color_sq[0])
    plt.plot(x, ct_t,color=color_sq[1])
    plt.plot(x, cf_t,color=color_sq[2])

plt.xticks(ticks,labels)

plt.text(20, 30,'light', fontsize=14, color=color_sq[0])
plt.text(20, 27,'count', fontsize=14, color=color_sq[1])
plt.text(20, 24,'cloud', fontsize=14, color=color_sq[2])

#print(light_t)
#print(ct_t)
#line, = plt.plot(x, y, '--', linewidth=2)

plt.show()

