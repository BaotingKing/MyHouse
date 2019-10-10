#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: ZK
# Time: 2019/10/09 18:56
"""    Dataset is come from: http://groups.csail.mit.edu/vision/SUN/"""
import json
from xml.dom.minidom import Document
import xml.etree.ElementTree as ET
import os
import re
import time
import cv2
import numpy as np
import random


def search_file(rootdir, target_file):
    target_file_path = None
    for parent, dirnames, filenames in os.walk(rootdir):
        if target_file in filenames:
            target_file_path = os.path.join(parent, target_file)
            break
    return target_file_path


KEY_CLASS = ['grass']
class_need = ['wall', 'sky', 'trees', 'person', 'grass', 'ground', 'river water']    # The name is original label name
std_class_ind = {'wall': 'wall',
                 'sky': 'sky',
                 'trees': 'trees',
                 'person': 'person',
                 'grass': 'grass',
                 'ground': 'ground',
                 'river water': 'river'
                 }
std_class_ID = {'wall': 0,
                'sky': 1,
                'trees': 2,
                'person': 3,
                'grass': 4,
                'ground': 5,
                'river': 6
                }

img_list_path = "G:\\Dataset\\SUN\\test.txt"
objs_anno_path = "G:\\Dataset\\SUN\\SUN2012pascalformat\\SUN2012pascalformat\\Annotations\\"
objs_segm_path = "G:\\Dataset\\SUN\\SUN2012\\SUN2012\\Annotations\\"
DATASET_PATH = "G:\\Dataset\\SUN\\SUN2012pascalformat\\SUN2012pascalformat\\JPEGImages\\"


def randomcolor():
    colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    rgb = []
    for i in range(3):
        color = ""
        for j in range(2):
            color += colorArr[random.randint(0, 14)]
        rgb.append(int(color, 16))
    return tuple(rgb)


def extract_xml(obj_anno, type='Anno'):
    if True:
        text = open(obj_anno).read()
        text = re.sub(u"[\x00-\x08\x0b-\x0c\x0e-\x1f]+", u"", text)
        root = ET.fromstring(text)
    else:
        tree = ET.parse(obj_anno_path)
        root = tree.getroot()

    object_info_list = []
    img_info_set = {}
    if type == 'Anno':
        contain_classes = []
        for obj in root.findall('object'):  # 提取图片中bbox信息
            label = str(obj.find('name').text).strip()
            contain_classes.append(label)
            bbox = obj.find('bndbox')
            object_ = {
                "class": label,  # bbox的左上角坐标和width、height
                "bbox": {
                    "x": int(bbox.find('xmin').text),
                    "y": int(bbox.find('ymin').text),
                    "w": int(bbox.find('xmax').text) - int(bbox.find('xmin').text),
                    "h": int(bbox.find('ymax').text) - int(bbox.find('ymin').text)
                }
            }
            object_info_list.append(object_)
        info = root.find('size')
        img_name = str(root.find('filename').text).strip()
        img_info_set = {
            "img_name": img_name,
            "path": search_file(DATASET_PATH, img_name),
            "classes_set": contain_classes,
            "width": int(info.find('width').text),
            "height": int(info.find('height').text),
            "depth": int(info.find('depth').text)
        }
    elif type == 'Segm':
        for obj in root.findall('object'):  # 提取图片中segmentaion信息
            label = str(obj.find('name').text).strip()
            polygon = obj.find('polygon')
            segm_info = []
            for obj in polygon.findall('pt'):
                x = int(obj.find('x').text)
                y = int(obj.find('y').text)
                segm_info.append(x)
                segm_info.append(y)
            object_ = {
                "class": label,  # segm按照x和y依次摆放
                "segmentation": segm_info
            }
            object_info_list.append(object_)
    return object_info_list, img_info_set


