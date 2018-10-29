#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/10/25

import os
# li = ['qwe', 'ewqead', '151654']
# for n in li:
#     tid = (n and 'p' or 'f')
#     print('n = %s is %s' %(n, tid))
#
# n = True
# tid = (n and 'p' or 'f')
# print('n = %s is %s' %(n, tid))

name = 'hello'
value = '258'
HEADING_ATTRIBUTE_TMPL = """<p class='attribute'><strong>%(name)s:</strong> %(value)s</p>"""

temp = HEADING_ATTRIBUTE_TMPL % dict(value=value, name=name)

print('this is a test temp = ', temp)

test = [('Start Time', '2018-10-26 11:31:04'), ('Duration', '0:08:53.921090'), ('Status', 'Failure 2')]
print(type(test), type(test[0]))
for name, value in [test[0]]:

    daf = 123
    print(name, value)

def file_location(filename):
    dir_name = os.getcwd()
    for root, dirs_labels, file_names in os.walk(dir_name):
        print("===========================")
        for case_name in file_names:
            if case_name == filename:
                current_path = os.path.join(root, case_name)
                return current_path


def extract_description(case_name):
    case_path = file_location(case_name)
    flag = 0
    description = ''
    with open(case_path, 'r') as case_handle:
        for one_line in case_handle:
            print(one_line)
            if flag == 0 and ('#Pre' in one_line):
                flag = 1
            elif flag == 1 and ('#Desc' in one_line):
                flag = 0

            if flag == 1 or ('#Desc' in one_line):
                description = description + one_line
    return description


case_name = 'F:\\myhouse\\MyHouse\\nnProject\\TestFramework\\test_case\\Osk2.1.1_Timer_test_log\\Osk_2.1.1_Timer_case\\button\\button1.tc'
a = extract_description('button1.tc')
pth = file_location('button1.tc')
print('hahahhahahha:', a)