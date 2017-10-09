#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhangjinsi'

class ErrorCode(object):
    SUCCESS = 0
    ERROR = -1
    INPUT_EMPTY = -2
    NO_LOGIN = -3
    NO_AUTH = -4

class Response(ErrorCode):

    @classmethod
    def responseJson(cls,code=None,data=None,msg=None):
        '''
        响应json
        :param code:
        :param data:
        :param msg:
        :return:
        '''

        error_msg = {
            cls.ERROR : '请求失败',
            cls.SUCCESS : '请求成功',
            cls.INPUT_EMPTY : '输入为空',
            cls.NO_LOGIN : '没有登录',
            cls.NO_AUTH : '没有权限'
        }
        if msg is None:
            msg = error_msg.get(code,'未定义信息')
        if data is None:
            data = []

        res = {
            'code' : code,
            'msg' : msg,
            'data' : data
        }
        return res

    @classmethod
    def responsehtml(cls,code=None,data=None,msg=None):
        pass