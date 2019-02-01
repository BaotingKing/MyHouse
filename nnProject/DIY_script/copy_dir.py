#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/12/29
"""
    Purpose: 利用Python实现目录拷贝
"""
import os
import shutil


def core_copy_dir(file_infor, dst_path):
    shutil.copy(copy_info, dst_path)


if __name__ == '__main__':
    print('###############################')
    file_names = 'pano.txt'
    compress_name = 'image_relt'
    src_path = '/home/zach/Downloads/pp/'
    dst_path = os.path.join(os.getcwd(), compress_name)
    with open(file_names, 'r') as file_handle:
        for one_record in file_handle:
            file_name = one_record.strip()    # 删除特殊字符，小心window和Linux系统字符有区别
            copy_info = os.path.join(src_path, file_name)
            dst_info = os.path.join(dst_path, file_name)
            if False:
                '''Linux OS: shell method to copy directory'''
                order = 'cp -r {0} {1}'.format(copy_info, dst_path)
                print order
                os.system(order)
            else:
                '''利用纯Python实现目录拷贝'''
                if os.path.isdir(copy_info):
                    shutil.copytree(copy_info, dst_info)
                elif os.path.isfile(copy_info):
                    pass

        if os.path.isdir(dst_path):
            shutil.make_archive(compress_name, 'gztar', dst_path)