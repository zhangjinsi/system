#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhangjinsi'

from connection import db_mongodb,db_mysql,db_redis
import config

class BaseModel(object):
    redis_db = db_redis.Connection(host=config.REDIS_HOST, port=config.REDIS_PORT)
    mongo_db = db_mongodb.Connection(host=config.MONGODB_HOST, port=config.MONGODB_PORT, database=config.MONGODB_DB)
    mysql_db = db_mysql.Connection(host=config.MYSQL_HOST, port=config.MYSQL_PORT, user=config.MYSQL_USER, password=config.MYSQL_PASSWORD, database=config.MYSQL_DATABASE)

    def __init__(self):
        self.redis_time = 60*60*24
        self.redis_key_prefix = 'xxx_'

    def product_redis_key(self, prefix, id):
        redis_key = self.redis_key_prefix+str(prefix)+str(id)
        return redis_key



