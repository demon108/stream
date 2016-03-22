#encoding:utf-8
import datetime
import csv
import sys

import mongo_util as mongo
import mysql_api as mysql
reload(sys)
sys.setdefaultencoding('utf-8')

def get_conn():
    conn_new = mysql.connect('bsppr', '192.168.241.32')
    conn_old = mysql.connect('bsppr', '192.168.241.7')
    return conn_new,conn_old

def get_object(conn):
    sql = 'select bsppr_id,end_date from pm.project;'
    datas = mysql.query_many(conn, sql)
    today = datetime.datetime.now().date()
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
    sql = 'select objectid from object where pid in %s or objectid in %s;'%(oids,oids)
    oids = mysql.query_many(conn, sql)
    oids = [oid[0] for oid in oids]
    return oids

def get_cinfo_obejctid(conn_new,conn_old,terrace,objectid):
    sql = 'select objectid,name,limiter,synonyms,exclude_limiter from object where objectid=%s'%(objectid)
    if terrace=='new':
        data = mysql.query_one(conn_new,sql)
    else:
	data = mysql.query_one(conn_old,sql)
    return data

mongo_conn = mongo.connect('192.168.241.12', 'stream')
conn_new,conn_old = get_conn()
mysql.insert(conn_new,'set names utf8')
mysql.insert(conn_old,'set names utf8')
tablename = 'general'
rawdatas = mongo.find(mongo_conn, tablename, {}, 30000)
csvwriter = csv.writer(open('general_filter.csv','w'))
csvwriter.writerow(['title,url,terrace_info,terrace'])
htmlwriter = open('general_filter.html','w')
html = '''
<html>
    <head>
	<title>平台过滤信息</title>
        <meta http-equiv="content-type" content="text/html;charset=utf-8">
    </head>
    <body>
'''
htmlwriter.write('%s\n'%(html))
oids_new = get_object(conn_new)
oids_old = get_object(conn_old)
for raw in rawdatas:
    title = raw['title']
    url = raw['url']
    objectid = raw['objectid']
    terrace = raw['terrace']  
    if terrace=='new':
	if objectid not in oids_new:
	    continue
    else:
	if objectid not in oids_old:
	    continue
    cinfo = get_cinfo_obejctid(conn_new,conn_old,terrace,objectid)
    terrace_info = 'keyword:%s####limiter:%s####synonyms:%s####exclude_limiter:%s'%(cinfo[1],cinfo[2],cinfo[3],cinfo[4])
    csvwriter.writerow([title,url,terrace_info,terrace]) 
    htmlwriter.write('<a href="%s">%s</a>:  %s</br>\n'%(url,title,terrace_info))
    
htmlend = '''
</body>
</html>
'''
htmlwriter.write('%s\n'%(htmlend))
htmlwriter.flush()
htmlwriter.close()
