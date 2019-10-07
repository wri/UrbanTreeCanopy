import json
import matplotlib.pyplot as plt
import pdal
import pyproj
import shapely.geometry
import timeit
import cartopy

etpepsg = pyproj.Proj(init='epsg:3857')
wsg84 = pyproj.Proj(init='epsg:4326')
lambert = pyproj.Proj(init='epsg:31370')
cazone = pyproj.Proj(init='epsg:32611')

zfill = 5


def download_lidar(tiles, data_path, place, lsource, resolution, tile_pad, tile_start=0):    
    for x in range(tile_start, len(tiles['features'])):
        tilecoords = tiles['features'][x]['geometry']['coordinates'][0] 
        coords = [pyproj.transform(wsg84,etpepsg,x,y) for (x,y) in tilecoords]
        coords_crop = [pyproj.transform(wsg84,cazone,x,y) for (x,y) in tilecoords]
        polygon = shapely.geometry.Polygon(coords)
        polygon_crop = shapely.geometry.Polygon(coords_crop)
    #     print(polygon)
    #     IPython.display.display(polygon)

        b = polygon.bounds

        tif_path = data_path+'raster/'+place+'_'+lsource+'_'+str(resolution)+'m'+'_'+'p'+str(tile_pad)+'_tile'+str(x).zfill(zfill)+'.tif'

        start_time = timeit.default_timer()
        acquire = {
        "pipeline": [ 
            {   "type": "readers.ept",
                "filename": "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/USGS_LPC_CA_LosAngeles_2016_LAS_2018",
                "spatialreference": 'EPSG:3857',
                "bounds":str(([b[0], b[2]],[b[1], b[3]]))},
            {   "type":"filters.hag"},
            {   "type": "filters.outlier",
                "method": "statistical",
                "multiplier": 3,
                "mean_k": 8},
            {   "type": "filters.range",
                "limits": "Classification![7:7],HeightAboveGround[-3:300]"},
            {   "type":"filters.reprojection",
                "in_srs":"EPSG:3857",
                "out_srs":"EPSG:32611"},
            {   "type":"filters.crop",
                'polygon':polygon_crop.wkt},
            {   "filename": tif_path,
                "dimension":'HeightAboveGround',
                "output_type":"mean",
                "gdaldriver":"GTiff",
                "resolution":"1.0",
                "window_size":"3",
                "type": "writers.gdal"}
        ]}
        pipeline = pdal.Pipeline(json.dumps(acquire))
        pipeline.validate() 
        pipeline.execute()
        elapsed = round((timeit.default_timer() - start_time),2)
        print (tif_path +',  '+ str(elapsed) +'s')

def download_lidar_sample(seed, tiles, data_path, place, lsource, resolution, tile_pad):
    
    randmax = len(tiles['features'])
    num_samps = int(randmax/10)
    random.seed(seed)
    randlist = random.sample(range(0, randmax), num_samps)
    print ('Sample Set: ' + str(len(randlist)))

    # for x in range(len(tiles['features'])):
    for i, x in enumerate(randlist):
        if i%100==0:
            print (i)
        tilecoords = tiles['features'][x]['geometry']['coordinates'][0] 
        coords = [pyproj.transform(wsg84,etpepsg,x,y) for (x,y) in tilecoords]
        coords_crop = [pyproj.transform(wsg84,cazone,x,y) for (x,y) in tilecoords]
        polygon = shapely.geometry.Polygon(coords)
        polygon_crop = shapely.geometry.Polygon(coords_crop)
    #     print(polygon)
    #     IPython.display.display(polygon)

        b = polygon.bounds

        tif_path = data_path+'raster/'+place+'_'+lsource+'_'+str(resolution)+'m'+'_'+'p'+str(tile_pad)+'_tile'+str(x).zfill(zfill)+'.tif'

        start_time = timeit.default_timer()
        acquire = {
        "pipeline": [ 
            {   "type": "readers.ept",
                "filename": "https://s3-us-west-2.amazonaws.com/usgs-lidar-public/USGS_LPC_CA_LosAngeles_2016_LAS_2018",
                "spatialreference": 'EPSG:3857',
                "bounds":str(([b[0], b[2]],[b[1], b[3]]))},
            {   "type":"filters.hag"},
            {   "type": "filters.outlier",
                "method": "statistical",
                "multiplier": 3,
                "mean_k": 8},
            {   "type": "filters.range",
                "limits": "Classification![7:7],HeightAboveGround[-3:300]"},
            {   "type":"filters.reprojection",
                "in_srs":"EPSG:3857",
                "out_srs":"EPSG:32611"},
            {   "type":"filters.crop",
                'polygon':polygon_crop.wkt},
            {   "filename": tif_path,
                "dimension":'HeightAboveGround',
                "output_type":"mean",
                "gdaldriver":"GTiff",
                "resolution":"1.0",
                "window_size":"3",
                "type": "writers.gdal"}
        ]}
        pipeline = pdal.Pipeline(json.dumps(acquire))
        pipeline.validate() 
        pipeline.execute()
        elapsed = round((timeit.default_timer() - start_time),2)
        print (tif_path +',  '+ str(elapsed) +'s')