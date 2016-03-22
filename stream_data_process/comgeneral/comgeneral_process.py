#!bin/python
#encoding:utf-8
import threading
import time
import datetime
import sys

import mysql_api as mysql
import mongo_util as mongo
import feed_xpost
from format_time import format_time
reload(sys)
sys.setdefaultencoding('utf-8')

def get_mongo_conn():
    mongo_conn = mongo.connect('192.168.241.12', 'stream')
    return mongo_conn

def process(terrace):
    if terrace=='new':
        conn = mysql.connect('bsppr', '192.168.241.32')
    else:
        conn = mysql.connect('bsppr', '192.168.241.7')
    mysql.insert(conn,'set names utf8')
    mongo_conn = get_mongo_conn()
    tablename = 'comgeneral'
    while True:
        total = 0
	before_total = 0
        raw_total = 0
        tmpdatas = mongo.find(mongo_conn, tablename, {'terrace':terrace},200)
        print '...%s get data ...'%(terrace)
        rawdatas = []
        for raw in tmpdatas:
            raw_total += 1
            url = raw['url']
            mongo.delete(mongo_conn, tablename, {'url':url})
            datestr = raw['pubtime']
            if not datestr:
                continue
            updatetime = raw.get('updatetime',time.time)
            try:
                date = format_time(datestr,updatetime)
                #open(self.terrace,'a+').write('%s\n'%str(date))
                now = datetime.datetime.now()
                diff = now - date
            except:
                open('date_error.dat','a+').write('%s\t%s\n'%(datestr,url))
                continue
            if diff.days>2:
                continue
            raw.update({'pubtime':date})
            rawdatas.append(raw)
	    before_total += 1
        if tmpdatas.count()==0:
            break
        insert_num = feed_xpost.feed_data_to_xpost(conn, rawdatas,terrace)
        total += insert_num

        open('total_%s.dat'%(terrace),'a+').write('%s\t%s\n'%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),total))
        open('raw_total_%s.dat'%(terrace),'a+').write('%s\t%s\n'%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),raw_total))
        open('before_total_%s.dat'%(terrace),'a+').write('%s\t%s\n'%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),before_total))
        
if __name__ == '__main__':
    #terrace: new feed新平台数据
    #terrace: old feed老平台数据
    terrace = sys.argv[1]
    process(terrace)

