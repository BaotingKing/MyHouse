""""
First day in WestWellLab
author: Baoting Zhang
date:   2018-07-18
"""
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2

img = np.zeros([512, 512, 3], np.uint8)
img = cv2.line(img, (0,0), (255, 255), (128, 128 ,128), 6)
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()


# while True:
#     if cv2.imshow('image', img) & 0xFF == ord('q'):
#         break
#     # cv2.waitKey(0)
# cv2.destroyAllWindows()