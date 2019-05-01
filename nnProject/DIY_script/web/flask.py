#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author: ZK
# Time: 2019/01/01
import sys
from flask import request, jsonify, Flask
from flask_apscheduler import APScheduler


class config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': '__main__: get_one',
            'trigger': 'interval',
            'seconds': 10,
        }
    ]


def get_one():
    pass


app = Flask(__name__)
app.config.from_object(config())


@app.route('/admin/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return 'Hello word!'
    elif request.method == 'GET':
        return 'Hello my homeland!'


if __name__ == '__main__':
    stdout_backup = sys.stdout  # make a copy of original stdout route
    print('This is a flask mini web, and it is only a case')



