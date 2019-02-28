#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2019/2/20

import os
import time
import cv2
import json
import mmap
import redis
import numpy as np
from datetime import datetime
SHARE_FILE = '/cv/master1'


def get_share_file_map(cam_file_name, write_resolution='1080'):
    """
    Lite: get share file map from cam file name
    """
    while True:
        if not os.path.exists(cam_file_name):
            shmfile = open(cam_file_name, 'w')
            shmfile.close()
        shmfile = open(cam_file_name, 'r+')
        if write_resolution == '720':
            test_image = np.zeros((720, 1280, 3), dtype=np.uint8).tostring()
        elif write_resolution == '1080':
            test_image = np.zeros((1080, 1921, 3), dtype=np.uint8).tostring()
        shmfile.write(test_image)
        break
    shmmap = mmap.mmap(shmfile.fileno(), 0, prot=mmap.PROT_WRITE)
    return shmmap


def video_clips(video_source, save_path, start_time):
    print '*********************0'
    video_info = catch_timestamp(video_source, save_path, start_time)
    print '*********************100'
    # video_save(video_source, save_path, video_info)


def catch_timestamp(video_source,
                    save_path,
                    start_timestamp,
                    data_server='127.0.0.1'):
    video_list = []
    trigger_lock = False
    print '*********************1:redis begin'
    redis_msg_transfer = redis.StrictRedis(host=data_server,
                                           port=6379, db=0)
    trigger_topic = "/WellOcean/roi_trigger/channel_3"
    output_topic = "/WellOcean/final_result/channel_3"
    share_map = get_share_file_map(SHARE_FILE)
    capture = cv2.VideoCapture(video_source)
    res, frame = capture.read()
    print '*********************redis_msg_transfer:', redis_msg_transfer.keys()
    print '*********************trigger_topic:', redis_msg_transfer.get(trigger_topic)
    print '*********************2:redis end'
    print '**********************video_source is: ', video_source
    while res:
        '''trigger wellocean'''
        image = frame
        image_str = image.tostring()
        share_map.seek(0)
        share_map.write(image_str)

        '''read redis'''
        car_exist = redis_msg_transfer.get(trigger_topic)
        # print '===============car_exist: ', car_exist
        if car_exist == '2' and not trigger_lock:
            print '****************************************************Begin'
            print 'TTTTT start_timestamp: ', datetime.fromtimestamp(int(str(start_timestamp)[:-3])).strftime('%Y-%m-%d %H:%M:%S')

            trigger_lock = True
            redis_info = redis_msg_transfer.get(output_topic)
            # video_start = data['token'][0:-3]  # token = timestampe + parity bit
            video_start = int(time.time() * 1000)
            if (video_start - start_timestamp) > 2 * 1000:
                video_start_ms = video_start - start_timestamp - 2 * 1000
            elif (video_start - start_timestamp) <= 2 * 1000:
                video_start_ms = video_start - start_timestamp
            else:
                print 'Time is error'

            print 'TTTTT video_start:     ', datetime.fromtimestamp(int(str(video_start)[:-3])).strftime('%Y-%m-%d %H:%M:%S')
            print 'TTTTT video_start_ms:  ', video_start_ms/1000

            if redis_info is None:
                video_result = str(video_start_ms)
            else:
                data = json.loads(redis_info)
                video_result = data['final_result0']  # Fetch a result as the name of the video file
        elif car_exist == '0' and trigger_lock:
            # print '*********************12'
            trigger_lock = False
            video_end = int(time.time() * 1000)
            print 'TTTTT video_end:       ', datetime.fromtimestamp(int(str(video_end)[:-3])).strftime('%Y-%m-%d %H:%M:%S')
            video_end_ms = video_end - start_timestamp + 1 * 1000
            print 'TTTTT video_end_ms:    ', video_end_ms/1000
            print 'TTTTT video_long:      ', (video_end_ms - video_start_ms)/1000
            video_dict = dict(video_start_ms=video_start_ms,
                              video_end_ms=video_end_ms,
                              video_name=video_result)
            print '*********************\n', video_dict
            # print '*********************13================'
            video_list.append(video_dict)
            video_save(video_source, save_path, [video_dict])
            # print '*********************14================'

        # cv2.imshow('VideoCat', frame)
        # cv2.waitKey(1)
        cv2.waitKey(24)
        res, frame = capture.read()
    capture.release()
    return video_list


def video_save(original_video, save_path, video_info=None):
    for video_dict in video_info:
        print '*********************20'
        print '+++++++++++: ', video_dict['video_name']
        print '+++++++++++: ', video_dict['video_name'] + '.avi'
        save_file = os.path.join(save_path, video_dict['video_name'] + '.avi')
        print '+++++++++++save_file is: ', save_file
        capture = cv2.VideoCapture(original_video)
        if not capture.isOpened():
            print 'Open read file fail'
        # capture.set(cv2.CAP_PROP_FPS, 30)
        # FPS = capture.get(cv2.CAP_PROP_FPS)
        # frame_weight = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        # frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        FPS = capture.get(5)
        frame_weight = int(capture.get(3))
        frame_height = int(capture.get(4))
        if os.path.exists(save_file):
            print 'write file exists'
            save_file = save_path + video_dict['video_name'] + '_1.avi'
        # fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fourcc = cv2.cv.CV_FOURCC(*'XVID')
        writer = cv2.VideoWriter(save_file, fourcc, FPS, (frame_weight, frame_height))
        if not writer.isOpened():
            # print('open write file fail')
            pass
        # capture.set(cv2.CAP_PROP_POS_MSEC, video_dict['video_start_ms'])
        capture.set(0, video_dict['video_start_ms'])
        res, frame = capture.read()
        i = 0
        print '#################video is: ', FPS * (video_dict['video_end_ms'] - video_dict['video_start_ms']) / 1000
        while i < (FPS * (video_dict['video_end_ms'] - video_dict['video_start_ms']) / 1000):
            writer.write(frame)
            res, frame = capture.read()
            cv2.waitKey(24)
            i += 1
        writer.release()
        capture.release()


if __name__ == '__main__':
    cur_path = os.getcwd()
    save_path = os.path.join(cur_path, 'Img_result')
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    original_videos = []
    for root, dirs_labels, file_names in os.walk(cur_path):  # Iterate label files
        if root == save_path:  # Skip save file
            continue
        for video_name in file_names:
            if video_name[-4:] == ".avi":
                video_path = str(os.path.join(root, video_name))
                original_videos.append(video_path)
    begin = time.time()
    for org_video in original_videos:
        init_timestamp = int(time.time() * 1000)
        save_path_video = os.path.join(save_path, os.path.split(org_video)[-1][:-4])
        if not os.path.exists(save_path_video):
            os.mkdir(save_path_video)

        video_clips(org_video, save_path_video, init_timestamp)

    print 'this is ok, total time: {0}s'.format(time.time() - begin)
