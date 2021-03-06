import fiona
import matplotlib.pyplot as plt
import shapely.geometry
import cartopy
import descarteslabs as dl



def info_studyareas(data_path, place):
    # NYU AoUE Study Region shape
    #print(place, place.title())# capitalized version of place name
    place_title = place.title()

    place_shapefile = data_path+place_title+"_studyArea.shp"
    command = 'ogrinfo -al -so {0}'.format(place_shapefile)   # the command goes here
    print('>>>',command)
#     print(subprocess.check_output(command.split(), shell=False))
    
    #!ogrinfo -al -so $ZINSHPNAME
    place_shapefile = data_path+place_title+"_studyAreaEPSG4326.shp"
    command = 'ogrinfo -al -so {0}'.format(place_shapefile)   # the command goes here
    print('>>>',command)
#     print(subprocess.check_output(command.split(), shell=False))
    # !ogr2ogr -t_srs EPSG:4326 $ZOUTSHPNAME $ZINSHPNAME  # First time only
    return


def load_shape(place_shapefile):
    c = fiona.open(place_shapefile)
    pol = c.next()
    shape = {}
    shape['type'] = pol['type']
    shape['properties'] = pol['properties']
    shape['geometry'] = {}
    shape['geometry']['type'] = 'Polygon'  # pol['geometry']['type']
    shape['geometry']['coordinates'] = [[]]
    # if MultiPolygon (e.g., city='kampala')
    if (len(pol['geometry']['coordinates'])>1):
        # identify largest single polygon
        print("MultiPolygon", len(pol['geometry']['coordinates']))
        p_argmax = 0 
        pn_max = 0
        for p in range(len(pol['geometry']['coordinates'])):
            pn = len(pol['geometry']['coordinates'][p][0])
            if pn>pn_max:
                p_argmax = p
                pn_max = pn
            print(p, pn, p_argmax, pn_max)
        # make largest polygon the only polygon, move other polys to a backup variable 
        polygon = pol['geometry']['coordinates'][p_argmax]
    else:
        print('simple polygon')
        polygon = pol['geometry']['coordinates']
       
    xmin =  180
    xmax = -180
    ymin =  90
    ymax = -90
    for x,y in polygon[0]:
        xmin = xmin if xmin < x else x
        xmax = xmax if xmax > x else x
        ymin = ymin if ymin < y else y
        ymax = ymax if ymax > y else y
        shape['geometry']['coordinates'][0].append([x,y])
    shape['bbox'] = [xmin,ymin,xmax,ymax]
    
    return shape


def draw_tiled_area(shape, tiles, projection, lonlat_crs, highlights={0:'black'}, figdim=8):
    print('number of tiles to cover region', len(tiles['features']))
#     print(tiles['features'][0].keys())

    fig = plt.figure(figsize=(figdim, figdim))
    ax = plt.subplot(projection=projection) # Specify projection of the map here

    # Get the geometry from each feature
    shapes = [shapely.geometry.shape(tile_j['geometry']) for
              tile_j in tiles['features']]

    ax.add_geometries(shapes, lonlat_crs, color='orange', alpha=0.3)

    ax.add_geometries([shapely.geometry.shape(shape['geometry'])],
                       lonlat_crs, color='blue', alpha=0.7)
    
    for key, value in highlights.items():
        tile = tiles['features'][key]
        ax.add_geometries([shapely.geometry.shape(tile['geometry'])],
                       lonlat_crs, color=value, alpha=0.5)
#         print('tile'+str(key).zfill(3), tile['geometry'])

    # Get a bounding box of the combined scenes
    union = shapely.geometry.MultiPolygon(polygons=shapes)
    ax.set_extent((union.bounds[0], union.bounds[2], union.bounds[1], union.bounds[3]), crs=lonlat_crs)
    ax.gridlines(crs=lonlat_crs)
    plt.show()
    
    
def get_tiles(shape, tile_resolution, tile_size, tile_pad):

    polygon = shape['geometry']['coordinates']
    # print(polygon)
    # pprint(shape)
    place_bbox = shape['bbox']
    # print(place_bbox)

    # using Albers projection
    lonlat_crs = cartopy.crs.PlateCarree()
    clat, clon = (place_bbox[0]+place_bbox[2])/2.0, (place_bbox[1]+place_bbox[3])/2.0
    print("center co-ordinates", clat, clon)
    # albers = cartopy.crs.AlbersEqualArea(central_latitude=clat, central_longitude=clon)
    albers = cartopy.crs.AlbersEqualArea()


    # visualize Study Region
    fig = plt.figure(figsize=(6,6))
    ax = plt.subplot(projection=albers) # Specify projection of the map here
    shp = shapely.geometry.shape(shape['geometry'])
    ax.add_geometries([shp], lonlat_crs)
    ax.set_extent((place_bbox[0], place_bbox[2], place_bbox[1], place_bbox[3]), crs=lonlat_crs)
    ax.gridlines(crs=lonlat_crs)
#     plt.show()
    
    tiles = dl.raster.dltiles_from_shape(tile_resolution, tile_size, tile_pad, shape)
    single_tile_id = 4
    highlights = {single_tile_id:'green'}
    draw_tiled_area(shape, tiles, albers, lonlat_crs, highlights=highlights)
    
    return tiles

def draw_shp(data_root, place, figdim=8): 
    print(place, place.title()) # capitalized version of place name
    place_title = place.title()
    # place_shapefile = data_path+place_title+"_studyAreaEPSG4326.shp"
    place_shapefile = data_root+place+'/shp/'+place+'_studyAreaEPSG4326.shp'
    # place_shapefile = '/data/phase_iv/hyderabad/Hyderabad_studyArea.shp'

    # UTC_util_shp.info_studyareas(data_path, place)

    shape = load_shape(place_shapefile)
    polygon = shape['geometry']['coordinates']
    # print(polygon)
    # pprint(shape)
    place_bbox = shape['bbox']
    # print(place_bbox)

    # using Albers projection
    lonlat_crs = cartopy.crs.PlateCarree()
    clat, clon = (place_bbox[0]+place_bbox[2])/2.0, (place_bbox[1]+place_bbox[3])/2.0
    print("center co-ordinates", clat, clon)
    # albers = cartopy.crs.AlbersEqualArea(central_latitude=clat, central_longitude=clon)
    albers = cartopy.crs.AlbersEqualArea()


    # visualize Study Region
    fig = plt.figure(figsize=(figdim,figdim))
    ax = plt.subplot(projection=albers) # Specify projection of the map here
    shp = shapely.geometry.shape(shape['geometry'])
    ax.add_geometries([shp], lonlat_crs)
    ax.set_extent((place_bbox[0], place_bbox[2], place_bbox[1], place_bbox[3]), crs=lonlat_crs)
    ax.gridlines(crs=lonlat_crs)
    plt.show()
    return shape, albers, lonlat_crs, place_shapefile