# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SinaNewsItem(scrapy.Item):
    grade_one_title = scrapy.Field()
    grade_one_link = scrapy.Field()

    grade_two_title = scrapy.Field()
    grade_two_link = scrapy.Field()

    grade_two_file_path = scrapy.Field()
    grade_two_file_link = scrapy.Field()

    news_title = scrapy.Field()
    news_author = scrapy.Field()
    news_content = scrapy.Field()
    news_datetime = scrapy.Field()

