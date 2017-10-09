#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhangjinsi'
from logger import logger

class BaseControl(object):
    def __init__(self, args={}, session={}):

        self.args = args
        self.session = session

        logger.info('request args -- {}'.format(self.args))
