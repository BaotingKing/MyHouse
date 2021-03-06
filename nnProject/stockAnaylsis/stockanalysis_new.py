#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: ZK
# Time: 2018/11/4

import os
import math
import shutil
import numpy as np
import pandas as pd
import tushare as ts
import matplotlib.pyplot as plt
import stock_network as snn
import config as cfg
from sklearn.model_selection import train_test_split

# 获取数据
stock_code = ['600031', '601398', '000333', '600519', '999999']
s_start = '2013-09-18'
s_end = '2018-09-18'


def vectorized_result(j, classes):
    """离散数据进行one-hot"""
    e = np.zeros((classes, 1))
    e[j] = 1.0
    return e


def get_format_data(X, y, is_test):
    n_dim = X.shape[1]
    inputs = []
    element = []
    length = len(X)

    for idx in range(cfg.RECEPTIVE, length):
        element = []
        for record in X[idx - cfg.RECEPTIVE:idx].values:
            element.extend(record)
        inputs.append(np.reshape(element, (len(element), 1)))

    if not is_test:
        results = y[cfg.RECEPTIVE:]
    else:
        results = y[cfg.RECEPTIVE:]
        cfg.set_idx(results.index)

    data = list(zip(inputs, results))
    # data = zip(inputs, results)
    return data


def normalize_data(data_source):
    min_data = data_source.min()
    max_data = data_source.max()
    # min_data = 0
    # max_data = 1
    norm_data_source = (data_source[:] - min_data)/(max_data - min_data)
    return norm_data_source


def log_data(data_source):
    denom = data_source[0]
    log_data_source = data_source.copy()
    for idx in range(len(data_source)):
        if denom != 0:
            log_data_source[idx] = math.log(data_source[idx]/denom)
        else:
            log_data_source[idx] = None
        denom = data_source[idx]
    return log_data_source


if __name__ == '__main__':
    large_cap_data = ts.get_index()
    stock_original_data = ts.get_hist_data('sh', start='2016-09-01', end='2018-09-26')
    # stock_original_data = pd.read_csv('./data/601398stock_normal_data.csv')
    # stock_original_data = pd.read_excel('./data/600519.xls')
    # stock_original_data.index = stock_original_data['date']

    print("[Debug]This is original data: \n", stock_original_data.head(), type(stock_original_data))

    stock_data = stock_original_data.copy()
    stock_data.index = pd.DatetimeIndex(stock_original_data.index)
    stock_data.loc[:, 'weekday'] = stock_data.index.weekday
    # print("[Debug]", stock_data.head(4), stock_data.tail(4))
    # print("[Debug]", stock_data.columns)
    print('====================')
    stock_normal_data = stock_data.sort_index(axis=0, ascending=True).copy()
    # stock_normal_temp = stock_normal_data.copy()

    max_close = stock_data['close'].max()   # 用于后期还原close price
    min_close = stock_data['close'].min()

    stock_data.to_csv('stock_normal_data.csv')
    for column in ('open', 'high', 'low', 'close', 'volume'):   # 数据归一化处理  stock_data.columns
        if column != "weekday":
            stock_normal_data[column] = log_data(stock_normal_data[column])

    # x = np.arange(len(stock_normal_data))
    # y = stock_normal_temp['close']
    # plt.plot(x, y)
    # plt.show()

    stock_normal_X = stock_normal_data[['open', 'high', 'low', 'close', 'volume']]  # 'weekday'
    stock_normal_y = stock_normal_data['close']

    train_x, test_x, train_y, test_y = train_test_split(stock_normal_X,
                                                        stock_normal_y,
                                                        test_size=0.030,
                                                        random_state=0,
                                                        shuffle=False)

    test_x = stock_normal_X.copy()
    test_y = stock_normal_y.copy()
    cfg.set_value(max_close=max_close,
                  min_close=min_close,
                  stock_original_data=stock_data.sort_index(axis=0, ascending=True),
                  test_idx=test_y[cfg.RECEPTIVE:].index)
    n_dim = train_x.shape[1]
    training_data = get_format_data(train_x, train_y, False)
    test_data = get_format_data(test_x, test_y, True)
    print("[Log_information]", type(training_data), len(training_data), type(test_data), len(test_data))
    """final result file operation"""
    if os.path.exists('fianl_result.csv'):
        shutil.copyfile('fianl_result.csv', 'fianl_result.csv.bak')
        os.remove('fianl_result.csv')
        if not os.path.exists('fianl_result.csv'):
            print('fianl_result.csv has been saved and delete')
    

    for hiden_layer_idx in [1]:   # [1, 2, 3, 4, 5]   # Tag is :2018.11.23
        if hiden_layer_idx == 1:
            hiden_com = [[x] for x in [9, 12]]
        elif hiden_layer_idx == 2:
            hiden_com = [[x, y] for x in range(1, 16) for y in range(1, 16)]
        elif hiden_layer_idx == 3:
            hiden_com = [[x, y, z] for x in [2, 10] for y in [2, 10] for z in [2, 10]]

        for hi in hiden_com:
            BP_size = [n_dim * cfg.RECEPTIVE, 1]
            BP_size.insert(1, hi)
            BP_sizes = []
            for x in BP_size:
                if isinstance(x, int):
                    BP_sizes.append(x)
                else:
                    BP_sizes.extend(x)

            for learn in [16]:
                for epoch in [200, 500, 1000, 2000, 3000, 4000]:
                    a = len(BP_sizes)
                    cfg.set_cfg(lay_num=len(BP_sizes) - 2, node_num=BP_sizes[1:-1], epoch=epoch)
                    print('hello,this is hiden_layer_num={0},hiden={1},out={2}'.format(hiden_layer_idx, hi, BP_sizes))
                    net = snn.StockNetwork(BP_sizes)
                    net.SGD(training_data=training_data,
                            epochs=epoch,
                            mini_batch_size=12,
                            learn_rate=learn*0.01,
                            test_data=test_data)    # test_data None

                    print('[Processing]: The config information is:.....')


