# define a class for accessing dataset

from collections import namedtuple
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

class dataset(object):
    tot_mean=0

    def __init__(self, data_in, dtype=np.float32):
        tot_mean=np.mean(np.float32(data_in.image), axis=(0), keepdims=True)
        self.data=np.float32(data_in.image)-tot_mean#mean along width and height axes
        self.label=data_in.label
        self.num_examples=data_in.image.shape[0]
        self.epochs_finished=0
        self.idx_in_epoch=0
        if dtype==np.float32:
            self.data=self.data/255.0
    
    def next_batch(self, batch_size=100, shuffle=True):
        if self.idx_in_epoch==0 and self.epochs_finished==0 and shuffle:
            perm=np.arange(self.num_examples)
            np.random.shuffle(perm)
            self.data=self.data[perm]
            self.label=self.label[perm]

        start=self.idx_in_epoch
        if start+batch_size>self.num_examples:
            self.epochs_finished+=1
            examples_rest=self.num_examples-start
            data_rest=self.data[start:self.num_examples]
            label_rest=self.label[start:self.num_examples]
            examples_new=batch_size-examples_rest
            self.idx_in_epoch=examples_new
            if shuffle:
                perm=np.arange(self.num_examples)
                np.random.shuffle(perm)
                self.data=self.data[perm]
                self.label=self.label[perm]
            start=0
            data_new=self.data[start:examples_new]
            label_new=self.label[start:examples_new]
            return np.concatenate((data_rest, data_new), axis=0),  \
            np.concatenate((label_rest, label_new), axis=0 )
        else:
            self.idx_in_epoch+=batch_size
            return self.data[start:self.idx_in_epoch], self.label[start:self.idx_in_epoch]


def dataset_tt(data_in, dtype=np.float32):
    #train-test split
    data_train=dataset(data_in.train, dtype)
    data_test=dataset(data_in.test, dtype)
    data_tuple_tt=namedtuple('data_tt_tuple', ['train', 'test'])
    data_tt=data_tuple_tt(data_train, data_test)
    return data_tt


def dataset_tvt(data_in, dtype=np.float32):
    #train-val-test split
    data_train=dataset(data_in.train, dtype)
    data_val=dataset(data_in.val, dtype)
    data_test=dataset(data_in.test, dtype)
    data_tuple_tvt=namedtuple('data_tvt_tuple', ['train', 'val', 'test'])
    data_tvt=data_tuple_tvt(data_train, data_val, data_test)
    return data_tvt

def data_aug(image_in):
    in_shape=image_in.shape
    #print('original image 0')
    #plt.imshow(image_in[0])
    #plt.show()
    N_pad=4
    image_cp=np.zeros(image_in.shape, np.float32)
    image_cp[:]=image_in
    for k in range(image_in.shape[0]):
        rnd=np.random.randint(0, 2)
        if(rnd==0):
            image_cp[k, :, :, :]=image_cp[k, :, -1::-1, :]
    image=np.zeros([image_in.shape[0], image_in.shape[1]+2*N_pad, image_in.shape[2]+2*N_pad, image_in.shape[3]], np.float32)
    image[:, N_pad:-N_pad, N_pad:-N_pad, :]=image_cp
    h_idx=np.random.randint(0, 2*N_pad+1)
    w_idx=np.random.randint(0, 2*N_pad+1)
    image_out=image[:, h_idx:h_idx+in_shape[1], w_idx:w_idx+in_shape[2], :]
    #print(h_idx)
    #print(w_idx)
    #print(image_out.shape)
    #print('augmented image 0')
    #plt.imshow(image_out[0])
    #plt.show()
    #image_out=image_cp
    return image_out
