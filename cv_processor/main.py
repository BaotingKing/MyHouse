# -*- coding: utf-8 -*-
"""
Created on 2018-07-25 星期三 14：04
@author: zhang baoting

for test function
"""
import cvtools as cvtl
import os
import numpy as np
import matplotlib.pyplot as plt
import fitools
import cv2
import UI
# boxes = np.arange(28).reshape(-1,4)
# print(boxes)

# ===========测试ExtendBox函数=========
# cvtl.ExtendBox(box, 0)
# cvtl.ExtendBox(box, 1)
print("===============================")


# ===========UpandDownPoint===========
# print(box)
# cvtl.UpandDownPoint(box)
# print(box)
print("===============================")


# ===========测试BoxOverlap函数=========
# Region1 = [2, 8, 5, 2]
# Region2 = [3, 6, 10, 2]
# are =cvtl.BoxOverlap(Region2, Region1)
# print(are)
# b = 8.0/38
# print(b)
print("===============================")

# ===========测试BoxOverlap函数=========
# np.random.seed(1)
# boxes = np.random.randint(0, 100, 28).reshape(-1, 4)
arr = [[3, 56, 20, 12],
         [12, 23, 20, 5],
         [50, 89, 80, 20],
         [12, 20, 40, 0],
         [6, 40, 52, 16],
         [18, 40, 20, 8],
         [2, 12, 8, 3]]
# boxes = np.array(arr)
# merge_box = cvtl.MergeBoxes(boxes, 0.2)
# print("boxes is %s" % boxes)
# print("merge_box is %s" % merge_box)


# ===========测试DrawBoxes函数=========
# cvtl.DrawBoxes(boxes)
# print("hi, boxes are drawn")
#
# plt.hold()
# cvtl.DrawBoxes(merge_box)
# print("hi, merge_box are drawn")

# ===========测试ShuffleFeature函数=========
# trainfeature = np.random.randint(0, 100, 28).reshape(-1, 4)
# trainlabel = np.arange(0, trainfeature.shape[0]).reshape(trainfeature.shape[0], -1)
#
# randomfreature, randomlabel = cvtl.ShuffleFeature(trainfeature, trainlabel)
# print("hi, before Shuffle trainfeature = ")
# print(trainfeature)
# print("hi, before Shuffle trainlabel = ")
# print(trainlabel)
#
# print("hi, after Shuffle randomfreature = ")
# print(randomfreature)
# print("hi, after Shuffle randomlabel = ")
# print(randomlabel)

# ===========测试drawLetters函数=========
# print("hi, 111111111111111111111111")
# image = cv2.imread("cat.jpg")
# resizedimage = cv2.resize(image, (1920, 1024))
# UI.drawLetters(resizedimage, "abcd 1234567 6666 True", 2, 150)
# cv2.imshow("cat", resizedimage)
# print("hi, 222222222222222222222222")

# ===========测试drawUI函数=========
# print("hi, 111111111111111111111111")
# image = cv2.imread("cat.jpg")
# paper = np.zeros([1017, 1909, 3], np.uint8)
# result = ['AAAA 0000000 0000 True', 'AAAA 0000000 0000 True']
# # for i in range(5):
# #         image = image
# #         if i == 0:
# #             resizedimage = cv2.resize(image, (560, 316))
# #             paper[376:692, 1349:1909, 0] = resizedimage[:, :, 0]
# #         elif i == 1:
# #             resizedimage = cv2.resize(image, (560, 316))
# #             paper[701:1017, 1349:1909, 1] = resizedimage[:, :, 1]
# #         elif i == 2:
# #             resizedimage = cv2.resize(image, (1329, 641))
# #             paper[376:1017, 10:1339, 2] = resizedimage[:, :, 2]
# #         elif i == 4:
# #             resizedimage = cv2.resize(image, (560, 316))
# #             paper[50:366, 1349:1909, :] = resizedimage
# papers = np.zeros([2, paper.shape[0], paper.shape[1], 3])
# images = np.zeros([4, image.shape[0], image.shape[1], 3])
# papers[0, :,:,:] = paper.copy()
# images[0, :,:,:] = image.copy()
# images[1, :,:,:] = image.copy()
# images[2, :,:,:] = image.copy()
# images[3, :,:,:] = image.copy()
#
# paper = UI.drawUI(images, papers, result, 1,1,'1','1')
# cv2.imshow('paper', paper)