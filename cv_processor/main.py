# -*- coding: utf-8 -*-
"""
Created on 2018-07-25 星期三 14：04
@author: zhang baoting

for test function
"""
import cvtools as cvtl
import os
import numpy as np

a = np.arange(28).reshape(-1,4)
# b = np.arange(7).reshape(7,-1)
# box = np.concatenate((b,a),-1)
box = a
print(a)
# cvtl.ExtendBox(box, 0)
# cvtl.ExtendBox(box, 1)


print("===============================")
print(box)
print("===============================")
cvtl.UpandDownPoint(box)
print(box)
print("===============================")
