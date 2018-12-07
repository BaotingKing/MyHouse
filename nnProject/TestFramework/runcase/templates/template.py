#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: wwl-ZK
# Time: 2018/11/22

from django.conf import settings
from django.template import Template, Context

settings.configure()


class Person(object):
    def __init__(self, first_name, last_name):
        self.first_name, self.last_name = first_name, last_name


def index(req):
    t = Template('My name is {{name}}.')
    c = Context({"name": "Stephane"})    # 将name传递到Template中
    print(t)

    t.render(c)





