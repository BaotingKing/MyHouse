#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: ZK
# Time: 2019/07/18 15:13
import cv2
import utils
import os
import random

MID_SIZE = (1048, 590)
TARGET_SIZE = (640, 360)
PATH = 'F:\\projects\\Semantic_segmentation\\data\\'


def get_cross_point(line_a, line_b):
    if (line_b[0] != line_b[2]) and (line_a[0] != line_a[2]):
        ka = (line_a[3] - line_a[1]) / (line_a[2] - line_a[0])  # Find the slope of the line
        kb = (line_b[3] - line_b[1]) / (line_b[2] - line_b[0])  # line is [x0, y0, x1, y1]
        if abs(ka - kb) < 1e-2:
            return None
        else:
            cross_x = (ka * line_a[0] - line_a[1] - kb * line_b[0] + line_b[1]) / (ka - kb)
            cross_y = (ka * kb * (line_a[0] - line_b[0]) + ka * line_b[1] - kb * line_a[1]) / (ka - kb)
            return [cross_x, cross_y]
    else:
        if line_a[0] != line_a[2]:
            ka = (line_a[3] - line_a[1]) / (line_a[2] - line_a[0])
            cross_x = line_b[0]
            cross_y = line_a[1] + ka * (cross_x - line_a[0])
            return [cross_x, cross_y]
        elif line_b[0] != line_b[2]:
            kb = (line_b[3] - line_b[1]) / (line_b[2] - line_b[0])
            cross_x = line_a[0]
            cross_y = line_b[1] + kb * (cross_x - line_b[0])
            return [cross_x, cross_y]
        else:
            return None


