#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/11/13

RECEPTIVE = 3

DATA_IDX = []
g_max_close = 0
g_min_close = 0


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


def set_value(max_close=None, min_close=None):
    global g_max_close
    global g_min_close
    g_max_close = max_close
    g_min_close = min_close


def get_value(name, d_value=None):
    global g_max_close
    global g_min_close
    try:
        if name == 'g_max_close':
            return g_max_close
        elif name == 'g_min_close':
            return g_min_close
    except KeyError:
        return d_value