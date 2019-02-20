#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: Zhang.Baoting
# Time: 2018/7/26

import os, time
from Crypto.Cipher import AES     # this is pycrypto package
from hashlib import md5

def creatLabelTxt(path, data_set_name, sub_labels_flag=0):
    i = 0  # 标签
    with open(path + '\\' + data_set_name, "w") as train_txt:
        for root, dirs_labels, _ in os.walk(path):  # 遍历各种label文件夹
            for label in dirs_labels:  # 遍历某一个label文件夹里面所有的文件和文件夹
                if 0 == sub_labels_flag:
                    for _, _, files in os.walk(path + '\\' + str(label)):
                        for file in files:
                            image_file = str(label) + "_" + str(file)
                            label_name = image_file + ' ' + str(i) + '\n'  # 文件路径+空格+标签编号+换行
                            train_txt.writelines(label_name)
                elif 1 == sub_labels_flag:
                    for _, sub_labels, _ in os.walk(path + '\\' + str(label)):
                        for subclass in sub_labels:
                            for _, _, files in os.walk(path + '\\' + str(label) + '\\' + str(subclass)):
                                for file in files:
                                    image_file = str(label) + "_" + str(file)
                                    label_name = image_file + ' ' + str(i) + '\n'  # 文件路径+空格+标签编号+换行
                                    train_txt.writelines(label_name)
                i += 1  # 类型编号加1
    return 0


def openTrainFile(filepath, categories):
    categorytrainlist = []
    for i in range(1, len(categories)):
        categorytrainlist.append(open(filepath + categories[i] + '_train.txt', 'w'))
        categorytrainlist.append(open(filepath + categories[i] + '_test.txt', 'w'))
    return categorytrainlist


def writeTrainFile(categorytrainlist, labels, categories, imname):
    for i in range(len(categorytrainlist)):
        singlelabel = i / 2 + 1
        if (labels == singlelabel).any():
            categorytrainlist[i].write(imname + ' ' + '1' + '\n')
        else:
            categorytrainlist[i].write(imname + ' ' + '-1' + '\n')


def closeTrainFile(categorytrainlist):
    for singlefile in categorytrainlist:
        singlefile.close()


def CheckFolderExists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def writeLog(path, logname, message):
    """
        &: write log to specified folder
    """
    CheckFolderExists(path)
    logfile = open(path + logname, 'a')
    logfile.write(str(time.localtime()) + '\n' + message + '\n')
    logfile.close()


# ====================================================
# =============== Encryption && Decryption ===========
"""
(1) AES(Advanced Encryption Standard),实现AES有若干模式,
(2) 其中的CBC模式因为其安全性而被TLS（就是https的加密标准）和IPSec（win采用的）作为技术标准.
(3) CBC:利用密码和salt(起到扰乱作用)按照md5算法产生key和iv(initial vector)，用来加解密;
注意：(a)加密文本text必须为16的倍数，不足补齐！
  (b)AES的密钥key 长度必须为16（AES-128）、24（AES-192）、或32（AES-256）Bytes 长度！
"""
def device_key_and_iv(password, salt, key_length, iv_length):
    """return key and iv for AES"""
    key = iv = ''
    while len(key) < key_length + iv_length:
        iv = md5(iv + password + salt).digest()    # be careful ->2018
        key += iv
    return key[0:key_length], key[key_length:key_length + iv_length]


def Decrypt(in_file, out_file, password, key_length=32):
    bs = AES.block_size
    salt = in_file.read(bs)[len('Salted__'):]  # AES算法特点，salt位于加密文件开头
