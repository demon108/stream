import mongo_util as mongo
#global mongo_conn
#mongo_conn = mongo.connect('192.168.241.12', 'stream')

def delete_weixin():
    mongo_conn = mongo.connect('192.168.241.12', 'stream')
    tablename = 'weixin'
    mongo.delete(mongo_conn, tablename)

def create_assemble():
    global mongo_conn
    tablename = 'assemble'
    mongo.create_unique_index(mongo_conn, tablename, uniques=['url'])

def delete_comgeneral():
    mongo_conn = mongo.connect('192.168.241.12', 'stream')
    tablename = 'comgeneral'
    mongo.delete(mongo_conn, tablename)

#create_general()
delete_weixin()
#create_assemble()
delete_comgeneral()

