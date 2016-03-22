#!/bin/python
#encoding:utf-8
import md5
import time
import datetime
import random
import msgpack

import mongo_util as mongo
import redis_api as redis

def disp_strategy(link_str,num_nodes,encoding):
    try:
        input_str = link_str.encode(encoding,errors='ignore')
        #input_str = link_str
        val = int(md5.md5(input_str).hexdigest(),16)
    except UnicodeEncodeError as e:
        f = open('dispatcher.error','a+')
        f.write("encode_error_url in:%s(%s)"%(input_str,e.message))
        return 0
    return val%num_nodes

def redis_conns():
    hosts = open('./hosts.conf').read().strip().split('\n')
    redis_conns = []
    for host in hosts:
        conn = redis.redis_connect(host)
        redis_conns.append(conn)
    return redis_conns

def dispatcher():
    redisconns = redis_conns()
    servernum = len(redisconns)
    mongo_conn = mongo.connect('192.168.241.12', 'stream')
    packer = msgpack.Packer()
    tablename = 'general'
    key = 'stream'
    try:
        total = int(open('total.dat').read().strip())
    except:
        total = 0
    while True:
        rawdatas = mongo.find(mongo_conn, tablename, {}, 3600)
        tag = False
        for raw in rawdatas:
            tag = True
            raw.pop('_id')
            url = raw['url']
            num = disp_strategy(url, servernum, 'utf-8')
            data = packer.pack(raw)
            try:
                redis.add_set_value(redisconns[num], key, data)
            except:
                fh = open('./error_server.dat','w')
                fh.write('%s\t%s\n'%(num,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                serverlists = range(servernum)
                while True:
                    if len(serverlists)==0:
                        open('stop.dat','w').write('所有服务器均已无法使用')
                        raise Exception('所有服务器均已无法使用')
                    serverlists.remove(num)
                    num = random.choice(serverlists)
                    try:
                        redis.add_set_value(redisconns[num], key, data)
                        break
                    except:
                        fh.write('%s\t%s\n'%(num,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                fh.close()
            total += 1
            mongo.delete(mongo_conn,tablename,prerequisite={'url':url})
        f = open('total.dat','w')
        f.write('%s\n'%(total))
        f.flush()
        f.close()
        if not tag:
            print 'wait urls...'
            time.sleep(120)


if __name__ == '__main__':
    dispatcher()
    
    
    
