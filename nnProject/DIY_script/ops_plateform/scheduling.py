# -*- coding: utf-8 -*-

import os
import json
import paramiko
import threading
import time
import copy
from ops_main import ops_main


def survival_check():
    server_status = {}
    return server_status


def dispatch_requests(ip, req_inform, username='westwell', port_num=22):
    script_path = '/cv/monitor/ops_main.py'
    p_key = '/home/zach/.ssh/id_rsa'
    try:
        servers_status = {}
        private_key = paramiko.RSAKey.from_private_key_file(p_key)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(hostname=ip,
                    port=port_num,
                    username=username,
                    pkey=private_key,
                    timeout=5)
        req_inform_str = str(req_inform).replace(' ', '')
        req_inform_json = json.dumps(req_inform_str)
        cmd = "python3 {0} {1}".format(script_path, req_inform_json)
        print('[info]: cmd is ', cmd)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        # print('[info]: stdin, stdout, stderr ', stdin, stdout, stderr)
        stdout_info = copy.deepcopy(stdout.readlines())    # [Hint]: stdout.readlines() is 'burn after reading'
        stderr_info = copy.deepcopy(stderr.readlines())

        if len(stderr_info) > 0:
            print('[error]: The {0} error inform is: \n'.format(ip))
            for err_info in stderr_info:
                print('-------:{0}'.format(err_info))
        else:
            # final_infor = eval(stdout_info[-1])       # [Hint]: stdout.readlines() is 'burn after reading'
            final_infor = stdout_info[-2]       # [Hint]: stdout.readlines() is 'burn after reading'
            # print('[Debug]: final_infor ---', final_infor, type(final_infor))
            # for item in stdout_info:
            #     print('[Debug]: item ---', item)
            servers_status['final_result'] = final_infor
    except Exception as e:
        print('[error]: SSH {0} maybe have problem: {1}'.format(ip, e))
    finally:
        ssh.close()
        servers_status['timestamp'] = int(time.time())
        print('[info]: {0} collect information - {1}'.format(ip,  {ip: servers_status}))
        return {ip: servers_status}


def threading_proc(req_dicts):
    hosts_ip = req_dicts['ip']
    threads = []
    for ip in hosts_ip:
        th = threading.Thread(target=dispatch_requests, args=(ip, req_dicts['type']))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()


if __name__ == '__main__':
    print('This is debug for threading_proc()')
    requests_dicts = {
        "ip": ["192.168.101.196", "192.168.100.89", "192.168.100.256"],
        "type": ["gpu", "cpu", "mem"]}   # ['ping', 'disk', 'cpu', 'mem'] , "192.168.100.89", "192.168.100.256"

    requests_dicts = {
        "ip": ["192.168.101.196", "192.168.100.89", "192.168.100.256"],
        "type": {
            "cpu": [
                "cpu_load",
                "cpu_usage"],
            "mem": [
                "mem_size",
                "mem_usage"],
            "gpu": [
                "gpu_temp"]
        }
    }
    threading_proc(requests_dicts)
    # print(requests_dicts['type'].keys())
    # hosts_ip = requests_dicts['ip']
    # for ip in hosts_ip:
    #     dispatch_requests(ip, requests_dicts)
    print('threading_proc() is end!')
