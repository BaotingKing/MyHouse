#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/10/22
from __future__ import print_function
import sys
import time
import logging


def analyze_one_log(file_name, log_file):
    key_words = ['final_0_result', 'final_1_result']
    cnt = 0
    sys.stdout = log_file
    with open(file_name, 'r') as log_handle:
        for one_record in log_handle:
            if '*0*' in one_record:
                cnt = cnt + 1
                time_stamp = one_record.split(' - ')[0].split(',')
                print('This is %s:  %s,%s\n' % (cnt, time_stamp[0], time_stamp[1]))
                time_temp = time.strptime(time_stamp[0], "%Y-%m-%d %H:%M:%S")
                time_stamp[0] = int(time.mktime(time_temp))
                continue

            for key in key_words:
                if key in one_record and 'True' in one_record:
                    timeArray = one_record.split(' - ')[0].split(',')
                    time_temp = time.strptime(timeArray[0], "%Y-%m-%d %H:%M:%S")
                    timeArray[0] = int(time.mktime(time_temp))
                    time_gap = (int(timeArray[0]) * 1000 + int(timeArray[1])) - (
                                int(time_stamp[0]) * 1000 + int(time_stamp[1]))

                    if time_gap >= 5000:
                        print('             ', one_record)


if __name__ == '__main__':
    stdout_backup = sys.stdout
    if len(sys.argv) > 1:
        for file_name in sys.argv[1:]:
            print(file_name)
            if file_name[-3:] == "log":
                log_file = open(file_name + '.log', "w")
                analyze_one_log(file_name, log_file)
    else:
        print("###############################")
        file_names = ['detection_result_process_9.log','double_container_detection_result_process_13.log']
        for file_name in file_names:
            if file_name[-3:] == "log":
                log_file = open(file_name + '.log', "w")
                analyze_one_log(file_name, log_file)

        print('it is ok')






