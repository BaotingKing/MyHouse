#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: zk
# Time: 2018/8/17
import os
import logging
from logging.handlers import TimedRotatingFileHandler

LOG_PATH = os.getcwd()

LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,
          'warning': logging.WARNING,
          'error': logging.ERROR,
          'critical': logging.CRITICAL}


class Logger(object):
    def __init__(self, logger_name='framework'):
        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)
        self.log_file_name = 'TestFrame.log'
        self.backup_count = 3
        # log output level
        self.console_output_level = 'WARNING'
        self.file_output_level = 'DEBUG'
        # create formatter
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def get_logger(self):
        """func is more complex"""
        if not self.logger.handlers:  # avoid rep
            console_handler = logging.StreamHandler()    # create console handler and set level to debug
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_output_level)
            self.logger.addHandler(console_handler)

            # create new log and backup_count
            file_handler = TimedRotatingFileHandler(filename=os.path.join(LOG_PATH, self.log_file_name),
                                                    when='H',
                                                    interval=1,
                                                    backupCount=self.backup_count,
                                                    delay=True,
                                                    encoding='utf-8')
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_output_level)
            self.logger.addHandler(file_handler)
        return self.logger

    def logger_running(self):
        if not self.logger.handlers:  # avoid rep   ????what
            console_handler = logging.FileHandler(filename=os.path.join(LOG_PATH, self.log_file_name),
                                                  mode='w')
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.file_output_level)
            self.logger.addHandler(console_handler)

        return self.logger


logger_running = Logger().logger_running()
