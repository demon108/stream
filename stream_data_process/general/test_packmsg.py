import msgpack

import mongo_util as mongo
mongo_conn = mongo.connect('192.168.241.12', 'stream')
tablename = 'general'
rawdatas = mongo.find(mongo_conn, tablename, {}, 500)

packer = msgpack.Packer()

packmsg = []
for raw in rawdatas:
    raw.pop('_id')
    data = packer.pack(raw)
    packmsg.append(data)
    

unpacker = msgpack.Unpacker()
for msg in packmsg:
    print 'msg: ',msg
    unpacker.feed(msg)
    #print 222
    raw = unpacker.unpack()
    print 
    print 'raw: ',raw
    #print 111111111
    break
