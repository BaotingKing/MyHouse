#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/8/24
import string
import random

class innerInterface(object):
    def __init__(self, category):
        self.content = {}
        self.category = category
        items_dict = interface_infor[category]
        for item_key in items_dict.iterkeys():
            self.content[item_key] = {}
            item_value_list = items_dict[item_key]
            for vl in item_value_list:
                self.content[item_key][vl] = ""

    def set_assign_content(self, assign_content):
        pass

    def set_random_content(self, minlength=0, maxlength=30):
        item_keys = self.content.keys()
        for item_key in item_keys:
            item_module_content = self.content[item_key]
            for module_key in item_module_content.iterkeys():
                length = random.randint(minlength, maxlength)
                letters = string.ascii_letters + string.digits
                random_content = ''.join([random.choice(letters) for _ in range(length)])
                item_module_content[module_key] = random_content
        return True


"""
@brief This is recognition module to OSK module interface information
"""
interface_infor = {
    "Bridge": {
        "ContainerInfo": ["remark",
                          "final_result1",
                          "container_imgpath1",
                          "detect_face1",
                          "dangerous_goods1",
                          "lead_sealing1",
                          "container_position1",
                          "final_result2",
                          "container_imgpath2",
                          "detect_face2",
                          "dangerous_goods2",
                          "lead_sealing2",
                          "container_position2",
                          "final_operation1",
                          "final_operation2"],
        "LorryInfo": ["lorry_number",
                      "lorry_imgpath"],
        "ExamineInfo": ["examine_img_top",
                        "examine_img_left",
                        "examine_img_right",
                        "examine_img_front",
                        "examine_img_back"],
        "AdditionalInfo": ["token",
                           "crane",
                           "gif_path",
                           "high_low_board",
                           "empty_full_status",
                           "timestamp"]
    },
    "Gate": {
        "GateInfo": ["plate_result",
                     "remark",
                     "final_result1",
                     "detect_face1",
                     "container_impath1",
                     "container_impath2",
                     "final_result2",
                     "detect_face2",
                     "plate_impath"],
        "ExamineInfo": ["dangerous_goods_class",
                        "sealing",
                        "examine_img_top",
                        "examine_img_left",
                        "examine_img_right",
                        "examine_img_front",
                        "examine_img_back"],
        "AdditionalInfo": ["lane",
                           "lane_in_out",
                           "token",
                           "empty_full_status",
                           "high_low_board",
                           "timestamp"]
    }
}
