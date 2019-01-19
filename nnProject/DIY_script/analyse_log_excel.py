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
import pandas as pd
# from numba import jit

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

# @jit
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

# @jit
def core_excel_func(file_handle, file_name):
    camera_set = []
    time_stamp = []
    camera_cont = []
    result_file = file_name[:-4] + '.csv'
    log_pd = pd.DataFrame(columns=['timestamp', 'camera_0', 'camera_1', 'camera_2', 'camera_3', 'camera_4'])
    for one_record in file_handle:
        time_array = one_record[:23]
        record_content = one_record.strip().split('-')[-1]
        if '*****************' in one_record:
            if len(camera_cont) != 0:
                camera_set.append(camera_cont)
                camera_cont = []

            timestamp = time_stamp[1].split(':')[-1]
            local_time = time_stamp[0].replace(',', ' ')
            log_record_pd = pd.DataFrame(columns=['timestamp'])
            log_record_pd.loc[local_time] = {'timestamp': timestamp}

            for camera_info in camera_set:
                if len(camera_info) == 0:
                    continue
                elif len(camera_info) == 1:
                    log_record_pd[camera_info[0].strip(':')] = 'nothing'
                else:
                    temp_info = ''
                    for i in camera_info[1:]:
                        temp_info = temp_info + i + '\n'
                    log_record_pd[camera_info[0].strip(':')] = temp_info
            log_pd = pd.concat([log_pd, log_record_pd], sort=False)
            time_stamp = []
            camera_set = []
            continue

        if 'timestamp' in record_content:
            time_stamp.append(time_array)
            record_content = record_content.strip()
            time_stamp.append(record_content)
        elif 'camera' in record_content:
            if len(camera_cont) != 0:
                camera_set.append(camera_cont)
                camera_cont = []
            camera_cont.append(record_content.strip())
        elif '  ' in record_content and 'Can not' not in record_content:
            record_content = record_content.strip()
            camera_cont.append(record_content)

    log_pd.to_csv(result_file)


def analyze_log(file_path):
    file_name = os.path.basename(file_path)
    with open(file_path, 'r', encoding='UTF-8') as log_handle:
        core_excel_func(log_handle, file_name)
        print('=============================')


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
        file_names = ['G:\\TestFramework\\result_process_18.log.2019-01-14']
        for file_name in file_names:
            a, b = os.path.split(file_name)
            log_create(file_name)
            log_name = file_name + '.log'
            log_file = open(log_name, "w")
            sys.stdout = log_file
            analyze_log(file_name)
            print('Analyse is finished')
            log_file.close()
    # restore the output to initial pattern
    sys.stdout = stdout_backup
