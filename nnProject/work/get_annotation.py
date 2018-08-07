# -*- coding: utf-8 -*-


import os.path as osp
import xml.etree.ElementTree as ET

import cv2
import numpy as np
import os
import scipy.io as sio
import shutil
import sys
# sys.path.insert(0, '/home/wy/Documents/workspace/analysis/code/basic')

import cv_utils as util


# src_dir = '/home/wy/disks/disk0/compress-file/plate/dinghuo/mainTask-Export-20170905/plate/ROI'
# dst_dir = '/home/wy/disks/disk0/datasets/PlateGeneral/dinghuo_0905/plate/roi'
# src_dir = '/home/wy/disks/disk0/compress-file/plate/zhongmao/0908/plate/roi'
# dst_dir = '/home/wy/disks/disk0/datasets/PlateGeneral/zhongmao_0908/plate/roi'
src_dir = '/home/wy/disks/disk0/compress-file/Port/DongSenDC/gyf8.4/digit'
dst_dir = '/home/wy/disks/disk0/compress-file/Port/DongSenDC/gyf8.4/digit_'
db_str = 'digit'# 'letter','digit','type'
varify = False

def get_ano_dir(one_dir):
    return osp.join(one_dir, 'data', 'Annotations/')

def get_img_dir(one_dir):
    return osp.join(one_dir, 'data', 'JPEGImages/')

# Generate Annotations

imagepath = osp.join(src_dir, 'image/')
annotationpath = osp.join(src_dir, 'annotation/')

savePath = get_ano_dir(dst_dir)
varifyPath = osp.join(dst_dir, 'data/varify/')
imagesavepath = get_img_dir(dst_dir)

# debugpath = '/cv/Rongqi/digits/Letters/debug/'
if db_str == 'roi':
    element_list = ['wordh', 'numhl', 'numhs', 'wordv', 'numvl', 'numvs']
    img_format = '.jpg'
elif db_str == 'digit':
    img_format = '.bmp'
    element_list = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
elif db_str == 'letter':
    img_format = '.bmp'
    element_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                    'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
elif db_str == 'type':
    img_format = '.bmp'
    element_list = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
              'nine', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
              'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
else:
    print 'ERROR: wrong db_str'
    sys.exit(0)

# element_list=['plate']
if db_str == 'roi':
    groundtruth = ['background']
elif db_str in ['digit','letter','type']:
    groundtruth = []
else:
    sys.exit(0)
# groundtruth = ['background']
# groundtruth = []
groundtruth.extend(element_list)
# groundtruth = ['plate', 'plate', 'plate', 'plate']
print element_list
util.CheckFolderExists(imagesavepath)
util.CheckFolderExists(varifyPath)
util.CheckFolderExists(savePath)

imdelete = []
# print os.listdir(annotationpath)
for annotationname in os.listdir(annotationpath):
    print annotationname
    imname = annotationname.split('.')[0]
    print "{}{}".format(imname, img_format)
    if (not os.path.exists(osp.join(imagepath, imname + img_format))) or (not os.path.exists(osp.join(annotationpath, imname + '.mat'))):
        continue
    image = cv2.imread(osp.join(imagepath, imname + img_format))
    mat_contents = sio.loadmat(osp.join(annotationpath, imname + '.mat'))
    boxes = mat_contents['boxes']
    ### add wy
    # boxes = np.insert(boxes, 0, 1, axis=1)
    # print boxes

    if image.shape[0] * 1.0 / image.shape[1] > 10:
        print 'ratio>10: ', imname
        imdelete.append(annotationname)
    elif np.any(boxes[:, 1] >= boxes[:, 3]) or np.any(boxes[:, 2] >= boxes[:, 4]):
        print 'boxes wrong: ', annotationname
        print boxes
        imdelete.append(annotationname)
    elif np.any(boxes[:, 1:] < 0):
        print '<0: ', annotationname
        imdelete.append(annotationname)
    elif (boxes[:, 3] + 1 > image.shape[1]).any():
        index = (boxes[:, 3] + 1) > image.shape[1]
        boxes[index, 3] = image.shape[1] - 2
    if not varify:
        shutil.copy(osp.join(imagepath, imname + img_format), osp.join(imagesavepath, imname + img_format))
    imshape = np.array([image.shape[1], image.shape[0], image.shape[2]])  # weight,height,channel
    tree = ET.parse('example.xml')
    root = tree.getroot()
    filename = root.find('filename')
    filename.text = imname + img_format
    size = root.find('size')
    for i in range(len(size)):
        size[i].text = str(imshape[i])
    util.CreateObjInXML(root, boxes.shape[0] - 1)
    label = []
    namelabel = ''
    # print "boxes.shape{}".format(boxes.shape[0])
    for i in range(boxes.shape[0]):
        # print boxes[i,0]
        label.append(groundtruth[int(boxes[i, 0])])
        # print label
        namelabel += groundtruth[int(boxes[i, 0])]
    # print label
    util.AssignValueToObj(root, boxes[:, 1:5], label)
    if not varify:
        tree.write(osp.join(savePath, imname + '.xml'))
        for i in range(boxes.shape[0]):
            util.DrawLocation(image, boxes[i, 1:5])
        cv2.imwrite(osp.join(varifyPath, imname + '_' + namelabel + img_format), image)
    
for deletename in imdelete:
    os.remove(osp.join(annotationpath, deletename))

