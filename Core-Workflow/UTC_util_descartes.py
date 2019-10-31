import os
import matplotlib.pyplot as plt
import descarteslabs as dl

def show_scene(ids, geom={}, resolution=60,
               bands=['red','green','blue','alpha'],
               scales=[[0,3000],[0,3000],[0,3000],None],
               figsize=[16,16], title=""):
    arr, meta = dl.raster.ndarray(
        ids,
        bands=bands,
        scales=scales,
        data_type='Byte',
        resolution=resolution,
        cutline=geom,
    )
    print('shape:', arr.shape)
    # pprint(meta)
    fig = plt.figure(figsize=figsize)
    fig.suptitle(title)
    plt.imshow(arr)
    return