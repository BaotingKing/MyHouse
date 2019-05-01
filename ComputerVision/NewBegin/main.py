import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
# from sklearn import cluster.AssertionError
import cv2
from PIL import Image



arr = np.arange(10)
print(arr)

img = cv2.imread('cat.jpg')

cv2.imshow('img', img)
cv2.waitKey(0)

# plt.imshow(img, cmap='gray')
# plt.show()