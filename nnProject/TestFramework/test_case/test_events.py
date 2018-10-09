#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/8/7
from __future__ import print_function
from __future__ import division
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

    def test_OSK(self):
        """Test R-OSK-DB"""
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main(verbosity=2)
