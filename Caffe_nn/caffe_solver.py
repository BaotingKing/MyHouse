#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Time: 2019/01/02
"""This file contains a few templates for solver.prototxt"""
import os
import argparse
from caffe.proto.caffe_pb2 import SolverParameter


def lenet_solver_simple():
    """A simple version of LeNet's solver proto"""
    solver = SolverParameter()

    solver.train_net = 'lenet_auto_train.prototxt'
    solver.test_net.append('lenet_auto_test.prototxt')
    solver.test_iter.append(100)
    solver.test_interval = 500
    solver.base_lr = 0.01
    solver.momentum = 0.9
    solver.weight_decay = 0.0005
    solver.lr_policy = 'inv'
    solver.gamma = 0.0001
    solver.power = 0.75
    # solver.stepsize = 2500
    solver.display = 100
    solver.max_iter = 10000
    solver.snapshot = 5000
    solver.snapshot_prefix = 'SNAPSHOT_FULL_PATH'
    solver.solver_mode = SolverParameter.GPU

    with open('SOLVER_FULL_PATH', 'w') as f:    # generating prototxt
        f.write(str(solver))


def lenet_solver():
    """A simple version of LeNet's solver proto"""
    parser = argparse.ArgumentParser()

    parser.add_argument('--train_net', default='../../Lenet/lenet_auto_train.prototxt',
                        help='path to train net prototxt. [DEFAULT=../../Section4/caffenet_train.prototxt]')
    parser.add_argument('--test_net', default='../../Lenet/lenet_auto_test.prototxt',
                        help='path to validation net prototxt. [DEFAULT=../../Section4/caffenet_valid.prototxt]')
    parser.add_argument('--solver_target_folder', default='../../Lenet/',
                        help='solver target FOLDER. [DEFAULT=../../Section5/]')
    parser.add_argument('--solver_filename', default='Lenet_solver.prototxt',
                        help='solver prototxt NAME. [DEFAULT=caffenet_solver.prototxt]')
    parser.add_argument('--snapshot_target_folder', default='../../Lenet/',
                        help='snapshot target FOLDER. [DEFAULT=../../Section6/')
    parser.add_argument('--snapshot_prefix', default='Lenet', help='snapshot NAME prefix, [DEFAULT=caffenet]')
    args = parser.parse_args()

    SOLVER_FULL_PATH = args.solver_target_folder + args.solver_filename
    SNAPSHOT_FULL_PATH = args.snapshot_target_folder + args.snapshot_prefix
    os.system('rm -rf ' + SOLVER_FULL_PATH)
    os.system('rm -rf ' + SNAPSHOT_FULL_PATH + '*')

    solver = SolverParameter()

    solver.train_net = 'lenet_auto_train.prototxt'
    solver.test_net.append('lenet_auto_test.prototxt')
    solver.test_iter.append(100)
    solver.test_interval = 500
    solver.base_lr = 0.01
    solver.momentum = 0.9
    solver.weight_decay = 0.0005
    solver.lr_policy = 'inv'
    solver.gamma = 0.0001
    solver.power = 0.75
    # solver.stepsize = 2500
    solver.display = 100
    solver.max_iter = 10000
    solver.snapshot = 5000
    solver.snapshot_prefix = SNAPSHOT_FULL_PATH
    solver.solver_mode = SolverParameter.GPU

    with open(args.solver_filename, 'w') as f:    # generating prototxt
        f.write(str(solver))
