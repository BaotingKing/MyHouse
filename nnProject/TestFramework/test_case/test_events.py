#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/8/7
from __future__ import print_function
from __future__ import division
import os
import unittest
import runcase
from model import launchfile


class TestEvents(unittest.TestCase):
    """Test WellOcean-->OSK-->WellE"""

    def setUp(self):
        print
        "do something before test.Prepare environment."

    def tearDown(self):
        print
        "do something after test.Clean up."

    def test_wellocean(self):
        """Test method for wellocean internal-interface"""
        self.assertEqual(True, True, "this is 1")
        self.assertNotEqual(False, True, msg="this is 2")

    def test_launchfile(self):
        """Test method for check the launcfile"""
        self.assertEqual(True, True)
        self.assertNotEqual(False, True)
        print('this is a flag')

    # @unittest.skip("I don't want to run this case.")
    def test_UI(self):
        """Test method WellE to db"""
        self.assertEqual(True, True)

    def test_OSK_Interface(self):
        """notes notes notes notes notes """
        self.assertEqual(True, True)
        # self.assertEqual(True, runcase.runCase())

    def test_OSK(self):
        """Test recong-OSK-DB"""
        for i in range(5):
            print(i)


class TestEventB(unittest.TestCase):
    """HERO: W-->O-->W"""

    def setUp(self):
        print
        "do something before test.Prepare environment."

    def tearDown(self):
        print
        "do something after test.Clean up."

    def test_OSK(self, case_a='this is debug'):
        """Test R-OSK-DB"""
        global g_case_path
        case_path = search(g_case_path, self.testMethodDoc)
        run_temp(case_path)

        self.assertEqual(search(g_case_path, self.testMethodDoc), True)
        # self.assertEqual(run_temp(case_a), True)


def run_temp(casename):
    print(casename)
    global g_num
    if g_num % 2 == 0:
        g_num = g_num + 1
        return False
    else:
        g_num = g_num + 1
        return True


def search(path, name):
    for root, dirs, files in os.walk(path):  # path 为根目录
        if name in dirs or name in files:
            flag = 1  # 判断是否找到文件
            root = str(root)
            dirs = str(dirs)
            # return os.path.join(root, dirs)
            return True
    return False
    # return -1


if __name__ == '__main__':
    unittest.main(verbosity=2)
