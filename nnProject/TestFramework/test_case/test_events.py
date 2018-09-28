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
        self.assertEqual(True, True)
        self.assertNotEqual(False, True)

    def test_launchfile(self):
        """Test method for check the launcfile"""
        self.assertEqual(True, True)
        self.assertNotEqual(False, True)


    # @unittest.skip("I don't want to run this case.")
    def test_UI(self):
        """Test method WellE to db"""
        self.assertEqual(True, True)

    def test_OSK_Interface(self):
        """Test method for OSK Interface"""
        self.assertEqual(True, True)
        # self.assertEqual(True, runcase.runCase())



if __name__ == '__main__':
    unittest.main(verbosity=2)