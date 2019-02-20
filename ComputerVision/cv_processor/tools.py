#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Zhang.Baoting
# Time: 2018/7/26

import os

# 定义Caffe根目录
caffe_root = 'D:/home/zach/house/'
dir_merge = caffe_root + 'models/my_models/labels'   # 按照不同categories文件夹存放的根目录
# 制作训练标签数据
i = 0     # 标签
sub_labels_flag = 0   # 子类开关
with open(dir_merge + 'train_txt', "w") as train_txt:
    for root, dirs_labels, _ in os.walk(dir_merge):   # 遍历各种label文件夹
        for label in dirs_labels:    # 遍历某一个label文件夹里面所有的文件和文件夹
            if 0 == sub_labels_flag:
                for _, _, files in os.walk(dir_merge + '\\' + str(label) + '\\' + str(subclass)):
                    for file in files:
                        image_file = str(label) + "_" + str(file)
                        label_name = image_file + ' ' + str(i) + '\n'  # 文件路径+空格+标签编号+换行
                        train_txt.writelines(label_name)
            elif 1 == sub_labels_flag:
                for _, sub_labels, _ in os.walk(dir_merge + '\\' + str(label)):
                    for subclass in sub_labels:
                        for _, _, files in os.walk(dir_merge + '\\' + str(label) + '\\' + str(subclass)):
                            for file in files:
                                image_file = str(label) + "_" + str(file)
                                label_name = image_file + ' ' + str(i) + '\n'       # 文件路径+空格+标签编号+换行
                                train_txt.writelines(label_name)
            i += 1  # 类型编号加1














