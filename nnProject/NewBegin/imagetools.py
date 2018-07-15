# -*- coding: utf-8 -*-
#
# __author__ = 'Baoting Zhang'
# Time:        2018-05-05 to 2018-07-13
#       for myself

import os

def get_imlist(path, suffix):
    """返回同级目录中所有JPG图像的文件名列表"""
    pathlist = []
    for filename in os.listdir(path):
        if filename.endswith(suffix):
            pathlist.append(os.path.join(path, filename))

    # return [os.path.join(path, f) for f in os.listdir(path) if f.endswith(suffix)]
    return pathlist



