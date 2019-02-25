#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2019/2/20

import os
import sys
import time
import cv2
import json
import redis
from cv2 import imshow
from matplotlib import pyplot as plt
# sys.path.append('/usr/local/lib/python2.7/dist-packages')


def vide_clips(video_source, savepath):
    video_save(video_source, savepath, time_stamp='123456')


def catch_timestamp(data_server):
    redis_msg_transfer = redis.StrictRedis(host=data_server,
                                           port=6379, db=0)
    trigger_topic = []
    redis_info = []
    car_exist = redis_msg_transfer.get(trigger_topic)
    data = json.loads(redis_info)
    timestampe = data['timestamp']


def video_save(original_video, save_path, time_stamp=None):
    save_file = save_path + time_stamp + '.avi'
    capture = cv2.VideoCapture(original_video)
    time_m = [[0, 0]]
    time_s = [[5, 15]]
    j = 0
    if not capture.isOpened():
        print('Open read file fail, time_stamp is {0}'.format(time_stamp))
    capture.set(cv2.CAP_PROP_FPS, 30)
    FPS = capture.get(cv2.CAP_PROP_FPS)
    frameweight = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameheight = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if os.path.exists(save_file):
        print('write file exists')
        save_file = save_path + time_stamp + '_1.avi'
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    writer = cv2.VideoWriter(save_file, fourcc, FPS, (frameweight, frameheight))
    if not writer.isOpened():
        print('open write file fail')
    rel = capture.set(cv2.CAP_PROP_POS_MSEC, (time_m[j][0] * 60 + time_s[j][0]) * 1000)
    res, frame = capture.read()
    i = 0
    while i < (FPS * ((time_m[j][1] - time_m[j][0]) * 60 + (time_s[j][1] - time_s[j][0]))):
        writer.write(frame)
        # save_path_img = os.path.join(save_path, 'image')
        # if not os.path.exists(save_path_img):
        #     os.mkdir(save_path_img)
        # cv2.imwrite(save_path_img + str(int(time.time())) + '.jpg', frame)  # The effect is to save once per second
        res, frame = capture.read()
        i += 1
        # cv2.imshow('test', frame)
        # cv2.waitKey(33)

    writer.release()
    capture.release()


if __name__ == '__main__':
    original_video = 'APHU730763345G1.avi'
    save_path = 'F://mystudio//'
    vide_clips(original_video, save_path)
    # img = cv2.Canny()
    print('this is ok')