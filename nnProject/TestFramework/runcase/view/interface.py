#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/8/24
import string
import random


class InnerInterface(object):
    def __init__(self, category):
        self.content = {}
        self.category = category
        items_dict = interface_infor[category]
        for items_key in items_dict.iterkeys():
            self.content[items_key] = {}
            module_dict = items_dict[items_key]
            for module_key in module_dict.iterkeys():
                self.content[items_key][module_key] = ""   # initialize

    def set_assign_content(self, assign_content):
        pass

    def set_random_content(self, minlength=0, maxlength=30):
        refer_interface = interface_infor[self.category]
        item_keys = self.content.keys()
        for item_key in item_keys:
            module_dict = self.content[item_key]
            for module_key in module_dict.iterkeys():
                ref_norm = refer_interface[item_key][module_key]
                if ref_norm[0][0:4] == "flag":
                    flag_type = ref_norm[0].split("_")
                    module_dict[module_key] = random_content(flag_type)
                else:
                    idx = random.randint(0, len(ref_norm)-1)
                    module_dict[module_key] = ref_norm[idx]
        return True


def random_content(type_values):
    type_flag = type_values[1]
    con_value = ""
    if type_flag == "num":
        nums = random.randint(1, 10**int(type_values[2]))
        con_value = str(nums)
    elif type_flag == "img":
        temp = random_str_gen("letters", 16)
        con_value = temp + '.jpg'
    elif type_flag == "result":
        con_value = final_result_gen()
    elif type_flag == "imgpath":
        temp = random_str_gen("letters", 16)
        con_value = temp + '.jpg'

    return con_value


def final_result_gen():
    output = ""
    letters = string.uppercase
    temp = ''.join([random.choice(letters) for _ in range(4)])
    output = output + temp + ' '
    letters = string.digits
    temp = ''.join([random.choice(letters) for _ in range(7)])
    output = output + temp + ' '
    letters = string.ascii_letters + string.digits
    temp = ''.join([random.choice(letters) for _ in range(4)])
    output = output + temp + ' ' + random.choice(["True", "False"])
    return output


def random_str_gen(type_flag="dig-lt", str_len=2):
    output = ""
    if type_flag == "digits":
        letters = string.digits
    elif type_flag == "letters":
        letters = string.letters
    else:
        letters = string.ascii_letters + string.digits

    output = ''.join([random.choice(letters) for _ in range(str_len)])
    return output



"""
@brief This is recognition module to OSK module interface information
"""
interface_infor = {
    "Bridge": {
        "ContainerInfo": {"remark": ["detect"],
                          "final_result1": ["flag_result"],
                          "container_imgpath1": ["flag_imgpath"],
                          "detect_face1": ["front", "back", "none"],
                          "dangerous_goods1": ["true", "false"],
                          "lead_sealing1": ["true", "false"],
                          "container_position1": ["front", "back", "middle"],
                          "final_result2": ["flag_result"],
                          "container_imgpath2": ["flag_imgpath"],
                          "detect_face2": ["front", "back", "none"],
                          "dangerous_goods2": ["true", "false"],
                          "lead_sealing2": ["true", "false"],
                          "container_position2": ["front", "back", "middle"],
                          "final_operation1": ["load", "unload"],
                          "final_operation2": ["load", "unload"]},
        "LorryInfo": {"lorry_number": ["flag_num_2"],
                      "lorry_imgpath": ["flag_img"]},
        "ExamineInfo": {"examine_img_top": ["flag_img"],
                        "examine_img_left": ["flag_img"],
                        "examine_img_right": ["flag_img"],
                        "examine_img_front": ["flag_img"],
                        "examine_img_back": ["flag_img"]},
        "AdditionalInfo": {"token": ["flag_num_2"],
                           "crane": ["flag_num_2"],
                           "gif_path": ["flag_path"],
                           "high_low_board": ["true", "false"],
                           "empty_full_status": ["full", "empty"],
                           "timestamp": ["flag_num_12"]}
    },
    "Gate": {
        "GateInfo": {"plate_result": ["flag_plate"],
                     "remark": ["detect"],
                     "final_result1": ["flag_result"],
                     "detect_face1": ["front", "back", "none"],
                     "container_impath1": ["flag_imgpath"],
                     "container_impath2": ["flag_imgpath"],
                     "final_result2": ["flag_result"],
                     "detect_face2": ["front", "back", "none"],
                     "plate_impath": ["flag_imgpath"]},
        "ExamineInfo": {"dangerous_goods_class": ["true", "false"],
                        "sealing": [""],
                        "examine_img_top": ["flag_img"],
                        "examine_img_left": ["flag_img"],
                        "examine_img_right": ["flag_img"],
                        "examine_img_front": ["flag_img"],
                        "examine_img_back": ["flag_img"]},
        "AdditionalInfo": {"lane": ["flag_num_2"],
                           "lane_in_out": ["in"],
                           "token": ["flag_num_2"],
                           "empty_full_status": ["full", "empty"],
                           "high_low_board": ["true", "false"],
                           "timestamp": ["flag_num_12"]}
    }
}

interface_db = {
    'DetectResultCam1': {
        'number': 'FinalResult1',
        'style': 'FinalResult1',
        'result_check': 'FinalResult1Check',
        'detect_face': 'DetectFace1',
        'side_fullimg_path': 'SideImpath1',

    },
    'DetectResultCam2': {
        'number': 'FinalResult2',
        'style': 'FinalResult2',
        'result_check': 'FinalResult2Check',
        'detect_face': 'DetectFace2',
        'side_fullimg_path': 'SideImpath2',
    },
    'LorryInfo': {
        'car_plate': 'PlateResult',
        'fullimg_path': 'PlateImpath',
    },
    'AdditionalInfo': {
        'dangerous_goods': 'DangerousGoods1',
        'high_low_board': 'HighLowBoard',
        'empty_full_status': 'EmptyFullStatus',
        'lane': 'Lane',
    },

}

if __name__ == '__main__':
    content_http = InnerInterface("Gate")
    content_http.set_random_content()
    print(content_http.content)
    print("==================")
