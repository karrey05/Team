from osgeo import gdal, osr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from matplotlib import colors, ticker
from colorbar import nlcmap                             #Loads module containing the non-linear colorbar
from matplotlib.colors import LinearSegmentedColormap   #Loads a module allowing for colors in colormaps to be obtained
from mpl_toolkits.basemap import Basemap, addcyclic     #Loads mapping data
import matplotlib.ticker as mpltick             #Load a script that allows for adjustments to colorbar ticks
import matplotlib as mpl                                #Loads map plotting library
import numpy as np                                      #Loads functions for array, linear algebra, array operations


gdal.UseExceptions()

#fname = '/home/di/viirs/data/SVDNB_npp_20151201-20151231_00N060W_vcmcfg_v10_c201601251413.avg_rade9.tif'
fname = '/media/Disk3T/Team/dwu/viirs/data/SVDNB_npp_20140101-20140131_75N060E_vcmcfg_v10_c201506171538.avg_rade9.tif'

ds = gdal.Open(fname)
data = ds.ReadAsArray()
gt = ds.GetGeoTransform()
#proj = ds.GetProjection()

#inproj = osr.SpatialReference()
#inproj.ImportFromWkt(proj)

xorig = gt[0]
yorig = gt[3]
cellsizex = gt[1]
cellsizey = gt[5]

ncols=ds.RasterXSize
nrows=ds.RasterYSize

#description=ds.GetDescription()
#band_num=raster.RasterCount
#banda=raster.GetRasterBand(1)
#BlockSize=banda.GetBlockSize()
#DataType  = gdal.GetDataTypeName(banda.DataType)
#Metadata = banda.GetMetadata()
#print(inproj)

ds=None

#projcs = inproj.GetAuthorityCode('PROJCS')
#projection = ccrs.epsg(projcs)
#print(projection)

xend = xorig+(ncols)*cellsizex
yend = yorig+(nrows)*cellsizey

if xorig < xend:
	xllcorner=xorig
	xurcorner=xend
else:
	xllcorner=xend
	xurcorner=xorig

if yorig < yend:
        yllcorner=yorig
        yurcorner=yend
else:
        yllcorner=yend
        yurcorner=yorig

#lon0=np.arange(xllcorner,xurcorner,abs(cellsizex))
#lat0=np.arange(yllcorner,yurcorner,abs(cellsizey))
lon0=np.arange(xorig,xend,cellsizex)
lat0=np.arange(yorig,yend,cellsizey)
lons, lats = np.meshgrid(lon0, lat0)

#---------- nonlinear color map ---------------
cmap=np.array([  [0.0/255.0,   0.0/255.0, 0.0/255.0],\
                 [255.0/255.0, 255.0/255.0, 255.0/255.0],\
                 [255.0/255.0, 255.0/255.0, 255.0/255.0],\
                 [255.0/255.0, 255.0/255.0, 255.0/255.0],\
                 [255.0/255.0, 255.0/255.0, 255.0/255.0],\
                 [255.0/255.0, 255.0/255.0, 255.0/255.0],\
                 [255.0/255.0, 255.0/255.0, 255.0/255.0],\
                 [255.0/255.0, 255.0/255.0, 255.0/255.0],\
                 [255.0/255.0, 255.0/255.0, 255.0/255.0],\
                 [255.0/255.0, 255.0/255.0, 255.0/255.0],\
                 [255.0/255.0, 255.0/255.0, 255.0/255.0],\
                 [255.0/255.0, 255.0/255.0, 255.0/255.0],\
                 [255.0/255.0, 255.0/255.0, 255.0/255.0]])


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

map = Basemap(projection='lcc', lat_1=lat1, lat_2=lat2, lon_0=stand_lon, llcrnrlon=ll_lon,\
llcrnrlat=ll_lat,urcrnrlon=ur_lon,urcrnrlat=ur_lat,resolution='l')
#map = Basemap(width=12000,height=7000,projection='lcc', \
#       lat_1=lat1, lat_2=lat2, lat_0=stand_lat, lon_0=stand_lon,resolution='l')
x, y = map(lons, lats)
# draw map boundary
map.drawmapboundary(fill_color="darkblue")
map.fillcontinents(color='black',lake_color='darkblue')
map.drawcoastlines()
# draw graticule (latitude and longitude grid lines)
map.drawmeridians(np.arange(0,360,30),color="0.9")
map.drawparallels(np.arange(-90,90,30),color="0.9")

#lev_exp = np.arange(30,np.ceil(np.log10(data.max())+1))
#levs = np.power(10, lev_exp)

levs=[30,32,34,36,38,40,50,60,100,500000]
#f len(levs) < len(cmap):
#   cmap = cmap[0:len(levs),:]

cm = mpl.colors.ListedColormap(cmap)    # First create a linear colormap
map_nonlin = nlcmap(cm, levs)          # Adjust colormap to be non-linear

#levs=[30,500000,10e10]
#levs=[30]
#levs=[10,100,200,300,500,600,1000,50000]
#cmap = plt.get_cmap('Greys_r')
#norm = colors.BoundaryNorm(levs, ncolors=cmap.N, clip=True)
#cs = map.pcolor(x,y,data,cmap=cmap,norm=norm)
cs = map.contourf(x,y,data,levs,cmap=map_nonlin,extend="both")
# draw blue marble image in background.
# (downsample the image by 50% for speed)
#map.bluemarble(scale=0.5)
bar=plt.colorbar(cs)
# Modifies colorbar ticks to match flevs and adds additional labels (where needed)
tick_locs=levs
tick_labels=levs
bar.locator = mpltick.FixedLocator(tick_locs)
bar.formatter = mpltick.FixedFormatter(tick_labels)
bar.update_ticks()

plt.show()

figure=plt.gcf()
figure.set_size_inches(8,6)

figure.savefig('lights3.png',format='png',dpi=100)
plt.close()


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
