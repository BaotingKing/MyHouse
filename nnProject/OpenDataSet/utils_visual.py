#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: ZK
# Time: 2019/10/11 18:08
import os
import re
import sys
import time
import cv2
import numpy as np
import random
from pycocotools import mask as maskUtils


# ***************************************************************************************
# *
# *    little tools
# *
# ***************************************************************************************
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
    target_file_path = None
    for parent, dirnames, filenames in os.walk(rootdir):
        if target_file in filenames:
            target_file_path = os.path.join(parent, target_file)
            break
    return target_file_path


# ***************************************************************************************
# *
# *    Fun:Mask show Fun
# *    Tips: It can been used for mask check!
# ***************************************************************************************
def apply_mask(image, mask, color, alpha=0.5):
    """Apply the given mask to the image.
    """
    for c in range(3):
        image[:, :, c] = np.where(mask == 1,
                                  image[:, :, c] *
                                  (1 - alpha) + alpha * color[c] * 255,
                                  image[:, :, c])
    return image


def annToRLE(ann, height, width):
    """
    Convert annotation which can be polygons, uncompressed RLE to RLE.
    :return: binary mask (numpy 2D array)
    """
    segm = ann['segmentation']
    if isinstance(segm, list):
        # polygon -- a single object might consist of multiple parts
        # we merge all parts into one mask rle code
        rles = maskUtils.frPyObjects(segm, height, width)
        rle = maskUtils.merge(rles)
    elif isinstance(segm['counts'], list):
        # uncompressed RLE
        rle = maskUtils.frPyObjects(segm, height, width)
    else:
        # rle
        rle = ann['segmentation']
    return rle


def annToMask(ann, height, width):
    """
    Convert annotation which can be polygons, uncompressed RLE, or RLE to binary mask.
    :return: binary mask (numpy 2D array)
    """
    rle = annToRLE(ann, height, width)
    m = maskUtils.decode(rle)
    return m


def load_mask(annotation, height, width):
    """Load instance masks for the given image.
    Different datasets use different ways to store masks. This
    function converts the different mask format to one format
    in the form of a bitmap [height, width, instances].
    Returns:
    masks: A bool array of shape [height, width, instance count] with
        one mask per instance.
    class_ids: a 1D array of class IDs of the instance masks.
    """
    instance_masks = []
    class_ids = []

    # Build mask of shape [height, width, instance_count] and list
    # of class IDs that correspond to each channel of the mask.
    class_id = annotation['category_id']
    m = annToMask(annotation, height, width)
    # Some objects are so small that they're less than 1 pixel area
    # and end up rounded out. Skip those objects.
    if m.max() < 1:
        pass
    else:
        # Is it a crowd? If so, use a negative class ID.
        if annotation['iscrowd']:
            # Use negative class ID for crowds
            class_id *= -1
            # For crowd masks, annToMask() sometimes returns a mask
            # smaller than the given dimensions. If so, resize it.
            if m.shape[0] != height or m.shape[1] != width:
                m = np.ones([height, width], dtype=bool)
        instance_masks.append(m)
        class_ids.append(class_id)

    # Pack instance masks into an array
    if class_ids:
        mask = np.stack(instance_masks, axis=2).astype(np.bool)
        class_ids = np.array(class_ids, dtype=np.int32)
        return mask, class_ids
    else:
        print("You are using the default load_mask(), maybe you need to define your own one.")
        mask = np.empty([0, 0, 0])
        class_ids = np.empty([0], np.int32)
        return mask, class_ids
