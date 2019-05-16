#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time: 2019/01/02
"""This file contains a few caffe network models define"""
import caffe
from caffe import layers as L
from caffe import params as P


def show_net_shape(net_prototxt, solver_type='SGD'):
    solver = None
    if solver_type == 'SGD':
        solver = caffe.SGDSolver(net_prototxt)  # load solver
    print('****************************************************')
    for layer_name, param in solver.params.iteritems():
        print(layer_name + '\t' + str(param[0].data.shape), str(param[1].data.shape))
    print('****************************************************')
    for layer_name, spatial_dim in solver.net.blobs.items():
        print(layer_name + '\t' + str(spatial_dim))
    print('****************************************************')



def lenet(lmdb, batch_size):
    """A simple version of LeNet: a series of linear and simple nonlinear transformations"""
    net = caffe.NetSpec()

    net.data, net.label = L.Data(batch_size=batch_size, backend=P.Data.LMDB, source=lmdb,
                                 transform_param=dict(scale=1. / 255), ntop=2)

    net.conv1 = L.Convolution(net.data, kernel_size=5, num_output=20, weight_filler=dict(type='xavier'))
    net.pool1 = L.Pooling(net.conv1, kernel_size=2, stride=2, pool=P.Pooling.MAX)
    net.conv2 = L.Convolution(net.pool1, kernel_size=5, num_output=50, weight_filler=dict(type='xavier'))
    net.pool2 = L.Pooling(net.conv2, kernel_size=2, stride=2, pool=P.Pooling.MAX)
    net.fc1 = L.InnerProduct(net.pool2, num_output=500, weight_filler=dict(type='xavier'))
    net.relu1 = L.ReLU(net.fc1, in_place=True)
    net.score = L.InnerProduct(net.relu1, num_output=10, weight_filler=dict(type='xavier'))
    net.loss = L.SoftmaxWithLoss(net.score, net.label)

    return net.to_proto()