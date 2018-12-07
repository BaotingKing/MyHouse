#!/usr/bin/env python3
# -*- coding: utf8 -*- 

import sys
import fileinput
import time
import json
import http.client
import datetime
import traceback
from os import path
from pathlib import Path

SERVER_IP = "192.168.100.234"
SERVER_PORT = 18100
SERVER_TIME_OUT = 15
STORE_URL = "/GateInfo/StoreGateInfo"
# use test script's dir path as current path
CUR_PATH = Path(path.dirname(path.abspath(__file__)))
PARENT_NODE = 'AdditionalInfo'
# take the time send costs into account 
WAIT_ADJUST = 200
UTC_timestamp = lambda: round(time.time() * 1000)
# time between multiply sending
TIME_GAP = 10


# --------------  FUNCTIONS  ------------------
def send_file(filename):
    if not path.isabs(filename):
        filename = str(CUR_PATH / filename)
    if not path.exists(filename):
        print("[STEP]: Not Exist!", filename)
    print("[STEP]: Loading file", filename)
    token = str(int(str(UTC_timestamp())) - 100) + "012"
    line_index = 0
    bMultiplyRequest = False
    whole_str = ""
    for aline in fileinput.input(files=filename):
        if aline.strip() == "":
            continue
        # test first line if there are multi '}'
        if line_index == 0 and not bMultiplyRequest and aline.count('}') > 1:
            line_index += 1
            bMultiplyRequest = True
        if bMultiplyRequest:
            print("Line", line_index, "is:", aline)
            line_index += 1
            if aline.find('WellGateAct') != -1:
                print(get_response(aline))
            else:
                data = json.loads(aline)
                print(send_request_with_token(data, token))
        else:
            whole_str += aline

    if not bMultiplyRequest:
        #print("[STEP]: Send whole file as a single request:", whole_str)
        if whole_str.find('WellGateAct') != -1:
            print(get_response(whole_str))
        else:
            data = json.loads(whole_str)
            print(send_request_with_token(data, token))
    print("[STEP]: File send finish for", filename)


def send_request_with_token(struct, token):
    if PARENT_NODE in struct and "token" in struct[PARENT_NODE] and "timestamp" in struct[PARENT_NODE]:
        oldtimestamp = struct[PARENT_NODE]["timestamp"]
        struct[PARENT_NODE]["token"] = token
        struct[PARENT_NODE]["timestamp"] = str(UTC_timestamp())
    data = json.dumps(struct, indent=4, sort_keys=True)
    send_request(data)


def send_request(json_text):
    send_json(json_text)


def get_response(json_text):
    return send_json(json_text, "/GateInfo/GetOne")


def send_json(json_text, url=STORE_URL):
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    try:
        print('------------------------------------------', datetime.datetime.now(), sep='\n')
        httpClient = http.client.HTTPConnection(SERVER_IP, SERVER_PORT, timeout=SERVER_TIME_OUT)
        httpClient.request("POST", url, json_text, headers)
        response = httpClient.getresponse()
        result = response.read()
        result = result.decode()
    except:
        einfo = sys.exc_info()
        print(einfo[0], str(einfo[1]), traceback.format_tb(einfo[2], 5))
        print("[STEP]: CAN'T CONNECT TO SERVER!!!")
        return None
    else:
        print("[STEP]: A new request will be send like:")
        print(json_text)
        print("Response:", response.status, response.reason, result[:30], "...")
        return result


# ===============   MAIN   =================
if __name__ == '__main__':
    print("[STEP]: Will send request to server:", SERVER_IP, ":", SERVER_PORT)
    isFirst = True
    if len(sys.argv) > 1:
        for afile in sys.argv[1:]:
            if not isFirst:
                print("\n[WAITING]: Going to wait", TIME_GAP, "seconds before sending next file...\n\n")
                time.sleep(TIME_GAP)
            send_file(afile.split('/')[-1])
            isFirst = False
    else:
        send_file('first.req')



