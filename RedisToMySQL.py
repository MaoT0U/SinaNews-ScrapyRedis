# -*- coding:utf-8 -*-

'''
    从主机redis中拿取数据并且放入MySQL数据库
'''

import json
import redis
import pymysql

def process_item() :
    '''创建redis数据库链接'''
    '''
        decode_responses=True
        写入的键值对中的value为str类型，不加这个参数写入的则为字节类型
    '''
    redis_cli = redis.Redis(host = "127.0.0.1", port = 6379, db = 0, password = "111111")

    '''创建mysql数据库链接'''
    mysql_cli = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        passwd="123456",
        db="sinanews",
        charset="utf8"
    )
    offset = 0
    while True :
        '''从redis中获取数据'''
        source, data = redis_cli.blpop("sinaguide:items")
        item = json.loads(str(data, encoding = "utf-8"))
        try :
            ''' 获取数据库游标 通过游标对数据库进行操作 返回结果默认是元组 可以修改为字典的形式 '''
            cursor = mysql_cli.cursor(
                cursor=pymysql.cursors.DictCursor
            )
            insertSQL = "INSERT INTO sinanews(grade_one_title, grade_one_link, grade_two_title, grade_two_link, grade_two_file_path, " \
                        "grade_two_file_link, news_title, news_author, news_content, news_datetime) VALUES(" \
                        "'" + item['grade_one_title'] + "', '" + item['grade_one_link'] + "', '" + item[
                            'grade_two_title'] + "', '" + item['grade_two_link'] + \
                        "', '" + item['grade_two_file_path'] + "', '" + item['grade_two_file_link'] + "', '" + item[
                            'news_title'] + "', '" + item['news_author'] + \
                        "', '" + item['news_content'] + "', '" + item['news_datetime'] + "')"
            number = cursor.execute(insertSQL)
            mysql_cli.commit()
            cursor.close()
            offset += 1
        except Exception as e:
            print(e.args)

if __name__ == "__main__" :
    process_item()