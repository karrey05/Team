from osgeo import gdal, osr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from matplotlib import colors, ticker, cm
from mpl_toolkits.basemap import Basemap, addcyclic     #Loads mapping data
import matplotlib as mpl                                #Loads map plotting library
import numpy as np                                      #Loads functions for array, linear algebra, array operations
from matplotlib.colors import ListedColormap 
import glob
import gc

gdal.UseExceptions()

files = glob.glob('/media/Disk3T/Team/dwu/viirs/data/subset/rade9/*asc')
#fname = '/home/di/viirs/data/SVDNB_npp_20151201-20151231_00N060W_vcmcfg_v10_c201601251413.avg_rade9.tif'

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

for f in files:
	fname = f
	print(f)

	temp=fname.split('_')
	time=temp[2]
	#time=temp[3]
	#time='20151201-20151231'
	ftype='light'
	#outpath='/media/Disk3T/Team/dwu/viirs/img/subset_gd/'
	outpath='./'
	outname=outpath+ftype+'_'+time+'_Ordos.png'
	
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

	#lon=np.asarray(lon)
	#lat=np.asarray(lat)
	data=np.asarray(data)

	#set up map projection with
	# use low resolution coastlines.
	#lat1=yllcorner+(yurcorner-yllcorner)/3.
	#lat2=yllcorner+(yurcorner-yllcorner)/3.*2
	#stand_lon=xllcorner+(xurcorner-xllcorner)/2.

	#ll_lon = -50
	#ll_lat = -20
	#ur_lon = -30
	#ur_lat = 0

	#ll_lon = 100
	#ll_lat = 20
	#ur_lon = 135
	#ur_lat = 40

        #ll_lon = xllcorner
        #ll_lat = yllcorner
        #ur_lon = xurcorner
        #ur_lat = yurcorner
	
	# Tangshan factory
	#ll_lon = 118.21
        #ll_lat = 39.63
        #ur_lon = 118.22
        #ur_lat = 39.64

        ## Tangshan factory
        #ll_lon = 117
        #ll_lat = 38
        #ur_lon = 118
        #ur_lat = 40
	
	# JJT
	ll_lon = 115.885
        ll_lat = 38.747
        ur_lon = 118.999
        ur_lat = 40.503

	#Ordos
	ll_lon = 109.752
        ll_lat = 39.584
        ur_lon = 109.813
        ur_lat = 39.624

	ll_lon = 109.63
        ll_lat = 39.51
        ur_lon = 110.19
        ur_lat = 39.87

	lat1=ll_lat+(ur_lat-ll_lat)/3.
	lat2=ll_lat+(ur_lat-ll_lat)/3.*2
	stand_lon=ll_lon+(ur_lon-ll_lon)/2.

	#map = Basemap(projection='llc', lat_1=lat1, lat_2=lat2, lon_0=stand_lon, llcrnrlon=ll_lon,\
	#llcrnrlat=ll_lat,urcrnrlon=ur_lon,urcrnrlat=ur_lat,resolution='l')
	#map = Basemap(width=12000,height=7000,projection='lcc', \
	#       lat_1=lat1, lat_2=lat2, lat_0=stand_lat, lon_0=stand_lon,resolution='l')
	#map=Basemap(projection='merc',llcrnrlat=yllcorner,urcrnrlat=yurcorner, \
	#		llcrnrlon=xllcorner, urcrnrlon=xurcorner, lat_ts=20, resolution='h')
        map=Basemap(projection='merc',llcrnrlat=ll_lat,urcrnrlat=ur_lat, \
                        llcrnrlon=ll_lon, urcrnrlon=ur_lon, lat_ts=20, resolution='h')
	x, y = map(lons, lats)
	x_city,y_city=map(city_lon,city_lat)
	# draw map boundary
	map.drawmapboundary(fill_color="darkblue")
	map.fillcontinents(color='black',lake_color='darkblue',zorder=1)
	map.drawcoastlines(zorder=20)
	# draw graticule (latitude and longitude grid lines)
	map.drawmeridians(np.arange(0,360,30),color="0.9")
	map.drawparallels(np.arange(-90,90,30),color="0.9")
	#map.drawlsmask(land_color='black', ocean_color='darkblue',lakes=True, resolution='f', grid=1.25)
	#map.bluemarble()
	#lev_exp = np.arange(10,np.ceil(np.log10(data.max())+1))
	#levs = np.power(10, lev_exp)

	#na_index=np.where(data<10)
	#data[na_index]=float('nan')

	#levs=[0,1000,2000,3000,4000,5000,6000,7000]
	#levs=[0,50,100,150,200,250,300,350,400,450,500]	
	#levs=[10,20,30,40,50,60,70,80,90,100]
	#cs = map.contourf(x,y,data,levs,cmap=cm.Greys)
	#cs = map.contourf(x,y,data,levs,cmap=cm.Pastel1_r,zorder=10)
	#cs = map.contourf(x,y,data,levs,cmap=cm.Greys_r,zorder=10)
	#cs = map.contourf(x,y,data,levs,cmap=cm.Oranges_r,zorder=10)
	#cs = map.contourf(x,y,data,levs,norm=colors.LogNorm(1, vmax=1e3),cmap=cm.Greys_r,zorder=10)
	
	#log scale
	#levs=[1,1e1,1e2,1e3]
	#levs=[10,20,30,40,50,60,70,80,90,100,500]
	#levs=[30,32,34,36,38,40,50,60,100,500]
	#cs = map.contourf(x,y,data,levs,norm=colors.LogNorm(),cmap=cm.Oranges_r,zorder=10)
	#cs = map.contourf(x,y,data,levs,norm=colors.LogNorm(10, vmax=1e5),cmap=cm.Oranges_r,zorder=10)
	#cs = map.pcolor(x,y,data,norm=colors.LogNorm(vmin=data.min(),vmax=data.max()),cmap=cm.Oranges_r,zorder=10)
	#cs = map.pcolor(x,y,data,norm=colors.LogNorm(vmin=1,vmax=1e5),cmap=cm.Oranges_r,zorder=10)
	#cs = map.contourf(x,y,data,locator=ticker.LogLocator(),cmap=cm.Oranges_r,zorder=10)
	#cs = map.contourf(x,y,data,levs,norm=colors.LogNorm(10, vmax=1e2),cmap=cm.gray,zorder=10)
	### uneven bounds (all orange)
	#bounds=np.array([0,10,20,30,40,50,60,70,80,90,100,1000])
	#norm = colors.BoundaryNorm(boundaries=bounds, ncolors=256)
	#cs = map.pcolormesh(x,y,data,norm=norm,vmin=10,cmap=cm.Oranges_r,zorder=10)

	# normalize data between 0 to 1
	floor=5.
	ceil=50.
	index=(data>floor)
	data_sub=data[index]
	data_sub[data_sub >ceil]=ceil
	data_nom=(data_sub-np.min(data_sub))/(np.max(data_sub)-np.min(data_sub))
	colors=cm.Oranges_r(data_nom)
	#colors=cm.Greys_r(data_nom)
	
	#map.scatter(x[data>floor],y[data>floor],s=1,marker='o',color=colors,zorder=10)
	map.scatter(x[data>floor],y[data>floor],s=9,marker='o',color=colors,zorder=10)
	#map.scatter(x_city,y_city,s=9,marker='o',color='#1f77b4',zorder=10)
	
	for c in range(len(city)):
		plt.text(x_city[c],y_city[c],city[c],fontsize=14, fontweight='bold',color='#1f77b4',zorder=20)
	#bar=plt.colorbar(cs)

	#plt.show()

	#stop

	figure=plt.gcf()
	figure.set_size_inches(12,8)
	figure.suptitle(time,fontsize=14, fontweight='bold')
	
	figure.savefig(outname,format='png',dpi=100)
	plt.close()
