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
              token_list,
              host="127.0.0.1",
              username="root",
              port=3306,
              passwd="westwell",
              dbname="GateRawData",
              tabname="Gate_gateinfo",
              charset="utf8"):
    print('--------------------------------------------')
    print('------------DB checkout begin---------------')
    try:
        check_result = False
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

        print('--------------------------------------------')
        print('Case result is     : %s' % check_list)
        print('DB query results is: %s' % result_db)
        for i in range(0, check_num):
            one_check = check_list[i]
            if checkDB(one_check, result_db, token_list):
                check_result = True

        return check_result

    except Exception:
        print("Query database failed")
        return False


def checkDB(check, records, tokenValue):
    matching = True
    try:
        check_list = check.split(',')  # to find token
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

        token_value = tokenValue[int(value)]
        for arecord in records:
            if arecord['Token'] == token_value:
                for acheck in check_list:
                    check_pair = re.split(':|/', acheck.strip())
                    if check_pair[0] != 'Token' and check_pair[0] != 'token':
                        interface_info = interface.interface_db[check_pair[0]]
                        db_key = interface_info[check_pair[1]]
                        arecord_value = arecord[db_key].replace(' ', '')  # To fit the format

                        if db_key == 'PlateResult':    # License plates have Chinese characters
                            plate_result_num = arecord_value.split('_')[-1]
                            if plate_result_num.strip('_*') not in check_pair[-1]:    # Less rigorous and e.g: TJ_*HB743
                                matching = False
                                print('I am so sorry0:', db_key, check_pair[-1], plate_result_num)
                                return matching
                        elif db_key == 'SideImpath1' or db_key == 'SideImpath2' or db_key == 'PlateImpath':   # path's string has '\'
                            image_infoes = check_pair[-1].split(' ')    # only checkout import image info
                            for frag in image_infoes:
                                if frag not in arecord_value:
                                    matching = False
                                    print('I am so sorry1:', db_key, image_infoes, arecord_value)
                                    return matching
                        else:
                            if not check_pair[-1].strip() in arecord_value:
                                matching = False
                                print('I am so sorry2:', db_key, check_pair[-1], arecord[db_key], arecord_value)
                                return matching
        print('DB check reslut: ', matching)
        return matching
    except:
        print('---------------I am here1---------------')
        einfo = sys.exc_info()
        print("checkResp Exception:", einfo[0], "msg:", str(einfo[1]), "\ntraceback:", traceback.format_tb(einfo[2], 1))
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
