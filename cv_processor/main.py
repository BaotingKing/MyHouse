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

a = np.arange(28).reshape(-1,4)

box = a
print(a)
# box = np.concatenate((b,a),-1)
# cvtl.ExtendBox(box, 0)
# cvtl.ExtendBox(box, 1)


print("===============================")
# print(box)
print("===============================")
# cvtl.UpandDownPoint(box)
# print(box)
print("===============================")


print("===============================")

Region1 = [2, 8, 5, 2]
Region2 = [3, 6, 10, 2]

are =cvtl.BoxOverlap(Region2, Region1)
print(are)
b = 8.0/38
print(b)
print("===============================")
