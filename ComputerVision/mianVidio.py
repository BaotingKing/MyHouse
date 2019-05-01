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

cap = cv2.VideoCapture('vtest.avi')
while True:
    ret, colr_img = cap.read()
    cv2.imshow('show_img', colr_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()


# '''写视频'''
# cap = cv2.VideoCapture(0)
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('output.avi', fourcc, 30.0, (640,480))
# while cap.isOpened():
#     ret, frame = cap.read()
#     if ret == True:
#         out.write(frame)
#         cv2.imshow('frame', frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     else:
#         break
#
# cap.release()
# out.release()
# cv2.destroyAllWindows()