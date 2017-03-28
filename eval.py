from __future__ import print_function
import config as config
import pandas as pd
import numpy as np

def MergeVal(info, validation_df):
    '''
    Merge with the validation data
    '''
    # The first column is always the image_id
    column = ['image_id', ]
    column.extend(['predicted_%d'%(k) for k in
                   range(len(validation_df.columns)-1)])
    validation_df.columns = column
    # Sanity check the validation has same number of images
    assert len(validation_df.image_id.unique()) == \
        info[info.type == 'val'].shape[0]
    return info.merge(validation_df, on='image_id')

def MergeValFile(info, validation_filename):
    return MergeVal(info,
        config._ParseTextFile(validation_filename))

# Metrics
def TopK(df, top_k, evalset='val'):
    '''
    Eval based on the top K accuracy
    '''
    top_k_columns = ['predicted_%d'%(k) for k in range(top_k)]
    # Calculate the top_k accurarcy
    eval_set = df[df.type == evalset]
    # Check the set label is not null
    assert eval_set.label.isnull().sum() == 0, 'Null value exists in label.'
    label_correct = np.min(
        np.abs((eval_set[top_k_columns].sub(
            eval_set.label, axis='index')).values), axis=1)
    return float(sum(label_correct==0)) / len(label_correct)
    
    
