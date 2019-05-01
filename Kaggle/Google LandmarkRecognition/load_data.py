import numpy as np
import pandas as pd
from collections import namedtuple

TRAIN_FILE='train.csv'
TEST_FILE='test.csv'

dataset_=namedtuple('dataset_', ['image', 'label'])

def load_data(normalize=True):
    train_df=pd.read_csv('train.csv')
    test_df=pd.read_csv('test.csv')
    train_df=dataset_(np.array(train_df.loc[:, 'pixel0':'pixel783']).reshape((-1, 28, 28, 1)), np.array(train_df.loc[:, 'label']))
    test_df=dataset_(np.array(test_df.loc[:, 'pixel0':'pixel783']).reshape((-1, 28, 28, 1)), np.zeros(shape=test_df.shape[0]))
    return (train_df, test_df)
    
    
