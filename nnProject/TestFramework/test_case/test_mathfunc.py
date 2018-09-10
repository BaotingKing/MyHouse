#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/8/7
from __future__ import print_function
from __future__ import division
import unittest
import runner_interface_test
from test_case.mathfunc import *


class TestMathFunc(unittest.TestCase):
    """Test mathfuc.py"""

    def setUp(self):
        print
        "do something before test.Prepare environment."

    def tearDown(self):
        print
        "do something after test.Clean up."

    def test_add(self):
        """Test method for wellocean internal-interface"""
        self.assertEqual(3, add(1, 2))
        self.assertNotEqual(3, add(2, 2))

    def test_minus(self):
        """Test method minus(a, b)"""
        self.assertEqual(1, minus(3, 2))

    def test_multi(self):
        """Test method multi(a, b)"""
        self.assertEqual(6, multi(2, 3))

    # @unittest.skip("I don't want to run this case.")
    def test_divide(self):
        """Test method divide(a, b)"""
        self.assertEqual(2, divide(6, 3))
        self.assertEqual(2.50, divide(5.0, 2))


    def test_OSK_Interface(self):
        """Test method for OSK Interface"""
        self.assertEqual(True, runner_interface_test.atest())



if __name__ == '__main__':
    unittest.main(verbosity=2)