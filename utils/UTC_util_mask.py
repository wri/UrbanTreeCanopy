import numpy as np
import UTC_util_raster
import gdal
import rasterio as rio

def mask_ndvi(params, tile, save_tile=False):
    
    data_path = params['data_path']
    tile_size = params['tile_size']
    tile_pad = params['tile_pad']
    imgtype = params['imgtype']
    imageryID = params['imageryID']
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
    source[source==255] = np.nan
    
    red = source[0]
    nir = source[3]
    ndvi = (source[3]-source[0])/(source[3]+source[0])
    
    veg = np.ma.masked_greater(ndvi, veg_threshold)
    vegop = np.ma.masked_less(ndvi, veg_threshold)
    vegmask = veg.mask
    vegmaskop = vegop.mask
    
    try:
        vegshp = veg.mask.shape
        vegshp[0] == tile_size
    except:
        vegmask = np.full((tile_size, tile_size), False)
        vegmaskop = np.full((tile_size, tile_size), False)
        
    if save_tile == True:
        out_path = data_path+imgtype+'/masks'+'/'+imageryID+'_maskVeg-'+str(veg_threshold)+\
        '_tile'+str(x).zfill(zfill)+'.tif'
        UTC_util_raster.write_1band_geotiff(out_path, veg.mask, out_geo, out_prj)      

    return out_prj, out_geo, vegmask, vegmaskop 


def mask_lidar_classes(params, mean, tile, vegmaskop, out_geo, out_prj, 
                       save_tile=False, composite_mask=True):
    
    place = params['place']
    data_path = params['data_path']
    tile_size = params['tile_size']
    tile_pad = params['tile_pad']
    imgtype = params['imgtype']
    imgsource = params['imgsource']
    imageryID = params['imageryID']
    lidarID = params['lidarID']
    suffix = params['suffix']
    zfill = params['zfill']
    threshold_s = params['threshold_s'] 
    threshold_m = params['threshold_m'] 
    threshold_l = params['threshold_l']
    vegtrsh = params['veg_threshold']
    resolution = params['resolution']
    binary_threshold = params['binary_threshold']
    masktype = params['masktype']
    
    thresholds = str(threshold_s)+str(threshold_m)+str(threshold_l)

    LTree = np.ma.masked_greater(mean, threshold_l)
    MTree = np.ma.masked_inside(mean, threshold_m, threshold_l)
    STree = np.ma.masked_inside(mean, threshold_s, threshold_m)
    shrub = np.ma.masked_less(mean, threshold_s)

    elvcat = np.zeros((tile_size, tile_size), dtype= int)
    elvcat[LTree.mask] = 4
    elvcat[MTree.mask] = 3
    elvcat[STree.mask] = 2
    elvcat[shrub.mask] = 1
    
    if save_tile: #saves elevation mask 
        output_raster = data_path+'elevation/masks'+'/'+lidarID+'_maskElv-class'+\
        thresholds+'_tile'+str(tile).zfill(zfill)+'.tif'
        print (output_raster)
        UTC_util_raster.write_1band_geotiff(output_raster, elvcat, out_geo, out_prj)
    
    if composite_mask: #computes and saves a composite mask (veg+elv)
        composite = np.zeros((tile_size, tile_size), dtype=int)
        composite = elvcat
        composite[vegmaskop] = 0

        output_path = data_path+'fullMasks'+'/'+masktype+'/'+place+'_'+imgsource+'_'+suffix+'_'+str(resolution)+\
        'm_p'+str(tile_pad)+'_T'+thresholds+'_tile'+str(tile).zfill(zfill)+'.tif'
        print (output_path)
        UTC_util_raster.write_1band_geotiff(output_path, composite, out_geo, out_prj)
        
        
def mask_lidar_binary(params, mean, tile, vegmask, out_geo, out_prj,
                      save_tile=False, composite_mask=True):
    
    place = params['place']
    data_path = params['data_path']
    tile_size = params['tile_size']
    tile_pad = params['tile_pad']
    imgtype = params['imgtype']
    imgsource = params['imgsource']
    imageryID = params['imageryID']
    lidarID = params['lidarID']
    suffix = params['suffix']
    zfill = params['zfill']
    threshold_s = params['threshold_s'] 
    threshold_m = params['threshold_m'] 
    threshold_l = params['threshold_l']
    vegtrsh = params['veg_threshold']
    resolution = params['resolution']
    binary_threshold = params['binary_threshold']
    masktype = params['masktype']

    elvcat = np.zeros((tile_size, tile_size), dtype= int)
    elv = np.ma.masked_greater(mean, binary_threshold)
    elvcat[elv.mask] = 1
    
    if save_tile: #saves elevation mask 
        output_raster = data_path+'elevation/masks'+'/'+lidarID+'_maskElv-binary'+str(binary_threshold)+'_tile'+str(tile).zfill(zfill)+'.tif'
        print (output_raster)
        UTC_util_raster.write_1band_geotiff(output_raster, elvcat, out_geo, out_prj)
        
    if composite_mask: #computes and saves a composite mask (veg+elv)
        composite = np.logical_and(vegmask,elvcat)
        
        output_path = data_path+'fullMasks'+'/'+masktype+'/'+place+'_'+imgsource+'_'+suffix+'_'+str(resolution)+\
        'm_p'+str(tile_pad)+'_bi'+str(binary_threshold)+'_tile'+str(tile).zfill(zfill)+'.tif'
        print (output_path)
        UTC_util_raster.write_1band_geotiff(output_path, composite, out_geo, out_prj)

        
