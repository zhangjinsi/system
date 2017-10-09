#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhangjinsi'

from common.response import Response
from dbmodel.userinfomodel import UserInfoModel
from basecontrol import BaseControl


class UserControl(BaseControl):


    def __init__(self, *args, **kwargs):
        super(UserControl, self).__init__(*args, **kwargs)

        self.userinfomodel = UserInfoModel()



    def user_login(self):

        fworkid = self.args.get('fworkid', None)
        fpassword = self.args.get('fpassword', None)

        if not fworkid:
            return Response.responseJson(Response.INPUT_EMPTY, msg='账号为空')

        if not fpassword:
            return Response.responseJson(Response.INPUT_EMPTY, msg='密码为空')


        res = self.userinfomodel.check_userauth(fwork_id=fworkid, fpassword=fpassword)
        if res:
            self.session['fworkid'] = fworkid

            return Response.responseJson(Response.SUCCESS, msg='登录成功')
        else:
            return Response.responseJson(Response.ERROR, msg='账户或者密码错误')


    def user_logout(self):
        self.session.pop('fworkid', None)
        return Response.responseJson(Response.SUCCESS, msg='注销成功')