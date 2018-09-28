#!/usr/bin/env python3
# -*- coding: utf8 -*- 

from os import path
from pathlib import Path
import sys
import fileinput
import time
import json
import http.client
import datetime
import traceback

# serverip = "192.168.101.196"
serverip = "192.168.101.234"
serverport = 18100
servertimeout = 15
storeurl = "/GateInfo/StoreGateInfo"
# use test script's dir path as current path
curpath = Path(path.dirname(path.abspath(__file__)))
parentnode = 'AdditionalInfo'
# take the time send costs into account 
waitadjust = 200
UTC_timestamp = lambda: round(time.time() * 1000)
# time between multiply sending
timegap = 10



# --------------  FUNCTIONS  ------------------
def sendfile(filename):
    if not path.isabs(filename):
        filename = str(curpath / filename)
    if not path.exists(filename):
        print("[STEP]: Not Exist!", filename)
    print("[STEP]: Loading file", filename)
    token = str(int(str(UTC_timestamp())) - 100) + "012"
    lineindex = 0
    bMultiplyRequest = False
    wholestr = ""
    for aline in fileinput.input(files=(filename)):
        if aline.strip() == "":
            continue
        # test first line if there are multi '}'
        if lineindex==0 and not bMultiplyRequest and aline.count('}') > 1:
            lineindex += 1
            bMultiplyRequest = True
        if bMultiplyRequest:
            print("Line", lineindex, "is:", aline)
            lineindex += 1
            if aline.find('WellGateAct') != -1:
                print(getresponse(aline))
            else:
                data = json.loads(aline)
                print(sendrequest_withtoken(data, token))
        else:
            wholestr += aline

    if not bMultiplyRequest:
        #print("[STEP]: Send whole file as a single request:", wholestr)
        if wholestr.find('WellGateAct') != -1:
            print(getresponse(wholestr))
        else:
            data = json.loads(wholestr)
            print(sendrequest_withtoken(data, token))
    print("[STEP]: File send finish for", filename)


def sendrequest_withtoken(struct, token):
    if parentnode in struct and "token" in struct[parentnode] and "timestamp" in struct[parentnode]:
        oldtimestamp = struct[parentnode]["timestamp"]
        struct[parentnode]["token"] = token
        struct[parentnode]["timestamp"] = str(UTC_timestamp())
    data = json.dumps(struct, indent=4, sort_keys=True)
    sendrequest(data)


def sendrequest(json_text):
    sendjson(json_text)


def getresponse(json_text):
    return sendjson(json_text, "/GateInfo/GetOne")


def sendjson(json_text, url=storeurl):
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    try:
        print('------------------------------------------', datetime.datetime.now(), sep='\n')
        httpClient = http.client.HTTPConnection(serverip, serverport, timeout=servertimeout)
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
    print("[STEP]: Will send request to server:", serverip, ":", serverport)
    isFirst = True
    if len(sys.argv) > 1:
        for afile in sys.argv[1:]:
            if not isFirst:
                print("\n[WAITING]: Going to wait", timegap, "seconds before sending next file...\n\n")
                time.sleep(timegap)
            sendfile(afile.split('/')[-1])
            isFirst = False
    else:
        sendfile('first.req')



