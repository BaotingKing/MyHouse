#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/8/22
import re
import sys
import traceback
from model import table_template as table
from model import interface
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def process_database(check_list,
                     check_num,
                     token_list,
                     username='root',
                     password='westwell',
                     host='localhost',
                     port=3306,
                     database_name='GateRawData'):
    print('------------DB checkout begin---------------')
    print('[Debug]: database\'s name is: ', database_name)
    check_result = False
    try:
        # Connect to the database
        engine = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}'
                               .format(username, password, host, port, database_name))

        # Init connect object
        db_session = sessionmaker(bind=engine)
        session = db_session()

        # Concrete operations
        results_db = session.query(table.GateInfo).order_by(table.GateInfo.id)[-check_num:]
        print('--------------------------------------------')
        print('Case result is     : %s' % check_list)
        print('DB query results is: %s' % results_db)
        for i in range(0, check_num):
            one_check = check_list[i]
            if result_check(one_check, results_db, token_list):
                check_result = True

        session.close()  # close database
        return check_result
    except:
        print('[Debug]TestFramework DB check--------------')
        print('Query database failed')
        exe_info = sys.exc_info()
        print("check_response Exception:", exe_info[0], "msg:", str(exe_info[1]), "\ntraceback:", traceback.format_tb(exe_info[2], 1))
        return False


def result_check(check, records, token_values):
    matching = True
    try:
        check_list = check.split(',')  # to find token
        value = ""
        for check in check_list:
            check_pair = check.strip().split(':', 1)
            if len(check_pair) > 1:
                if check_pair[0] == 'Token' or check_pair[0] == 'token':
                    value = check_pair[1].lstrip()
                    break
        if value == "":
            print('check_response Exception:')
            return False

        token_value = token_values[int(value)]
        for record in records:
            if record.Token == token_value:
                for check in check_list:
                    check_pair = re.split(':|/', check.strip())
                    if check_pair[0] != 'Token' and check_pair[0] != 'token':
                        interface_info = interface.interface_db[check_pair[0]]
                        db_key = interface_info[check_pair[1]]
                        one_record_value = record.get_value_by_name(db_key).replace(' ', '')  # To fit the format
                    
                        if db_key == 'PlateResult':  # License plates have Chinese characters
                            plate_result_num = one_record_value.split('_')[-1]
                            if plate_result_num.strip('_*') not in check_pair[-1]:  # Less rigorous and e.g: TJ_*HB743
                                matching = False
                                print('I am so sorry0:', db_key, check_pair[-1], plate_result_num)
                                return matching
                        elif db_key == 'SideImpath1' or db_key == 'SideImpath2' or db_key == 'PlateImpath':  # path's string has '\'
                            image_infoes = check_pair[-1].split(' ')  # only checkout import image info
                            for frag in image_infoes:
                                if frag not in one_record_value:
                                    matching = False
                                    print('I am so sorry1:', db_key, image_infoes, one_record_value)
                                    return matching
                        else:
                            if not check_pair[-1].strip() in one_record_value:
                                matching = False
                                print('I am so sorry2:', db_key, check_pair[-1], record.get_value_by_name(db_key), one_record_value)
                                return matching
        print('DB check reslut: ', matching)
        return matching
    except:
        print('[Debug] database result check failed---------------')
        exe_info = sys.exc_info()
        print("check_response Exception:", exe_info[0], "msg:", str(exe_info[1]), "\ntraceback:", traceback.format_tb(exe_info[2], 1))
        return False

"""
def process_database_old(check_list,
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
            if result_check(one_check, result_db, token_list):
                check_result = True

        return check_result

    except Exception:
        print("Query database failed")
        return False
"""


def main(username='root', password='westwell', host='localhost', port=3306, dbname=None):
    check_num = 3
    try:
        # Connect to the database
        engine = create_engine('mysql+pymysql://{0}:{1}@{2}:{3}/{4}'
                               .format(username, password, host, port, dbname))

        # Init connect object
        db_session = sessionmaker(bind=engine)
        session = db_session()

        # Concrete operations
        # # method 1:
        # user = session.query(GateInfo).filter(GateInfo.id == '1000').one()
        # print('haha', user.id, user.PlateResult, user.FinalResult1)

        # # method 2:
        # i = 0
        # for instance in session.query(table.GateInfo).order_by(table.GateInfo.id, )[-check_num:]:
        #     print('this is %d:\n' % i)
        #     i += 1
        #     print(instance.id, instance.FinalResult1)

        # method 3:
        result_db = session.query(table.GateInfo).order_by(table.GateInfo.id, )[-check_num:]
        # result_db = session.query(table.GateInfo).filter_by().all()
        # db_key = ['FinalResult1', 'PlateResult', 'Timestamp', 'DetectFace1', 'Token', 'DetectFace2', 'PlateImpath']
        print(type(result_db), len(result_db), result_db)
        print('====+++++++')
        for arecord in result_db:
            print(arecord.FinalResult1)
            print('----------', type(arecord))
            print(arecord.get_value_by_name('id'))
            print(arecord.get_value_by_name('FinalResult1'))
        session.close()  # close database
    except:
        print('[Debug]TestFramework DB check---------------')
        exe_info = sys.exc_info()
        print("check_response Exception:", exe_info[0], "msg:", str(exe_info[1]), "\ntraceback:", traceback.format_tb(exe_info[2], 1))
        return False


if __name__ == '__main__':
    print('[Debug]: this file is {0}'.format(__file__))
    main(dbname='GateRawData')

    check_con = {}
    # with ssh.SSHTunnelForwarder(
    #         ('192.168.101.234', 22),
    #         ssh_username="westwell",
    #         ssh_password='1',
    #         remote_bind_address=('127.0.0.1', 3306)
    # ) as server:
    #     processDB(
    #         check_list=check_con,
    #         check_num=6,
    #         host='127.0.0.1',
    #         port=server.local_bind_port)
    #     server.start()
    #
    # server.close()
