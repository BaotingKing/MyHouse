#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: ZK
# Time: 2019/6/27 17:04
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import json
import random


def randomcolor():
    colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    rgb = []
    for i in range(3):
        color = ""
        for j in range(2):
            color += colorArr[random.randint(0, 14)]
        rgb.append(int(color, 16))

    return tuple(rgb)


def search_file(rootdir, target_file):
    target_file_path = ''
    for parent, dirnames, filenames in os.walk(rootdir):
        if target_file in filenames:
            target_file_path = os.path.join(parent, target_file)
            break
    return target_file_path


def draw_labels(img_labels):
    try:
        img_path_info = search_file(img_path, img_labels['name'])
        if img_path_info is not None:
            img_mat = cv2.imread(img_path_info)
            print('-----------------------: ', img_path_info)
            for label_info in img_labels['labels']:
                if label_info['category'] == 'lane':
                    shape_info = label_info['poly2d'][0]['vertices']
                    rng = randomcolor()
                    a_point = tuple((int(shape_info[0][0]), int(shape_info[0][1])))
                    b_point = tuple((int(shape_info[1][0]), int(shape_info[1][1])))
                    # cv2.line(img_mat, a_point, b_point, color=rng, thickness=2)

                elif label_info['category'] == 'drivable area':
                    shape_info = label_info['poly2d'][0]['vertices']
                    points = []
                    rng = randomcolor()
                    for p in shape_info:
                        points.append([int(p[0]), int(p[1])])
                    cv2.fillPoly(img_mat, np.array([points], dtype=np.int32), rng)

            cv2.imshow('ShowTag', img_mat)
            cv2.waitKey(0)
    except Exception as e:
        print('[Error]:', e)


def draw_paper():
    # test_image = np.zeros((720, 1280, 3), dtype=np.uint8).tostring()
    test_image = np.zeros((720, 1280, 3), dtype=np.uint8)
    cv2.line(test_image, (0, 0), (511, 511), (255, 0, 0), 5)
    cv2.imshow('line', test_image)
    cv2.waitKey()


if __name__ == '__main__':
    img_path = 'G:\\Dataset\\BDD100k\\bdd100k_images\\bdd100k\\images\\'
    img_label = 'G:\\Dataset\\BDD100k\\bdd100k_labels_release\\bdd100k\\labels\\bdd100k_labels_images_val.json'

    with open(img_label, 'r') as file_handle:
        label_info = json.load(file_handle)

    # draw_labels(label_info[2])

    for img_info in label_info:
        # if img_info['name'] not in ['b1e88fd2-c1e4fd2b.jpg', 'b23f7012-fab06dac.jpg', 'b23f7012-fab06dac.jpg', 'b26ba07a-1c7593b1.jpg', 'b2715214-13e3dd85.jpg']:
            # continue
        print(img_info)
        draw_labels(img_info)
        # break

    # print(label_info[0]['labels'])