def mask_lidar_continuous(params, mean, tile, vegmaskop,out_geo, out_prj, 
                          composite_mask=True):
    
    place = params['place']
    data_path = params['data_path']
    tile_size = params['tile_size']
    tile_pad = params['tile_pad']
    imgtype = params['imgtype']
    imgsource = params['imgsource']
    imageryID = params['imageryID']
    lidarID = params['lidarID']
    suffix = params['suffix']
    zfill = params['zfill']
    threshold_s = params['threshold_s'] 
    threshold_m = params['threshold_m'] 
    threshold_l = params['threshold_l']
    vegtrsh = params['veg_threshold']
    resolution = params['resolution']
    binary_threshold = params['binary_threshold']
    masktype = params['masktype']

    if composite_mask: #computes and saves a composite mask (veg+elv)
        composite = np.ma.array(mean, mask=vegmaskop, fill_value=-9999)

        output_path = data_path+'fullMasks'+'/'+masktype+'/'+place+'_'+imgsource+'_'+suffix+'_'+str(resolution)+\
        'm_p'+str(tile_pad)+'_cont'+'_tile'+str(tile).zfill(zfill)+'.tif'
        print (output_path)
        UTC_util_raster.write_1band_geotiff(output_path, composite.filled(), out_geo, out_prj, data_type=gdal.GDT_Float32)
     
        
def mask_lidar(params, tile, out_prj, out_geo, vegmask, vegmaskop):
    
    place = params['place']
    data_path = params['data_path']
    tile_size = params['tile_size']
    tile_pad = params['tile_pad']
    imgtype = params['imgtype']
    imgsource = params['imgsource']
    imageryID = params['imageryID']
    lidarID = params['lidarID']
    suffix = params['suffix']
    zfill = params['zfill']
    threshold_s = params['threshold_s'] 
    threshold_m = params['threshold_m'] 
    threshold_l = params['threshold_l']
    vegtrsh = params['veg_threshold']
    resolution = params['resolution']
    binary_threshold = params['binary_threshold']
    masktype = params['masktype']
    
    
    input_lidar = data_path+'elevation/raster'+'/'+lidarID+'_tile'+str(tile).zfill(zfill)+'.tif'
    
    with rio.open(input_lidar) as src:
            source0 = src.read()
    source = source0.astype(float)
    source[source==-9999] = np.nan
    mean = source[0]

    if source.shape[1]!=tile_size:
        print ("in bad shape! Tile" + str(tile))
    else:
        pass
    
    if masktype == 'class':
        mask_lidar_classes(params, mean, tile, vegmaskop, out_geo, out_prj, 
                       save_tile=False, composite_mask=True)
    
    elif masktype == 'binary':
        mask_lidar_binary(params, mean, tile, vegmask, out_geo, out_prj,
                      save_tile=False, composite_mask=True)
    
    elif masktype == 'continuous':
        mask_lidar_continuous(params, mean, tile, vegmaskop,out_geo, out_prj, 
                          composite_mask=True)

def get_output_path(params):
    
    place = params['place']
    data_path = params['data_path']
    tile_size = params['tile_size']
    tile_pad = params['tile_pad']
    imgtype = params['imgtype']
    imgsource = params['imgsource']
    imageryID = params['imageryID']
    lidarID = params['lidarID']
    suffix = params['suffix']
    zfill = params['zfill']
    threshold_s = params['threshold_s'] 
    threshold_m = params['threshold_m'] 
    threshold_l = params['threshold_l']
    vegtrsh = params['veg_threshold']
    resolution = params['resolution']
    binary_threshold = params['binary_threshold']
    masktype = params['masktype']
    
    if masktype == 'class':
        thresholds = str(threshold_s)+str(threshold_m)+str(threshold_l)
        output_path = data_path+'fullMasks'+'/'+masktype+'/'+place+'_'+imgsource+'_'+suffix+'_'+str(resolution)+\
        'm_p'+str(tile_pad)+'_T'+thresholds
        return output_path
    
    elif masktype == 'binary':
        output_path = data_path+'fullMasks'+'/'+masktype+'/'+place+'_'+imgsource+'_'+suffix+'_'+str(resolution)+\
        'm_p'+str(tile_pad)+'_bi'+str(binary_threshold)
        return output_path
    
    elif masktype == 'continuous':
        output_path = data_path+'fullMasks'+'/'+masktype+'/'+place+'_'+imgsource+'_'+suffix+'_'+str(resolution)+\
        'm_p'+str(tile_pad)+'_cont'
        return output_path