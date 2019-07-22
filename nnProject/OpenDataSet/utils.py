#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: ZK
# Time: 2019/07/17 17:34
import numpy as np
import cv2
import os
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


def draw_paper():
    # test_image = np.zeros((720, 1280, 3), dtype=np.uint8).tostring()
    test_image = np.zeros((720, 1280, 3), dtype=np.uint8)
    cv2.line(test_image, (0, 0), (511, 511), (255, 0, 0), 5)
    cv2.imshow('line', test_image)
    cv2.waitKey()


def merge_imge(mat_a, mat_b, factor=0.5):
    size = mat_a.shape
    new_a = cv2.resize(mat_a, (int(size[1] * factor), int(size[0] * factor)), cv2.INTER_LINEAR)
    new_b = cv2.resize(mat_b, (int(size[1] * factor), int(size[0] * factor)), cv2.INTER_LINEAR)
    return np.vstack((new_a, new_b))


def fitting_lines(fitting_point_x, fitting_point_y):
    param = np.polyfit(np.array(fitting_point_x), np.array(fitting_point_y), 5)
    func = np.poly1d(param)
    distance_mm = func(0)
    return distance_mm


def get_cross_point(line_a, line_b):
    ka = (line_a[3] - line_a[1]) / (line_a[2] - line_a[0])  # Find the slope of the line
    kb = (line_b[3] - line_b[1]) / (line_b[2] - line_b[0])  # line is [x0, y0, x1, y1]
    if abs(ka - kb) < 1e-2:
        return None
    else:
        cross_x = (ka * line_a[0] - line_a[1] - kb * line_b[0] + line_b[1]) / (ka - kb)
        cross_y = (ka * kb * (line_a[0] - line_b[0]) + ka * line_b[1] - kb * line_a[1]) / (ka - kb)
        return [cross_x, cross_y]


# def adjust_param(x_points, y_points):
#     line_A = [x_points[0][0], y_points[0][0], x_points[0][-1], y_points[0][-1]]
#     line_B = [x_points[1][0], y_points[1][0], x_points[1][-1], y_points[1][-1]]
#     cross_point = utils.get_cross_point(line_A, line_B)
#     lines[0].append(cross_point)
#     lines[1].append(cross_point)
#     lines[2].append(cross_point)
#     print(line_A, line_B, cross_point)
#     length = 1048
#     if cross_point[0] <= length/2:
#         left = 0
#         right = length
#     elif cross_point[0] + length/2 > 1640:
#         left = 1640 - length/2
#         right = 1640
#     else:
#         left = int(cross_point[0] - length/2)
#         right = int(cross_point[0] + length/2)
#
#     find_target_point(x_points, y_points, left, right)
#     print('=======', left, right, abs(left - right))
#     return left, right


def find_target_point_old(x_points_set, y_points_set, left, right):
    X_line_a = [i - left for i in x_points_set[0]]
    Y_line_a = y_points_set[0]
    for idx, val in enumerate(X_line_a):
        if val > 0:
            break
    X_line_a = X_line_a[idx:]
    Y_line_a = Y_line_a[idx:]
    print('------------------', len(X_line_a), X_line_a)
    print('------------------', len(Y_line_a), Y_line_a)
    for idx, val in enumerate(X_line_a):
        if val > 1048:
            break
    X_line_a = X_line_a[:idx]
    Y_line_a = Y_line_a[:idx]
    print('------------------', len(X_line_a), X_line_a)
    print('------------------', len(Y_line_a), Y_line_a)


def draw_culane(img_mat, lane_lines):
    for lane_info in lane_lines:
        for idx in range(len(lane_info) - 1):
            rng = randomcolor()
            a_point = tuple((int(lane_info[idx][0]), int(lane_info[idx][1])))  # cv2.line's points must be int
            b_point = tuple((int(lane_info[idx + 1][0]), int(lane_info[idx + 1][1])))
            cv2.line(img_mat, a_point, b_point, color=rng, thickness=3)
    return img_mat
