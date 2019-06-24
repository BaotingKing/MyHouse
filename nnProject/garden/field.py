#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: ZK
# Time: 2018/11/4
import random
import numpy as np
import pandas as pd
import magic_network as snn
from sklearn.model_selection import train_test_split


def vectorized_result(j, classes):
    """离散数据进行one-hot"""
    e = np.zeros((classes, 1))
    e[j] = 1.0
    return e


def get_format_data(X, y, is_test):
    n_dim = X.shape[1]
    inputs = []
    for record in X.values:
        inputs.append(np.reshape(record, (n_dim, 1)))

    if not is_test:
        results = y
    else:
        results = y
    data = list(zip(inputs, results))
    # data = zip(inputs, results)
    return data


def normalize_data(data_source):
    min_data = data_source.min()
    max_data = data_source.max()
    norm_data_source = (data_source[:] - min_data) / (max_data - min_data)
    return norm_data_source


if __name__ == '__main__':
    n_dim = (5 + 2) * 2
    out_dim = 5 + 2
    original_seed_data = pd.read_csv('new_seed.csv')

    seed_normal_data = original_seed_data.copy()

    seed_normal_X = seed_normal_data[:-1]     # 最后一个是要预测的待定值
    seed_normal_y = seed_normal_data[1:]

    print(len(seed_normal_data), len(seed_normal_X), len(seed_normal_y))
    train_x, test_x, train_y, test_y = train_test_split(seed_normal_X,
                                                        seed_normal_y,
                                                        test_size=0.2,
                                                        random_state=0)
    training_data = get_format_data(train_x, train_y, False)
    test_data = get_format_data(test_x, test_y, True)

    print("[Debug]", len(seed_normal_data), len(seed_normal_X), len(seed_normal_y))
    print("[Debug]", type(training_data), len(training_data), type(test_data), len(test_data))
    # BP_size = [n_dim, n_dim * 256, n_dim * 16, n_dim * 3, out_dim]
    # net = snn.StockNetwork(BP_size)
    # net.SGD(training_data=training_data,
    #         epochs=5,
    #         mini_batch_size=10,
    #         learn_rate=0.1,
    #         test_data=None)  # test_data None
    #
    # print(type(net))
