# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field,Item

class StreamSpiderItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PageMetaItem(Item):
    url = Field()
    http_code = Field()
    content = Field()
    resp_time = Field()
    encoding = Field()
