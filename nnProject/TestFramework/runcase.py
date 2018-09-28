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
import logging
import sshtunnel as ssh
from model.db import processDB
import copy

from model.sendfile import curpath, sendrequest, getresponse, UTC_timestamp
g_req = None
g_getone = None
g_costtime = 600 # milli-
g_tokenTestDbg = False
g_tokenlist = None
g_timestamp = UTC_timestamp()

def loadGetOne(lane=None):
    try:
        filename = 'getone.req'
        filename = str(curpath / filename)
        afile = open(filename)
        orig = afile.read()
        temp = json.loads(orig)
        if lane:
            temp["AdditionalInfo"]["lane"] = str(lane)
            orig = json.dumps(temp, indent=4, sort_keys=True)
        global g_getone
        g_getone = orig
    except:
        print("Can't load original GetOne from file", filename)
        

def loadOrig():
    try:
        filename = 'first.req'
        filename = str(curpath / filename)
        afile = open(filename)
        orig = afile.read()
        global g_req
        g_req = json.loads(orig)
    except:
        print("Can't load original request from file", filename)


def generateToken(lane):
    global g_tokenlist
    # if token already generated
    if g_tokenlist:
        return 
    g_tokenlist = []
    token = round(time.time() * 10000)
    for item in range(1, 100):
        g_tokenlist.append(str(token+item*10)+str(lane))
        
    
def getToken(index):
    index = int(index)
    return g_tokenlist[index]


def sleep(dest):
    while True:
        time.sleep(0.1)
        now = UTC_timestamp()
        if now > dest:
            #print(now, dest, now-dest)
            return


# check is a str like Part/Part/Key:Value
def checkResp(resp, check_str):
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
                value = getToken(value)
                tmp = result['AdditionalInfo']['token']
            else:
                tmp = result
                for item in check:
                    tmp = tmp[item.strip()]
            if tmp != value:
                print('[Failed]: Check Failed, Key =', check_pair[0], ', Value = ', tmp, ', Expect to be ', value, sep="'")
                success = False

        print('\n')
        # All check passed
        return success
    except:
        einfo = sys.exc_info()
        print("checkResp Exception:",einfo[0], "msg:", str(einfo[1]), "\ntraceback:", traceback.format_tb(einfo[2], 1))
        return False


def divideTime(milli_seconds, divisor):
    if divisor == 0:
        return [milli_seconds]
    time_list = []
    result = int(milli_seconds/divisor)
    for i in range(0, divisor):
        time_list.append(result)
    return time_list
            

def generateReq(req_str, init=False):
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
    generateToken(lane)

    if not g_tokenTestDbg:
        if tokenindex:
            g_req['AdditionalInfo']['token'] = getToken(tokenindex)
        elif init:
            g_req['AdditionalInfo']['token'] = getToken(0)


    return json.dumps(g_req, indent=4, sort_keys=True)


def generateGetOne(check_str):
    check_list = check_str.split(',')
    for item in check_list:
        check = item.split(':', 1)
        if check[0].strip() == 'AdditionalInfo/lane':
            loadGetOne(check[1].strip())
    return g_getone

    
