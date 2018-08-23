#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Zhang.Baoting
# Time: 2018/8/10
import os
import json
import tools
from report.Logger import logger_running
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
        for key, value in self.cfgcontent.items():
            name_list.append(value["module_name"])
            module_list.append(key)

        target_mdl = "read_config"
        if target_mdl in name_list:
            print('%s module is checking.....' % target_mdl)
            logger_running.info(target_mdl + ' module is checking.....')
            idx = name_list.index(target_mdl)
            target_module = self.cfgcontent[module_list[idx]]
            file_name = target_module["run_param"]["file_name"]
            if not os.path.isfile(file_name):
                print('     Error item configuration: %s' % file_name)
                logger_running.warn('     Error item configuration: ' + file_name)


        target_mdl = "video_processing"
        if target_mdl in name_list:
            print('%s module is checking.....' % target_mdl)
            logger_running.info(target_mdl + ' module is checking.....')
            idxes = [i for i in range(len(name_list)) if name_list[i] == target_mdl]
            for idx in idxes:
                pass


        target_mdl = "image_processing"
        if target_mdl in name_list:
            print('%s module is checking.....' % target_mdl)
            logger_running.info(target_mdl + ' module is checking.....')
            idxes = [i for i in range(len(name_list)) if name_list[i] == target_mdl]
            for idx in idxes:
                pass


        target_mdl = "osk2_master_shell"
        if target_mdl in name_list:
            logger_running.info(target_mdl + ' module is checking.....')
            print('%s module is checking.....' % target_mdl)
            idxes = [i for i in range(len(name_list)) if name_list[i] == target_mdl]
            idxes_cmp = [i for i in range(len(name_list)) if name_list[i] == "roi_recog"]
            for idx in idxes:
                pass


        target_mdl = "object_roi"
        if target_mdl in name_list:
            logger_running.info(target_mdl + ' module is checking.....')
            print('%s module is checking.....' % target_mdl)
            idxes = [i for i in range(len(name_list)) if name_list[i] == target_mdl]
            for idx in idxes:
                target_module = self.cfgcontent[module_list[idx]]
                topic_set = []
                x_topic = "/WellOcean/" + target_module["run_param"]["target"] + "_subimage/channel_"
                for idx_para in range(target_module["run_param"]["cam_name"].__len__()):
                    channel_para = target_module["run_param"]["channel_num"][idx_para]
                    cam_para = target_module["run_param"]["cam_name"][idx_para]
                    for ty_name in ["letter", "digit", "type", "plate"]:
                        temp_topic = x_topic + channel_para + '_' + cam_para + '_' + ty_name
                        topic_set.append(temp_topic)

                topic_target = tools.unfold_list(target_module["run_param"]["output_topic"])
                # topic_set = set(topic_set)
                for topic_check in topic_target:
                    if topic_check not in topic_set:
                        print('     Error item configuration: %s' % "output_topic")


        target_mdl = "roi_recog"
        if target_mdl in name_list:
            logger_running.info(target_mdl + ' module is checking.....')
            print('%s module is checking.....' % target_mdl)
            idxes = [i for i in range(len(name_list)) if name_list[i] == target_mdl]
            idxes_cmp = [i for i in range(len(name_list)) if name_list[i] == "object_roi"]
            for idx in idxes:     # checkout "output_topic"
                trans_set = set(self.cfgcontent[module_list[idx]]["run_param"]["input_topic"])
                flag = 0
                for idx_cmp in idxes_cmp:
                    tmp_cmp = self.cfgcontent[module_list[idx_cmp]]["run_param"]["output_topic"]
                    topic_cmp = tools.unfold_list(tmp_cmp)
                    if trans_set.issubset(topic_cmp):
                        flag = 1   # this is ok
                        break

                if flag == 0:
                    print("This should be an error record and warning")
                else:
                    # print("This roi_recog's topic is ok")
                    flag = 0

            for idx in idxes:  # checkout "other run_param params"
                target_module = self.cfgcontent[module_list[idx]]
                detect_type = target_module["run_param"]["detect_type"]
                if detect_type == "char":    # I am he_he
                    detect_type = "plate"
                topic_list = []
                input_list = []
                output_list = []
                input_list = target_module["run_param"]["input_topic"]
                output_list = target_module["run_param"]["output_topic"]
                topic_list.append(input_list)
                topic_list.append(output_list)
                topic_list = tools.unfold_list(topic_list)
                for idx_para in output_list:    # checkout output_list's naming rule reference input
                    new_para = idx_para.replace("result", "subimage")
                    if new_para not in input_list:
                        print('     Error item configuration: %s' % "output_topic")

                for idx_para in topic_list:
                    tail_word = idx_para.split('_')[-1]
                    if tail_word != detect_type:
                        print('     Error item configuration: detect_type %s' % tail_word)





        target_mdl = "roi_trigger"
        if target_mdl in name_list:
            logger_running.info(target_mdl + ' module is checking.....')
            print('%s module is checking.....' % target_mdl)
            idxes = [i for i in range(len(name_list)) if name_list[i] == target_mdl]
            idxes_cmp = [i for i in range(len(name_list)) if name_list[i] == "roi_recog"]
            for idx in idxes:
                pass


        target_mdl = "result_transfer"
        if target_mdl in name_list:
            logger_running.info(target_mdl + ' module is checking.....')
            print('%s module is checking.....' % target_mdl)
            idxes = [i for i in range(len(name_list)) if name_list[i] == target_mdl]
            idxes_cmp = [i for i in range(len(name_list)) if name_list[i] == "roi_recog"]
            for idx in idxes:
                target_module = self.cfgcontent[module_list[idx]]
                for idx_cmp in idxes_cmp:
                    target_infor = []
                    cmp_infor = []
                    cmp_module = self.cfgcontent[module_list[idx_cmp]]
                    output_topic = cmp_module['run_param']['output_topic']

                    if type(output_topic) == str:  # this is he_he, avoid the unknown problem
                        cmp_infor.append(output_topic)
                    else:
                        for i in output_topic:
                            cmp_infor.append(i)

                    x_topic = tools.type2topic(cmp_module['run_param']['detect_type'])
                    types_topic = target_module['run_param'][x_topic]
                    if type(types_topic) == list:   # this is he_he, avoid the unknown problem
                        for i in types_topic:
                            target_infor.append(i)
                    else:     # cfg has illegality write
                        target_infor.append(str(types_topic))


                    if target_infor != cmp_infor:
                        print()
                        print('     Error item configuration: %s' % x_topic)


        target_mdl = "result_send"
        if target_mdl in name_list:
            logger_running.info(target_mdl + ' module is checking.....')
            print('%s module is checking.....' % target_mdl)
            idx = name_list.index("result_send")
            idx_cmp = name_list.index("roi_trigger")
            target_module = self.cfgcontent[module_list[idx]]
            cmp_module = self.cfgcontent[module_list[idx_cmp]]
            # for idx_topic in ["trigger_topic", "container_trigger_topic", "plate_trigger_topic", "plate_roi_topic"]:
            for idx_topic in ["trigger_topic", "container_trigger_topic", "plate_trigger_topic"]:
                cmp_topic = tools.check_item_ref_resultsend(idx_topic)
                target_infor = target_module["run_param"][idx_topic]
                cmp_infor = cmp_module["run_param"][cmp_topic]
                tools.check_adaptive(target_infor, cmp_infor, idx_topic)

            for idx_topic in ["result_topic"]:
                idx_cmp = name_list.index("result_transfer")
                cmp_module = self.cfgcontent[module_list[idx_cmp]]
                cmp_topic = tools.check_item_ref_resultsend(idx_topic)
                target_infor = target_module["run_param"][idx_topic]
                cmp_infor = cmp_module["run_param"][cmp_topic]
                tools.check_adaptive(target_infor, cmp_infor, idx_topic)





        target_mdl = "ui"
        if target_mdl in name_list:
            logger_running.info(target_mdl + ' module is checking.....')
            print('%s module is checking.....' % target_mdl)
            idx = name_list.index(target_mdl)
            target_module = self.cfgcontent[module_list[idx]]
            idxes_cmp = [i for i in range(len(name_list)) if name_list[i] == "object_roi"]
            flag = 0
            cmp_container = []
            for idx_cmp in idxes_cmp:
                cmp = self.cfgcontent[module_list[idx_cmp]]["run_param"]["output_topic"]
                cmp_container.append(cmp)
            cmp_infor = tools.unfold_list(cmp_container)
            target_infor = tools.unfold_list(target_module["run_param"]["roi_topic"])

            for idx_infor in target_infor:
                if idx_infor not in cmp_infor:
                    flag = 1
                    print(idx_infor)
                    print('     Error item configuration: %s' % "roi_topic")

            for idx_topic in ["trigger_topic"]:
                idx_cmp = name_list.index("roi_trigger")
                cmp_module = self.cfgcontent[module_list[idx_cmp]]
                cmp_topic = tools.check_item_ref_resultsend(idx_topic)
                target_infor = target_module["run_param"][idx_topic]
                cmp_infor = cmp_module["run_param"][cmp_topic]
                tools.check_adaptive(target_infor, cmp_infor, idx_topic)

            for idx_topic in ["result_topic"]:
                idx_cmp = name_list.index("result_transfer")
                cmp_module = self.cfgcontent[module_list[idx_cmp]]
                cmp_topic = tools.check_item_ref_resultsend(idx_topic)
                target_infor = target_module["run_param"][idx_topic]
                cmp_infor = cmp_module["run_param"][cmp_topic]
                tools.check_adaptive(target_infor, cmp_infor, idx_topic)


        target_mdl = "object_catorgery"
        if target_mdl in name_list:
            logger_running.info(target_mdl + ' module is checking.....')
            print('%s module is checking.....' % target_mdl)
            idxes = [i for i in range(len(name_list)) if name_list[i] == target_mdl]
            idxes_cmp = [i for i in range(len(name_list)) if name_list[i] == "roi_recog"]
            for idx in idxes:
                pass