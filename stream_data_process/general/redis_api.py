#encoding:utf-8
import random
import redis

def redis_connect(host):
    return redis.StrictRedis(host,port=6379,db='0')

def set_expire_time(handle,key,time):
    handle.expire(key,time)

def add_set_value(handle,key,value):
    handle.sadd(key,value)

def check_set_value(handle,key,value):
    #判value是否在set集合中，若在返回True
    return handle.sismember(key,value)

def pop_set_urls(handle,key,num):
    results = set()
    for _ in range(num):
        v = handle.spop(key)
        results.add(v)
    return results

def delete_key(handle,key):
    handle.delete(key)

def add_sort_url(handle,url,key,score = 0):
    score = random.random()
    handle.zadd(key,score,url)

def delete_sort_url(handle,url,key):
    handle.zrem(key,url)

def pop_sort_urls(handle,num,key):
    start = 0
    end = num - 1
    urls = handle.zrevrange(key,start,end)
    for url in urls:
        delete_sort_url(handle, url, key)
    return urls

if __name__ == '__main__':
    #清空zhihu_author2_spider.py的抓取记录的url
    handle = redis_connect()
    redis_key_list = 'zhihu_list_urls'
    delete_key(handle,redis_key_list)
    redis_key_unfetch = 'zhihu_unfetch_urls'
    delete_key(handle,redis_key_unfetch)
    key = 'zhihu_urls'
    delete_key(handle, key)
    
    

