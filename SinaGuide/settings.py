# -*- coding: utf-8 -*-

# Scrapy settings for SinaGuide project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'SinaGuide'

SPIDER_MODULES = ['SinaGuide.spiders']
NEWSPIDER_MODULE = 'SinaGuide.spiders'

'''不遵守爬虫协议'''
ROBOTSTXT_OBEY = False

'''配置MySQL数据库连接信息'''
HOST = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "123456"
DATABASE = "sinanews"

'''设置下载延迟1.5秒'''
DOWNLOAD_DELAY = 1.5

'''默认请求头'''
DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'en',
   'Upgrade-Insecure-Requests' : '1',
   'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3343.4 Safari/537.36'
}

'''设置管道'''
ITEM_PIPELINES = {
   'SinaGuide.pipelines.SinaNewsPipelineByFiles': 300,
   # 'SinaGuide.pipelines.MySQLPipeline': 600,
   'scrapy_redis.pipelines.RedisPipeline': 800,
}

'''----------新增的分布式设置信息----------'''
'''使用的去重模块（使用scrapy-redis的去重组件 不使用scrapy默认的去重组件）'''
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

'''使用的调度器模块（使用scrapy-redis的调度器模块 不使用scrapy默认的调度器模块）'''
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

'''设置该爬虫程序可暂停，不会清空之前的redis数据库存储的请求数据、请求记录、下载数据....'''
SCHEDULER_PERSIST = True

'''选择其中一个开启（设置请求进出队列规则）'''
'''scrapy默认的请求队列模式（按照优先级顺序 先进先出）'''
SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
'''
队列形式规则（请求先进先出
   SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
栈形式（请求 先进后出）
   SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"
'''

'''指定redis数据库主机ip 默认为本机127.0.0.1'''
REDIS_HOST = "127.0.0.1"

'''指定数据库的端口号 默认为6379'''
REDIS_PORT = 6379

'''指定redis链接参数'''
REDIS_PARAMS = {
   "password": "111111",
}
'''
redis编码类型 默认utf-8
REDIS_ENCODING = "utf-8"

redis链接参数 默认
   REDIS_PARAMS = {
      'socket_timeout': 30,
      'socket_connect_timeout': 30,
      'retry_on_timeout': True,
      'encoding': REDIS_ENCODING,
   }
   
设置redis数据库链接信息(可选设置 设置此值则此值优先级大于REDIS_HOST、REDIS_PORT...)
   REDIS_URL = 'redis://root:密码@主机ＩＰ:端口'
   REDIS_URL = 'redis://root:111111@127.0.0.1:6379'
'''

'''保存日志信息的文件名
LOG_FILE = "sinanews.log"
'''
'''
   保存日志等级，低于|等于此等级的信息都被保存
   INFO(一般信息) DEBUG(调试信息) WARNING(警告信息) ERROR(一般错误) CRITICAL(严重错误)

LOG_LEVEL = "DEBUG"
'''

'''
   ITEM_PIPELINES = {
    支持将数据存储到redis数据库 必须启动
    'scrapy_redis.pipelines.RedisPipeline': 400,
   }
'''

'''----------新增的分布式设置信息----------'''

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'SinaGuide (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32


# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'SinaGuide.middlewares.SinaguideSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'SinaGuide.middlewares.SinaguideDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

