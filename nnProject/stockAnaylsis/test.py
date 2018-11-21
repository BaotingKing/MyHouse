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


    serx = pd.DataFrame({"time":[23, 60, 77, 56, 99, 12, 58, 88],"year":[2, 0, 7, 5, 9, 1, 8, 8]}, index=['a','b','c','d','e','f','g','h'])
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
    # serx = pd.DataFrame({"time": [23, 60, 77, 56, 99, 12, 58, 88], "year": [2, 0, 7, 5, 9, 1, 8, 8]})
    # sery = pd.Series([1, 0, 1, 1, 0, 0, 1])
    # temp = serx.sort_index(axis=0, ascending=False).copy()
    # serx.iloc[0] = 666
    # print(serx.sort_index(axis=0, ascending=False))
    # print("=====\n:", temp)

    # info = [((3, 4), 2), ((3, 4), 4), ((3, 4), 6), ((9, 8), 8), ((9, 8), 8), ((9, 8), 18), ((9, 8), 28)]
    # for i in range(len(info)):
    #     if i < 3:
    #         continue
    #     print('ok')
    #     # print(info[i-3:i])
    #     print(info[i])
    #     X =[]
    #     for x, y in info[i-3:i]:
    #         X.extend(x)
    #     X = np.array(X)
    #     print(type(X), X)
    # inputs = []
    # for idx in range(3, len(serx)):
    #     element = []
    #     for record in serx[idx - 3:idx].values:
    #         element.extend(record)
    #     print(element)
    #     inputs.append(np.reshape(element, (len(element), 1)))
    # # print(serx)
    # print('==============')
    # print(inputs)
    # for learn in range(0, 100, 2):
    #     print(learn*0.001)

    # ser = pd.Series([23, 60, 77, 56, 99, 12, 58, 88],index=['a','b','c','d','e','f','g','h'])
    # a = ser.index
    # sery = pd.DataFrame({"time": [23, 60, 77, 56, 99, 12, 58, 88], "year": [2, 0, 7, 5, 9, 1, 8, 8]},
    #                     index=ser.index)
    # print(sery)
    #
    # te = 2 * np.random.randint(-1, 1) + 1
    # print('++++++++++')
    # for i in range(6):
    #     te = 2 * np.random.randint(-1, 1) + 1
    #     print(te)
    # # pd.to_csv()
    # a = 99999
    # test = [23, 60, 77, a, 56, 99, 12]
    # print(test[1:-1])
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
         [14, 1, 1], [14, 5, 5], [14, 10, 10], [14, 14, 1], [14, 14, 10], [14, 14, 14]]
    ]
    layer_num = [1, 2, 3]

    for layer_idx in layer_num:
        for hi in hiden_combination[layer_idx - 1]:
            BP_size = [15, 1]
            BP_size.insert(1, hi)
            BP_sizes = []
            for x in BP_size:
                if isinstance(x, int):
                    BP_sizes.append(x)
                else:
                    BP_sizes.extend(x)

            print('hello,this is layer_idx={0},hiden={1},out={2}'.format(layer_idx, hi, BP_sizes))