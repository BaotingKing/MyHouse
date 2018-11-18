#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/11/13

g_fitting_size = 3

RECEPTIVE = 3

g_max_close = 0
g_min_close = 0


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