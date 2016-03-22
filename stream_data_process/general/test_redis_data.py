import msgpack

import redis_api as redis

conn = redis.redis_connect('192.168.241.12')

key = 'stream'
datas = redis.pop_set_urls(conn, key, 100)
unpacker = msgpack.Unpacker()
for data in datas:
    unpacker.feed(data)
    raw = unpacker.unpack()
    print raw

