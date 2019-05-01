import matplotlib.pyplot as plt
import matplotlib.image as img
import pandas as pd
# import cv2
import tensorflow as tf
# import cv2wrap as cv2
import numpy as np


import os

img_dir=['./train', './test']
label_dir='./labels.csv'


class dataset_from_df():
    def __init__(self, df):
        self._df = df.copy()
        self._batch_idx = 0
        self._size = df.shape[0]

    def shuffle(self):
        df_idx = np.arange(self._size)
        np.random.shuffle(df_idx)
        self._df = self._df.iloc[df_idx, :]

    def next_batch(self, batch_size=64):
        next_batch_idx = self._batch_idx + batch_size
        if (next_batch_idx - 1 >= self._size):
            df_part1 = self._df[self._batch_idx:].copy()
            self.shuffle()
            remained = next_batch_idx - self._size
            df_part2 = self._df[0:remained]
            df_total = df_part1.append(df_part2, ignore_index=True)
            self._batch_idx = remained
        else:
            df_total = self._df[self._batch_idx:next_batch_idx].copy()
            self._batch_idx = next_batch_idx
            if (self._batch_idx == self._size):
                self._batch_idx = 0
                self.shuffle()
        return df_total



dog_breeds_map=[]
dog_breeds_demap=[]
IMAGE_SIZE=[224, 224]
dog_breeds=[]
validation_size=0.1
train_images=[]
test_images=[]

def read_img_file():
    global train_images
    global test_images

    train_images=[f for f in os.listdir(img_dir[0]) if os.path.isfile(os.path.join(img_dir[0], f)) and f[-3:]=='jpg']
    test_images=[f for f in os.listdir(img_dir[1]) if os.path.isfile(os.path.join(img_dir[1], f)) and f[-3:]=='jpg']

    image_labels=pd.read_csv(os.path.join(label_dir, 'labels.csv'), index_col=0)

    print(image_labels.head())

    train_df=pd.DataFrame({'img':train_images, 'breed':image_labels.loc[[f.split('.')[0] for f in train_images], 'breed'].tolist()})

    print(train_df.head())


    test_df=pd.DataFrame({'img':test_images, 'breed':0})

    print(test_df.head())

    global dog_breeds

    print(train_df.info())
    dog_breeds=train_df.loc[:, 'breed'].unique().tolist()
    dog_breeds.sort()

    if(len(dog_breeds)!=120):
        raise('dog breeds is not 120')

    global dog_breeds_map
    global dog_breeds_demap

    dog_breeds_map=dict(zip(dog_breeds, np.arange(120)))
    dog_breeds_demap=dict(zip(np.arange(120), dog_breeds))

    train_df['breed']=train_df['breed'].map(dog_breeds_map)

    print(train_df.head())

    global validation_size

    val_size=np.floor(train_df.shape[0]*validation_size).astype(np.int)
    val_df=train_df[-val_size+1:]
    train_df=train_df[0:-val_size+1]

    train_dataset=dataset_from_df(train_df)
    validation_dataset=dataset_from_df(val_df)
    test_dataset=dataset_from_df(test_df)

    global IMAGE_SIZE

    if(IMAGE_SIZE==[0, 0]):
        for image_file in train_images:
            im_shape=img.imread(os.path.join(img_dir[0], image_file)).shape
            if(im_shape[0]>IMAGE_SIZE[0]):
                IMAGE_SIZE[0]=im_shape[0]
            if(im_shape[1]>IMAGE_SIZE[1]):
                IMAGE_SIZE[1]=im_shape[1]

        for image_file in test_images:
            im_shape=img.imread(os.path.join(img_dir[1], image_file)).shape
            if(im_shape[0]>IMAGE_SIZE[0]):
                IMAGE_SIZE[0]=im_shape[0]
            if(im_shape[1]>IMAGE_SIZE[1]):
                IMAGE_SIZE[1]=im_shape[1]


    return train_dataset, validation_dataset, test_dataset


def warp_image(image):
    # image=cv2.resize(image, tuple(IMAGE_SIZE))
    image = tf.image.resize_images(image, tuple(IMAGE_SIZE))
    return image


def image_batch_from_df(batch_df, image_path):
    image_batch=batch_df['img'].map(lambda x: img.imread(os.path.join(image_path, x)).astype(np.float32)/255.0).values.tolist()
    image_batch=[warp_image(image) for image in image_batch]
    image_batch=np.stack(image_batch, axis=0)
    label_batch=np.array(batch_df['breed'].tolist()).astype(np.int32)
    return image_batch, label_batch

def get_next_batch(dataset, batch_size, image_path):
    batch=dataset.next_batch(batch_size)
    batch=image_batch_from_df(batch, image_path)
    return batch