def check_bbox_segm(bbox, segm):
    x_min = bbox['x']
    y_min = bbox['y']
    x_max = bbox['w'] + bbox['x']
    y_max = bbox['h'] + bbox['y']
    x_set = segm[::2]
    y_set = segm[1::2]
    if (min(x_set) >= x_min) or (max(x_set) <= x_max) or (min(y_set) >= y_min) or (max(y_set) <= y_max):
        return True
    else:
        return False


def tran_proc():        # 直接从segmentation标签集提取有用信息
    cnt = 0
    cnt_n = 0
    cnt_m = 0
    begin = time.clock()
    with open(img_list_path, 'r', encoding='UTF-8') as file_handle:
        whole_label_list = []
        for one_record in file_handle:
            cnt += 1
            xml_name = str(one_record).strip() + '.xml'
            obj_anno_path = search_file(objs_anno_path, xml_name)  # 存放image信息和bbox等信息
            obj_segm_path = search_file(objs_segm_path, xml_name)  # 存放polygon信息
            if os.path.isfile(obj_anno_path) and os.path.isfile(obj_segm_path):
                print(cnt, one_record)
                anno_list, img_info = extract_xml(obj_anno_path)
                if len(list(set(KEY_CLASS).intersection(set(img_info['classes_set'])))) != 0:
                    segm_list, _ = extract_xml(obj_segm_path, type='Segm')
                    cnt_n += 1
                    obj_info = []
                    for idx in range(len(segm_list)):
                        if segm_list[idx]['class'] in class_need:
                            std_class_name = std_class_ind[segm_list[idx]['class']]
                            segm_info = segm_list[idx]['segmentation']
                            bbox = [
                                min(segm_info[::2]),
                                min(segm_info[1::2]),
                                max(segm_info[::2]) - min(segm_info[::2]),
                                max(segm_info[1::2]) - min(segm_info[1::2])
                            ]
                            obj_ = {
                                "class": std_class_name,
                                "category_id": std_class_ID[std_class_name],
                                "segmentation": [segm_info],
                                "iscrowd": 0,
                                "bbox": bbox
                            }
                            obj_info.append(obj_)
                    if len(obj_info) != 0:
                        cnt_m += 1
                        img_info_dict = {
                            "img_name": img_info['img_name'],
                            "path": img_info['path'],
                            "height": img_info['height'],
                            "width": img_info['width'],
                            "depth": img_info['depth'],
                            "object": obj_info
                        }
                        whole_label_list.append(img_info_dict)
        whole_label_dict = {"annotations": whole_label_list}
    with open("test_label.json", 'w') as out_file:
        json.dump(whole_label_dict, out_file, ensure_ascii=False, indent=2)

    end = time.clock()
    total = end - begin
    print(cnt, cnt_n, cnt_m)
    print("Total time is: ", total)


def ver_sun():
    ROOT_DIR = os.path.abspath('')  # Root directory of the project
    DEFAULT_SAVE_DIR = os.path.join(ROOT_DIR, "cityscapes")
    label_path = os.path.join(DEFAULT_SAVE_DIR, "train")
    with open("label.json", 'r') as f:
        infile = json.load(f)
    cnt = 0
    for img_info in infile['annotations']:
        cnt += 1
        print(cnt, img_info['img_name'])
        img_path = img_info['path']
        img = cv2.imread(img_path)
        cv2.imshow('000', img)
        objects = img_info['object']
        for obj in objects:
            points = []
            rng = randomcolor()
            segmentation = obj['segmentation'][0]
            bbox = obj['bbox']
            for i in range(int(len(segmentation) / 2)):
                points.append([segmentation[i * 2], segmentation[i * 2 + 1]])
            pts = np.array(points, np.int32)
            cv2.rectangle(img, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), rng, 3)
            cv2.putText(img, obj['class'], (bbox[0], bbox[1]), cv2.FONT_HERSHEY_PLAIN, 2.0, rng, 2, 1)
            cv2.polylines(img, [pts], True, rng, 2)

        cv2.imshow('111', img)
        cv2.waitKey(0)


if __name__ == '__main__':
    tran_proc()
    ver_sun()