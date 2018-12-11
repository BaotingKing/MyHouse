# -*- coding: utf8 -*-

'''
Case format: Total 1+X+N lines
T, N, M1, M2...MX
X lines of GetOne result, one result per line; use ',' to separate Part/Key:Value
result line used to check GetOne result data
N lines of request data, one request per line. use ',' to separate Part/Key:Value
request line used to modify request, before send
(GetOne Request will be send after the Mth request)
(All request will be send within T seconds, every two near requests will be send at similar duration)
'''
import sys
import traceback
import json
import time
import os
from runcase.view.database_handle import process_database
from runcase.models.send_file import CUR_PATH, send_request, get_response, UTC_timestamp

g_req = None
GET_ONE = None
COST_TIME = 600  # milli-
g_tokenTestDbg = False
g_tokenlist = None
g_timestamp = UTC_timestamp()


def load_get_one(lane=None):
    try:
        filename = 'getone.req'
        filename = str(CUR_PATH / filename)
        a_file = open(filename)
        orig = a_file.read()
        temp = json.loads(orig)
        if lane:
            temp["AdditionalInfo"]["lane"] = str(lane)
            orig = json.dumps(temp, indent=4, sort_keys=True)
        global GET_ONE
        GET_ONE = orig
    except:
        print("Can't load original GetOne from file", filename)


def load_orig():
    try:
        filename = 'first.req'
        filename = str(CUR_PATH / filename)
        a_file = open(filename)
        orig = a_file.read()
        global g_req
        g_req = json.loads(orig)
    except:
        print("Can't load original request from file", filename)


def generate_token(lane):
    global g_tokenlist
    # if token already generated
    if g_tokenlist:
        return
    g_tokenlist = []
    token = round(time.time() * 10000)
    for item in range(1, 100):
        g_tokenlist.append(str(token + item * 10) + str(lane))


def get_token(index):
    index = int(index)
    return g_tokenlist[index]


def sleep(dest):
    while True:
        time.sleep(0.1)
        now = UTC_timestamp()
        if now > dest:
            # print(now, dest, now-dest)
            return


# check is a str like Part/Part/Key:Value
def check_response(resp, check_str):
    try:
        print('\n')
        success = True
        if not resp:
            print('Response is None...\n')
            return False
        result = json.loads(resp)
        check_list = check_str.split(',')
        for acheck in check_list:
            check_pair = acheck.strip().split(':', 1)
            if len(check_pair) > 1:
                value = check_pair[1].lstrip()
            else:
                value = ""
            check = check_pair[0].strip().split('/')
            key = check[-1]
            print('        : Check Start, Key =', check_pair[0], 'Value =', value)
            if check[0] == 'Token' or check[0] == 'token':
                value = get_token(value)
                tmp = result['AdditionalInfo']['token']
            else:
                tmp = result
                for item in check:
                    tmp = tmp[item.strip()]
            if tmp != value:
                print('[Failed]: Check Failed, Key =', check_pair[0], ', Value = ', tmp, ', Expect to be ', value,
                      sep="'")
                success = False

        print('\n')
        # All check passed
        return success
    except:
        einfo = sys.exc_info()
        print("check_response Exception:", einfo[0], "msg:", str(einfo[1]), "\ntraceback:", traceback.format_tb(einfo[2], 1))
        return False


def divide_time(milli_seconds, divisor):
    if divisor == 0:
        return [milli_seconds]
    time_list = []
    result = int(milli_seconds / divisor)
    for i in range(0, divisor):
        time_list.append(result)
    return time_list


def generate_req(req_str, init=False):
    tokenindex = None
    req_list = req_str.split(',')
    for item in req_list:
        req = item.strip().split(':', 1)
        if len(req) > 1:
            value = req[1].lstrip()
        else:
            value = ""
        req = req[0].strip().split('/')
        if req[0] == 'token' or req[0] == 'Token':
            tokenindex = value
        else:
            g_req[req[0].strip()][req[1].strip()] = value
    lane = g_req['AdditionalInfo']['lane']
    global g_timestamp
    g_timestamp += 1
    g_req['AdditionalInfo']['timestamp'] = str(g_timestamp)
    generate_token(lane)

    if not g_tokenTestDbg:
        if tokenindex:
            g_req['AdditionalInfo']['token'] = get_token(tokenindex)
        elif init:
            g_req['AdditionalInfo']['token'] = get_token(0)

    return json.dumps(g_req, indent=4, sort_keys=True)


def generate_get_one(check_str):
    check_list = check_str.split(',')
    for item in check_list:
        check = item.split(':', 1)
        if check[0].strip() == 'AdditionalInfo/lane':
            load_get_one(check[1].strip())
    return GET_ONE


