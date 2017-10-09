#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhangjinsi'


from flask import Flask, g, request,session
from viewhandler.page_blueprint import page
from viewhandler.user_blueprint import user
from viewhandler.data_blueprint import data
from logger import logger

app = Flask(__name__)
app.config.from_pyfile('config.py')

BLURPRINT = [page, user, data]

@app.context_processor
def common():
    return {
        'isLogin' : True if session.get('fworkid',None) else False
    }

#中间件
def bootstrap_app(app):
    for view in BLURPRINT:
        app.register_blueprint(view)

    @app.before_request
    def before():
        args = {k : v[0] for k, v in dict(request.args).items()} #get
        args_form = {k : v[0] for k, v in dict(request.form).items()} #post
        args.update(args_form)

        g.args = args

bootstrap_app(app)

if __name__ == '__main__':
    app.run(host=app.config['WEB_HOST'],port=app.config['WEB_PORT'])