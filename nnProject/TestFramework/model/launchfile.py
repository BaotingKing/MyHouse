#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Zhang.Baoting
# Time: 2018/8/10
import json
import tools
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
        print('%s module is checking.....' % target_mdl)
        if target_mdl in name_list:
            idxes = [i for i in range(len(name_list)) if name_list[i] == target_mdl]
            for idx in idxes:
                pass

        target_mdl = "video_processing"
        print('%s module is checking.....' % target_mdl)
        if target_mdl in name_list:
            idxes = [i for i in range(len(name_list)) if name_list[i] == target_mdl]
            for idx in idxes:
                pass

        target_mdl = "image_processing"
        print('%s module is checking.....' % target_mdl)
        if target_mdl in name_list:
            idxes = [i for i in range(len(name_list)) if name_list[i] == target_mdl]
            for idx in idxes:
                pass

        target_mdl = "object_roi"
        print('%s module is checking.....' % target_mdl)
        if target_mdl in name_list:
            idxes = [i for i in range(len(name_list)) if name_list[i] == target_mdl]
            for idx in idxes:
                pass

        target_mdl = "roi_recog"
        print('%s module is checking.....' % target_mdl)
        if target_mdl in name_list:
            idxes = [i for i in range(len(name_list)) if name_list[i] == target_mdl]
            idxes_cmp = [i for i in range(len(name_list)) if name_list[i] == "object_roi"]
            for idx in idxes:
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


        target_mdl = "roi_trigger"
        print('%s module is checking.....' % target_mdl)
        if target_mdl in name_list:
            idxes = [i for i in range(len(name_list)) if name_list[i] == target_mdl]
            idxes_cmp = [i for i in range(len(name_list)) if name_list[i] == "roi_recog"]
            for idx in idxes:
                pass



        target_mdl = "result_transfer"
        print('%s module is checking.....' % target_mdl)
        if target_mdl in name_list:
            idxes = [i for i in range(len(name_list)) if name_list[i] == target_mdl]
            idxes_cmp = [i for i in range(len(name_list)) if name_list[i] == "roi_recog"]
            for idx in idxes:
                target_module = self.cfgcontent[module_list[idx]]
                flag = 0
                for idx_cmp in idxes_cmp:
                    cmp_module = self.cfgcontent[module_list[idx_cmp]]
                    output_topic = set(cmp_module['run_param']['output_topic'])
                    x_topic = tools.type2topic(cmp_module['run_param']['detect_type'])
                    types_topic = target_module['run_param'][x_topic]
                    if output_topic.issubset(types_topic):
                        flag = 1  # this is ok
                    elif types_topic in output_topic:  # Cfg files are not standard, and fault tolerance is added here
                        flag = 1  # this is ok
                    else:
                        print('     Error item configuration: %s' % x_topic)

        target_mdl = "result_send"
        print('%s module is checking.....' % target_mdl)
        if target_mdl in name_list:
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
        print('%s module is checking.....' % target_mdl)
        if target_mdl in name_list:
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
