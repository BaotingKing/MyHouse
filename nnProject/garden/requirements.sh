#!/bin/bash
###################################################################
#
#pip freeze > requirements.txt
#pip install -r requirements.txt
#
###################################################################
cfg_name='pip.conf'

src="[global]\ntrusted-host = mirrors.aliyun.com\nindex-url = http://mirrors.aliyun.com/pypi/simple
"

mirr="mirrors.aliyun.com"

# 这里的-f参数判断$cfg_name是否存在
dir_path=`pwd`
mkdir -p ~/.pip/ && cd ~/.pip/

if [ ! -f "$cfg_name" ]; then
echo "$cfg_name is not exist and it will be created"
touch $cfg_name
fi

grep ${mirr} ${cfg_name} > /dev/null
if [ $? -eq 0 ]; then 
    echo "software source is ok!"
else
    echo ${src} >> ${cfg_name}
fi


cd $dir_path


sudo apt install python3-pip

sudo pip3 install --upgrade setuptools
sudo pip3 install -r requirements.txt
