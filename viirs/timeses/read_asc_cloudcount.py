import matplotlib.pyplot as plt
from matplotlib import colors, ticker, cm
import matplotlib as mpl                                #Loads map plotting library
import numpy as np                                      #Loads functions for array, linear algebra, array operations
import glob
import gc
import datetime
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange
#import json

city=[]
city_lat=[]
city_lon=[]

city.append("Beijing")
city_lat.append(39.907)
city_lon.append(116.397)

city.append("Shanghai")
city_lat.append(31.222)
city_lon.append(121.458)

city.append("Xian")
city_lat.append(34.277) 
city_lon.append(108.948)

city.append("Guangzhou")
city_lat.append(23.15)
city_lon.append(113.25)

city.append("Nanjing")
city_lat.append(32.06)
city_lon.append(118.79)

city.append("Tangshan")
city_lat.append(39.65)
city_lon.append(118.18) 

city.append("Shijiazhuang")
city_lat.append(38.04)
city_lon.append(114.51) 

city.append("Zibo")
city_lat.append(36.83) 
city_lon.append(118.07) 

city.append("Zhengzhou")
city_lat.append(34.75)
city_lon.append(113.63)

city.append("TSfactory")
city_lat.append(39.635)
city_lon.append(118.215)

city.append("Ordos")
city_lat.append(39.605)
city_lon.append(109.787)

city.append("Dongsheng")
city_lat.append(39.815)
city_lon.append(110.015)

dbox=0.05

files = glob.glob('/media/Disk3T/Team/dwu/viirs/data/subset/cf/*asc')
#fname = '/home/di/viirs/data/SVDNB_npp_20151201-20151231_00N060W_vcmcfg_v10_c201601251413.avg_rade9.tif'
files=sorted(files)

cloudcount_t={}
ct_t={}
for c in city:
	cloudcount_t[c]=[]
	ct_t[c]=[]

#cloudcount_t={'Beijing':[],'Shanghai':[],'Xian':[],'Guangzhou':[],'Nanjing':[],'Tangshan':[],'Shijiazhuang':[],'Zibo':[],'Zhengzhou':[]}
time_t=[]
#ct_t={'Beijing':[],'Shanghai':[],'Xian':[],'Guangzhou':[],'Nanjing':[],'Tangshan':[],'Shijiazhuang':[],'Zibo':[],'Zhengzhou':[]}

for f in files:

	fname = f
	print(f)

	temp=fname.split('_')
	temp1=temp[2]
	year=temp1[2:4]
	mon=temp1[4:6]
	time_t.append(year+'/'+mon)
	#time='20151201-20151231'
	ftype='cloudcount'
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
	#cloudcount_t.append(np.mean(data[dd]))
	#ct_t.append(len(data[dd])/1000.)
	
	for c in range(len(city)):
		lon_box=[city_lon[c]-dbox,city_lon[c]+dbox]
		lat_box=[city_lat[c]-dbox,city_lat[c]+dbox]
		id_box=(lons>lon_box[0])&(lons<lon_box[1])&(lats>lat_box[0])&(lats<lat_box[1])
		
		value=np.mean(data[id_box])
		if np.isnan(value):
			cloudcount_t[city[c]].append(0)
		else:
			cloudcount_t[city[c]].append(value)
		ct_t[city[c]].append(len(data[id_box]))
		print(len(data[id_box]))

#fdata={'data':data,'lons':lons,'lats':lats,'cloudcount_t':cloudcount_t,'ct_t':ct_t}
fdata={'cities':city,'time_t':time_t,'cloudcount_t':cloudcount_t,'ct_t':ct_t}

np.save('city_cloudcount_'+str(dbox)+'.npy',fdata)

