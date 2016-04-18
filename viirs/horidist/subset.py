import os
inDS = '/media/Disk3T/Team/dwu/viirs/data/SVDNB_npp_20140101-20140131_75N060E_vcmcfg_v10_c201506171538.avg_rade9.tif' # input raster
outDS = 'subset.tif' # output raster
lon =  # lon of your flux tower
lat = ... # lat of your flux tower
ulx = lon - 24.5
uly = lat + 24.5
lrx = lon + 24.5
lry = lat - 24.5
translate = 'gdal_translate -projwin %s %s %s %s %s %s' %(ulx, uly, lrx, lry, inDS, outDS)
os.system(translate)
