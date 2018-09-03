# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

'''将数据存入文件中'''
class SinaNewsPipelineByFiles(object) :
    def process_item(self, item, spider) :
        item["grade_two_file_path"] = item["grade_two_file_path"] + (item["news_title"] + ".txt").strip()\
            .replace("\n", "").replace("/", "_").replace("\\", "_").replace(":", "-").replace("*", "_")\
            .replace("?", "").replace('"', "'").replace("<", "'''").replace(">", "'''").replace("|", "--")
        '''三无新闻不写入文件以及数据库 无作者 无内容 无日期'''
        if item["news_content"] == "本新闻暂无内容信息" :
            return item
        if item["news_author"] == "本新闻暂无作者信息" and item["news_content"] == "本新闻暂无内容信息" and item["news_datetime"] == "本新闻暂无日期信息" :
            return item
        with open(item["grade_two_file_path"], "w", encoding = "utf-8") as news_file :
            news_file.write(item["news_content"])
        return item

import pymysql
class MySQLPipeline(object):
    def __init__(self, host, port, username, password, database) :
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

    '''从配置文件中获取MySQL连接信息'''
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host = crawler.settings.get("HOST"),
            port = crawler.settings.get("PORT"),
            username = crawler.settings.get("USERNAME"),
            password = crawler.settings.get("PASSWORD"),
            database = crawler.settings.get("DATABASE")
        )

    # 连接MySQL
    def open_spider(self, spider):
        '''获取数据库链接'''
        self.connect_line = pymysql.connect(
            host = self.host,
            port = self.port,
            user = self.username,
            passwd = self.password,
            db = self.database,
            charset = "utf8"
        )
        ''' 获取数据库游标 通过游标对数据库进行操作 返回结果默认是元组 可以修改为字典的形式 '''
        self.cursor = self.connect_line.cursor(
            cursor = pymysql.cursors.DictCursor
        )

    ''' 关闭数据库链接 '''
    def close_spider(self, spider):
        self.cursor.close()
        self.connect_line.close()

    ''' 进行数据存储 '''
    def process_item(self, item, spider):
        collection_name = item.__class__.__name__
        '''三无新闻不存入数据库'''
        if item["news_content"] == "本新闻暂无内容信息" :
            return item
        if item["news_author"] == "本新闻暂无作者信息" and item["news_content"] == "本新闻暂无内容信息" and item["news_datetime"] == "本新闻暂无日期信息" :
            return item
        '''添加数据'''
        insertSQL = "INSERT INTO sinanews(grade_one_title, grade_one_link, grade_two_title, grade_two_link, grade_two_file_path, " \
                    "grade_two_file_link, news_title, news_author, news_content, news_datetime) VALUES(" \
                    "'" + item['grade_one_title']  + "', '" + item['grade_one_link'] + "', '" + item['grade_two_title'] + "', '" + item['grade_two_link'] + \
                    "', '" + item['grade_two_file_path'] + "', '" + item['grade_two_file_link'] + "', '" + item['news_title'] + "', '" + item['news_author'] + \
                    "', '" + item['news_content'] + "', '" + item['news_datetime'] + "')"
        try :
            number = self.cursor.execute(insertSQL)
            self.connect_line.commit()
            if number > 0 :
                print("数据插入成功！")
            else :
                print("存储程序出错！")
            return item
        except Exception as e :
            print(e.args)
            '''执行回滚操作'''
            self.connect_line.rollback()