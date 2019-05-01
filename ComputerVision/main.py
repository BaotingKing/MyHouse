""""
First day in WestWellLab
author: Baoting Zhang
date:   2018-07-16
"""
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2

# arr = np.arange(10)
# img = cv2.imread('cat.jpg')
#
# cv2.imshow('firstcat', img)
# cv2.waitKey()
# print(arr)
cap = cv2.VideoCapture(0)

while True:
    ret, colr_img = cap.read()
    cv2.imshow('show_img', colr_img)
    if cv2.waitKey(1)&0xFF == ord('q'):
        break
cap.release()

cv2.destroyAllWindows()