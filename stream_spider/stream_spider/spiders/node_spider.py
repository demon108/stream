#encoding:utf-8
import urlparse
import codecs
import sys
import csv
import datetime
import time
import re
import json
import math
from bs4 import BeautifulSoup
import urlparse
import msgpack

from scrapy.selector import Selector
from scrapy.spider import Spider
from scrapy.http import Request,FormRequest
from scrapy import log
from scrapy.signalmanager import SignalManager
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

from pageclean import pgcleaner
from stream_spider.items import *
from stream_spider import redis_api as redis 
from stream_spider import mongo_util as mongo
reload(sys)
sys.setdefaultencoding('utf-8')

class NodeSpider(Spider):
    
    name = 'stream_spider'
    
    REDISKEY = 'stream'
    MONGOTABLE = 'assemble'
    total = 0
    def __init__(self):
        self.redis_conn = redis.redis_connect('127.0.0.1')
        self.unpacker = msgpack.Unpacker()
        self.mongo_conn = mongo.connect('192.168.241.12','stream')
        #sig = SignalManager(dispatcher.Any)
        #sig.connect(self.idle,signal=signals.spider_idle)
        
    def process_redis_rawdatas(self,num=1000):
	try:
            rawdatas = redis.pop_set_urls(self.redis_conn, self.REDISKEY, num)
	except Exception,e:
	    rawdatas = []
        reqs = []
        for raw in rawdatas:
            if not raw:
                continue
            self.unpacker.feed(raw)
            #data为utf-8格式
            data = self.unpacker.unpack()
	    try:
                objectid = data['objectid']
                title = data['title']
                url = data['url']
	        terrace = data['terrace']
                pagetype = data.get('pagetype','N')
	    except:
		continue
            #首先判断url是否存在与mongo库中
            result = mongo.find_one(self.mongo_conn,self.MONGOTABLE,query_dict={'url':url})
            if result:
                pubtime = result['pubtime']
                #放入comgeneral表中，由feed程序集中上前台
                table = 'comgeneral'
                mongo.insert(self.mongo_conn,table,value={'url':url,'pubtime':pubtime,'objectid':objectid,'title':title,'pagetype':pagetype,'updatetime':time.time(),'terrace':terrace})
		self.total += 1
            else:
                req = Request(url,meta={'title':title,'pagetype':pagetype,'objectid':objectid,'terrace':terrace})
                reqs.append(req)
        return reqs

    def start_requests(self):
        reqs = self.process_redis_rawdatas(1000)
        return reqs

    def idle(self,spider):
        log.msg('catch idle signal...',log.INFO)
        if spider != self:
            return
        while True:
            req = self.create_request()
            if not req:
                time.sleep(50)
            else:
                break
        if req:
            self.crawler.engine.crawl(req[0], spider)

    def create_request(self):
        reqs = self.process_redis_rawdatas(1)
        return reqs
    
    def parse(self,response):
	self.total += 1
	#f = open('total.dat','w')
	#f.write('%s\n'%(self.total))
	#f.flush()
        pagetype = response.request.meta['pagetype']
        title = response.request.meta['title']
        objectid = response.request.meta['objectid']
	terrace = response.request.meta['terrace']
        try:
            content = response.body_as_unicode()
        except:
            content = response.body
        url = response.url
        http_code = response.status
	try:
            encoding = response.encoding
	except:
	    encoding = 'utf-8'
        retDict = pgcleaner.clean(content, id=url, pagetype=pagetype)
        pubtime = retDict['date']
        # 抓取之后需要把url和date保存下来，以供下次应用
        mongo.insert(self.mongo_conn,self.MONGOTABLE,value={'url':url,'pubtime':pubtime})
        #放入comgeneral表中，由feed程序集中上前台
        table = 'comgeneral'
        mongo.insert(self.mongo_conn,table,value={'url':url,'pubtime':pubtime,'objectid':objectid,'title':title,'pagetype':pagetype,'updatetime':time.time(),'terrace':terrace})
        #存入到rawdb，供后续程序处理
        page_info= PageMetaItem()
        page_info['url'] = response.url
        page_info['http_code'] = http_code
        page_info['resp_time'] = int(time.time())
        page_info['encoding'] = encoding
        page_info['content'] = content
        yield page_info

        reqs = self.process_redis_rawdatas(100)
        for req in reqs:
            yield req

