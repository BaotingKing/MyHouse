#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/8/22

import requests
# config Class
class ConfigHttp:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:29.0) Gecko/20100101 Firefox/29.0'}
    # http head
    def set_header(self, headers):
        self.headers = headers
    # package HTTP GET
    def get(self, url, params):
        url = "http://"+self.host+":"+self.port+url
        try:
            r = requests.get(url, params=params, headers=self.headers)
            r.encoding = 'UTF-8'
            return r.text
        except Exception:
            print('no json data returned')
            return {}
    # package HTTP POST and support update image
    def post(self, url, data=None, files=None):
        data = eval(data)
        url = 'http://' + self.host + ':' + str(self.port)+url
        r =requests.post(url, files=files, data=data)
        print(data)
        json_response = r.text
        return json_response



http_json = [{
        "GateInfo": {
            "plate_result": "SH_AB1234",
            "remark": "detect",
            "final_result1": "ABCD 1234567 22G1 True",
            "detect_face1": "front/back/none",
            "container_impath1": "/cv/DongSen/imagesave/defect_check/a.jpg",
            "container_impath2": "",
            "final_result2": "",
            "detect_face2": "front/back/none",
            "plate_impath": "/cv/DongSen/imagesave/鲁B87914.jpg"
        },

        "ExamineInfo": {
            "dangerous_goods_class": "true/false",
            "sealing": "lead sealing eg: yes/no",
            "examine_img_top": "",
            "examine_img_left": "/cv/DongSen/imagesave/defect_check",
            "examine_img_right": "/cv/DongSen/imagesave/defect_check",
            "examine_img_front": "/cv/DongSen/imagesave/defect_check",
            "examine_img_back": "/cv/DongSen/imagesave/defect_check"
        },

        "AdditionalInfo": {
            "lane": "1",
            "lane_in_out": "in",
            "token": "6",
            "empty_full_status": "empty/full",
            "high_low_board": "true/false",
            "timestamp": "1524558726000"
        }
    }]