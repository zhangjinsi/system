#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhangjinsi'

from pymongo import ASCENDING, DESCENDING
from dbmodel.dbbase import BaseModel
from datetime import datetime,timedelta
import time

class ClearMongoDBCache(BaseModel):
    def __init__(self):
        self.maxcount = 995

    def insert_test(self):
        for i in range(10):
            date = (datetime.now()+timedelta(days=i)).strftime('%Y-%m-%d')
            for j in range(100):
                params = {
                    'sql' : 'select * from fdate={} and i={}'.format(date, str(j)),
                    'flushdate' : date,
                    'flushcount' : j,
                    'data' : {'a':i}
                }
                self.mongo_db.buniss.insert_one(params)

    #时间，访问频率, 定时清除数据
    def run_script(self):
        count = self.mongo_db.buniss.count()
        overcount = count-self.maxcount
        print overcount
        if overcount>0:
            #排序筛选出来
            res_data = self.mongo_db.buniss.find().sort([('flushdate', ASCENDING), ('flushcount',ASCENDING)]).limit(overcount)
            res_sql_list = [item.get('sql', '') for item in res_data]
            print res_sql_list
            self.mongo_db.buniss.remove({"sql":{"$in":res_sql_list}})

def run():
    db = ClearMongoDBCache()
    while True:
        time.sleep(60*60*60)
        db.run_script()


if __name__ == '__main__':
    run()
    #db.insert_test()

#crontab linux 定时任务