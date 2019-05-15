# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
import csv
import commands


def print_method(data):
    logtxt = open('title.log', 'w+')
    sys.stdout = logtxt
    with open('title.log', 'r+') as f:
        print("IID     Title")
        for i in range(len(data)):
            print(data[i]['iid'], end="     ")
            print(data[i]['title'])
            print('\n')


def csv_method(data):
    result_file = 'title.csv'
    headers = ['iid', 'title', 'state', 'web_url']    # Add Required information
    with open(result_file, 'w') as csvfile:
        f_scv = csv.writer(csvfile)
        f_scv.writerow(headers)
        for i in range(len(data)):
            ti = data[i]['title']
            iid = data[i]['iid']
            state = data[i]['state']
            src = data[i]['web_url']
            f_scv.writerow([iid, ti, state, src])


if __name__ == '__main__':
    with open('a.json', 'r+') as f:
        a = f.readline()
    a = a[1:-1]
    a = a.replace('null', 'None')
    a = a.replace('false', 'False')
    a = a.replace('ture', 'True')
    data = eval(a)

    cmd = 'curl --header "PRIVATE-TOKEN: ksax5iSArE1tcVyyhxyz" ' \
          'http://192.168.105.19:30000/api/v4/projects/64/issues?per_page=100 '
    recode, stdout = commands.getstatusoutput(cmd)
    print(recode)
    print('===================')
    stdout = commands.getoutput(cmd)
    print(stdout)

    metod = 0
    if metod == 0:
        csv_method(data)
    elif metod == 1:
        print_method(data)

