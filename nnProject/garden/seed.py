#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/11/14

# -*- coding: utf-8 -*-

from network import *

def vectorized_result(j,nclass):
    """离散数据进行one-hot"""
    e = np.zeros((nclass, 1))
    e[j] = 1.0
    return e

def get_format_data(X,y,isTest):
    ndim = X.shape[1]
    nclass = len(np.unique(y))
    inputs = [np.reshape(x, (ndim, 1)) for x in X]
    if not isTest:
        results = [vectorized_result(y,nclass) for y in y]
    else:
        results = y
    data = list(zip(inputs, results))
    # data = zip(inputs, results)
    return data

#随机生成数据
from sklearn.datasets import *
np.random.seed(0)
X, y = make_moons(600, noise=0.20)
ndim = X.shape[1]
nclass = len(np.unique(y))

#划分训练、测试集
from sklearn.model_selection import train_test_split
train_x,test_x,train_y,test_y = train_test_split(X,y,test_size=0.2,random_state=0)

training_data = get_format_data(train_x,train_y,False)
test_data = get_format_data(test_x,test_y,True)

net = Network(sizes=[ndim,12,6,nclass])
net.SGD(training_data=training_data,epochs=1000,mini_batch_size=12,eta=0.1,test_data=test_data)
