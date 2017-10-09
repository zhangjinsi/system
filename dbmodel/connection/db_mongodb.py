#!/usr/bin/env python
# coding=utf-8
__author__ = 'zhangjinsi'
from pymongo import MongoClient

def Connection(host='127.0.0.1',port=27017, database=None):
    conn = MongoClient(host=host,port=port)
    mongo = eval('conn.'+database)
    return mongo

if __name__ == '__main__':
    db = Connection('192.168.1.69',database='xxx')

    print db.test.insert_one({'a' : 1})
    print db.test.find_one()
