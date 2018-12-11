#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/11/22

"""
HTML
    +------------------------+
    |<html>                  |
    |  <head>                |
    |                        |
    |   STYLESHEET           |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </head>               |
    |                        |
    |  <body>                |
    |                        |
    |   HEADING              |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   REPORT               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   ENDING               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </body>               |
    |</html>                 |
    +------------------------+

"""


class TemplateHeadInfo(object):
    """html head information"""
    def __init__(self, title='', start_time='', duration='', status=''):
        self.title = title
        self.Start_Time = start_time
        self.Duration = duration
        self.Status = status

    def set_value(self, case_result):
        for key, value in case_result.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def get_value(self):
        pass


class CaseReport(object):
    """Record the results of the case run"""
    def __init__(self, tid='', cls='', style='', desc='', status='', script=''):
        self.tid = tid
        self.Class = cls
        self.style = style
        self.desc = desc
        self.status = status
        self.script = script

    def set_value(self, case_result):
        for key, value in case_result.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def get_value(self):
        pass


class ReportSummary(object):
    """Statistical result"""
    def __init__(self, style='', desc='', count='', Pass='', fail='', error='', cid=''):
        self.style = style
        self.desc = desc
        self.Count = count
        self.Pass = Pass
        self.Fail = fail
        self.Error = error
        self.cid = cid

    def set_value(self, sum_repot):
        for key, value in sum_repot.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def get_value(self):
        pass





