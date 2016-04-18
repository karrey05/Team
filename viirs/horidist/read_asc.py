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

files = glob.glob('/media/Disk3T/Team/dwu/viirs/data/subset_gd/rade9/*asc')
#fname = '/home/di/viirs/data/SVDNB_npp_20151201-20151231_00N060W_vcmcfg_v10_c201601251413.avg_rade9.tif'

for f in files:
	fname = f
	print(f)

	temp=fname.split('_')
	time=temp[3]
	#time='20151201-20151231'
	ftype='light'
	outpath='/media/Disk3T/Team/dwu/viirs/img/subset_gd/'
	outname=outpath+ftype+'_'+time+'_sub_org.png'

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

	ll_lon = 100
	ll_lat = 20
	ur_lon = 135
	ur_lat = 40

	lat1=ll_lat+(ur_lat-ll_lat)/3.
	lat2=ll_lat+(ur_lat-ll_lat)/3.*2
	stand_lon=ll_lon+(ur_lon-ll_lon)/2.

	#map = Basemap(projection='llc', lat_1=lat1, lat_2=lat2, lon_0=stand_lon, llcrnrlon=ll_lon,\
	#llcrnrlat=ll_lat,urcrnrlon=ur_lon,urcrnrlat=ur_lat,resolution='l')
	#map = Basemap(width=12000,height=7000,projection='lcc', \
	#       lat_1=lat1, lat_2=lat2, lat_0=stand_lat, lon_0=stand_lon,resolution='l')
	map=Basemap(projection='merc',llcrnrlat=yllcorner,urcrnrlat=yurcorner, \
			llcrnrlon=xllcorner, urcrnrlon=xurcorner, lat_ts=20, resolution='h')
	x, y = map(lons, lats)
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

	na_index=np.where(data<10)
	data[na_index]=float('nan')

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
	levs=[30,32,34,36,38,40,50,60,100,500]
	cs = map.contourf(x,y,data,levs,norm=colors.LogNorm(),cmap=cm.Oranges_r,zorder=10)
	#cs = map.contourf(x,y,data,levs,norm=colors.LogNorm(10, vmax=1e5),cmap=cm.Oranges_r,zorder=10)
	#cs = map.pcolor(x,y,data,norm=colors.LogNorm(vmin=data.min(),vmax=data.max()),cmap=cm.Oranges_r,zorder=10)
	#cs = map.pcolor(x,y,data,norm=colors.LogNorm(vmin=1,vmax=1e5),cmap=cm.Oranges_r,zorder=10)
	#cs = map.contourf(x,y,data,locator=ticker.LogLocator(),cmap=cm.Oranges_r,zorder=10)
	#cs = map.contourf(x,y,data,levs,norm=colors.LogNorm(10, vmax=1e2),cmap=cm.gray,zorder=10)
	### uneven bounds (all orange)
	#bounds=np.array([0,10,20,30,40,50,60,70,80,90,100,1000])
	#norm = colors.BoundaryNorm(boundaries=bounds, ncolors=256)
	#cs = map.pcolormesh(x,y,data,norm=norm,vmin=10,cmap=cm.Oranges_r,zorder=10)
	


	bar=plt.colorbar(cs)

	#plt.show()

	figure=plt.gcf()
	#figure.set_size_inches(12,8)
	figure.suptitle(time,fontsize=14, fontweight='bold')

	figure.savefig(outname,format='png',dpi=100)
	plt.close()
	
	del cs
	del map
	del x
	del y
	del lons
	del lats
	del data
	gc.collect()
	#subplot_kw = dict(projection=projection)
	#fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=subplot_kw)
	#fig, ax = plt.subplots(figsize=(9, 9))

	#extent = (gt[0], gt[0] + ds.RasterXSize * gt[1],
	#          gt[3] + ds.RasterYSize * gt[5], gt[3])

	#img = ax.imshow(data[:3, :, :].transpose((1, 2, 0)), extent=extent,
	#                origin='upper')
	#print data
	#img = ax.imshow(data, origin='upper')
	#plt.show()
