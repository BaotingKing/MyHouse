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


def analyze_log(file_name):
    sum_v = 0
    num_num = 0
    single_v = 0
    double_v = 0
    field_flag = 0
    field_temp = 0
    lock_flag = 0
    sta = 0
    problem_num = 0
    pingpong_idx = 0
    pingpong = ['', '']
    problem_timestap = []
    with open(file_name, 'r', encoding='UTF-8') as log_handle:
        for one_record in log_handle:
            if 'timestamp' in one_record:
                pingpong[pingpong_idx] = one_record
                pingpong_idx += 1
                pingpong_idx = pingpong_idx % 2
                field_temp = field_flag

            if 'number' in one_record and '_number' not in one_record and 'number_' not in one_record:
                num_num += 1
                if num_num % 2 == 1:
                    field_flag = 0
                    lock_flag = 1
                    sum_v += 1
                else:
                    lock_flag = 0
                    sta = 0

                if len(one_record.split(':')[-1].strip()) > 7:
                    field_flag += 1
                else:
                    if num_num % 2 == 1:
                        pass

            if 'ftp' in one_record:
                sta = sta + one_record.count('ftp')

            if lock_flag == 1 and num_num != 1:
                # print(field_flag)
                if sta == 4 and field_temp == 1:
                    single_v += 1
                elif sta == 6 and field_temp == 2:
                    double_v += 1
                else:
                    problem_num += 1
                    problem_timestap.append(pingpong[pingpong_idx % 2])
                    # print(pingpong[(pingpong_idx - 0) % 2])
        if sta == 4 and field_temp == 1:
            single_v += 1
        elif sta == 6 and field_temp == 2:
            double_v += 1
        else:
            problem_num += 1
            problem_timestap.append(pingpong[pingpong_idx % 2])
            # print(pingpong[(pingpong_idx - 0) % 2])

    print_detail_info(file_name, problem_timestap)

    return sum_v, single_v, double_v, problem_num


if __name__ == '__main__':
    stdout_backup = sys.stdout  # make a copy of original stdout route
    if len(sys.argv) > 1:
        for file_name in sys.argv[1:]:
            log_name = file_name + '.log'
            log_file = open(log_name, "w")
            sys.stdout = log_file
            sum_v, single_v, double_v, problem_num = analyze_log(file_name)
            print('{0} the results of statistical analysis is:\n '
                  'sum = {1}, single = {2}, double = {3}, problem_num={4}'.format(file_name, sum_v, single_v, double_v,
                                                                                  problem_num))
            log_file.close()
    else:
        print('###############################')
        file_names = ['quetu-cars.txt', 'quetu-cars_1.txt']
        for file_name in file_names:
            log_name = file_name + '.log'
            log_file = open(log_name, "w")
            sys.stdout = log_file
            sum_v, single_v, double_v, problem_num = analyze_log(file_name)
            print('{0} the results of statistical analysis is:\n '
                  'sum = {1}, single = {2}, double = {3}, problem_num={4}'.format(file_name, sum_v, single_v, double_v, problem_num))
            log_file.close()
    # restore the output to initial pattern
    sys.stdout = stdout_backup



