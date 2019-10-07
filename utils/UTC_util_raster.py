import subprocess
import gdal
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

def crop_raster(cutline, input, output):
   command = 'gdalwarp -q -cutline {0} -of GTiff {1} {2}'.format(cutline, input, output)
   print('>>>',command)
   try:
       s=0
       print(subprocess.check_output(command.split(), shell=False))
   except subprocess.CalledProcessError as e:
       raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
   return

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