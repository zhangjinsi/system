#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhangjinsi'

from common.auth import auth
from flask import Blueprint,jsonify,session,g
from common.response import Response
from control.datacontrol import DataControl

data = Blueprint('data',__name__,url_prefix='/data')

@data.route('/get_data',methods=['GET'])
@auth.login_require
def get_data():
    control = DataControl(args=g.args, session=session)
    return jsonify(control.user_get_data())
