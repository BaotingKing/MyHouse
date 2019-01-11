#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl
# Time: 2019/01/11
import os
import re
import sys


def osk_settings_init(start=False,
                      end=False,
                      settings_dir='/home/westwell/Documents/Oskrovski/WellOceanGate/WellOceanGate/settings.py'):
    try:
        settings_bak = settings_dir + '.bak'
        if start:
            shutil.copyfile(os.path.abspath(settings_dir), os.path.abspath(settings_bak))
        elif end:
            shutil.copyfile(os.path.abspath(settings_bak), os.path.abspath(settings_dir))
            os.remove(os.path.abspath(settings_bak))
    except:
        print('[Warning]: Initialization settings.py failed')


def config_set(dir_name,
               config_name='settings.cfg',
               settings_dir='/home/westwell/Documents/Oskrovski/WellOceanGate/WellOceanGate/settings.py'):
    for root, dirs_labels, file_names in os.walk(dir_name):
        for file_name in file_names:
            if file_name == config_name:
                try:
                    config_dir = os.path.join(root, file_name)
                    with open(config_dir, 'r', encoding='UTF-8') as cfg_handle:
                        for out_record in cfg_handle:
                            items = re.split(':|=', out_record)
                            key_item = items[0].strip()
                            key_value = items[-1].strip()
                            le = len(key_value)
                            a = filter(str.isalpha, key_value)
                            le = len(a)
                            if not key_item:
                                continue
                            with open(settings_dir, 'r', encoding='UTF-8') as setting_handle:
                                lines = []
                                for in_record in setting_handle:
                                    if key_item in in_record:
                                        if 'false' in in_record:
                                            in_record = in_record.replace('false', key_value)
                                        elif 'true' in in_record:
                                            in_record = in_record.replace('true', key_value)
                                    lines.append(in_record)
                            with open(settings_dir, 'w+') as setting_handle:
                                setting_handle.writelines(lines)

                except:
                    pass