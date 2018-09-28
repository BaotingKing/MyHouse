#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/8/10

import xml.etree.cElementTree as ET
import sys
from model import db
# test = ET.parse(sys.argv[2])

# db = pymysql.connect("localhost","wwl","admin123","table1" )
# db = pymysql.connect(
#     host="127.0.0.1",  port=3306, user="root",
#     passwd="admin", db="db0821",charset="utf8"
# )
check_con = {}
db = db.processDB(check_list=check_con,
                  check_num=6,
                  host="localhost",
                  username="root",
                  passwd="admin",
                  dbname="db0821",
                  tabname='table_001',
                  charset="utf8")

# db = db.checkout_DB(
#     host='192.168.101.234', username="root",
#     passwd="westwell", dbname="GateRawData", tabname="Gate_gateinfo", charset="utf8")

# cur = db.cursor()
# search_method = "select sex from table_001"
#
# print(cur.execute(search_method))
#
# row_1 = cur.fetchone()
# print("row_1 = ", row_1)
# print("######################")
# row_2 = cur.fetchmany(3)
# print("row_2 = ", row_2)
# print("======================")
# row_3 = cur.fetchall()
# print("row_3 = ", row_3)
#
#
# # 关闭游标
# cur.close()
# # 关闭连接
# db.close()
