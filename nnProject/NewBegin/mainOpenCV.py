# -*- coding: utf-8 -*-
#
# __author__ = 'Baoting Zhang'
# Time:        2018-05-05 to 2018-07-13
#       for myself
import numpy as np
import matplotlib.pyplot as plt
import imagetools
import cv2

# read image
img_cv = cv2.imread('cat.jpg')

# show high & width
high, width = img_cv.shape[:2]
print(img_cv.shape)
print("high is %d", high)
print("width is %d", width)

# save image=============================================
cv2.imwrite('newCat.jpg', img_cv)

# 颜色空间变换=============================================
# img_cvt = cv2.cvtColor(img_cv, cv2.COLOR_BAYER_BG2GRAY)

# show image=============================================
# cv2.imshow('dog', img_cv)
# cv2.waitKey()
plt.imshow(img_cv)
plt.show()