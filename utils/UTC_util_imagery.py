import time
import descarteslabs as dl
import random
import shapely
from shapely.geometry import Polygon

def download_imagery(data_path, place, imgtype, source, bands, shape, tiles, naip1_dict, spot2_dict, plds2_dict, resampler='bilinear', processing_level=None, tile_start=0):
    print (source)
    if source == 'naip1':
        image_dict = naip1_dict
    elif source == 'spot2':
        image_dict = spot2_dict
    elif source == 'plds2':
        image_dict = plds2_dict
    resolution = int(tiles['features'][0]['properties']['resolution'])
    pad   = int(tiles['features'][0]['properties']['pad'])
    zfill = 5

    for suffix, ids in image_dict.items():
        print(suffix, ids)
        for tile_id in range(tile_start, len(tiles['features'])):
            tile = tiles['features'][tile_id]
            try:
                fail_count=0
#                 print (tile)
                basename = data_path+imgtype+'/imagery/'+str(processing_level).lower()+'/'+\
          place+'_'+source+'_'+suffix+'_'+str(resolution)+'m'+'_'+'p'+str(pad)+'_'+'tile'+str(tile_id).zfill(zfill)
                print('downloading tile'+str(tile_id).zfill(zfill)+':', basename+'.tif')
                vir = dl.raster.raster(
                    ids,
                    bands=bands,
                    resampler=resampler,
                    data_type='UInt16',
                    dltile=tile,
                    cutline=shape['geometry'], # how can she cut
                    processing_level=processing_level,
                    save=True,
                    outfile_basename=basename)
            except Exception as e:
                # this should be more specific, so other errors rightfully get raised
                # target error:
                # HTTPSConnectionPool(host='platform.descarteslabs.com', port=443): Max retries exceeded with url: /raster/v1/npz (Caused by ResponseError('too many 503 error responses',))
                print ('Error encountered mapping tile #', tile_id)
                print (e)
                fail_count = fail_count + 1
                if fail_count > 5:
                    break
                else:
                    tile_id = tile_id - 1
                    time.sleep(5)
                    continue
            fail_count = 0
            
def download_imagery_samp(seed, suffix, data_path, place, imgtype, source, bands, shape, tiles, 
                          naip1_dict, spot2_dict, plds2_dict, resampler='bilinear', processing_level=None, tile_start = 0):        
#     print (source)
    if source == 'naip1':
        image_dict = naip1_dict
    elif source == 'spot2':
        image_dict = spot2_dict
    elif source == 'plds2':
        image_dict = plds2_dict
    resolution = int(tiles['features'][0]['properties']['resolution'])
    pad   = int(tiles['features'][0]['properties']['pad'])
    zfill = 5

    randmax = len(tiles['features'])
    num_samps = int(randmax/10)
    random.seed(seed)
    randlist = random.sample(range(0, randmax), num_samps)
    print ('Sample Set: ' + str(len(randlist)))
    
    randlist = randlist[tile_start:]

    for i, tile_id in enumerate(randlist):
        if i%100==0:
            print (i)
        else:
            pass
        tile = tiles['features'][tile_id]
        a = tile['geometry']['coordinates'][0]
        p1 = Polygon(a)
#         print (tile_id)

        for x in image_dict[suffix]:
            metadata = dl.metadata.get(x)
            b = metadata['geometry']['coordinates'][0]
            p2 = Polygon(b)
            within = p1.within(p2)

            if within == False:
                pass
            if within == True:
                basename = data_path+imgtype+'/imagery/'+str(processing_level).lower()+'/'+ place+'_'+source+'_'+\
                suffix+'_'+str(resolution)+'m'+'_'+'p'+str(pad)+'_'+'tile'+str(tile_id).zfill(zfill)
                print('downloading tile'+str(tile_id).zfill(zfill)+':', basename+'.tif')
                vir = dl.raster.raster(
                    x,
                    bands=bands,
                    resampler=resampler,
                    data_type='UInt16',
                    dltile=tile,
                    cutline=shape['geometry'], # how can she cut
                    processing_level=processing_level,
                    save=True,
                    outfile_basename=basename)
                break
                
# def download_imagery_samp(seed, data_path, place, imgtype, source, bands, shape, tiles, naip1_dict, spot2_dict, plds2_dict, resampler='bilinear', processing_level=None):    
#     print (source)
#     if source == 'naip1':
#         image_dict = naip1_dict
#     elif source == 'spot2':
#         image_dict = spot2_dict
#     elif source == 'plds2':
#         image_dict = plds2_dict
#     resolution = int(tiles['features'][0]['properties']['resolution'])
#     pad   = int(tiles['features'][0]['properties']['pad'])
#     zfill = 5

#     randmax = len(tiles['features'])
#     num_samps = int(randmax/10)
#     random.seed(seed)
#     randlist = random.sample(range(0, randmax), num_samps)
                 
#     print (len(randlist))
    
#     for suffix, ids in image_dict.items():
#         print(suffix, ids)
#         for tile_id in randlist:
#             tile = tiles['features'][tile_id]
#             try:
#                 fail_count=0
# #                 print (tile)
#                 basename = data_path+imgtype+'/imagery/'+str(processing_level).lower()+'/'+\
#           place+'_'+source+'_'+suffix+'_'+str(resolution)+'m'+'_'+'p'+str(pad)+'_'+'tile'+str(tile_id).zfill(zfill)
#                 print('downloading tile'+str(tile_id).zfill(zfill)+':', basename+'.tif')
#                 vir = dl.raster.raster(
#                     ids,
#                     bands=bands,
#                     resampler=resampler,
#                     data_type='UInt16',
#                     dltile=tile,
#                     cutline=shape['geometry'], # how can she cut
#                     processing_level=processing_level,
#                     save=True,
#                     outfile_basename=basename)
#             except Exception as e:
#                 # this should be more specific, so other errors rightfully get raised
#                 # target error:
#                 # HTTPSConnectionPool(host='platform.descarteslabs.com', port=443): Max retries exceeded with url: /raster/v1/npz (Caused by ResponseError('too many 503 error responses',))
#                 print ('Error encountered mapping tile #', tile_id)
#                 print (e)
#                 fail_count = fail_count + 1
#                 if fail_count > 5:
#                     break
#                 else:
#                     tile_id = tile_id - 1
#                     time.sleep(5)
#                     continue
#             fail_count = 0
