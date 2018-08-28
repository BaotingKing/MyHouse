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
        url = "http://" + self.host + ":" + self.port + url
        try:
            r = requests.get(url, params=params, headers=self.headers)
            r.encoding = 'UTF-8'
            return r.text
        except Exception:
            print('no json data returned')
            return {}

    # package HTTP POST and support update image
    def post(self, url, data=None, files=None, print_flag=False):
        if type(data) == str:
            data = eval(data)
        url = 'http://' + self.host + ':' + str(self.port) + url
        r = requests.post(url, files=files, data=data)
        if print_flag:
            print(url)
            print(data)
        json_response = r.text
        return json_response
