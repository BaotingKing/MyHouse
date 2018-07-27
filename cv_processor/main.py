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
import cv2

# boxes = np.arange(28).reshape(-1,4)
# print(boxes)

# ===========测试ExtendBox函数=========
# cvtl.ExtendBox(box, 0)
# cvtl.ExtendBox(box, 1)
print("===============================")


# ===========UpandDownPoint===========
# print(box)
# cvtl.UpandDownPoint(box)
# print(box)
print("===============================")


# ===========测试BoxOverlap函数=========
# Region1 = [2, 8, 5, 2]
# Region2 = [3, 6, 10, 2]
# are =cvtl.BoxOverlap(Region2, Region1)
# print(are)
# b = 8.0/38
# print(b)
print("===============================")

# ===========测试BoxOverlap函数=========
# np.random.seed(1)
# boxes = np.random.randint(0, 100, 28).reshape(-1, 4)
arr = [[3, 56, 20, 12],
         [12, 23, 20, 5],
         [50, 89, 80, 20],
         [12, 20, 40, 0],
         [6, 40, 52, 16],
         [18, 40, 20, 8],
         [2, 12, 8, 3]]
boxes = np.array(arr)
merge_box = cvtl.MergeBoxes(boxes, 0.2)
print("boxes is %s" % boxes)
print("merge_box is %s" % merge_box)