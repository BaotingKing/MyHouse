#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/8/22
import pymysql


def get_connect(host="localhost", user="root",
    passwd="admin", db="db0821",charset="utf8"):
    db = pymysql.connect(
        host="localhost", user="root",
        passwd="admin", db="db0821",charset="utf8")

    cur = db.cursor()

    search_method = "select sex from table_001"

    row_1 = cur.fetchone()

    row_2 = cur.fetchmany(3)

    row_3 = cur.fetchall()

    # close cursor
    cur.close()
    # close connect
    cur.close()