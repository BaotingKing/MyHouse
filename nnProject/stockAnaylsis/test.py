#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/11/4
import numpy as np
import pandas as pd
# import tushare as ts
# import draft as df
# import tensorflow as tf
# from sklearn.datasets import *

def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))

print('000000')

if __name__ == '__main__':
    # stock_original_data = ts.get_hist_data('000333', start='2018-01-18', end='2018-09-08')
    # # stock_original_data = ts.get_h_data('000333', start='2013-09-18', end='2018-09-08')
    # print(stock_original_data.head(), type(stock_original_data))
    #
    # stock_data = stock_original_data.copy()
    # stock_data.index = pd.DatetimeIndex(stock_original_data.index)
    # stock_data.ix[:, 'weekday'] = stock_data.index.weekday
    # print(stock_data.head(8))
    #
    # weekday_counts = stock_data.groupby('weekday').sum()
    # print(weekday_counts)
    #
    # stock_data_temp = stock_data.dropna(axis=1, how='all')
    # print(stock_data_temp.head())
    #
    # stock_data_sum = stock_data.sum(axis=1).to_frame()
    # print(stock_data_sum.head(), type(stock_data_sum))
    # index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', \
    #          'Saturday', 'Sunday']
    # d = {'col1': [1, 2], 'col2': [3, 4]}
    # df_data = pd.DataFrame({'open': ['11', '12', '13', '14', '15', '16', '17']}, index=index)
    # df = pd.DataFrame(data=d)
    # print(df_data.columns)
    # print(df)
    # sizes = [3, 2, 4]
    # biases = [np.random.randn(y, 1) for y in sizes[1:]]
    #
    # weights = [np.random.randn(y, x)
    #            for x, y in zip(sizes[:-1], sizes[1:])]
    # print('biases is =', biases, len(biases))
    # print('weights is =', weights, len(weights))
    #
    # for (x, y) in zip(sizes[:-1], sizes[1:]):
    #     print(x, y)
    #
    # # loss = tf.train.GradientDescentOptimizer()
    #
    # nabla_b = [2, 3, 5, 8]
    # delta_nabla_b = [1, 2, 3, 4]
    #
    # nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
    # print('==============', nabla_b)


    # ser = pd.Series([23,60,77,56,99,12,58,88])
    # # ser = [23,60,77,56,99,12,58,88]
    #
    # a = ser.max()
    # b = ser.min()
    # ser[:] = (ser[:] - b)/(a - b)
    # print(ser, a, b)
    #
    # np.random.seed(0)
    # X, y = make_moons(200, noise=0.20)
    # ndim = X.shape[1]
    # nclass = len(np.unique(y))
    # print("ndim is x = {}, y ={}:".format(X.shape, y.shape))
    # print(nclass, np.unique(y))
    # print("====")
    # print("x is = {}, y is = {}".format(X, y))


    serx = pd.DataFrame({"time":[23, 60, 77, 56, 99, 12, 58, 88],"year":[2, 0, 7, 5, 9, 1, 8, 8]})
    # serx = pd.Series([23, 60, 56, 99, 12, 58, 88])
    # sery = pd.Series([1,0,1,1,0,0,1])
    # data = zip(serx, sery)
    # print(serx, sery.name)
    # print("data is:", sery.name, data)
    # for a, b in data:
    #     print("a = {} and b = {}".format(a, b))
    # print(serx)
    # n_dim = 2
    # inputs = []
    # inputsss = []
    # for indexs in serx.index:
    #     print(serx.loc[indexs].values[:])
    #     inputs.append(np.reshape(serx.loc[indexs].values[:], (n_dim, 1)))
    #     inputsss.append(serx.loc[indexs].values[:])
    #     print(inputs)
    # print("=========\n", type(inputs))
    # print(inputs[1], len(inputs[1]),inputsss)
    serx = pd.DataFrame({"time": [23, 60, 77, 56, 99, 12, 58, 88], "year": [2, 0, 7, 5, 9, 1, 8, 8]})
    sery = pd.Series([1, 0, 1, 1, 0, 0, 1])
    temp = serx.sort_index(axis=0, ascending=False).copy()
    serx.iloc[0] = 666
    print(serx.sort_index(axis=0, ascending=False))
    print("=====\n:", temp)
