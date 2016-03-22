import redis_api as redis

conn = redis.redis_connect('192.168.241.56')

redis.add_set_value(conn,'key', 'data')
