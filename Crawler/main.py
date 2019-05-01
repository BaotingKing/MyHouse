# -*- coding: utf-8 -*-
# __author__ = 'Baoting Zhang'

import urllib.request

def getlist():
    html = urllib.request("https://www.bilibili.com/video/av19382711?spm_id_from=333.338.__bofqi.19")
    print(html)

getlist()