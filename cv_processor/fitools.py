#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Zhang.Baoting
# Time: 2018/7/26

import os


def creatLabelTxt(path, data_set_name, sub_labels_flag=0):
    i = 0  # 标签
    with open(path + '\\' + data_set_name, "w") as train_txt:
        for root, dirs_labels, _ in os.walk(path):  # 遍历各种label文件夹
            for label in dirs_labels:  # 遍历某一个label文件夹里面所有的文件和文件夹
                if 0 == sub_labels_flag:
                    for _, _, files in os.walk(path + '\\' + str(label)):
                        for file in files:
                            image_file = str(label) + "_" + str(file)
                            label_name = image_file + ' ' + str(i) + '\n'  # 文件路径+空格+标签编号+换行
                            train_txt.writelines(label_name)
                elif 1 == sub_labels_flag:
                    for _, sub_labels, _ in os.walk(path + '\\' + str(label)):
                        for subclass in sub_labels:
                            for _, _, files in os.walk(path + '\\' + str(label) + '\\' + str(subclass)):
                                for file in files:
                                    image_file = str(label) + "_" + str(file)
                                    label_name = image_file + ' ' + str(i) + '\n'  # 文件路径+空格+标签编号+换行
                                    train_txt.writelines(label_name)
                i += 1  # 类型编号加1
    return 0


def openTrainFile(filepath, categories):
    categorytrainlist = []
    for i in range(1, len(categories)):
        categorytrainlist.append(open(filepath + categories[i] + '_train.txt', 'w'))
        categorytrainlist.append(open(filepath + categories[i] + '_test.txt', 'w'))
    return categorytrainlist


def writeTrainFile(categorytrainlist, labels, categories, imname):
    for i in range(len(categorytrainlist)):
        singlelabel = i / 2 + 1
        if (labels == singlelabel).any():
            categorytrainlist[i].write(imname + ' ' + '1' + '\n')
        else:
            categorytrainlist[i].write(imname + ' ' + '-1' + '\n')


def closeTrainFile(categorytrainlist):
    for singlefile in categorytrainlist:
        singlefile.close()
