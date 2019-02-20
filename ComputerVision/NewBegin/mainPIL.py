# -*- coding: utf-8 -*-
#
# __author__ = 'Baoting Zhang'
# Time:        2018-05-05 to 2018-07-13
#       for myself
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import imagetools
import pylab
img = Image.open('cat.jpg')

# 对图片进行灰度化处理
img_L = Image.open('cat.jpg').convert('L')
im = np.array(img)

filelist = imagetools.get_imlist(
    '/home/bbz/myhouse/MyHouse/nnProject/NewBegin/', suffix='.jpg')
print('==========================')
print('==========================')
print(filelist)
print('==========================')
print('==========================')
plt.imshow(img)
plt.show()
