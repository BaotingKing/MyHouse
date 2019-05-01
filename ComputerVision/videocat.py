#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2019/2/20

import os
import sys
import time
import cv2
from matplotlib import pyplot as plt
# sys.path.append('/usr/local/lib/python2.7/dist-packages')


def vide_clips(capture, savepath):
    time_m = [[4, 5]]
    time_s = [[29, 00]]
    for j in range(len(time_m)):
        save_file = savepath + '2.avi'
        if not capture.isOpened():
            print('open read file fail')
        FPS = capture.get(5)
        frameweight = int(capture.get(3))
        frameheight = int(capture.get(4))
        if os.path.exists(save_file):
            print('write file exists')
            sys.exit()
        # fourcc = cv2.cv.CV_FOURCC(*'XVID')
        fourcc = cv2.CAP_PROP_FOURCC(*'XVID')
        writer = cv2.VideoWriter(save_file, fourcc, 15, (frameweight, frameheight))
        if not writer.isOpened():
            print('open write file fail')
        capture.set(0, (time_m[j][0] * 60 + time_s[j][0]) * 1000)
        res, frame = capture.read()
        i = 0
        while i < (30 * ((time_m[j][1] - time_m[j][0]) * 60 + (time_s[j][1] - time_s[j][0]))):
            writer.write(frame)
            # cv2.imwrite('/cv2/distortedimage/' + str(int(time.time())) + '.jpg', frame)
            res, frame = capture.read()
            i += 1
            cv2.imshow('test', frame)
            cv2.waitKey(33)

        writer.release()


if __name__ == '__main__':
    capture = cv2.VideoCapture('APHU730763345G1.avi')
    save_path = 'F://mystudio//'
    vide_clips(capture, save_path)
