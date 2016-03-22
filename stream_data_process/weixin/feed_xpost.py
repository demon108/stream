#encoding:utf-8
import urlparse

import mysql_api as mysql

def get_site_id(conn,url):
    domain = urlparse.urlparse(url).netloc
    sql = "select siteid,name from xsite where url='%s';"%(domain)
    data = mysql.query_one(conn, sql)
    if not data:
        isql = "insert into xsite(name,url) values('%s','%s');"%(domain,domain)
        mysql.insert(conn, isql)
        mysql.commit(conn)
        data = mysql.query_one(conn, sql)
    return data

SOURCE_TYPE_MAP = {'news':1,'forum':2,'blog':3,'qa':6,'weixin':12,'SNS':8} 
MAX_INT_VALUE = 2147483647
#qualified_datas:[{'title':title,'url':url,'pubtime':pubtime,'author':author,'objectid':objectid,'type':'weixin'}]
def feed_data_to_xpost(conn,qualified_datas,terrace):
    cursor = conn.cursor()
    try:
        n = len(qualified_datas)
        key_counter_update_sql = 'UPDATE key_counter SET value=LAST_INSERT_ID(value+%d) WHERE name="xpostid";'%(n)
        cursor.execute(key_counter_update_sql)
        conn.commit()
        key_counter_sql = 'SELECT LAST_INSERT_ID();'
        if terrace=='old':
            xpostid = mysql.query_one(conn, key_counter_sql)[0]
            xpostid = xpostid - n
            next_xpostid = MAX_INT_VALUE - xpostid - n
        else:
            xpostid = mysql.query_one(conn, key_counter_sql)[0]
            next_xpostid = xpostid - n
        #xpostid.write('%s %s\n'%(next_xpostid,next_xpostid+n))
    except Exception,e:
        print e
        conn.rollback()
        return -1
    insert_num = 0
    for qualified_data in qualified_datas:
        objectid = qualified_data['objectid']
        date = qualified_data['pubtime'].strftime('%Y-%m-%d')
        facet_sql = 'select id from xfacet where objectid=%s and type=1;'%(objectid)
	try:
            facetid = mysql.query_one(conn, facet_sql)[0]
	except Exception,e:
	    #print e
	    continue
        xentry_sql = 'select entryid from xentry where facetid=%s and date="%s";'%(facetid,date)
        xentryid = mysql.query_one(conn, xentry_sql)
        if not xentryid:
            xentry_insert_sql = 'insert into xentry(facetid,date) values(%s,"%s");'%(facetid,date)
            mysql.insert(conn, xentry_insert_sql)
            mysql.commit(conn)
            xentryid = mysql.query_one(conn, xentry_sql)
        try:
            xentryid = xentryid[0]
        except Exception,e:
            print e
            return -1
        xpostnum = xentryid%8
        title,abstract,posttime,url,author,comment_count,click_count,template_type = qualified_data['title'],'',qualified_data['pubtime'],qualified_data['url'],qualified_data['author'],0,0,qualified_data['type']
        duplicate_sql = 'select postid from xpost%d where entryid=%d and url="%s";'%(xpostnum,xentryid,conn.escape_string(url))
        cursor.execute(duplicate_sql)
        postid = cursor.fetchall()
        if postid:
	    #print xpostnum,postid
            continue
        sourcetype = SOURCE_TYPE_MAP.get(template_type,4)
        site_id,domain = get_site_id(conn,url) 
        hidden = 0
        #title,abstract,posttime,url,author,comment_count,click_count
        xpost_sql = 'insert into xpost%d(postid,entryid,title,abstract,posttime,url,author,reply,click,sourcetype,source,domain,hidden) values(%s,%s,"%s","%s","%s","%s","%s",%s,%s,%s,%s,"%s",%s);'
        xpost_sql = xpost_sql%(xpostnum,next_xpostid,xentryid,conn.escape_string(title),\
                               abstract,posttime,conn.escape_string(url),\
                               conn.escape_string(author),comment_count,click_count,sourcetype,site_id,domain,hidden)
        #xpostsql.write(xpost_sql+'\n')
        ###mysql.insert(conn, xpost_sql)
        try:
            cursor.execute(xpost_sql)
	    open('xpost_sql_%s.my'%(terrace),'a+').write(xpost_sql+'\n')
        except Exception,e:
            insert_xpost_error = open('insert_old_xpost_error.error','a+')
            insert_xpost_error.write(str(e)+'\n')
            insert_xpost_error.write(xpost_sql+'\n')
            insert_xpost_error.write('\n')
        next_xpostid += 1
        insert_num += 1
    conn.commit()
    return insert_num
    
        
        
