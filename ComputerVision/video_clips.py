#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2019/2/19
import cv2

print(cv2.__version__)
videoCapture = cv2.VideoCapture('APHU730763345G1.avi')

fps = 120  # 保存视频的帧率
# size = (1920, 1080)  # 保存视频的大小
size = (1072, 603)  # 保存视频的大小

videoWriter = cv2.VideoWriter('video4.avi', cv2.VideoWriter_fourcc('X', 'V', 'I', 'D'), fps, size)
i = 0

while True:
    success, frame = videoCapture.read()
    if success:
        i += 1
        print('i = ', i)
        if (i >= 30 and i <= 250):
            videoWriter.write(frame)
    else:
        print('end')
        break
