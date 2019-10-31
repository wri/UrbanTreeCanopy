import subprocess
import gdal
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import rasterio as rio

def crop_raster(cutline, input, output):
   command = 'gdalwarp -q -cutline {0} -of GTiff {1} {2}'.format(cutline, input, output)
   print('>>>',command)
   try:
       s=0
       print(subprocess.check_output(command.split(), shell=False))
   except subprocess.CalledProcessError as e:
       raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
   return

def combine_rasters(params, tile):
    
    data_path = params['data_path']
    tile_size = params['tile_size']
    tile_pad = params['tile_pad']
    imgtype = params['imgtype']
    imageryID = params['imageryID']
    lidarID = params['lidarID']
    zfill = params['zfill']
    veg_threshold = params['veg_threshold']
    
    input_raster = data_path+imgtype+'/imagery/none'+'/'+imageryID+'_tile'+str(tile).zfill(zfill)+'.tif'
    
    #     establishing proj and georef
    obj = gdal.Open(input_raster, gdal.gdalconst.GA_ReadOnly)
    out_prj = obj.GetProjection()
    out_geo = obj.GetGeoTransform()

    with rio.open(input_raster) as src:
        source0 = src.read()
    source = source0.astype(float)
    source[source==-9999] = np.nan
    red = source[0]
    nir = source[3]
    ndvi = (source[3]-source[0])/(source[3]+source[0])
 
    input_lidar = data_path+'elevation/raster'+'/'+lidarID+'_tile'+str(tile).zfill(zfill)+'.tif'
    
    with rio.open(input_lidar) as src:
            source1 = src.read()
    sourceL = source1.astype(float)
    sourceL[sourceL==-9999] = np.nan
    mean = sourceL[0]

    img = np.array([mean, ndvi])
    if img.shape!=(2,tile_size,tile_size):
        print ('check yo self! tile' + str(tile))
    
    return img, out_geo, out_prj


def write_1band_geotiff(outfile, img, geo, prj, data_type=gdal.GDT_Byte):
    driver = gdal.GetDriverByName('GTiff')
    rows = img.shape[0]
    cols = img.shape[1]
    outds = [ ]
    if (data_type == gdal.GDT_Byte):
        opts = ["INTERLEAVE=BAND", "COMPRESS=LZW", "PREDICTOR=1", "TILED=YES", "BLOCKXSIZE=256", "BLOCKYSIZE=256"]
        outds  = driver.Create(outfile, cols, rows, 1, data_type, options=opts)
    else:
        outds  = driver.Create(outfile, cols, rows, 1, data_type)
    outds.SetGeoTransform(geo)
    outds.SetProjection(prj)
    outband = outds.GetRasterBand(1)
    outband.WriteArray(img)
    del outds

def write_multiband_geotiff(outfile, img, geotrans, prj, data_type=gdal.GDT_Byte):
    driver = gdal.GetDriverByName('GTiff')
    bands = img.shape[0]
    rows = img.shape[1]
    cols = img.shape[2]
    outds = [ ]
    if (data_type == gdal.GDT_Byte):
        opts = ["INTERLEAVE=BAND", "COMPRESS=LZW", "PREDICTOR=1", "TILED=YES", "BLOCKXSIZE=512", "BLOCKYSIZE=512"]
        outds  = driver.Create(outfile, cols, rows, bands, data_type, options=opts)
    else:
        #print(outfile, cols, rows, bands, data_type)
        outds  = driver.Create(outfile, cols, rows, bands, data_type)
    outds.SetGeoTransform(geotrans)
    outds.SetProjection(prj)
    for b in range(bands):
        outds.GetRasterBand(b+1).WriteArray(img[b])
    del outds
    
def plotfig(a, amin, amax):
    fig, ax = plt.subplots(figsize=(8,8))
    ndvi = ax.imshow(a, cmap='Greys', vmin=amin, vmax=amax) 
    fig.colorbar(ndvi,  shrink=0.25)
    ax.set_axis_off()
    plt.show()

def plotfig_adj(a, clrmap = 'Greys'):
    fig, ax = plt.subplots(figsize=(8,8))
    ndvi = ax.imshow(a, cmap=clrmap, vmin=np.nanmin(a), vmax=np.nanmax(a)) 
    fig.colorbar(ndvi,  shrink=0.25)
    ax.set_axis_off()
    plt.show()

def get_bandStats(input_band):
    numNaN = np.isnan(input_band).sum()
    mean = np.nanmean(input_band)
    std = np.nanstd(input_band)
    return mean, std, numNaN