def processCase(wholetime, req_list, check_list, check_point):
    success = True

    # every test case should use orig req at first
    loadOrig()
    loadGetOne()
    # and new set of tokens
    global g_tokenlist
    g_tokenlist = None

    getone_sequence = []
    for item in check_list:
        getone_sequence.append(generateGetOne(item))

    req_sequence = []
    sleep_sequence = []
    time_list = divideTime(wholetime*1000-g_costtime, len(req_list)-1)
    for i in range(0, len(req_list)):
        req_sequence.append(generateReq(req_list[i]))
        if i != len(req_list)-1:
            resp_num = check_point.count(str(i+1))
            sleep_sequence.extend(divideTime(time_list[i], resp_num+1))
    if len(req_list) == 1:
        sleep_sequence.append(time_list[0])
    sleep_sequence.append(g_costtime)
    sleep_sequence += [400] * check_point.count(str(len(req_list)))
    #print("[DEBUG]:", check_point)
    #print("[DEBUG]:", sleep_sequence)

    sleep_index = 0
    check_index = 0
    for i in range(0, len(req_list)):
        if i!=0:
            sleep(sleep_sequence[sleep_index])
            sleep_index += 1
        else:
            now = UTC_timestamp()
            for j in range(0, len(sleep_sequence)):
                now += sleep_sequence[j]
                sleep_sequence[j] = now
            #print("[DEBUG]:", sleep_sequence)
        sendrequest(req_sequence[i])
        while check_index<len(check_point) and str(i+1)==check_point[check_index].strip() and i!=len(req_list)-1:
            if not sendGetOne(getone_sequence[check_index], check_list[check_index], sleep_sequence[sleep_index], check_index):
                success = False
            sleep_index += 1
            check_index += 1

    # after all Store req is send, sleep to set timeout (T)
    sleep(sleep_sequence[sleep_index])
    sleep_index += 1

    while check_index<len(check_point):
        if not sendGetOne(getone_sequence[check_index], check_list[check_index], sleep_sequence[sleep_index], check_index):
            success = False
        sleep_index += 1
        check_index += 1

    if not processDB(check_list=check_list, check_num=len(check_point)):
        success = False

    return success


def sendGetOne(getone, check, sleep_time, index):
    sleep(sleep_time)
    result = getresponse(getone)
    print("[RETGetOne]:", result)
    if checkResp(result, check):
        print("Check", index, "Pass")
        return True
    else:
        print("Check", index, "Failed")
        return False


def runCase(filename, host, port):
    print("\n===========================================================")
    filepath = str(curpath / filename)
    check_list = []
    req_list = []
    try:
        afile = open(filepath)
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

        # Use test case to process it and check
        # if processCase(T, req_list, check_list, check_point):
        #     print("\n[Finished]: Test Case: ", filename, ": SUCCESS\n")
        # else:
        #     print("\n[Finished]: Test Case: ", filename, ": FAILED\n")

        processDB(check_list=check_list,
                  check_num=len(check_point),
                  host='127.0.0.1',
                  port=server.local_bind_port
                  )

    except:
        print("Error: Can't parse test case")
        einfo = sys.exc_info()
        print("runCase Exception:",einfo[0], "msg:", str(einfo[1]), "\ntraceback:", traceback.format_tb(einfo[2], 5))


if __name__ == '__main__':
    # stdout_backup = sys.stdout
    # log_file = open("messageOSK.log", "w")
    # logger = logging.getLogger("AppName")
    if len(sys.argv) > 1:
        # sys.stdout = log_file
        for file_name in sys.argv[1:]:
            for root, dirs_labels, file_names in os.walk(file_name):
                print("===========================")
                for case_name in file_names:
                    if case_name[-2:] == "tc":
                        current_path = os.path.join(root, case_name)
                        runCase(current_path)
    else:
        # sys.stdout = log_file
        cnt = 0
        dir_merge = "F:\\myhouse\\MyHouse\\nnProject\\TestFramework\\test_case\\Osk_2.0.9case"

        with ssh.SSHTunnelForwarder(
                ('192.168.101.234', 22),
                ssh_username="westwell",
                ssh_password='1',
                remote_bind_address=('127.0.0.1', 3306)
        ) as server:
            runCase("first2.tc",
                    host='127.0.0.1',
                    port=server.local_bind_port
                    )
            server.start()

        for root, dirs_labels, file_names in os.walk(dir_merge):  # 遍历各种label文件夹
            # print("===========================", cnt)
            # logger.debug('this is debug info', cnt)
            # logger.warn('this is warning message')
            # logger.error('this is error message')
            cnt = cnt + 1
            for case_name in file_names:
                if case_name[-2:] == "tc":
                    current_path = os.path.join(root, case_name)
                    # runCase(current_path)

    server.close()
    print("runcase.py is over")


