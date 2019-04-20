import json
"""
Used to generate interface files
"""
dic_data = {
    "ip": ["192.168.111.111", "192.168.111.112"],
    "type": {
        "disk": ["disk_cv_space",
                 "disk_cv_usage",
                 "disk_root_space",
                 "disk_root_usage",
                 "disk_io_read",
                 "disk_io_write",
                 "disk_io_read_ms",
                 "disk_io_write_ms",
                 "disk_io_read_ops",
                 "disk_io_write_ops"],

        "cpu": ["cpu_core_num",
                "cpu_load",
                "cpu_usage"],

        "gpu": ["gpu_temp",
                "gpu_mem",
                "gpu_usage",
                "gpu_cuda_usage"],

        "mem": ["mem_size",
                "mem_usage"],

        "carme": ["192.168.111.222",
                  "192.168.111.223",
                  "192.168.111.224"],

        "sysproc": ["mysql",
                    "redis",
                    "nginx",
                    "php",
                    "vsftp"],

        "wellocean": "default"
    }
}

if __name__ == '__main__':
    with open('ops_interface.json', 'w') as f:
        json.dump(obj=dic_data, fp=f, indent=4)

    with open('ops_interface.json', 'r') as f:
        ops_interface = json.load(f)

    print(type(ops_interface))
    print(ops_interface)
