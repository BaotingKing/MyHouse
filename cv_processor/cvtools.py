# -*- coding: utf-8 -*-
"""
Created on 2018-07-25 星期三 14：04
@author: zhang baoting
"""
import sys, cv2, os, time, sqlite3, collections, hashlib
# import cpuid,pika
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

"""
This is for box operation
"""
def UpandDownPoint(Boxes):
    """将boxes的（左下，右上）转换为（左上， 右下）"""
    Boxes[:, [1, 3]] = Boxes[:, [3, 1]]



def DownandUpPoint():
    pass

def ExtendBox(Boxes, dim, pixelthd = 36):
    """将box的某一边放大到pixelthd大小"""
    for i in range(Boxes.shape[0]):
        singleBox = Boxes[i, :]
        if(singleBox[dim] > singleBox[dim + 2]):
            edgelength = singleBox[dim] - singleBox[dim + 2]
        else:
            edgelength = singleBox[dim + 2] - singleBox[dim]

        if edgelength < pixelthd:
            diff = (pixelthd - edgelength) / 2.0
            singleBox[dim]     = int(singleBox[dim] - diff)
            singleBox[dim + 2] = int(singleBox[dim + 2] + diff)
        elif edgelength > pixelthd:
            diff = (edgelength - pixelthd) / 2.0
            singleBox[dim] = int(singleBox[dim] + diff)
            singleBox[dim + 2] = int(singleBox[dim + 2] - diff)

def BoxOverlap(Region1, Region2):
    """
        Note: RegionX is box, it is 1d ndarray;
        Func: Find the overlap area
    """
    if Region1[0] > Region2[0]:
        return 0
    if Region1[1] > Region2[0]:
        return 0

def MergeBoxes(Boxes, threshold = 0):
    FinalBoxes = np.zeros((0, 5))


