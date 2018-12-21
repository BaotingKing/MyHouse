#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/10/22
from __future__ import print_function
import sys


def print_detail_info(file_name, timestap_list):
    print_lock = 0
    cnt = 0
    with open(file_name, 'r', encoding='UTF-8') as log_handle:
        for one_record in log_handle:
            if 'timestamp' in one_record:
                # time_stap = one_record.split(':')[-1].strip()
                if one_record in timestap_list:
                    print_lock = 0
                    cnt += 1
                    print('The No.{0}:\n'.format(cnt))
                else:
                    print_lock = 1
            if print_lock == 0:
                print(one_record)


def extract_log(file_name):
    with open(file_name, 'r', encoding='UTF-8') as log_handle:
        cnt = 0
        last_record = ''
        for one_record in log_handle:
            record = one_record.strip('\n')
            if 'AdditionalInfo' in record:
                dict_record = eval(record)
                print(last_record)
                for extr_key in ['timestamp', 'number', 'examine_img_back', 'examine_img_front', 'side_fullimg_path']:
                    for key in ['AdditionalInfo', 'ExamineInfo', 'DetectResultCam1', 'DetectResultCam2', 'LorryInfo']:
                        module_value = dict_record[key]
                        if extr_key in module_value.keys():
                            print(extr_key, ':', module_value[extr_key])
                print('\n')
            last_record = record

    return True


if __name__ == '__main__':
    stdout_backup = sys.stdout  # make a copy of original stdout route
    if len(sys.argv) > 1:
        for file_name in sys.argv[1:]:
            log_name = file_name + '.log'
            log_file = open(log_name, "w")
            sys.stdout = log_file
            sum_v = extract_log(file_name)
            print('It is OK')
            log_file.close()
    else:
        print('###############################')
        file_names = ['sender_log_2018-12-20_10-08']
        for file_name in file_names:
            log_name = file_name + '.log'
            log_file = open(log_name, "w")
            sys.stdout = log_file
            sum_v = extract_log(file_name)
            print('It is OK')
            log_file.close()
    # restore the output to initial pattern
    sys.stdout = stdout_backup



