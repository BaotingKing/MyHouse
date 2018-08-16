#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Zhang.Baoting
# Time: 2018/8/14


def unfold_list(mult_list):
    new_list = []
    for sublist in mult_list:
        if isinstance(sublist, list):
            new_list = new_list + unfold_list(sublist)
        else:
            new_list.append(sublist)
    return new_list


def check_param_topic():
    pass


def type2topic(detect_type):   # I am hehe, It's a little tricky to name
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
    elif detect_type == 'char':       # he_he
        type_topic = set_topic[4]

    return type_topic


def check_item_ref_resultsend(topic_name):
    comparison_relationship = {
        "trigger_topic": "output_topic",
        "container_trigger_topic": "container_cam_trigger",
        "plate_trigger_topic": "plate_cam_trigger",
        "plate_roi_topic": "plate_cam_trigger",
        "result_topic": "output_topic",
    }

    return comparison_relationship[topic_name]


def check_adaptive(target, compare, para_name='TestTopic'):   # adaptive str and list compare
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


