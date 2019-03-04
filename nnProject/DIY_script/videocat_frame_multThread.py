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
import threading
import numpy as np
from datetime import datetime


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


def video_clips(video_source, save_path, share_path):
    """
    函数功能：视频截取
    :param video_source: 源视频
    :param save_path: 根据视频名来保存对应截取视频的路径
    :param share_path: 触发wellocean的共享路径
    :return:
    """
    video_info = capture_video_trigger(video_source, share_path)
    video_save(video_source, save_path, video_info)


def capture_video_trigger(video_source,
                          share_path,
                          data_server='127.0.0.1'):
    video_list = []
    trigger_lock = False
    frame_cnt = 0
    frame_begin = 0
    frame_end = 0
    frame_redundancy_front = 60
    frame_redundancy_back = 20
    # print '*********************1:redis begin'
    redis_msg_transfer = redis.StrictRedis(host=data_server,
                                           port=6379, db=0)
    trigger_topic = "/WellOcean/roi_trigger/channel_3"
    output_topic = "/WellOcean/final_result/channel_3"
    share_map = get_share_file_map(share_path)
    capture = cv2.VideoCapture(video_source)
    FPS = capture.get(5)
    res, frame = capture.read()
    # print '*********************redis_msg_transfer:', redis_msg_transfer.keys()
    # print '*********************2:redis end'
    print 'video_source is: ', video_source
    while res:
        '''trigger wellocean'''
        frame_cnt += 1
        image_str = frame.tostring()
        share_map.seek(0)
        share_map.write(image_str)

        '''read redis'''
        car_exist = redis_msg_transfer.get(trigger_topic)
        # print '===============car_exist: ', car_exist
        if car_exist == '2' and not trigger_lock:
            # print '****************************************************Begin'
            # print '******* Frame begin: ', frame_cnt
            trigger_lock = True
            frame_begin = frame_cnt + frame_redundancy_front
            video_start_ms = int(time.time() * 1000)
        elif car_exist == '0' and trigger_lock:
            # print '*********************12'
            trigger_lock = False
            frame_end = frame_cnt + frame_redundancy_back
            redis_info_pub = redis_msg_transfer.pubsub()
            redis_info = redis_info_pub.subscribe(output_topic)
            if redis_info is None:
                video_result = str(video_start_ms)
            else:
                data = json.loads(redis_info)
                video_result = data['final_result0']  # Fetch a result as the name of the video file

            # print '******* Frame end   : ', frame_cnt
            video_dict = dict(video_start_frame=frame_begin,
                              video_end_frame=frame_end,
                              video_name=video_result)
            # print '*********************\n', video_dict
            # if (video_end_ms - video_start_ms)/1000 < 20:
            #     print 'this maybe have problem'
            #     continue
            # print '*********************13================'
            video_list.append(video_dict)
        # cv2.imshow('VideoCat', frame)
        # cv2.waitKey(1)
        cv2.waitKey(24)
        res, frame = capture.read()
    capture.release()
    return video_list


def video_save(original_video, save_path, video_info=None):
    """根据视频提取信息截取保存视频"""
    for video_dict in video_info:
        # print '+++++++++++: ', video_dict['video_name'] + '.avi'
        save_file = os.path.join(save_path, video_dict['video_name'] + '.avi')
        # print '+++++++++++save_file is: ', save_file
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
            print 'open write file fail'
        # capture.set(cv2.CAP_PROP_POS_MSEC, video_dict['video_start_ms'])
        video_start_time = int((video_dict['video_start_frame'])/FPS * 1000)
        capture.set(0, video_start_time)
        res, frame = capture.read()
        i = 0
        while i < (video_dict['video_end_frame'] - video_dict['video_start_frame']):
            writer.write(frame)
            res, frame = capture.read()
            i += 1
        writer.release()
        capture.release()


if __name__ == '__main__':
    cur_path = os.getcwd()
    share_file = ['/cv/master1', '/cv/master2', '/cv/master3']    # 根据launch file的实际配置和测试机能力设置这里
    save_path = os.path.join(cur_path, 'Img_result')
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    original_videos = []
    for root, dirs_labels, file_names in os.walk(cur_path):  # Iterate label files
        if 'Img_result' in root:  # Skip save file: root == save_path
            continue
        for video_name in file_names:
            if video_name[-4:] == ".avi":
                video_path = str(os.path.join(root, video_name))
                original_videos.append(video_path)
    threadings = []
    cnt = 0
    print '**************************************************************'
    begin = datetime.now()
    print 'The start time of videocat is: {0}'.format(begin)
    print 'Share file list: ', share_file
    for org_video in original_videos:
        save_path_video = os.path.join(save_path, os.path.split(org_video)[-1][:-4])
        if not os.path.exists(save_path_video):
            os.mkdir(save_path_video)

        temp_thread = threading.Thread(target=video_clips, args=(org_video, save_path, share_file[cnt]))
        cnt += 1
        threadings.append(temp_thread)
        temp_thread.start()

        if cnt % len(share_file) == 0:
            cnt = 0
            for one_thread in threadings:
                one_thread.join()

    print 'This is ok, total time: {0}'.format(time.time() - begin)
