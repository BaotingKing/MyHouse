""""
First day in WestWellLab
author: Baoting Zhang
date:   2018-07-19
"""
# -*- coding: utf-8 -*-
import numpy as np
import cv2


# mouse callback
def draw_circle_by_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        cv2.circle(img, (x, y), 64, (255, 355, 0), -1)


# create a image map
img = np.zeros((512, 512, 3), np.uint8)
cv2.namedWindow('imge')
cv2.setMouseCallback('imge', draw_circle_by_mouse)

while (1):
    cv2.imshow('imge', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
