# Configuration file for the data folders.

from __future__ import print_function
import os
import  pandas as pd
from os.path import join, isdir, basename, isfile
from glob import glob

# Global configuration
DATA_BASE = '/Users/wel/Downloads/webvision_release_sample/'
INFO = join(DATA_BASE, 'info')
DATA_SOURCE = ['google', 'flickr']
TRAIN_FOLDER = join(DATA_BASE, 'train_images_256')
VAL_FOLDER = join(DATA_BASE, 'val_images_256')
TEST_FOLDER = join(DATA_BASE, 'test_images_256')
META_FOLDER = join(DATA_BASE, 'meta')

def _ParseTextFile(filename, columns=None):
    data = pd.read_csv(filename,
                       delim_whitespace=True,
                       header=None)
    if columns:
        data.columns = columns
    return data

def LoadInfo():
    '''
    Load the dataset info from the dataset
    '''
    print ("Loading configuration from %s"%(INFO))
    # Load train file list
    all_train_data = []
    for dataset in DATA_SOURCE:
        # Load training file
        trn = _ParseTextFile(
            join(INFO, 'train_filelist_%s.txt'%(dataset)),
            ['image_id', 'label'])
        print ('Data %s has %d training samples'%(dataset, trn.shape[0]))
        trn['type'] = 'train'
        trn['source'] = dataset
        # Load meta
        meta = _ParseTextFile(join(INFO, 'train_meta_list_%s.txt'%(dataset)),
                              ['meta_path', 'row_number'])
        meta['meta_path'] = meta.meta_path.map(lambda x : join(META_FOLDER, x))
        all_train_data.append(trn.join(meta[['meta_path']]))
    training_df = pd.concat(all_train_data)
    training_df['image_path'] = training_df['image_id'].map(
        lambda x : join(TRAIN_FOLDER, x))
    # Load testing file list
    test_df = _ParseTextFile(
        join(INFO, 'test_filelist.txt'),
        ['image_id'])
    test_df['type'] = 'test'
    test_df['image_path'] = test_df['image_id'].map(
        lambda x : join(TEST_FOLDER, x))
    # Load validation file list
    val_df = _ParseTextFile(
        join(INFO, 'val_filelist.txt'),
        ['image_id', 'label'])
    val_df['type'] = 'val'
    val_df['image_path'] = val_df['image_id'].map(
        lambda x : join(VAL_FOLDER, x))
    data_info =pd.concat([training_df, val_df, test_df])
    return data_info
    
def ValidateIntegrity(info):
    # Validate all files exist
    for _, row in info.iterrows():
        assert isfile(row.image_path), 'Image file does not exist %s'%row.image_path
        if row.type == 'train':
            assert isfile(row.meta_path), 'Meta file does not exist %s'%row.meta_path

    return True
