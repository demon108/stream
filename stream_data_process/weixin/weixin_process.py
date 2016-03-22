#!bin/python
#encoding:utf-8
import time
import datetime
import sys

import mysql_api as mysql
import mongo_util as mongo
import feed_xpost
from filter import filter
reload(sys)
sys.setdefaultencoding('utf-8')

def get_cinfos(conn):
    sql = 'select objectid,name,limiter,synonyms,exclude_limiter from object'
    cinfos = mysql.query_many(conn, sql)
    return cinfos

def get_cinfos_moa(conn):
    sql = 'select bsppr_id,end_date,state from pm.project;'
    datas = mysql.query_many(conn, sql)
    today = datetime.datetime.now().date()
    userids = ''
    for tmp in datas:
        end_date = tmp[1]
        state = tmp[2]
        if state == 0 or state == 1:
            if end_date>=today:
                userids = userids+str(tmp[0])+','
    userids = '('+userids[:-1]+')'
    sql = 'select objectid from userconf where userid in %s;'%(userids)
    datas = mysql.query_many(conn, sql)
    oids = ''
    for tmp in datas:
        oids = oids+str(tmp[0])+','
    oids = '('+oids[:-1]+')'
    sql = 'select objectid,name,limiter,synonyms,exclude_limiter from object where pid in %s or objectid in %s;'%(oids,oids)
    cinfos = mysql.query_many(conn, sql)
    return cinfos


def get_mongo_conn():
    mongo_conn = mongo.connect('192.168.241.12', 'stream')
    return mongo_conn

def process():
    conn_old = mysql.connect('bsppr', '192.168.241.7')
    mysql.insert(conn_old,'set names utf8')
    conn_new = mysql.connect('bsppr', '192.168.241.32')
    mysql.insert(conn_new,'set names utf8')
    cinfos_old = get_cinfos_moa(conn_old)
    cinfos_new = get_cinfos_moa(conn_new)
    mongo_conn = get_mongo_conn()
    tablename = 'weixin'
    while True:
	tmpdatas = mongo.find(mongo_conn, tablename, {},1000)
        rawdatas = []
        for raw in tmpdatas:
	    url = raw['url']
            mongo.delete(mongo_conn, tablename, {'url':url})
            date = raw['pubtime']
            now = datetime.datetime.now()
            diff = now - date
            if diff.days>2:
                continue
            rawdatas.append(raw)
        if len(rawdatas)==0:
	    print 'wait datas...'
            time.sleep(300)
        raw_old_qualified = filter(cinfos_old,rawdatas)
	if raw_old_qualified:
            old_insert_num = feed_xpost.feed_data_to_xpost(conn_old, raw_old_qualified,'old')
	    print 'old_insert_num: ',old_insert_num
        raw_new_qualified = filter(cinfos_new,rawdatas)
	if raw_new_qualified:
            new_insert_num = feed_xpost.feed_data_to_xpost(conn_new, raw_new_qualified,'new')
	    print 'new_insert_num: ',new_insert_num
        
       
if __name__ == '__main__':
    process()
        
        
    
