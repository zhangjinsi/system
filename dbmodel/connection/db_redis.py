#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhangjinsi'

import redis

def Connection(host='127.0.0.1',port=6379):
    pool = redis.ConnectionPool(host=host,port=port)

    redis_tmp = redis.Redis(connection_pool=pool)
    return redis_tmp




if __name__ == '__main__':
    redis_db = Connection(host='192.168.1.69')
    print redis_db.get('test')
