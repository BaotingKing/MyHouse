#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/12/29
import re
import os
import sys

import config

def core_fun(img_names, image_type='examine'):
    """统计文件夹中图片数量"""
    token_set = []
    stat_0 = []
    stat_1 = []
    stat_2 = []
    stat_3 = []
    stat_4 = []
    stat_5 = []
    for img in img_names:
        img_token = img[0:18]
        if img_token in token_set:
            continue
        else:
            token_set.append(img_token)

        cnt = 0
        for i_img in img_names:
            i_token = i_img[0:18]
            if img_token == i_token:
                if image_type in i_img:
                    cnt += 1
        if cnt == 0:
            stat_0.append(img_token)
        elif cnt == 1:
            stat_1.append(img_token)
        elif cnt == 2:
            stat_2.append(img_token)
        elif cnt == 3:
            stat_3.append(img_token)
        elif cnt == 4:
            stat_4.append(img_token)
        else:
            stat_5.append(img_token)

    print("There's a list of 0 images:\n    total = {0}, list = {1}".format(len(stat_0), stat_0))
    print("There's a list of 1 images:\n    total = {0}, list = {1}".format(len(stat_1), stat_1))
    print("There's a list of 2 images:\n    total = {0}, list = {1}".format(len(stat_2), stat_2))
    print("There's a list of 3 images:\n    total = {0}, list = {1}".format(len(stat_3), stat_3))
    print("There's a list of 4 images:\n    total = {0}, list = {1}".format(len(stat_4), stat_4))






def statistic(dir_merge):
    img_list = []
    for root, dirs_labels, file_names in os.walk(dir_merge):  # Iterate label files
        for case_name in file_names:
            timestamp = case_name.split()[0][0:13]
            if (case_name[-3:] == "jpg" and int(timestamp) > config.start_time
                    and int(timestamp) < config.stop_time):
                img_list.append(case_name)
        # print(img_list)
        core_fun(img_list)


if __name__ == '__main__':
    stdout_backup = sys.stdout  # make a copy of original stdout route
    if len(sys.argv) > 1:
        for file_name in sys.argv[1:]:
            log_name = file_name + '.log'
            log_name = 'statistic.log'
            log_file = open(log_name, "w")
            sys.stdout = log_file
            statistic(file_name)
            print('Analyse is ok')
            log_file.close()
    else:
        print('###############################')
        file_dir = 'F:\\MyHouse\\nnProject\\DIY_script\\imsave\\yancan'
        for file_name in file_dir:
            log_name = file_name + '.log'
            log_name = 'statistic.log'
            log_file = open(log_name, "w")
            sys.stdout = log_file
            statistic(file_dir)
            print('Analyse is ok')
            log_file.close()
    # restore the output to initial pattern
    sys.stdout = stdout_backup