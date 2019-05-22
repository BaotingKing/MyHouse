#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time: 2019/01/02
"""This file contains a few caffe network models define"""
import caffe
import numpy as np
import matplotlib as plt
from caffe import layers as L
from caffe import params as P


def show_solver_info(solver):
    print('============= This is information in solver: ========')
    # print('Print solver infor:\n', dir(solver))
    print('Dispay = {0}'.format(solver.param.display))
    print('Layer_wise_reduce = {0}'.format(solver.param.layer_wise_reduce))
    print('max_iter = {0}'.format(solver.param.max_iter))
    print('****************Each output size**************************')
    print('        batch size, feature dim, spatial dim')
    for layer_name, spatial_dim in solver.net.blobs.items():
        print(layer_name + '\t' + str(spatial_dim.data.shape))
    print('****************Weight sizes******************************')
    for layer_name, weight_dim in solver.net.params.items():
        print(layer_name + '\t' + str(weight_dim[0].data.shape))


def show_net_info(net):
    print('Print caffe net methods:\n', dir(net))
    print('----------------------------------------------------')
    print('------------Show the output shape-------------------')
    print('****** (batch_size, channel_dim, height, width)')
    for layer_name, blob in net.blobs.iteritems():
        print(layer_name + '\t' + str(blob.data.shape))

    print('****************************************************')
    print('************Show the param shapes*******************')
    for layer_name, param in net.params.iteritems():
        print(layer_name, str(param[0].data.shape), str(param[1].data.shape))


def visual_heatmap(data):
    """Take an array of shape (n, height, width) or (n, height, width, 3)
    and visualize each (height, width) thing in a grid of size approx. sqrt(n) by sqrt(n)"""
    # normalize data for display
    data = (data - data.min()) / (data.max() - data.min())

    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = (((0, n ** 2 - data.shape[0]),
                (0, 1), (0, 1))  # add some space between filters
               + ((0, 0),) * (data.ndim - 3))  # don't pad the last dimension (if there is one)
    data = np.pad(data, padding, mode='constant', constant_values=1)  # pad with ones (white)

    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])

    plt.imshow(data)
    plt.axis('off')


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