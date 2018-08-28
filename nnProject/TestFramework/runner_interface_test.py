#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/8/27
from model.launchfile import Launchfile
from model import interface
from model import db
from controller import config


if __name__ == '__main__':
    iterations = 10000
    path = "F:\\myhouse\\MyHouse\\nnProject\\TestFramework\\tianjin.conf"
    cfg = Launchfile()
    cfg_send = cfg.load_launchfile(file_path=path)
    send_cfg = cfg.cfgcontent
    name_list = []
    module_list = []
    for key, value in send_cfg.items():
        name_list.append(value["module_name"])
        module_list.append(key)

    model_idx = name_list.index("result_send")
    model_content = send_cfg.get(module_list[model_idx])

    web_server_ip = model_content["run_param"]["web_server_ip"]
    port_id = model_content["run_param"]["web_server_port"]
    url_content = model_content["run_param"]["data_send_url"]

    httpconnet = config.ConfigHttp(host=web_server_ip, port=port_id)

    content_http = interface.innerInterface("Gate")
    post_feedback = httpconnet.post(url=url_content, data=content_http.content)

    if post_feedback == "Success":
        pass
    else:
        print(post_feedback)

    print "haha"