def process_case(whole_time, req_list, check_list, check_point, case_name):
    success = True

    # every test case should use orig req at first
    load_orig()
    load_get_one()
    # and new set of tokens
    global g_tokenlist
    g_tokenlist = None

    getone_sequence = []
    for item in check_list:
        getone_sequence.append(generate_get_one(item))

    req_sequence = []
    sleep_sequence = []
    time_list = divide_time(whole_time * 1000 - COST_TIME, len(req_list) - 1)
    for i in range(0, len(req_list)):
        req_sequence.append(generate_req(req_list[i]))
        if i != len(req_list) - 1:
            resp_num = check_point.count(str(i + 1))
            sleep_sequence.extend(divide_time(time_list[i], resp_num + 1))
    if len(req_list) == 1:
        sleep_sequence.append(time_list[0])
    sleep_sequence.append(COST_TIME)
    sleep_sequence += [400] * check_point.count(str(len(req_list)))
    # print("[DEBUG]:", check_point)
    # print("[DEBUG]:", sleep_sequence)

    sleep_index = 0
    check_index = 0
    for i in range(0, len(req_list)):
        if i != 0:
            sleep(sleep_sequence[sleep_index])
            sleep_index += 1
        else:
            now = UTC_timestamp()
            for j in range(0, len(sleep_sequence)):
                now += sleep_sequence[j]
                sleep_sequence[j] = now
            # print("[DEBUG]:", sleep_sequence)
        send_request(req_sequence[i])
        while check_index < len(check_point) and str(i + 1) == check_point[check_index].strip() and i != len(
                req_list) - 1:
            if not sendGetOne(getone_sequence[check_index], check_list[check_index], sleep_sequence[sleep_index],
                              check_index):
                success = False
            sleep_index += 1
            check_index += 1

    # after all Store req is send, sleep to set timeout (T)
    sleep(sleep_sequence[sleep_index])
    sleep_index += 1

    while check_index < len(check_point):
        if not sendGetOne(getone_sequence[check_index], check_list[check_index], sleep_sequence[sleep_index],
                          check_index):
            success = False
        sleep_index += 1
        check_index += 1

    print("*********************************************")
    print('case_name = %s' % case_name)
    print('Identify module to OSK: case test results is %s' % success)
    print("*********************************************")

    if True:
        if ('failed' not in case_name) and ('Failed' not in case_name):
            if not process_database(check_list=check_list,
                                    check_num=len(check_point),
                                    token_list=g_tokenlist,
                                    database_name='GateRawData'):
                success = False

        print("*********************************************")
        print('case_name = %s' % case_name)
        print('OSK to DB: case test results is %s' % success)
        print("*********************************************")

    return success


def sendGetOne(getone, check, sleep_time, index):
    sleep(sleep_time)
    result = get_response(getone)
    print("[RETGetOne]:", result)
    if check_response(result, check):
        print("Check", index, "Pass")
        return True
    else:
        print("Check", index, "Failed")
        return False


def run_case(filename, host='127.0.0.1', port=3309):
    print('\n===========================================================')
    # temp, filename = os.path.split(file_path)
    file_path = str(CUR_PATH / filename)
    check_list = []
    req_list = []
    try:
        afile = open(file_path)
        case = afile.readline().rstrip('\n').replace(' ', '')
        temp = case.split(',')
        N = int(temp[1])
        X = len(temp) - 2
        T = int(temp[0])
        check_point = temp[2:]
        print(filename, ": Test Case has", N, "requests send in", T, "seconds")
        print("GetOne will be send and check on", ','.join(check_point))
        for i in range(0, X):
            acheck = afile.readline()
            check_list.append(acheck.rstrip('\n'))
        for i in range(0, N):
            areq = afile.readline()
            req_list.append(areq.rstrip('\n'))

        # # Use test case to process it and check
        if process_case(T, req_list, check_list, check_point, filename):
            print("\n[Finished]: Test Case: ", filename, ": SUCCESS\n")
            final_result = True
        else:
            print("\n[Finished]: Test Case: ", filename, ": FAILED\n")
            final_result = False

        return final_result
    except:
        print("Error: Can't parse test case")
        einfo = sys.exc_info()
        print("run_case Exception:", einfo[0], "msg:", str(einfo[1]), "\ntraceback:", traceback.format_tb(einfo[2], 5))
        return False


if __name__ == '__main__':
    # stdout_backup = sys.stdout
    # log_file = open("messageOSK.log", "w")
    # logger = logging.getLogger("AppName")
    # if len(sys.argv) > 1:
    #     # sys.stdout = log_file
    #     for file_name in sys.argv[1:]:
    #         for root, dirs_labels, file_names in os.walk(file_name):
    #             print("===========================")
    #             for case_name in file_names:
    #                 if case_name[-2:] == "tc":
    #                     current_path = os.path.join(root, case_name)
    #                     run_case(current_path)
    # else:
    #     # sys.stdout = log_file
    #     cnt = 0
    #     dir_merge = "F:\\myhouse\\MyHouse\\nnProject\\TestFramework\\test_case\\Osk_2.0.9case"
    #
    #     with ssh.SSHTunnelForwarder(
    #             ('192.168.101.234', 22),
    #             ssh_username="westwell",
    #             ssh_password='1',
    #             remote_bind_address=('127.0.0.1', 3306)
    #     ) as server:
    #         run_case("first2.tc",
    #                 host='127.0.0.1',
    #                 port=server.local_bind_port
    #                 )
    #         server.start()
    #
    #     for root, dirs_labels, file_names in os.walk(dir_merge):  # 遍历各种label文件夹
    #         # print("===========================", cnt)
    #         # logger.debug('this is debug info', cnt)
    #         # logger.warn('this is warning message')
    #         # logger.error('this is error message')
    #         cnt = cnt + 1
    #         for case_name in file_names:
    #             if case_name[-2:] == "tc":
    #                 current_path = os.path.join(root, case_name)
    #                 # run_case(current_path)
    #
    # server.close()
    # print("runner.py is over")

    if len(sys.argv) > 1:
        for file_name in sys.argv[1:]:
            for root, dirs_labels, file_names in os.walk(file_name):
                print("===========================")
                for case_name in file_names:
                    if case_name[-2:] == "tc":
                        current_path = os.path.join(root, case_name)
                        run_case(current_path)
    else:
        run_case('one_request_failed.tc')  # button.tc   first
