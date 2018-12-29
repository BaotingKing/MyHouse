#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/12/29
"""
    Purpose: For analysis of common log format analysis,
            core functions can be modified as required
"""
import os
import re
import sys


def log_create(path):
    try:
        if os.path.isdir(path):
            path_file = os.path.split('PATH')
        elif os.path.isfile(path):
            file_name = os.path.split()
            if '\\' or '/' in path:
                file_name = path.split('\\' or '/')
                log_name = file_name + '.log'
                log_file = open(log_name, "w")
        else:
            print
            "it's a special file(socket,FIFO,device file)"
    except:
        pass


def str_to_dict(info, head):
    p1 = re.compile(r'[{](.*?)[}]', re.S)  # 最小匹配{}
    p2 = re.compile(r'[{](.*)[}]', re.S)    # 最大匹配{}
    info_temp = str(info)
    list_temp = re.findall(p2, info_temp)
    info_list = str(list_temp)[2:-2]       # 规避python未知的问题，待修复2018-12-29
    info_list = '{' + info_list + '}'
    return eval(info_list)


def core_fun(information, cnt_error, check_key):
    check_item = information[check_key]
    cnt = 0
    for key_name in ['examine_img_back', 'examine_img_left', 'examine_img_front', 'examine_img_right']:
        if '.jpg' in check_item[key_name]:
            cnt += 1
    if cnt != 4:
        print('This timestamp {0} is error:\n'
              '     crane = {1}\n'
              '     number= {2}\n'
              '     number= {3}\n'.format(information['AdditionalInfo']['timestamp'],
                                          information['AdditionalInfo']['crane'],
                                          information['DetectResultCam1']['number'],
                                          information['DetectResultCam2']['number']))
    # else:
    #     print('This timestamp {0} is ok:\n '.format(information['AdditionalInfo']['timestamp']))


def analyze_log(file):
    with open(file, 'r', encoding='UTF-8') as log_handle:
        cnt_flg = 0
        for one_record in log_handle:
            one_record = one_record.strip()
            if 'AdditionalInfo' in one_record:
                record_infor = str_to_dict(one_record, 'AdditionalInfo')
                if record_infor == {}:      # TODO 2018-12-29
                    continue

                core_fun(record_infor, cnt_flg, 'ExamineInfo')


if __name__ == '__main__':
    stdout_backup = sys.stdout  # make a copy of original stdout route
    if len(sys.argv) > 1:
        for file_name in sys.argv[1:]:
            log_name = file_name + '.log'
            log_file = open(log_name, "w")
            sys.stdout = log_file
            analyze_log(file_name)
            print('Analyse is ok')
            log_file.close()
    else:
        print('###############################')
        file_names = ['F:\\MyHouse\\nnPrject\\DIY_script\\CraneDataSender.log']
        for file_name in file_names:
            a, b = os.path.split(file_name)
            log_create(file_name)
            log_name = file_name + '.log'
            log_file = open(log_name, "w")
            sys.stdout = log_file
            analyze_log(file_name)
            print('Analyse is ok')
            log_file.close()
    # restore the output to initial pattern
    sys.stdout = stdout_backup
