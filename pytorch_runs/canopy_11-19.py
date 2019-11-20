import os,sys
PROJECT_DIR=f'..'
sys.path.append(PROJECT_DIR)

from pprint import pprint
import pandas as pd

import torch
import torch.nn as nn

import torch_kit.functional as F
from torch_kit.optimizers.radam import RAdam
import pytorch_models.deeplab.model as dm

# from config import DATA, VALUE_MAP, VALUE_MAP_CLASSES, S2_BANDS
# from config import DATA, VALUE_MAP_BUILT_UP, VALUE_MAP_BUILT_UP_CLASSES

from utils.dataloader import UrbanTreeDataset #Changed
# import utils.helpers as h

import pytorch_models.unet.model as um

#
# RUN CONFIG
#
CROPPING=False
FLOAT_CROPPING=18
REGION='all'
RESOLUTION=1 #Changed
TRAIN='train'
VALID='valid'
BATCH_SIZE=8
NB_EPOCHS=50
DEV=False
DEFAULT_OPTIMIZER='adam'
# NB_BANDS=len(S2_BANDS)
# CATEGORIES=[ VALUE_MAP_CLASSES[k]  for k in sorted(VALUE_MAP_CLASSES.keys()) ]
# NB_CATEGORIES=len(CATEGORIES)
# pprint(VALUE_MAP_CLASSES)
# STATS=h.get_aue_data('stats','master_all',typ='s2') #Changed
LRS=[1e-3,1e-4]
NB_CATEGORIES = 1

DATA_ROOT = PROJECT_DIR

#
# UTILS
#


#
# TORCH_KIT CLI
#
def model(**cfig):   
    _header('model',cfig)
    model_type=cfig.pop('type','dlv3p')
    cfig['out_ch']=cfig.get('out_ch',NB_CATEGORIES)
    if model_type=='dlv3p':
        mod=dm.DeeplabV3plus(**cfig)
    elif model_type=='unet':
        mod=um.UNet(**cfig)
    else:
        raise ValueError(f'model_type ({model_type}) not implemented')
    if torch.cuda.is_available():
        mod=mod.cuda()
    return mod


def criterion(**cfig):
    pos_weight=cfig.get('pos_weight')
    if pos_weight:
        pos_weight=torch.Tensor(pos_weight)
        if torch.cuda.is_available():
            pos_weight=pos_weight.cuda()
    criterion=nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    return criterion


def optimizer(**cfig):
    _header('optimizer',cfig)
    opt_name=cfig.get('name',DEFAULT_OPTIMIZER)
    if opt_name=='adam':
        optimizer=torch.optim.Adam
    elif opt_name=='radam':
        optimizer=RAdam
    else:
        ValueError(f'optimizer "{opt_name}" not implemented')
    return optimizer


def loaders(**cfig):
    """
    """
    # INITAL DATASET HANDLING
    train_df=pd.read_csv(f'{DATA_ROOT}/datasets/train.csv')
    valid_df=pd.read_csv(f'{DATA_ROOT}/datasets/valid.csv')
    df = pd.concat([train_df,valid_df]) # combining the train and valid dataset to train due to lack of data
    #
    # on with the show
    #
    dev=cfig.get('dev')
    vmap=cfig.get('vmap')
    batch_size=cfig.get('batch_size',BATCH_SIZE)
    band_indices=['ndvi']
    augment=cfig.get('augment',True)
    shuffle=cfig.get('shuffle',True)
    update_version=cfig.get('update_version',False)

    if (train_df.shape[0]>batch_size*8) and (valid_df.shape[0]>batch_size*2):
        if dev:
            df=df.sample(batch_size*3)
#             train_df=train_df.sample(batch_size*8)
#             valid_df=valid_df.sample(batch_size*2)

        dl_train=UrbanTreeDataset.loader(
            batch_size=batch_size,
            band_indices=band_indices,
            dataframe=df, #train_df
            augment=augment,
            value_map=vmap, 
            train_mode=True,
            target_expand_axis=None,
            UPDATE_VERSION=update_version,
            shuffle_data=shuffle)

        dl_valid=None
#         dl_valid=UrbanTreeDataset.loader(
#             batch_size=batch_size,
#             band_indices=band_indices,
#             dataframe=valid_df,
#             augment=augment,
#             value_map=vmap,
#             train_mode=True,
#             target_expand_axis=None,
#             UPDATE_VERSION=update_version,
#             shuffle_data=shuffle)

        return dl_train, dl_valid
    else:
        print('NOT ENOUGH DATA',train_df.shape[0],valid_df.shape[0],batch_size*8,batch_size*30)
        return False, False

#
# HELPERS
#
def _header(title,cfig=None):
    print('='*100)
    print(title)
    print('-'*100)    
    if cfig:
        pprint(cfig)


