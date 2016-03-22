#encoding:utf-8
import md5
import time
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

def dispatcher():
    hosts = open('./hosts.conf').read().strip().split('\n')
    redis_conns = []
    for host in hosts:
        conn = redis.redis_connect(host)
        redis_conns.append(conn)
    mongo_conn = mongo.connect('192.168.241.12', 'stream')
    servernum = len(hosts)
    packer = msgpack.Packer()
    tablename = 'general'
    key = 'stream'
    maps = {}
    rawdatas = mongo.find(mongo_conn, tablename, {}, 30000)
    for raw in rawdatas:
	raw.pop('_id')
        #print raw
        url = raw['url']
        num = disp_strategy(url, servernum, 'utf-8')
        data = packer.pack(raw)
        redis.add_set_value(redis_conns[num], key, data)
        if num not in maps:
            maps.update({num:1})
        else:
            maps[num] += 1
    print maps
        

if __name__ == '__main__':
    dispatcher()
    
