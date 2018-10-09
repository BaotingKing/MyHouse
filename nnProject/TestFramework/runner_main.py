#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl
# Time: 2018/8/13
import os
import sys
import unittest

import test_case.test_events
from model.HTMLTestRunner_py3 import HTMLTestRunner

if __name__ == '__main__':
    suite = unittest.TestSuite()

    if len(sys.argv) > 1:
        for file_name in sys.argv[1:]:
            for root, dirs_labels, file_names in os.walk(file_name):
                print("===========================")
                for case_name in file_names:
                    if case_name[-2:] == "tc":
                        current_path = os.path.join(root, case_name)
                        tests = [test_case.test_events.TestEvents(case_name)]
                        suite.addTests(tests)
    else:
        cnt = 0
        dir_merge = "F:\\myhouse\\MyHouse\\nnProject\\TestFramework\\test_case\\Osk_2.0.9case"

        for root, dirs_labels, file_names in os.walk(dir_merge):  # Iterate label files
            for case_name in file_names:
                if case_name[-2:] == "tc":
                    current_path = os.path.join(root, case_name)
                    tests = [test_case.test_events.TestEventB('test_OSK')]
                    tests[0]._testMethodDoc = case_name
                    suite.addTests(tests)



    with open('UnittestTextReport.html', 'w') as f:  # 将结果保存到文件中
        runner = HTMLTestRunner(stream=f,
                                title='Well-X Test Report',
                                description='generated by HTMLTestRunner.',
                                verbosity=3
                                )
        results0 = runner.run(suite)

    # unittest.TestCase()
    # runner = unittest.TextTestRunner(verbosity=2)
    # runner.run(suite)

    # unittest.main(verbosity=3)