# -*- coding: utf-8 -*-
import sys
import status as status


def main_core(category, items=None):
    static_dict = {}
    if category == 'cpu':
        static_infor = status.cpu_info()
    elif category == 'gpu':
        static_infor = status.gpu_info()
    elif category == 'mem':
        static_infor = status.mem_info()
    elif category == 'sysproc':
        static_infor = status.sysproc_info()

    if items is None:
        static_dict = static_infor
    else:
        for i in items:
            if i in static_infor.keys():
                static_dict[i] = static_infor[i]
            else:
                static_dict[i] = None
    return static_dict


def ops_main():
    servers_status = {}
    if len(sys.argv) > 1:
        req_inform_json = sys.argv[1]
        req_inform = eval(req_inform_json)
        servers_status = {}
        print('[Inform]: Request information contents --', req_inform, type(req_inform))
        if type(req_inform) == list:
            for category in req_inform:
                print(category, type(category), type(req_inform))
                servers_status[category] = main_core(category)
        elif type(req_inform) == dict:
            for category, items in req_inform.items():
                print(category, items, type(category), type(items), type(req_inform))
                servers_status[category] = main_core(category, items)
    else:
        print('[Warning]: No argv request was received!')
    print(servers_status)
    # sys.exit('hello, world!')
    return servers_status


if __name__ == '__main__':
    print('[Debug]: This is debug for ops_main.py')
    ops_main()
    print('[info]: ops_main.py has been executed.')

