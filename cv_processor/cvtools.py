# -*- coding: utf-8 -*-
"""
Created on 2018-07-25 星期三 14：04
@author: zhang baoting
"""
import sys, cv2, os, time, sqlite3, collections, hashlib
# import cpuid, pika
# import ConfigParser
# from matplotlib import pyplot as plt
from random import shuffle
# from Crypto.Cipher import AES
# from Crypto import Random
from hashlib import md5
import xml.etree.ElementTree as ET
import numpy as np


def CheckLicence():
    pass


def CheckFolderExists(foldername):
    """
    判断folder是否存在，不存在的话就创建相应的folder
    注意：foledername是指同级目录下面的文件夹名
    """
    if os.path.exists(foldername):
        os.makedirs(foldername)


# ====================================================
# ===============This is for box operation============
# ===============This is for box operation============
def UpandDownPoint(Boxes):
    """将boxes的（左下，右上）转换为（左上， 右下）"""
    Boxes[:, [1, 3]] = Boxes[:, [3, 1]]


def DownandUpPoint():
    pass


def ExtendBox(Boxes, dim, pixelthd=36):
    """将box的某一边放大到pixelthd大小"""
    for i in range(Boxes.shape[0]):
        single_box = Boxes[i, :]
        if single_box[dim] > single_box[dim + 2]:
            edgelength = single_box[dim] - single_box[dim + 2]
        else:
            edgelength = single_box[dim + 2] - single_box[dim]

        if edgelength < pixelthd:
            diff = (pixelthd - edgelength) / 2.0
            single_box[dim]     = int(single_box[dim] - diff)
            single_box[dim + 2] = int(single_box[dim + 2] + diff)
        elif edgelength > pixelthd:
            diff = (edgelength - pixelthd) / 2.0
            single_box[dim] = int(single_box[dim] + diff)
            single_box[dim + 2] = int(single_box[dim + 2] - diff)


def BoxOverlap(Region1, Region2):
    """
        Func: Find the overlap area
        Note: RegionX is box, it is 1d ndarray;（up point and down point）
    """
    if (Region1[0] > Region2[2]) | (Region1[1] < Region2[3]):
        return 0
    if (Region1[2] < Region2[0]) | (Region1[3] > Region2[1]):
        return 0

    width  = min(Region1[2], Region2[2]) - max(Region1[0], Region2[0])
    height = min(Region1[1], Region2[1]) - max(Region1[3], Region2[3])
    intersection_area = width * height
    region1_area = (Region1[1] - Region1[3]) * (Region1[2] - Region1[0])
    region2_area = (Region2[1] - Region2[3]) * (Region2[2] - Region2[0])
    # another way:
    # if (Region1[0] > Region2[2])|(Region1[1] > Region2[3])|
    #     (Region1[2] < Region2[0])|(Region1[3] < Region2[1]):
    #     return 0
    # Width = min(Region1[2], Region2[2]) - max(Region1[0], Region2[0])
    # Height = min(Region1[3], Region2[3]) - max(Region1[1], Region2[1])
    # IntersectionArea = Width * Height
    # Area1 = (Region1[3] - Region1[1]) * (Region1[2] - Region1[0])
    # Area2 = (Region2[3] - Region2[1]) * (Region2[2] - Region2[0])

    if region1_area + region2_area - intersection_area == 0:
        return 1000
    else:
        return intersection_area * 1.0 / (region1_area + region2_area - intersection_area)


def MergeBoxes(boxes, threshold=0):
    """
        Func: IOU boxes merge,
            and finalBoxes are completely independent of one another.
        Note: Up point and down point
    """
    finalBoxes = np.zeros((0, 4))  # finalBoxes = np.zeros((0, 5))
    mergedboxes = boxes[0:1, :].copy()
    leftboxes = boxes[1:, :].copy()
    while leftboxes.shape[0] > 0:
        IOU = np.zeros((leftboxes.shape[0], 1))
        for i in range(leftboxes.shape[0]):
            IOU[i, 0] = BoxOverlap(mergedboxes[0, :], leftboxes[i, :])
        index = IOU[:, 0] >= threshold

        if not index.any():
            finalBoxes = np.concatenate((finalBoxes, mergedboxes), 0)  # add unIOU box
            mergedboxes = leftboxes[0:1, :].copy()   # update
            leftboxes = leftboxes[1:, :].copy()  # update left boxes
        else:
            crossedboxes = np.concatenate((mergedboxes, leftboxes[index, :]), 0)
            mergedboxes = np.array(
                [crossedboxes[:, 0].min(), crossedboxes[:, 1].max(),
                 crossedboxes[:, 2].max(), crossedboxes[:, 3].min()])
            # another way:
            # mergedboxes = np.array(
            #     [CrossedBoxes[:, 0].min(), CrossedBoxes[:, 1].min(),
            #      CrossedBoxes[:, 2].max(), CrossedBoxes[:, 3].max(),
            #      CrossedBoxes[:, 4].max()])
            mergedboxes = mergedboxes.reshape((1, 4))
            leftboxes = leftboxes[False == index, :].copy()  # update left boxes
    finalBoxes = np.concatenate((finalBoxes, mergedboxes), 0)
    return finalBoxes

# ====================================================
# ===============This is for Draw operation============
# ===============This is for Draw operation============
def DrawBoxes(boxes):
    pass








