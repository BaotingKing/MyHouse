#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/11/13

RECEPTIVE = 3

DATA_IDX = []
g_max_close = 0
g_min_close = 0
g_test_idx = 0
g_stock_original_data = 0


LAY_NUM = 1
NODE_NUM = 10
EPOCH = 100


def set_cfg(lay_num=None, node_num=None, epoch=None):
    global LAY_NUM
    global NODE_NUM
    global EPOCH
    if lay_num:
        LAY_NUM = lay_num

    if node_num:
        NODE_NUM = node_num

    if epoch:
        EPOCH = epoch


def get_cfg(lay_num=None, node_num=None, epoch=None):
    global LAY_NUM
    global NODE_NUM
    global EPOCH
    return LAY_NUM, NODE_NUM, EPOCH


def set_idx(data_idx=None):
    global DATA_IDX
    DATA_IDX = data_idx


def get_idx():
    global DATA_IDX
    return DATA_IDX


def set_value(max_close=None, min_close=None, stock_original_data=None, test_idx=None):
    global g_max_close
    global g_min_close
    global g_test_idx
    global g_stock_original_data
    g_max_close = max_close
    g_min_close = min_close
    g_test_idx = test_idx
    g_stock_original_data = stock_original_data


def get_value(name, d_value=None):
    global g_max_close
    global g_min_close
    global g_test_idx
    global g_stock_original_data
    try:
        if name == 'g_max_close':
            return g_max_close
        elif name == 'g_min_close':
            return g_min_close
        elif name == 'g_stock_original_data':
            return g_stock_original_data
        elif name == 'g_test_idx':
            return g_test_idx
    except KeyError:
        return d_value