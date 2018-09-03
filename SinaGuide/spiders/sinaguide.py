# -*- coding: utf-8 -*-
import os
import scrapy
from scrapy.selector import Selector
from SinaGuide.items import SinaNewsItem

'''分布式项目设置'''
from scrapy_redis.spiders import RedisSpider, RedisCrawlSpider


'''
    --scrapy--
    class SinaguideSpider(scrapy.Spider) : 
'''
'''--scrapy-redis--'''
class SinaguideSpider(RedisSpider) :
    name = 'sinaguide'

    '''
        --scrapy--
        start_urls = ['http://news.sina.com.cn/guide/',] 
    '''

    '''--scrapy-redis--'''
    redis_key = "SinaguideSpider:start_urls"

    '''
        --scrapy--
        allowed_domains = None
    '''
    '''
        --scrapy-redis-- 
        动态域名,自动获取域范围
    '''
    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(SinaguideSpider, self).__init__(*args, **kwargs)

    def parse(self, response) :
        if response.status == 200 :
            '''存储item信息'''
            items = []
            '''获取所有的一级资讯列表DIV对象'''
            type_one_divs = Selector(response=response).xpath("//div[@class='section'][@id='tab01']/div[@class='clearfix']")

            for div_number_index in range(0, len(type_one_divs)) :
                '''不爬取地方站新闻信息'''
                if div_number_index != 19 :
                    '''获取一级资讯链接地址、链接标题'''
                    type_one_link= type_one_divs[div_number_index].xpath("./h3/a/@href").extract_first().strip()
                    type_one_title = type_one_divs[div_number_index].xpath("./h3/a/text()").extract_first().strip()

                    '''获取本一级资讯链接下所有的二级资讯链接地址、链接标题'''
                    type_two_links = type_one_divs[div_number_index].xpath("./ul//a/@href").extract()
                    type_two_titles = type_one_divs[div_number_index].xpath("./ul//a/text()").extract()

                    for type_two_index in range(0, len(type_two_titles)):
                        '''创建目录'''
                        type_two_path = "E:/PYthon/Spider Text/SinaGuideSpider-scrapy-redis/SinaGuide/SinaGuide/Data/" + type_one_title + "/" + type_two_titles[type_two_index].strip()

                        '''创建item对象存储新闻信息'''
                        news_item = SinaNewsItem()

                        '''判断该目录是否存在 不存在则创建相应目录'''
                        if not os.path.exists(type_two_path):
                            os.makedirs(type_two_path)

                        '''
                            存储一级链接地址、链接标题、二级链接地址、链接标题、新闻文件存储路径
                        '''
                        news_item["grade_one_link"] = type_one_link
                        news_item["grade_one_title"] = type_one_title

                        news_item["grade_two_link"] = type_two_links[type_two_index].strip()
                        news_item["grade_two_title"] = type_two_titles[type_two_index].strip()

                        news_item["grade_two_file_path"] = type_two_path + "/"

                        items.append(news_item)

                        '''请求二级资讯链接 获取所有以 .shtml 结尾的链接地址'''
                        '''meta = {"meta_one", news_item}, 将数据封装至本请求的回调函数response中 后续方便在下一个回调函数中使用该数据'''
                        yield scrapy.Request(
                            url=news_item["grade_two_link"],
                            meta={"meta_one": news_item},
                            callback=self.find_news_links,
                            dont_filter=True
                        )

                else :
                    continue
        else :
            print("-----------请求链接失败-----------")



    '''获取所有以 .shtml结尾的链接 并请求 得到文章信息'''
    def find_news_links(self, response) :
        if response.status == 200 :
            '''存储item信息'''
            items = []

            '''抽取response中的mata数据'''
            meta_one = response.meta["meta_one"]
            '''获取所有的a标签链接地址'''
            news_links_all = Selector(response=response).xpath("//a/@href").extract()
            '''匹配所有以.shtml结尾 并且以一级链接地址开头 的链接'''
            for link_index in range(0, len(news_links_all)):

                if news_links_all[link_index].endswith('.shtml') and news_links_all[link_index].startswith(meta_one["grade_one_link"]):
                    '''存储新闻信息'''
                    news_item = SinaNewsItem()

                    news_item["grade_one_link"] = meta_one["grade_one_link"]
                    news_item["grade_one_title"] = meta_one["grade_one_title"]

                    news_item["grade_two_link"] = meta_one["grade_two_link"]
                    news_item["grade_two_title"] = meta_one["grade_two_title"]

                    news_item["grade_two_file_path"] = meta_one["grade_two_file_path"]

                    news_item["grade_two_file_link"] = news_links_all[link_index].strip()
                    items.append(news_item)

                    '''请求所有的新闻链接获取新闻标题、新闻发布日期、新闻内容'''
                    yield scrapy.Request(
                        url=news_links_all[link_index].strip(),
                        meta={"meta_two": news_item},
                        callback=self.find_news_detail,
                        dont_filter=True
                    )
        else:
            print("-----------请求链接失败-----------")


    '''请求所有的新闻链接获取新闻标题、新闻发布日期、新闻内容'''
    def find_news_detail(self, response) :
        if response.status == 200 :
            '''抽取response中的mata数据'''
            meta_two = response.meta["meta_two"]

            '''获取新闻详情'''
            news_item = SinaNewsItem()

            news_item["grade_one_link"] = meta_two["grade_one_link"]
            news_item["grade_one_title"] = meta_two["grade_one_title"]

            news_item["grade_two_link"] = meta_two["grade_two_link"]
            news_item["grade_two_title"] = meta_two["grade_two_title"]

            news_item["grade_two_file_path"] = meta_two["grade_two_file_path"]
            news_item["grade_two_file_link"] = meta_two["grade_two_file_link"]

            '''设置匹配规则 若第一种匹配规则查询不到信息则采用第二种匹配规则 以此类推'''
            news_item = self.match_news(response, news_item)

            yield news_item
        else:
            print("-----------请求链接失败-----------")

    '''新闻作者匹配规则'''
    def match_news(self, response, news_item) :

        title_match_rules = [
            "//h1[@class='main-title']/text()", "//h1[@id='artibodyTitle']/text()",
        ]
        news_item["news_title"] = news_item["grade_two_file_link"]

        author_match_rules = [
            "//span[@class='source ent-source']/text()", "//a[@data-sudaclick='content_media_p']/text()",
            "//span[@id='author_ename']/a/text()", "//div[@id='page-tools']/span/span[1]/a/text()", "//span[@id='author_ename']/text()",
            "//div[@id='top_bar']/div/div[1]/span[1]/text()", "//span[@id='media_name']/span/a/text()","//div[@id='wrapOuter']/div/div[1]/div[0]/a/text()",
            "//span[@id='media_name']/a[0]/text()", "/html/body/div[3]/div[3]/div[2]/div/div[0]/p/a/text()"
        ]
        news_item["news_author"] = "本新闻暂无作者信息"

        content_match_rules = [
            "//div[@id='article_content']/div[0]//div[@id='artibody']/p/text()", "//div[@id='article_content']/div[0]//div[@id='article']/p/text()",
            "//div[@id='artibody']/p/text()", "//div[@id='article']/p/text()", "/html/body/div[3]/div[3]/div[1]/div[1]/p/text()",
        ]
        news_item["news_content"] = "本新闻暂无内容信息"

        datetime_match_rules = [
            "//span[@class='date']/text()", "//span[@id='pub_date']/text()", "//div[@id='page-tools']/span/span[0]",
            "//div[@id='top_bar']/div/div[1]/span[0]", "/html/body/div[3]/div[3]/div[0]/div[0]/text()",
        ]
        news_item["news_datetime"] = "本新闻暂无日期信息"

        for title_match_rule in title_match_rules :
            '''查询该匹配规则是否可以匹配到指定新闻信息 匹配不到则更换匹配规则'''
            match_title = Selector(response = response).xpath(title_match_rule).extract_first()
            if match_title == None :
                continue
            else :
                '''将默认值进行覆盖 跳出当前循环'''
                news_item["news_title"] = match_title
                break

        for author_match_rule in author_match_rules :
            '''查询该匹配规则是否可以匹配到指定新闻信息 匹配不到则更换匹配规则'''
            match_author = Selector(response = response).xpath(author_match_rule).extract_first()
            if match_author == None :
                continue
            else :
                '''将默认值进行覆盖 跳出当前循环'''
                news_item["news_author"] = match_author
                break

        for content_match_rule in content_match_rules :
            '''查询该匹配规则是否可以匹配到指定新闻信息 匹配不到则更换匹配规则'''
            match_content_list = Selector(response = response).xpath(content_match_rule).extract()
            if len(match_content_list) == 0 :
                continue
            else :
                news_content = ""
                '''将默认值进行覆盖 跳出当前循环'''
                for content_text in match_content_list :
                    news_content = news_content + content_text + "\n"
                news_item["news_content"] = news_content
                break

        for datetime_match_rule in datetime_match_rules :
            '''查询该匹配规则是否可以匹配到指定新闻信息 匹配不到则更换匹配规则'''
            match_datetime = Selector(response = response).xpath(datetime_match_rule).extract_first()
            if match_datetime == None :
                continue
            else :
                '''将默认值进行覆盖 跳出当前循环'''
                news_item["news_datetime"] = match_datetime
                break

        return news_item


