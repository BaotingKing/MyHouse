#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl
# Time: 2018/8/10
import json
# 读取校验配置
class Launchfile:
    def __init__(self):
        self.cfgcontent = {}


    def load_launchfile(self, file_path):
        try:
            file_handle = open(file_path)
            file_content = file_handle.read()
            self.cfgcontent = json.loads(file_content)
            file_handle.close()
        except Exception:
            print('no or error launch.cfg')
        # finally:
        #     file_handle.close()

        self.checkoutCfg()
        return self.cfgcontent


    def checkoutCfg(self):    # checkout launch.cfg
        name_list = []
        module_list = []
        for key,value in self.cfgcontent.items():
            name_list.append(value["module_name"])
            module_list.append(key)

        idxes = []
        if "roi_recog" in name_list:
            idxes = [i for i in range(len(name_list)) if name_list[i] == "roi_recog"]
            for idx in idxes:


            print("it's ok, idx=%s" % idx)



        print("11111111111111111111")
        print(name_list)
        print("22222222222222222222", len(name_list))
        print(module_list)
        print("33333333333333333333", len(module_list))

