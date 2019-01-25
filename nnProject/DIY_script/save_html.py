#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2019/1/25
import urllib


def refresh_save_html(url = None):
    with open('result_html.html', 'wb') as html_handle:
        try:
            http = urllib.request.urlopen(url).read()
            html_handle.write(http)
        except Exception:
            print('download error!!!')


if __name__ == "__main__":
  url = 'http://www.baidu.com'
  refresh_save_html(url)
  print('******ok')