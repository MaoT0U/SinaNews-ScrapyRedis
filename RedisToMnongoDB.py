# -*- coding:utf-8 -*-
import redis
import pymongo
import json

def process_item():
    '''创建redis数据库连接'''
    redis_cli = redis.Redis(host = "127.0.0.1", port = 6379, db = 0, password = "111111")

    '''创建MongoDB数据库连接'''
    mongo_cli = pymongo.MongoClient(host = "127.0.0.1", port = 27017)

    '''创建mongodb数据库名称'''
    dbname = mongo_cli["sinanews"]
    '''创建mongodb数据库sinanews的表名称'''
    sheetname = dbname["sinaguide"]
    offset = 0
    while True :
        '''redis 数据表名 和 数据'''
        source, data = redis_cli.blpop("sinaguide:items")
        print(data)
        offset += 1
        '''将json对象转换为Python对象'''
        data = json.loads(data, encoding = "utf-8")
        '''将数据插入到sheetname表里'''
        sheetname.insert(data)

if __name__ == "__main__":
    process_item()