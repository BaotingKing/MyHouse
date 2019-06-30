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
    STEP_CFG = 3
    n_dim = 5 + 2     # red is 5, blue is 2
    inputs = []
    for idx in range(len(X)):
        if (idx + STEP_CFG) > len(X):
            break
        else:
            cell = []
            for i in range(STEP_CFG):
                record = X[idx + i]
                flower = dict(Issue=record['Issue'], Red=record['Red'], Blue=record['Blue'])
                cell.append(flower)
            # inputs.append(np.reshape(record, (n_dim, 1)))
            inputs.append(cell)

    results = []
    if not is_test:
        for record in y[STEP_CFG:]:
            flower = dict(Issue=record['Issue'], Red=record['Red'], Blue=record['Blue'])
            results.append(flower)
    else:
        for record in y[STEP_CFG:]:
            flower = dict(Issue=record['Issue'], Red=record['Red'], Blue=record['Blue'])
            results.append(flower)

    data = list(zip(inputs, results))     # data = zip(inputs, results)
    return data


def normalize_data(data_source):
    """data needed normalize"""
    print('Normalize has put behind')
    data_normal_source = data_source
    # data_normal_source = pd.DataFrame(columns=['Index', 'Issue', 'Red', 'Blue'])
    # for index, row in data_source.iterrows():
    #     red = [i / 35 for i in eval(row['Red'])]
    #     blue = [i / 35 for i in eval(row['Blue'])]
    #     new = pd.DataFrame(columns=['Index', 'Issue', 'Red', 'Blue'])
    #     new.loc[index] = {'Index': index,
    #                       'Issue': row['Issue'],
    #                       'Red': red,
    #                       'Blue': blue}
    #     data_normal_source = pd.concat([data_normal_source, new], sort=False)
    return data_normal_source


if __name__ == '__main__':
    n_dim = (5 + 2) * 3
    out_dim = 5 + 2
    earth = 35 + 12
    original_seed_data = pd.read_csv('new_seed.csv')

    seed_data = original_seed_data.copy()
    seed_normal_data = normalize_data(seed_data)

    seed_normal_X_pd = seed_normal_data[:-1]     # 最后一个是要预测的待定值
    seed_normal_y_pd = seed_normal_data[:]

    seed_normal_X = []
    seed_normal_y = []
    for row in seed_normal_X_pd.iterrows():
        seed_normal_X.append(row[1])
    for row in seed_normal_y_pd.iterrows():
        seed_normal_y.append(row[1])

    print(len(seed_normal_data), len(seed_normal_X), len(seed_normal_y))

    # train_x, test_x, train_y, test_y = train_test_split(seed_normal_X,
    #                                                     seed_normal_y,
    #                                                     test_size=0.2,
    #                                                     random_state=0)
    train_test_boundary = int(len(seed_normal_X)*0.85)
    train_x = seed_normal_X[0:train_test_boundary]
    train_y = seed_normal_y[0:train_test_boundary]

    test_x = seed_normal_X[train_test_boundary:]
    test_y = seed_normal_y[train_test_boundary:]

    print(len(train_x), len(train_y), len(test_x), len(test_y))
    training_data = get_format_data(train_x, train_y, False)
    test_data = get_format_data(test_x, test_y, True)

    print("[Debug]", len(seed_normal_data), len(seed_normal_X), len(seed_normal_y))
    print("[Debug]", type(training_data), len(training_data), type(test_data), len(test_data))
    BP_size = [n_dim, n_dim * 256, earth * 16, earth * 3, out_dim]
    net = snn.StockNetwork(BP_size)
    net.SGD(training_data=training_data,
            epochs=2,
            mini_batch_size=10,
            learn_rate=0.1,
            test_data=test_data)  # test_data None

    print(type(net))
