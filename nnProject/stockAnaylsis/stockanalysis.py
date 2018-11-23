#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: ZK
# Time: 2018/11/4

import os
import shutil
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


if __name__ == '__main__':
    large_cap_data = ts.get_index()
    stock_original_data = ts.get_hist_data('601398', start='2016-06-01', end='2018-06-26')
    print("[Debug]This is original data: \n", stock_original_data.head(), type(stock_original_data))

    stock_data = stock_original_data.copy()
    stock_data.index = pd.DatetimeIndex(stock_original_data.index)
    stock_data.loc[:, 'weekday'] = stock_data.index.weekday
    # print("[Debug]", stock_data.head(4), stock_data.tail(4))
    # print("[Debug]", stock_data.columns)
    print('====================')
    stock_normal_data = stock_data.sort_index(axis=0, ascending=True).copy()

    max_close = stock_data['close'].max()   # 用于后期还原close price
    min_close = stock_data['close'].min()
    cfg.set_value(max_close=max_close, min_close=min_close)
    stock_data.to_csv('stock_normal_data.csv')
    for column in stock_data.columns:   # 数据归一化处理
        if column != "weekday":
            stock_normal_data[column] = normalize_data(stock_data[column])

    # stock_normal_X = stock_normal_data.drop('close', axis=1)
    stock_normal_X = stock_normal_data[['open', 'high', 'low', 'close', 'volume']]  # 'weekday'
    stock_normal_y = stock_normal_data['close']

    train_x, test_x, train_y, test_y = train_test_split(stock_normal_X,
                                                        stock_normal_y,
                                                        test_size=0.035,
                                                        random_state=0,
                                                        shuffle=False)
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

    hiden_combination = [
        [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        [[2, 1], [2, 2], [3, 1], [3, 2], [3, 3], [4, 1], [4, 2], [4, 4], [5, 1], [5, 2], [5, 5], [6, 1], [6, 3], [6, 6],
         [10, 1], [10, 2], [10, 5], [10, 8], [10, 10], [11, 1], [11, 2], [11, 5], [11, 8], [11, 10], [11, 11],
         [12, 1], [12, 2], [12, 5], [12, 10], [12, 12], [13, 1], [13, 2], [13, 15], [13, 10], [13, 12], [13, 13],
         [14, 1], [14, 2], [14, 5], [14, 10], [14, 13], [14, 14], [15, 1], [15, 2], [15, 5], [15, 10], [15, 14],
         [15, 15]],
        [[2, 1, 1], [2, 2, 1], [2, 2, 2], [3, 1, 1], [3, 2, 1], [3, 3, 1], [3, 2, 2], [3, 3, 2], [3, 3, 3],
         [5, 1, 1], [5, 2, 2], [5, 3, 3], [5, 4, 4], [5, 5, 5], [10, 1, 1], [10, 5, 5], [10, 8, 8], [10, 10, 1],
         [10, 10, 10],
         [11, 1, 1], [11, 5, 5], [11, 11, 1], [11, 11, 11],
         [14, 1, 1], [14, 5, 5], [14, 10, 10], [14, 14, 1], [14, 14, 10], [14, 14, 14]],
        [[2, 1, 1, 1], [2, 2, 1, 1], [2, 2, 2, 1], [2, 2, 2, 2], [3, 1, 1, 1], [3, 3, 3, 3],
         [5, 1, 1, 1], [5, 4, 3, 2], [5, 4, 4, 4], [5, 5, 5, 5], [6, 1, 1, 1], [6, 5, 4, 3], [6, 5, 5, 5], [6, 6, 6, 6],
         [7, 1, 1, 1], [7, 6, 5, 4], [7, 6, 6, 6], [7, 7, 7, 7],
         [10, 1, 1, 1], [10, 9, 8, 7], [10, 10, 5, 5], [10, 10, 10, 10],
         [14, 1, 1, 1], [14, 13, 12, 11], [14, 14, 6, 6], [14, 14, 14, 14], [15, 1, 1, 1], [15, 15, 1, 1], [15, 15, 15, 15]],
        [[2, 1, 1, 1, 1], [2, 2, 2, 1, 1], [2, 2, 2, 2, 2], [3, 1, 1, 1, 1], [3, 3, 3, 3, 3],
         [5, 1, 1, 1, 1], [5, 4, 3, 2, 1], [5, 5, 5, 5, 5], [6, 1, 1, 1, 1], [6, 5, 5, 5, 5], [6, 6, 6, 6, 6],
         [7, 1, 1, 1, 1], [7, 6, 5, 4, 3], [7, 6, 6, 6, 6], [7, 7, 7, 7, 7],
         [10, 1, 1, 1, 1], [10, 9, 8, 7, 6], [10, 10, 5, 5, 5], [10, 10, 10, 10, 10],
         [14, 1, 1, 1, 1], [14, 13, 12, 11, 10], [14, 14, 14, 6, 6], [14, 14, 14, 14, 14], [15, 1, 1, 1, 1],
         [15, 15, 15, 15, 1], [15, 15, 15, 15, 15]],
    ]

    for hiden_layer_idx in [1, 2, 3, 4, 5]:   # [1, 2, 3, 4, 5]
        for hi in hiden_combination[hiden_layer_idx - 1]:
            BP_size = [n_dim * cfg.RECEPTIVE, 1]
            BP_size.insert(1, hi)
            BP_sizes = []
            for x in BP_size:
                if isinstance(x, int):
                    BP_sizes.append(x)
                else:
                    BP_sizes.extend(x)

            for learn in [16]:
                for epoch in [200, 500, 1000]:
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