def proc_label(file_name):
    with open(file_name, 'r') as file_handle:
        label_info = file_handle.readlines()
    lines_set = []
    x_lines = []
    y_lines = []
    for record in label_info:
        record = record.strip()
        one = record.split(' ')
        if len(one) % 2 != 0:
            print('Failed to read coordinates!')
            break
        x_coord = one[::2]
        y_coord = one[1::2]
        points = []
        x_points = []
        y_points = []
        for idx in range(len(one) // 2):
            x = eval(x_coord[idx])
            y = eval(y_coord[idx])
            points.append([x, y])
            x_points.append(x)
            y_points.append(y)
        lines_set.append(points)
        x_lines.append(x_points)
        y_lines.append(y_points)

    if len(lines_set) == 0:
        return False, lines_set, x_lines, y_lines
    else:
        return True, lines_set, x_lines, y_lines


def find_target_point(x_points_set, y_points_set, left, right, img_path, img_info):
    lines_num = len(x_points_set)
    x_axis = [0, TARGET_SIZE[1] - 1, TARGET_SIZE[0] - 1, TARGET_SIZE[1] - 1]
    y_axis = [0, 0, 0, TARGET_SIZE[1] - 1]
    y_axis_r = [TARGET_SIZE[0] - 1, 0, TARGET_SIZE[0] - 1, TARGET_SIZE[1] - 1]
    left_point = [-1920, 0]
    right_point = [1920, 0]
    key_points = []
    x_points_new = []
    y_points_new = []

    if lines_num < 2:
        print('[Warning] lines_num is:', lines_num)
        return False, key_points
    elif lines_num == 2:
        for line in range(lines_num):
            temp = [(i - left) * TARGET_SIZE[0] / MID_SIZE[0] for i in x_points_set[line]]
            x_points_new.append(temp)
            temp = [i * TARGET_SIZE[1] / MID_SIZE[1] for i in y_points_set[line]]
            y_points_new.append(temp)

        center_cross = get_cross_point(
            [x_points_new[0][0], y_points_new[0][0], x_points_new[0][-1], y_points_new[0][-1]],
            [x_points_new[1][0], y_points_new[1][0], x_points_new[1][-1], y_points_new[1][-1]])

        if center_cross is not None:
            left_point = get_cross_point([x_points_new[0][0], y_points_new[0][0], x_points_new[0][-1], y_points_new[0][-1]],
                                         x_axis)
            right_point = get_cross_point([x_points_new[1][0], y_points_new[1][0], x_points_new[1][-1], y_points_new[1][-1]],
                                          x_axis)
            if left_point is None or right_point is None:
                key_points = [-1, -1, -1, -1, -1, -1]
            else:
                if left_point[0] < 0:
                    left_point = get_cross_point([x_points_new[0][0], y_points_new[0][0], x_points_new[0][-1], y_points_new[0][-1]],
                                                 y_axis)
                elif left_point[0] > TARGET_SIZE[0]:
                    left_point = get_cross_point([x_points_new[0][0], y_points_new[0][0], x_points_new[0][-1], y_points_new[0][-1]],
                                                 y_axis_r)

                if right_point[0] < 0:
                    right_point = get_cross_point([x_points_new[1][0], y_points_new[1][0], x_points_new[1][-1], y_points_new[1][-1]],
                                                  y_axis)
                elif right_point[0] > TARGET_SIZE[0]:
                    right_point = get_cross_point([x_points_new[1][0], y_points_new[1][0], x_points_new[1][-1], y_points_new[1][-1]],
                                                  y_axis_r)
                if left_point is None or right_point is None:
                    key_points = [-1, -1, -1, -1, -1, -1]
                else:
                    key_points = center_cross + left_point + right_point
        else:
            key_points = [-1, -1, -1, -1, -1, -1]

        print('[Info]: Key_points is:', key_points)
        if key_points != [-1, -1, -1, -1, -1, -1]:
            txt_name = img_info.split('.')[0] + '.txt'
            indx = img_path.find('CULane')
            path = PATH + img_path[indx:]
            if not os.path.exists(path):
                os.makedirs(path)
            with open(os.path.join(path, txt_name), 'w') as f_handle:
                f_handle.write(str(key_points))
            return True, key_points
        else:
            return False, key_points
    else:
        for line in range(lines_num):
            temp = [(i - left) * TARGET_SIZE[0] / MID_SIZE[0] for i in x_points_set[line]]
            x_points_new.append(temp)
            temp = [i * TARGET_SIZE[1] / MID_SIZE[1] for i in y_points_set[line]]
            y_points_new.append(temp)

        temp_idx = 0
        for i in range(lines_num - 1):
            fst_cross = get_cross_point([x_points_new[i][0], y_points_new[i][0], x_points_new[i][-1], y_points_new[i][-1]],
                                        [x_points_new[i + 1][0], y_points_new[i + 1][0], x_points_new[i + 1][-1], y_points_new[i + 1][-1]])
            if fst_cross is not None:
                temp_idx = i
                break
        sed_cross = get_cross_point([x_points_new[temp_idx][0], y_points_new[temp_idx][0], x_points_new[temp_idx][-1], y_points_new[temp_idx][-1]],
                                    [x_points_new[-1][0], y_points_new[-1][0], x_points_new[-1][-1], y_points_new[-1][-1]])
        print('[Info]: fst_cross and sed_cross ', fst_cross, sed_cross)
        if fst_cross is None or sed_cross is None:
            return False, key_points

        if (abs(fst_cross[0] - sed_cross[0]) + abs(fst_cross[1] - sed_cross[1])) < 30:
            center_x_temp = (fst_cross[0] + sed_cross[0]) // 2
            print('[Info]: center_x_temp, fst_cross, sed_cross are ', center_x_temp, fst_cross, sed_cross)
            for line in range(lines_num):
                line_x = x_points_new[line]
                line_y = y_points_new[line]
                temp_cross = get_cross_point([line_x[0], line_y[0], line_x[-1], line_y[-1]], x_axis)
                if temp_cross is not None:
                    if line == 0:
                        left_point = temp_cross
                        right_point = temp_cross
                        left_idx = 0
                        right_idx = 0
                        continue

                    if temp_cross[0] < center_x_temp:
                        if left_point[0] < center_x_temp:
                            if left_point[0] < temp_cross[0]:
                                left_point = temp_cross
                                left_idx = line
                        else:
                            left_point = temp_cross
                            left_idx = line
                    else:
                        if right_point[0] > center_x_temp:
                            if right_point[0] > temp_cross[0]:
                                right_point = temp_cross
                                right_idx = line
                        else:
                            right_point = temp_cross
                            right_idx = line
                else:
                    print('[Warning]', img_path_info)
                    return False, key_points

            center_cross = get_cross_point(
                [x_points_new[left_idx][0], y_points_new[left_idx][0], x_points_new[left_idx][-1],
                 y_points_new[left_idx][-1]],
                [x_points_new[right_idx][0], y_points_new[right_idx][0], x_points_new[right_idx][-1],
                 y_points_new[right_idx][-1]])
            if left_point[0] < 0:
                left_point = get_cross_point(
                    [x_points_new[left_idx][0], y_points_new[left_idx][0], x_points_new[left_idx][-1],
                     y_points_new[left_idx][-1]],
                    y_axis)
            elif left_point[0] > TARGET_SIZE[0]:
                left_point = get_cross_point(
                    [x_points_new[left_idx][0], y_points_new[left_idx][0], x_points_new[left_idx][-1],
                     y_points_new[left_idx][-1]],
                    y_axis_r)
            if right_point[0] > TARGET_SIZE[0]:
                right_point = get_cross_point(
                    [x_points_new[right_idx][0], y_points_new[right_idx][0], x_points_new[right_idx][-1],
                     y_points_new[right_idx][-1]],
                    y_axis_r)
            elif right_point[0] < 0:
                right_point = get_cross_point(
                    [x_points_new[right_idx][0], y_points_new[right_idx][0], x_points_new[right_idx][-1],
                     y_points_new[right_idx][-1]],
                    y_axis)

            print('[Info]: left_point={0}, right_point={1}, center_cross={2}'.format(left_point, right_point, center_cross))
            if (center_cross is not None) and (left_point is not None) and (right_point is not None):
                key_points = center_cross + left_point + right_point
            else:
                key_points = [-1, -1, -1, -1, -1, -1]

            print('[Info]: Key_points is:', key_points)
            if key_points != [-1, -1, -1, -1, -1, -1]:
                txt_name = img_info.split('.')[0] + '.txt'
                indx = img_path.find('CULane')
                path = PATH + img_path[indx:]
                if not os.path.exists(path):
                    os.makedirs(path)
                with open(os.path.join(path, txt_name), 'w') as f_handle:
                    f_handle.write(str(key_points))
                return True, key_points
            else:
                return False, key_points
        else:
            print('[Warning]', img_path_info)
            return False, key_points


def adjust_param(line_a, line_b):
    cross_point = utils.get_cross_point(line_a, line_b)
    print(line_a, line_b, cross_point)
    length = 1048
    if cross_point[0] <= length / 2:
        left = 0
        right = length
    elif cross_point[0] + length / 2 > 1640:
        left = int(1640 - length / 2)
        right = 1640
    else:
        left = int(cross_point[0] - length / 2)
        right = int(cross_point[0] + length / 2)

    print('=======', left, right, cross_point, abs(left - right))
    return left, right


def pre_resize(img, left, right, img_path, img_name):
    new_img = img[:, left:right, :]
    dst = cv2.resize(new_img, TARGET_SIZE, interpolation=cv2.INTER_AREA)
    idx = img_path.find('CULane')
    path = PATH + img_path[idx:]
    if not os.path.exists(path):
        os.makedirs(path)
    cv2.imwrite(os.path.join(path, img_name), dst)
    return dst


if __name__ == '__main__':
    cnt = 0
    data_path = 'F:\\BaiduNetdiskDownload\\Dataset\\CULane\\'
    for root, dirs_labels, file_names in os.walk(data_path):  # Iterate label files
        print('=====', root, dirs_labels)
        for img_name in file_names:
            if (img_name[-4:] == ".jpg") and (img_name[:4] != "new_"):  # find picture and txt file
                # img_path_info = utils.search_file(img_path, img_name)
                img_path_info = os.path.join(root, img_name)
                img_label = os.path.join(root, img_name[:-3] + 'lines.txt')
                if os.path.isfile(img_path_info) and os.path.isfile(img_label):
                    print('[Begin]: ----------------Process Image name: ', img_path_info)
                    rvl, lines, X_points, Y_points = proc_label(img_label)  # Read and process label files
                    cnt += 1
                    if len(lines) == 1:
                        continue

                    if rvl:
                        img_mat = cv2.imread(img_path_info)
                        # left, right = adjust_param(line_a, line_b)  # Calculate cutting size：1640*590 -->1048*590
                        temp_sift = random.randrange(0, 50)
                        left = 200 + temp_sift
                        right = 1248 + temp_sift
                        print('[Info]: Left={0} right={1} and size={2} '.format(left, right, right - left))
                        rvl2, key_points_set = find_target_point(X_points, Y_points, left, right, root, img_name)
                        print('[Info]: Key point={0} State={1} Path={2} {3}:'.format(key_points_set, rvl2, root, img_name))
                        if rvl2:
                            img_new = pre_resize(img_mat, left, right, root, img_name)
                            cv2.line(img_new, (int(key_points_set[0]), int(key_points_set[1])),
                                     (int(key_points_set[2]), int(key_points_set[3])), (255, 0, 0), 2)
                            cv2.line(img_new, (int(key_points_set[0]), int(key_points_set[1])),
                                     (int(key_points_set[4]), int(key_points_set[5])), (255, 255, 0), 2)

                        img_mat = utils.draw_culane(img_mat, lines)
                        cv2.imshow('ShowTag0', img_mat)
                        cv2.imshow('ShowTag', img_new)
                        # cv2.waitKey(1)
                        if cv2.waitKey(1) & 0xFF == ord(' '):
                            cv2.waitKey(0)
                    else:
                        img_mat = cv2.imread(img_path_info)
                        txt_name = img_name.split('.')[0] + '.txt'
                        idx = root.find('CULane')
                        path = PATH + root[idx:]
                        if not os.path.exists(path):
                            os.makedirs(path)
                        with open(os.path.join(path, txt_name), 'w') as handle:
                            handle.write(str([-1, -1, -1, -1, -1, -1]))
                        left, right = 0, 1048
                        img_new = pre_resize(img_mat, left, right, root, img_name)
                        cv2.imshow('ShowTag0', img_mat)
                        cv2.imshow('ShowTag', img_new)
                        # cv2.waitKey(1)
                        if cv2.waitKey(1) & 0xFF == ord(' '):
                            cv2.waitKey(0)

                        # with open('no_process_img.log', 'a') as log_handle:
                        #     log_handle.write(img_path_info + '\n')
                else:
                    print('[Warning]: Can not process img!')

    print('[Info]: Total images processed is  ', cnt)

