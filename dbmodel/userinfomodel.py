#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhangjinsi'

from dbbase import BaseModel
from logger import logger
import json

class UserInfoModel(BaseModel):
    def check_userauth(self, fwork_id=None, fpassword=None):

        if not fwork_id or not fpassword:
            logger.warning('账户或者密码为空')
            return False

        sql = 'select fcname, fwork_id, fdept_id, flevel_id from userinfo where fwork_id={fwork_id} and fpassword={fpassword}'.format(fwork_id=fwork_id, fpassword=fpassword)
        data = self.mysql_db.query_one_dict(sql)

        return True if data else False



    def get_userinfo(self, fworkid):
        '''
        获取用户信息
        :param fworkid:
        :return:
        '''
        if not fworkid:
            logger.warning('工号为空')
            return {}

        #redis字符串类型
        #hash
        #redis_key = self.redis_key_prefix+'userinfo_'+str(fworkid)+':'
        redis_key = self.product_redis_key('userinfo_', fworkid)
        #先查redis

        data = self.redis_db.hgetall(redis_key)  #返回字典

        if not data:
            #print '从mysql中获取数据'
            sql = 'select fcname, fwork_id, fdept_id, flevel_id from userinfo where fwork_id={fworkid}'.format(fworkid=fworkid)
            data = self.mysql_db.query_one_dict(sql)
            if data:
                self.redis_db.hmset(redis_key, data)
                self.redis_db.expire(redis_key, self.redis_time)

        return data

if __name__ == '__main__':
    db = UserInfoModel()
    print db.get_userinfo(fworkid=1000)