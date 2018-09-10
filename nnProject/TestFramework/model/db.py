#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/8/22
import pymysql


def get_connect(SQL_method,
                host="localhost",
                username="root",
                passwd="admin",
                dbname="db0821",
                charset="utf8"):
    db = pymysql.connect(
        host=host, user=username, passwd=passwd, db=dbname, charset=charset)

    cur = db.cursor()
    cur.execute(SQL_method)

    row_1 = cur.fetchone()
    print(row_1)
    row_2 = cur.fetchmany(3)
    print(row_2)
    row_3 = cur.fetchall()
    print(row_3)

    cur.close()    # close cursor
    cur.close()    # close connect


if __name__ == '__main__':
    table_name = "table_001"
    get_connect(table_name,
                host="localhost",
                user="root",
                passwd="admin",
                db="db0821",
                charset="utf8")

    temp = "we are family " + table_name
    print(temp)
