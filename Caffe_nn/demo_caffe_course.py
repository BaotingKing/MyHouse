#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: ZK
# Time: 2019/01/02    https://nbviewer.jupyter.org/github/BVLC/caffe/blob/master/examples/
import caffe
import caffe_network_model as nn_model
import caffe_solver as nn_solver

caffe_root = '/home/zach/mylab/ml/caffe/'
model_def = caffe_root + 'models/bvlc_reference_caffenet/deploy.prototxt'
model_weights = caffe_root + 'models/bvlc_reference_caffenet/bvlc_reference_caffenet.caffemodel'
model_solver = caffe_root + 'models/bvlc_reference_caffenet/solver.prototxt'


if __name__ == '__main__':
    with open('lenet_auto_train.prototxt', 'w') as f:
        f.write(str(nn_model.lenet('temp', 64)))

    with open('lenet_auto_test.prototxt', 'w') as f:
        f.write(str(nn_model.lenet('temp', 100)))

    nn_solver.lenet_solver()

    """This is for solver"""
    # solver = caffe.SGDSolver(model_solver)  # load solver
    # nn_model.show_solver_info(solver)

    """This is for network"""
    # net = caffe.Net(model_def,
    #                 model_weights,
    #                 caffe.TEST)
    # nn_model.show_net_info(net)




