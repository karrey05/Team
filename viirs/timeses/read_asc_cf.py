import matplotlib.pyplot as plt
from matplotlib import colors, ticker, cm
import matplotlib as mpl                                #Loads map plotting library
import numpy as np                                      #Loads functions for array, linear algebra, array operations
import glob
import gc
import datetime
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
#import json

files = glob.glob('/media/Disk3T/Team/dwu/viirs/data/subset_gd/cf/*asc')
#fname = '/home/di/viirs/data/SVDNB_npp_20151201-20151231_00N060W_vcmcfg_v10_c201601251413.avg_rade9.tif'
files=sorted(files)

#files_cf = glob.glob('/media/Disk3T/Team/dwu/viirs/data/subset_gd/cf/*asc')
#files_cf=sorted(files_cf)

time_t=[]
cf_t=[]
for f in files:

	fname = f
	print(f)

	temp=fname.split('_')
	temp1=temp[3]
	year=temp1[2:4]
	mon=temp1[4:6]
	time_t.append(year+'/'+mon)
	#time='20151201-20151231'
	ftype='light'
	#outpath='/media/Disk3T/Team/dwu/viirs/img/subset_gd/'
	#outname=outpath+ftype+'_'+time+'_sub_org.png'

	fi=open(fname,'r')
	header1 = fi.readline()
	header2 = fi.readline()
	header3 = fi.readline()
	header4 = fi.readline()
	header5 = fi.readline()

	temp = header1.strip()
	temp1 = temp.split()
	ncols = int(temp1[1])

	temp = header2.strip()
	temp1 = temp.split()
	nrows = int(temp1[1])

	temp = header3.strip()
	temp1 = temp.split()
	xllcorner = float(temp1[1])

	temp = header4.strip()
	temp1 = temp.split()
	yllcorner = float(temp1[1])

	temp = header5.strip()
	temp1 = temp.split()
	cellsize = float(temp1[1])

	xurcorner = xllcorner+(ncols-1)*cellsize
	yurcorner = yllcorner+(nrows-1)*cellsize
	#lon0=np.arange(xllcorner,xurcorner,cellsize)
	#lat0=np.arange(yllcorner,yurcorner,cellsize)
	lon0=xllcorner+np.arange(ncols)*cellsize
	lat0=yllcorner+np.arange(nrows)*cellsize

	lat0 = lat0[::-1]

	lons, lats = np.meshgrid(lon0, lat0)

	data=[]

	i = 0
	for line in fi:
		i = i+1
		line = line.strip()
		columns = line.split()
		source = np.float_(columns)
		data.append(source)

	fi.close()

	data=np.asarray(data)

	#dd=np.where(data>10)
	cf_t.append(np.mean(data))

fdata={'cf_t':cf_t,'time_t':time_t}
#with open('data.txt','w') as outfile:
#	json.dump(fdata,outfile)

#fdata={'data':data}
np.save('cf.npy',fdata)

#read_dict=np.load('my_file.npy').item()
#data_sav=read_dict['data']

#date1 = datetime.datetime(2014, 1, 1)
#date2 = datetime.datetime(2016, 1, 1)
#delta = datetime.timedelta(weeks=4)
#dates = drange(date1, date2, delta)
exit()
x = range(len(time_t))

with plt.style.context('fivethirtyeight'):
    plt.plot(x, light_t)
    plt.plot(x, ct_t)

print(light_t)
print(ct_t)
#line, = plt.plot(x, y, '--', linewidth=2)

plt.show()

