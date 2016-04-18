import matplotlib.pyplot as plt
from matplotlib import colors, ticker, cm
import matplotlib as mpl                                #Loads map plotting library
import numpy as np                                      #Loads functions for array, linear algebra, array operations
import glob
import gc
import datetime as dt
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
#import json

dbox=0.05
read_dict=np.load('city_lights_'+str(dbox)+'.npy').item()
ct_t=read_dict['ct_t']
light_t=read_dict['light_t']
city=read_dict['cities']
city=['Ordos','Dongsheng']

time_t=read_dict['time_t']
ticks=np.arange(len(time_t))

read_dict=np.load('city_cloudcount_'+str(dbox)+'.npy').item()
cloud_t=read_dict['cloudcount_t']

#labels=np.asarray(time_t[::2])
labels=[" " for x in range(len(time_t))]
for x in range(0,len(time_t),2):
	labels[x]=time_t[x]
#dates=time_t
#x = [dt.datetime.strptime(d,'%y/%m').date() for d in dates]
x=ticks
color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                  '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                  '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                  '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5']

fig, ax = plt.subplots(1, 1, figsize=(14, 6))

# Remove the plot frame lines. They are unnecessary here.
ax.spines['top'].set_visible(False)
#ax.spines['bottom'].set_visible(False)
ax.spines['right'].set_visible(False)
#ax.spines['left'].set_visible(False)

# Ensure that the axis ticks only show up on the bottom and left of the plot.
# Ticks on the right and top of the plot are generally unnecessary.
ax.get_xaxis().tick_bottom()
ax.get_yaxis().tick_left()

ax.get_xgridlines()

plt.xlim(0,28)

#with plt.style.context('fivethirtyeight'):
#plt.plot(x, light_t,lw=2.5,color=color_sq[0])
#plt.plot(x, ct_t,lw=2.5,color=color_sq[1])
#plt.plot(x, cf_t,lw=2.5,color=color_sq[2])

# Remove the tick marks; they are unnecessary with the tick lines we just
# plotted.
plt.tick_params(axis='both', which='both', bottom='off', top='off',
                labelbottom='on', left='off', right='off', labelleft='on')

#for ii in city:
#	y_pos.append(ct_t[ii][-1])
y_max=np.max([ct_t[ii] for ii in city])
dy=0.05*y_max
y_pos=y_max-np.arange(len(city))*dy

for c in range(len(city)):
	value=np.asarray(ct_t[city[c]])
	cloud=np.asarray(cloud_t[city[c]])
        index=(cloud > 10)
	#value_mask=ma.masked_array(value,mask=index)
	
	plt.plot(x[index], value[index],lw=2.5,color=color_sequence[c])
	#plt.plot(x, ct_t[city[c]],lw=2.5,color=color_sequence[c])
	plt.text(25, y_pos[c],city[c], fontsize=14, fontweight='bold',color=color_sequence[c])
	#plt.text(25, y_pos,city[c], fontsize=14, fontweight='bold',color=color_sequence[c])

# Remove the tick marks; they are unnecessary with the tick lines we just
# plotted.
plt.tick_params(axis='both', which='both', bottom='off', top='off',
                labelbottom='on', left='off', right='off', labelleft='on')

plt.xticks(ticks,labels)

#plt.text(20, 30,'light', fontsize=14, fontweight='bold',color=color_sq[0])
#plt.text(20, 27,'count', fontsize=14, fontweight='bold',color=color_sq[1])
#plt.text(20, 24,'cloud', fontsize=14, fontweight='bold',color=color_sq[2])
#print(light_t)
#print(ct_t)
#line, = plt.plot(x, y, '--', linewidth=2)

#plt.show()

figure=plt.gcf()
outname='./city_light_count_'+str(dbox)+'_new.png'
figure.savefig(outname,format='png',dpi=100)
plt.close()

