import MySQLdb

def connect(dbname,host):
    conn = MySQLdb.connect(user='oopin',passwd='OOpin2007Group',db=dbname,host=host);
    return conn

def close(conn):
    conn.cursor().close()
    conn.close()
    
def query_many(conn,sql):
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()
    except:
        raise Exception('sql error') 

def query_one(conn,sql):
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchone()
    except:
        raise Exception('sql error') 

def insert(conn,sql):
    try:
        cursor = conn.cursor()
        num = cursor.execute(sql)
        return num
    except:
        pass

def commit(conn):
    conn.commit()
    
