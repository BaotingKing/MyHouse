#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: ZK
# Time: 2019/6/27 17:04
import os
import cv2
import numpy as np
import json
import utils
from utils import randomcolor


def search_file(rootdir, target_file):
    target_file_path = ''
    for parent, dirnames, filenames in os.walk(rootdir):
        if target_file in filenames:
            target_file_path = os.path.join(parent, target_file)
            break
    return target_file_path


def draw_labels(img_name, lane_lines, img_path):
    try:
        img_path_info = search_file(img_path, img_name)
        if img_path_info is not None:
            img_mat = cv2.imread(img_path_info)
            img_mat_lane = cv2.imread(img_path_info)
            print('-----------------------: ', img_path_info)
            for lane_info in lane_lines:
                for idx in range(len(lane_info) - 1):
                    rng = randomcolor()
                    a_point = tuple((int(lane_info[idx][0]), int(lane_info[idx][1])))   # cv2.line's points must be int
                    b_point = tuple((int(lane_info[idx + 1][0]), int(lane_info[idx + 1][1])))
                    cv2.line(img_mat_lane, a_point, b_point, color=rng, thickness=3)
            img_whole = utils.merge_imge(img_mat, img_mat_lane)
            cv2.imshow('ShowTag', img_whole)
            cv2.waitKey(0)
    except Exception as e:
        print('[Error]:', e)


if __name__ == '__main__':
    img_path = 'F:\\BaiduNetdiskDownload\\Dataset\\CULane\\driver_161_90frame\\06030852_0766.MP4\\'
    img_label = 'F:\\BaiduNetdiskDownload\\Dataset\\CULane\\driver_161_90frame\\06030852_0766.MP4\\01440.lines.txt'
    img_infos = ['01440.jpg']

    img_path = 'F:\\BaiduNetdiskDownload\\Dataset\\CULane\\driver_37_30frame\\05181520_0219.MP4\\'
    img_label = 'F:\\BaiduNetdiskDownload\\Dataset\\CULane\\driver_37_30frame\\05181520_0219.MP4\\00450.lines.txt'
    img_infos = ['00450.jpg']

    with open(img_label, 'r') as file_handle:
        label_info = file_handle.readlines()
    lines = []
    for record in label_info:
        print(type(record), record)
        record = record.strip()
        one = record.split(' ')
        a = len(one) % 2
        if len(one) % 2 != 0:
            print('Failed to read coordinates!')
            break
        x_coord = one[::2]
        y_coord = one[1::2]
        points = []
        for idx in range(len(one)//2):
            x = eval(x_coord[idx])
            y = eval(y_coord[idx])
            points.append([x, y])
        lines.append(points)
    print('-------lines', type(lines), len(lines), lines)

    for img_info in img_infos:
        print(img_info)
        draw_labels(img_info, lines, img_path)
        # break

    # print(label_info[0]['labels'])
