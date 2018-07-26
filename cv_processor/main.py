# -*- coding: utf-8 -*-
"""
Created on 2018-07-25 星期三 14：04
@author: zhang baoting

for test function
"""
import cvtools as cvtl
import os
import numpy as np
import fitools

# a = np.arange(28).reshape(-1,4)
# b = np.arange(7).reshape(7,-1)
# box = np.concatenate((b,a),-1)
# box = a
# print(a)
# cvtl.ExtendBox(box, 0)
# cvtl.ExtendBox(box, 1)


print("===============================")
# print(box)
print("===============================")
# cvtl.UpandDownPoint(box)
# print(box)
print("===============================")

# 定义Caffe根目录
caffe_root = 'D:/home/zach/house/'
dir_merge = "F:\myhouse\MyHouse\\nnProject"   # 按照不同categories文件夹存放的根目录
print("1111111111111")
fitools.creatLabelTxt(dir_merge, "train_label.txt")
fitools.creatLabelTxt(dir_merge, "test_label.txt")
print("2222222222222")