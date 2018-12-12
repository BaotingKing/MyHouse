#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/11/14

import pandas as pd
import tushare as ts
from sklearn.model_selection import train_test_split
from data.network import *


def normalize_data(data_source):
    min_data = data_source.min()
    max_data = data_source.max()
    norm_data_source = (data_source[:] - min_data)/(max_data - min_data)
    return norm_data_source


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
    data = list(zip(inputs, results))
    # data = zip(inputs, results)
    return data


if __name__ == '__main__':
    large_cap_data = ts.get_index()
    stock_original_data = ts.get_hist_data('601398', start='2013-09-18', end='2018-11-08')
    print("[Debug]This is original data: \n", stock_original_data.head(), type(stock_original_data))

    stock_data = stock_original_data.copy()
    stock_data.index = pd.DatetimeIndex(stock_original_data.index)
    stock_data.ix[:, 'weekday'] = stock_data.index.weekday
    print("[Debug]", stock_data.head(4), stock_data.tail(4))
    print("[Debug]", stock_data.columns)
    print('====================')
    stock_normal_data = stock_data.sort_index(axis=0, ascending=True).copy()

    max_close = stock_data['close'].max()   # 用于后期还原close price
    min_close = stock_data['close'].min()
    cfg.set_value(max_close=max_close, min_close=min_close)
    # stock_data.to_csv('stock_normal_data.csv')
    for column in stock_data.columns:   # 数据归一化处理
        if column != "weekday":
            stock_normal_data[column] = normalize_data(stock_data[column])

    # stock_normal_X = stock_normal_data.drop('close', axis=1)
    stock_normal_X = stock_normal_data[['open', 'high', 'low', 'close', 'volume']]  # 'weekday'
    stock_normal_y = stock_normal_data['close']

    train_x, test_x, train_y, test_y = train_test_split(stock_normal_X,
                                                        stock_normal_y,
                                                        test_size=0.15,
                                                        random_state=0,
                                                        shuffle=False)

    n_dim = train_x.shape[1]
    training_data = get_format_data(train_x, train_y, False)
    test_data = get_format_data(test_x, test_y, True)

    print("[Debug0]", type(training_data), len(training_data), type(test_data), len(test_data))
    BP_size = [n_dim*3, 14, 1]

    # net = snn.StockNetwork(BP_size)
    net = Network(BP_size)
    net.SGD(training_data=training_data,
            epochs=1000,
            mini_batch_size=12,
            eta=0.1,
            test_data=test_data)  # test_data None

    print('It is OK!', type(net))
