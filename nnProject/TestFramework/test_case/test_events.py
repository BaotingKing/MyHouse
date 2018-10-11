#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/8/7
from __future__ import print_function
from __future__ import division
import os
import unittest
from runcase import runCase
from os import path
from pathlib import Path


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

    def test_OSK(self):
        """Test R-OSK-DB"""
        curpath = path.dirname(path.abspath(__file__))
        case_name = str(self._testMethodDoc)
        case_path = search(curpath, case_name)

        if ('failed' in case_name) or ('Failed' in case_name):
            self.assertEqual(runCase(case_path), False)
        else:
            self.assertEqual(runCase(case_path), True)


def run_temp(casename):

    if 'failed' in str(casename):
        return False
    else:
        return True


def search(path, name):
    for root, dirs, files in os.walk(path):  # path is root direction
        if name in dirs or name in files:
            root = str(root)
            dirs = str(dirs)
            parent_dir = os.path.join(root, dirs)
            return os.path.join(root, name)
    return False


if __name__ == '__main__':
    unittest.main(verbosity=2)
