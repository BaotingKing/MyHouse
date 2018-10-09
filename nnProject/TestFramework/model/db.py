#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/8/22
import pymysql
import pymysql.cursors
import sshtunnel as ssh
import sys
import re
import traceback
from model import interface

def processDB(check_list,
              check_num,
              host="127.0.0.1",
              username="root",
              port=3306,
              passwd="westwell",
              dbname="GateRawData",
              tabname="Gate_gateinfo",
              charset="utf8"):
    try:
        print("-------0---------")
        db = pymysql.connect(host=host,
                             port=port,
                             user=username,
                             passwd=passwd,
                             db=dbname,
                             charset=charset)
        cur = db.cursor(cursor=pymysql.cursors.DictCursor)
        method = "select * from (select * from {table_name} ORDER BY {key_name} DESC LIMIT 0,{check_num}) \
            as {table_name} ORDER BY {key_name} ASC" \
            .format(table_name=tabname, key_name='Timestamp', check_num=check_num)
        cur.execute(method)
        result_db = cur.fetchall()
        cur.close()  # close cursor
        db.close()  # close connect

        # this is for test
        g_tokentest = ['0', '153804006188541', '153804006188641', '153804006188741']
        print("-------3---------")

        for i in range(0, check_num):
            print("hello,this is %d---------------------" % i)
            one_check = check_list[i]
            if not checkDB(one_check, result_db, g_tokentest):
                print('DB is checked and it is error in %d' % i)

        print("-------6---------")

    except Exception:
        print("Query database failed")


def checkDB(check, records, tokenValue):
    matching = True
    print('this is debug0')
    try:
        check_list = check.split(',')     # to find token
        value = ""
        for acheck in check_list:
            check_pair = acheck.strip().split(':', 1)
            if len(check_pair) > 1:
                if check_pair[0] == 'Token' or check_pair[0] == 'token':
                    value = check_pair[1].lstrip()
                    break

        if value == "":
            print("checkResp Exception:")
            return False
        print('this is debug1')
        token_value = tokenValue[int(value)]
        for arecord in records:
            if arecord['Token'] == token_value:
                for acheck in check_list:
                    check_pair = re.split(':|/', acheck.strip())
                    if check_pair[0] != 'Token' and check_pair[0] != 'token':
                        interface_info = interface.interface_db[check_pair[0]]
                        db_key = interface_info[check_pair[1]]
                        arecord_value = arecord[db_key].replace(' ', '')   # To fit the format
                        if not check_pair[-1] in arecord_value:
                            matching = False
                            print('I am so sorry:', db_key, check_pair[-1], arecord[db_key], arecord_value)
                            # return matching
        print('this is debug2', matching)
        return matching
    except:
        print('---------------I am here1---------------')
        einfo = sys.exc_info()
        print("checkResp Exception:",einfo[0], "msg:", str(einfo[1]), "\ntraceback:", traceback.format_tb(einfo[2], 1))
        return False


if __name__ == '__main__':
    check_con = {}
    with ssh.SSHTunnelForwarder(
            ('192.168.101.234', 22),
            ssh_username="westwell",
            ssh_password='1',
            remote_bind_address=('127.0.0.1', 3306)
    ) as server:
        processDB(
            check_list=check_con,
            check_num=6,
            host='127.0.0.1',
            port=server.local_bind_port)
        server.start()

    server.close()
