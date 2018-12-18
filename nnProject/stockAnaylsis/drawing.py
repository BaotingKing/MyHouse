#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/12/16
import re
import pandas as pd

if __name__ == '__main__':
    stock_result_data = pd.read_csv('./data/601398fianl_result.csv')
    cloumns_name = stock_result_data.columns.values.tolist()
    epoch_type = cloumns_name[2].split('/')[-1]
    layer_type = re.split('-|_|\]|\[', cloumns_name[2])[1]
    node_type = re.split('-|_|\]|\[', cloumns_name[2])[4]
    a = stock_result_data.iloc[:, 1]
    b = stock_result_data.iloc[:, -2]
    for idx in range(len(stock_result_data)):
        if stock_result_data.iloc[idx, 1] == 'ture_value':
            continue
        e = type(stock_result_data.iloc[idx, 1])
        c = float(stock_result_data.iloc[idx, 1])
        d = stock_result_data.iloc[idx, -2]

        new_mee = abs(float(stock_result_data.iloc[idx, 1]) - float(stock_result_data.iloc[idx, -2]))

    for i in range(len(stock_result_data)):
        for j in range(len(stock_result_data)//16):
            ture_value = 1