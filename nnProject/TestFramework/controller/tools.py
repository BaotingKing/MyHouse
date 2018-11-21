#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Zhang.Baoting
# Time: 2018/8/14
import os
import random
import string
import logging


def unfold_list(mixed_list):
    """将list中包含的list、tuple等全部展开"""
    new_list = []
    for sublist in mixed_list:
        if isinstance(sublist, list):
            new_list = new_list + unfold_list(sublist)
        else:
            new_list.append(sublist)
    return new_list


def check_param_topic():
    pass


def type2topic(detect_type):
    """It's a little tricky to name"""
    set_topic = ['trigger_topic',
                 'letters_topic',
                 'digits_topic',
                 'types_topic',
                 'plate_topic']
    type_topic = []
    if detect_type == 'trigger':
        type_topic = set_topic[0]
    elif detect_type == 'letter':
        type_topic = set_topic[1]
    elif detect_type == 'digit':
        type_topic = set_topic[2]
    elif detect_type == 'type':
        type_topic = set_topic[3]
    elif detect_type == 'char':  # he_he
        type_topic = set_topic[4]

    return type_topic


def check_relationship_trans(topic_name):
    comparison_relationship = {
        "trigger_topic": "output_topic",
        "container_trigger_topic": "container_cam_trigger",
        "plate_trigger_topic": "plate_cam_trigger",
        "plate_roi_topic": "plate_cam_trigger",
        "result_topic": "output_topic",
    }

    return comparison_relationship[topic_name]


def check_adaptive(target, compare, para_name='TestTopic'):  # adaptive str and list compare
    if type(target) == type(compare):
        if target == compare:
            return True
        else:
            # print(target)
            # print(compare)
            print('     Error item configuration: %s' % para_name)
            return False
    elif type(target) == str:
        if target in compare:
            return True
        else:
            print('     Error item configuration: %s' % para_name)
            return False
    elif type(compare) == str:
        if compare in target:
            return True
        else:
            print('     Error item configuration: %s' % para_name)
            return False


def logging_run(filename=os.path.join(os.getcwd(), 'log.txt'),
                level=logging.WARN,
                filemode='w',
                format='%(asctime)s - %(levelname)s: %(message)s'):
    # pass
    logging.basicConfig(filename=filename, level=level, filemode=filemode, format=format)
    logging.debug('debug')  # 被忽略
    logging.info('info')  # 被忽略
    logging.warning('warn')
    logging.error('error')


def random_gen_content(min_length=0, max_length=25):
    length = random.randint(min_length, max_length)
    letters = string.ascii_letters + string.digits
    return ''.join([random.choice(letters) for _ in range(length)])
