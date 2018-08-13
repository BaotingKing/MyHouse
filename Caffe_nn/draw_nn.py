#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Zhang.Baoting
# Time: 2018/8/13

import sys
caffe_root = '/home/zk/caffe/'
sys.path.insert(0, caffe_root + 'python')
from caffe import layers as L
from caffe import params as P
import caffe


def  lenet(lmdb, batch_size):
    n = caffe.NetSpec()
    n.data, n.label = L.Data(
        batch_size = batch_size, backend=P.Data.LMDB, source=lmdb,
        transform_para = dict(scale=1./255), ntop=2)
    n.conv1 = L.Convolution(n.data, kernel_size=5, num_output=20, weight_filler=dict(type='xavier'))
    n.pool1 = L.Pooling(n.conv1, kernel_size=2, stride=2, pool=P.Pooling.MAX)
    n.conv2 = L.Convolution(n.pool1, kernel_size=5, num_output=50, weight_filler=dict(type='xavier'))
    n.pool2 = L.Pooling(n.conv2, kernel_size=2, stride=2, pool=P.Pooling.MAX)
    n.ip1   = L.InnerProduct(n.pool2, num_output=500, weight_filler=dict(type='xavier'))
    n.relu1 = L.ReLU(n.ip1, in_place=True)
    n.ip2   = L.InnerProduct(n.relu1, num_output=10, weight_filler=dict(type='xavier'))
    n.loss  = L.SoftmaxWithLoss(n.ip2, n.label)
    return n.to_proto()

with open('lenet_auto_train.prototxt', 'w') as f:
    f.write(str(lenet('examples/mnist/mnist_train.lmdb', 64)))

with open('lenet_auto_test.prototxt', 'w') as f:
    f.write(str(lenet('examples/mnist/mnist_test.lmdb', 100)))