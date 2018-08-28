#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/8/22

import httplib
import urllib
import json
from controller import config
from model.launchfile import Launchfile
from model import interface
# try:
#
#     httpClient = httplib.HTTPConnection('127.0.0.1',5000,30)
#     httpClient.request('GET', '/data/get/')
#     response = httpClient.getresponse()
#     print "1"
#     print response.status
#     print response.reason
#     print response.read()
# except Exception, e:
#     print "2"
#     print e
# finally:
#     if httpClient:
#         httpClient.close()
#
#
#
# httpClient =None
# try:
#     params =urllib.urlencode({'name':'zhouyang','age':21})
#     headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
#     httpClient=httplib.HTTPConnection('127.0.0.1',5000,30)
#     httpClient.request("POST",'/test/',params,headers)
#     response =httpClient.getresponse()
#     print "11"
#     print response.status
#     print response.reason
#     print response.read()
#     print response.getheaders()
# except Exception ,e:
#     print e
# finally:
#     if httpClient:
#         httpClient.close()

path = "F:\\myhouse\\MyHouse\\nnProject\\TestFramework\\tianjin.conf"
cfg = Launchfile()
cfg_send = cfg.load_launchfile(file_path=path)
send_cfg = cfg.cfgcontent

name_list = []
module_list = []
for key, value in send_cfg.items():
    name_list.append(value["module_name"])
    module_list.append(key)
print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
print "++++++++++++++++++++++++++++++++++"
# print name_list
# print module_list
model_idx = name_list.index("result_send")
model_content = send_cfg.get(module_list[model_idx])
# print model_content

web_server_ip = model_content["run_param"]["web_server_ip"]
port_id = model_content["run_param"]["web_server_port"]
url_content = model_content["run_param"]["data_send_url"]
print web_server_ip,port_id
print url_content
httpconnet = config.ConfigHttp(host=web_server_ip,port=port_id)


# test = httpconnet.get(url=url_content, params='')
# post_way = httpconnet.post(url=url_content)
content_http = interface.innerInterface("Gate")
post_way = httpconnet.post(url=url_content, data=content_http.content)
print post_way
print "#############********************"
# a = config.http_json
# print type(a)
# print type(content_http.content)



