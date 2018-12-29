#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl
# Time: 2018/8/13
import os
import sys
import unittest
from runcase.test_case import test_events
from runcase.templates.html_show_runner import HTMLTestRunner


def dir_location(filename):
    dir_name = os.getcwd()
    for root, dirs_labels, file_names in os.walk(dir_name):
        for case_name in dirs_labels:
            if case_name == filename:
                current_path = os.path.join(root, case_name)
                return current_path


def app_main(case_file='test_case'):
    suite = unittest.TestSuite()
    dir_merge = dir_location(case_file)
    for root, dirs_labels, file_names in os.walk(dir_merge):  # Iterate label files
        for case_name in file_names:
            if case_name[-2:] == "tc":
                current_path = os.path.join(root, case_name)
                tests = [test_events.TestEventB('test_OSK')]
                tests[0]._testMethodDoc = case_name
                suite.addTests(tests)

    with open('UnittestTextReport.html', 'w') as f:  # 将结果保存到文件中
        runner = HTMLTestRunner(stream=f,
                                title='Well-X Test Report',
                                description='generated by HTMLTestRunner.',
                                verbosity=3
                                )

        print("======I am here, this is begin======")
        results = runner.run(suite)
        print('The test is over:')
    return results


if __name__ == '__main__':
    if len(sys.argv) > 1:
        case_dir = sys.argv[1]
    else:
        case_dir = 'test_case'
    app_main(case_dir)
