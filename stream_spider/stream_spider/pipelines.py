# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from stream_bkb_wirter.writer import Write_BKB 
from items import *

class StreamSpiderPipeline(object):

    def __init__(self):
        self.writer = Write_BKB()
        
    def process_item(self, item, spider):
        http_code = item['http_code']
        if http_code >= 200 and http_code < 300:
            url = item['url']
            encoding = item['encoding']
            content = item['content']
            item={'url':url,'content':content,'encoding':encoding}
            self.writer.process_item(item)
            
    def close_spider(self,spider):
        self.writer.close()
