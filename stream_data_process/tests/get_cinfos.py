#encoding:utf-8
import datetime

import mysql_api as mysql

global cinfos_new,cinfos_old,mongo_conn

cinfos_new,cinfos_old,mongo_conn = '','',''
def get_conn():
    conn_new = mysql.connect('bsppr', '192.168.241.32')
    conn_old = mysql.connect('bsppr', '192.168.241.7')
    return conn_new,conn_old

def get_cinfos(conn):
    sql = 'select bsppr_id,end_date from pm.project;'
    datas = mysql.query_many(conn, sql)
    today = datetime.datetime.now().date()
    print today
    userids = ''
    for tmp in datas:
	end_date = tmp[1]
	if end_date>=today:
    	    userids = userids+str(tmp[0])+','
    userids = '('+userids[:-1]+')'
    sql = 'select objectid from userconf where userid in %s;'%(userids)
    datas = mysql.query_many(conn, sql)
    oids = ''
    for tmp in datas:
	oids = oids+str(tmp[0])+','
    oids = '('+oids[:-1]+')'
    print oids
    sql = 'select objectid,name,limiter,synonyms,exclude_limiter from object where pid in %s or objectid in %s;'%(oids,oids)
    cinfos = mysql.query_many(conn, sql)
    print len(cinfos)
    return cinfos_new

conn,conn2 = get_conn()
get_cinfos(conn)
