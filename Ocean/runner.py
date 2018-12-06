#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Zhang.Baoting
# Time: 2018/8/3
import unittest
import time
# from controller import config
# from model.common import Goals as go
# from controller import con_api_xml
# from controller import check
# import BaseExcelReport as be
import xlsxwriter
# import sendMail as sd
from model.HTMLTestRunner_py2 import HTMLTestRunner
import sys
reload(sys)
sys.setdefaultencoding('utf8')
# gm = con_api_xml.ret_xml() # 读取xml
# hb = con_api_xml.ret_http_base(gm) #读取http参数

data = {"info":[]}
# 初始化报告
# html_report1 = htmlreport.HtmlReport(gm)

# 测试用例(组)类
class TestInterfaceCase(unittest.TestCase):
    pass


# 获取测试套件
def get_test_suite(index):
    pass


# 运行测试用例函数
def run_case(runner):
    pass


# 运行测试套件
if __name__ == '__main__':
    pass

















