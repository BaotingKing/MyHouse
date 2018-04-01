import scipy
import numpy as np
import matplotlib.pyplot as plt

def data_aug(image):
    image=random_flip_lr(image)
    image=random_rotate(image)
    image=random_crop(image, 4)
    return image




def random_crop(image, delta):
    delta=delta+1
    image_copy=np.zeros(shape=image.shape, dtype=image.dtype)
    size=image.shape[1]
    for idx, im in enumerate(image):
        seed_h=np.random.randint(0, delta)
        seed_v=np.random.randint(0, delta)
        lr=np.random.randint(0, 2)
        if(lr==0):#left/upper crop
            image_=im[seed_h:, seed_v:, :]
        else:# right/lower crop
            image_=im[0:size-seed_h, 0:size-seed_v, :]
            
        end_h=im.shape[0]-seed_h
        end_v=im.shape[1]-seed_v
        image_copy[idx, 0:end_h, 0:end_v, :]=image_
        #plt.imshow(image_)
    return image_copy


def random_rotate(image):
    max_angle=10
    image_copy=np.zeros(shape=image.shape, dtype=image.dtype)
    for idx, im in enumerate(image):
        angle=np.random.randint(-max_angle, max_angle+1)
        image_copy[idx, :, :, :]=scipy.ndimage.rotate(im, np.float32(angle), axes=(0, 1), reshape=False)
        #plt.imshow(image_copy[idx, :, :, :])
    return image_copy



def random_flip_lr(image):
    for idx, im in enumerate(image):
        is_flip=np.random.randint(0, 2)
        if(is_flip):
            image[idx,  :, :, :]=image[idx, :, -1:, :]
    return image

        
