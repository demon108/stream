from scrapy.http import Request
from scrapy.exceptions import DropItem
import scrapy
from scrapy.conf import settings
from scrapy.signalmanager import SignalManager
from scrapy import signals


from scrapy.spider import Spider


from stream_spider.items import *

class NodeSpider(Spider):
    name = 'test'
