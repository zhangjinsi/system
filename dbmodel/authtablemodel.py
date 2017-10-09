#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhangjinsi'

from dbbase import BaseModel
from logger import logger

class AuthTableModel(BaseModel):
    def get_dims_levelinfo(self, dimsname=None):
        if not dimsname:
            logger.warning('输入dimsname为空')
            return {}

        #redis_key = self.redis_key_prefix+'authtable_'+str(dimsname)
        redis_key = self.product_redis_key('authtable_', dimsname)

        data = self.redis_db.hgetall(redis_key)
        if not data:
            print '从mysql中获取数据'
            sql = "select fdimsname, flevel_id from authtable where fdimsname='{fdimsname}'".format(fdimsname=dimsname)
            data = self.mysql_db.query_one_dict(sql)
            if data:
                self.redis_db.hmset(redis_key, data)
                self.redis_db.expire(redis_key, self.redis_time)

        return data

if __name__ == '__main__':
    db = AuthTableModel()
    print db.get_dims_levelinfo(dimsname='activeacount')