#encoding:utf-8
import datetime
import time
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

def get_mongo_conn():
    mongo_conn = mongo.connect('192.168.241.12', 'stream')
    return mongo_conn

def process():
    conn_old = mysql.connect('bsppr', '192.168.241.7')
    mysql.insert(conn_old,'set names utf8')
    conn_new = mysql.connect('bsppr', '192.168.241.32')
    mysql.insert(conn_new,'set names utf8')
    cinfos_old = get_cinfos(conn_old)
    #print cinfos_old
    cinfos_new = get_cinfos(conn_new)
    mongo_conn = get_mongo_conn()
    tablename = 'weixin'
    tmpdatas = mongo.find(mongo_conn, tablename, {},50)
    rawdatas = []
    for raw in tmpdatas:
	date = raw['pubtime']
	now = datetime.datetime.now()
	diff = now - date
	print diff.days
	rawdatas.append(raw)
    if len(rawdatas)==0:
        time.sleep(10)
    raw_old_qualified = filter(cinfos_old,rawdatas)
    old_insert_num = feed_xpost.feed_data_to_xpost(conn_old, raw_old_qualified,'old')
    raw_new_qualified = filter(cinfos_new,rawdatas)
    new_insert_num = feed_xpost.feed_data_to_xpost(conn_new, raw_new_qualified,'new')
        
       
process() 
        
        
    
