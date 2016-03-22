# -*- coding: utf-8 -*-

# Scrapy settings for stream_spider project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'stream_spider'

SPIDER_MODULES = ['stream_spider.spiders']
NEWSPIDER_MODULE = 'stream_spider.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'stream_spider (+http://www.yourdomain.com)'
DOWNLOAD_DELAY = 0

#default 180secs
DOWNLOAD_TIMEOUT = 60

ITEM_PIPELINES = {
    'stream_spider.pipelines.StreamSpiderPipeline':0
}

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19'
LOG_LEVEL='INFO'
#LOG_LEVEL='DEBUG'
LOG_FILE='scrapy.log'
LOG_ENCODING='utf-8'
