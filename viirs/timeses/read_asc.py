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

city.append("Xi'an")
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

dbox=0.75

for c in range(len(city)):

	lon_box=[city_lon[c]-dbox,city_lon[c]+dbox]
	lat_box=[city_lat[c]-dbox,city_lat[c]+dbox]

	files = glob.glob('/media/Disk3T/Team/dwu/viirs/data/subset_gd/rade9/*asc')
	#fname = '/home/di/viirs/data/SVDNB_npp_20151201-20151231_00N060W_vcmcfg_v10_c201601251413.avg_rade9.tif'
	files=sorted(files)

	files_cf = glob.glob('/media/Disk3T/Team/dwu/viirs/data/subset_gd/cf/*asc')
	files_cf=sorted(files_cf)

	light_t=[]
	time_t=[]
	ct_t=[]
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
		#light_t.append(np.mean(data[dd]))
		#ct_t.append(len(data[dd])/1000.)

		id_box=(data>10)&(lons>lon_box[0])&(lons<lon_box[1])&(lats>lat_box[0])&(lats<lat_box[1])
		light_t.append(np.mean(data[id_box]))
		ct_t.append(len(data[id_box]))

	#fdata={'data':data,'lons':lons,'lats':lats,'light_t':light_t,'ct_t':ct_t}
	fdata={'light_t':light_t,'ct_t':ct_t}
	#with open('data.txt','w') as outfile:
	#	json.dump(fdata,outfile)

	#fdata={'data':data}
	np.save('my_file.npy',fdata)

#read_dict=np.load('my_file.npy').item()
#data_sav=read_dict['data']

#date1 = datetime.datetime(2014, 1, 1)
#date2 = datetime.datetime(2016, 1, 1)
#delta = datetime.timedelta(weeks=4)
#dates = drange(date1, date2, delta)
#exit()
x = range(len(time_t))

with plt.style.context('fivethirtyeight'):
    plt.plot(x, light_t)
    plt.plot(x, ct_t)

print(light_t)
print(ct_t)
#line, = plt.plot(x, y, '--', linewidth=2)

plt.show()

