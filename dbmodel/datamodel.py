#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhangjinsi'

from dbbase import BaseModel
from sql_tpl import SQL_TPL
from logger import logger
from datetime import datetime

class DataModel(BaseModel):

    def get_data(self, dims=None, args={}):
        sql = SQL_TPL.get(dims,None)
        if not sql:
            logger.warning('没有找到sql')
            return []
        #先从缓存中获取数据

        #再从mysql中获取数据
        sql = sql % args
        #mongo  100000
        #数据库， 集合， 文档
        #时间，访问频率, 定时清除数据
        #bjson
        params = {
            'sql' : sql
        }
        datenow = datetime.now().date().strftime('%Y-%m-%d')
        res = self.mongo_db.buniss.find_one(params)
        if not res:
            logger.info('从mysql中查找数据')
            data = self.mysql_db.query_list(sql=sql)#数据量很大的时候就会变得很慢
            for item in data:
                fcount = int(item.get('activeacount', 0))
                item['activeacount'] = fcount
            params = {
                'sql' : sql,
                'data' : data,
                'flushdate' : datenow,
                'flushcount' : 1
            }
            print 'params',params
            self.mongo_db.buniss.insert_one(params)
        else:
            logger.info('从mongodb中查找数据')
            self.mongo_db.buniss.update(params, {"$set" : {"flushdate": datenow}, "$inc":{"flushcount":1}}, False, True)
            data = res.get('data',[])

        return data

if __name__ == '__main__':
    db = DataModel()

    params = {
            'sdate' : '2017-09-16',
            'edate' : '2017-09-26'
        }
    print db.get_data(dims='chart1',args=params)
