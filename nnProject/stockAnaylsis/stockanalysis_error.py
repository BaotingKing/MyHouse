#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: ZK
# Time: 2018/11/4

import os
import shutil
import math
import numpy as np
import pandas as pd
import tushare as ts
import stock_network as snn
import config as cfg
from sklearn.model_selection import train_test_split

# 获取数据
stock_code = ['000333', '600519', '601398', '999999']
s_start = '2013-09-18'
s_end = '2018-09-18'


def vectorized_result(j, classes):
    """离散数据进行one-hot"""
    e = np.zeros((classes, 1))
    e[j] = 1.0
    return e


def get_format_data(X, y, is_test):
    inputs = []
    element = []
    length = len(X)

    for idx in range(cfg.RECEPTIVE, length):
        element = []
        if isinstance(X, pd.DataFrame):
            for record in X[idx - cfg.RECEPTIVE:idx].values:
                element.extend(record)
        else:
            for record in [X[idx - cfg.RECEPTIVE:idx]]:
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
    # stock_original_data = ts.get_hist_data('601398', start='2016-06-01', end='2018-06-26')
    stock_normal_data = pd.read_excel('./data/2018-12-28_600519fianl_result.xlsx')
    stock_normal_data.index = stock_normal_data['date']

    max_close = stock_normal_data['error'].max()  # 用于后期还原close price
    min_close = stock_normal_data['error'].min()

    for column in ['error']:  # 数据归一化处理  stock_data.columns
        if column != "weekday":
            stock_normal_data[column] = normalize_data(stock_normal_data[column])

    stock_predict_err = stock_normal_data['error']
    stock_predict_X = stock_predict_err.copy()
    stock_predict_y = stock_predict_err.copy()
    train_x, test_x, train_y, test_y = train_test_split(stock_predict_X,
                                                        stock_predict_y,
                                                        test_size=0.038,
                                                        random_state=0,
                                                        shuffle=False)
    cfg.set_value(max_close=max_close,
                  min_close=min_close,
                  stock_original_data=stock_predict_err.sort_index(axis=0, ascending=True),
                  test_idx=test_y[cfg.RECEPTIVE:].index)
    if isinstance(stock_predict_err, pd.DataFrame):
        n_dim = stock_predict_err.columns.size
    else:
        n_dim = 1
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
            hiden_com = [[x] for x in range(2, 16)]
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
                for epoch in [200, 500, 2000, 4000]:
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


