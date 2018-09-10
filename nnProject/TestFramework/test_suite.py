#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time: 2018/8/7
# import unittest
# import re
# from test_case.test_mathfunc import TestMathFunc
# from model.HTMLTestRunner_py2 import HTMLTestRunner
# import pymysql
# from model.launchfile import Launchfile
# import itertools
# import tools
# import pymysql
# import sys, os
# import logging
# # reload(sys)
# # sys.setdefaultencoding('utf8')
#
# path = "F:\\myhouse\\MyHouse\\nnProject\\TestFramework\\tianjin.conf"
# # path = "F:\\myhouse\\MyHouse\\nnProject\\TestFramework\\dongsen.conf"
# testa = Launchfile()
# # testa.cheakoutCfg()
# testb = testa.load_launchfile(path)
#
#
# # stdout_backup = sys.stdout
# # # define the log file that receives your log info
# # log_file = open("message.log", "w")
# # # redirect print output to log file
# # sys.stdout = log_file
# # log_file.close()
# # # restore the output to initial pattern
# # sys.stdout = stdout_backup
# print("================")
# # print(testb['module_0'])
# # # print("****************")
# # print("cfg keys are\n", testb.keys())
# # print("@@@@@@@@@@@@@@@@")
# # # for key in testb.iterkeys():
# # #     print(testb[key]["module_name"])
# # # print(testb[:]["module_name"])
# # print("################")
# # module = testb.get("module_8")
# # print(module.keys())
# # print("%%%%%%%%%%%%%%%%")
# # param = module.get("run_param")
# # print(param.keys())
#
# print("11111111111111111111")
# # a = ['lalla', ['abc', 'wdc'], 'were']
# # a = tools.unfold_list(a)
# b = 'abc'
# c = 'abc'
# d = [['lalla', ['abc', 'wdc'], 'were'],"/WellOcean/roi_trigger/channel_04_front", "/WellOcean/roi_trigger/channel_04_bak"]
# e = ["/WellOcean/roi_trigger/channel_04_front", "/WellOcean/roi_trigger/channel_04_bak"]
#
# # # bo = tools.check_adaptive(d,e)
# # idx_para = "/WellOcean/container_subimage/channel_04_front_letter"
# # tail_word = idx_para.replace("subimage", "result")
# filename = os.path.join(os.getcwd(), 'log.txt')
# print(filename)
# tools.logging_run()
# print("====================")
# print("33333333333333333333")
# # logger = logging.getLogger('log_haha')
# # logger.addHandler(logging.StreamHandler())
# # logger.addHandler(logging.FileHandler('test.log'))  # 再添一个FileHandler
# # # logger.setLevel(logging.INFO)  # 输出所有大于INFO级别的log
# # logger.info('I am <info> message.')
# # logger.debug('I am <debug> message.')  # 不输出
# # logger.warn("hahah123")


# filepath = "F:\\myhouse\\MyHouse\\nnProject\\TestFramework\\TestFrame.log"
filepath = "F:\\myhouse\\MyHouse\\nnProject\\TestFramework\\model\\first.tc"
filepath = str(filepath)
afile = open(filepath)
print("hello, this is a new world")
temp = afile.readline()
case = afile.readline().rstrip('\n').replace(' ', '')