from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

def connect(host,dbname):
    client = MongoClient(host, 27017)
    conndb = client[dbname]
    return conndb

#handle: handle = connect(host,dbname)
def create_unique_index(handle,tablename,uniques=[]):
    conn_table = handle[tablename]
    for unique in uniques:
        conn_table.ensure_index(unique,unique=True)

def create_index(handle,tablename,indexs=[]):
    conn_table = handle[tablename]
    for index in indexs:
        conn_table.ensure_index(index,unique=False)

def insert(handle,tablename,value={}):
    conn_table = handle[tablename]
    try:
        conn_table.insert(value)
    except DuplicateKeyError:
        pass
    
def delete(handle,tablename,prerequisite={}):
    conn_table = handle[tablename]
    conn_table.remove(prerequisite)

def update(handle,tablename,query_dict,new_dict):
    conn_table = handle[tablename]
    conn_table.update(query_dict,new_dict)

'''
if res.count()==0:
    print can`t find res
'''
def find(handle,tablename,query_dict={},limitnum=0):
    conn_table = handle[tablename]
    if limitnum==0:
        res = conn_table.find(query_dict)
    else:
        res = conn_table.find(query_dict).limit(limitnum)
    return res

def close(handle):
    handle.connection.close()

if __name__=='__main__':
    handle = connect('localhost','test_db')
    insert(handle, 'test_table', {'a':1,'b':2})
    
