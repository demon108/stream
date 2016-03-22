import mongo_util as mongo
global mongo_conn
#mongo_conn = ''
mongo_conn = mongo.connect('192.168.241.12', 'stream')
def create_general():
    global mongo_conn
    if not mongo_conn:
        tablename = 'general'
        mongo_conn = mongo.connect('192.168.241.12', 'stream')
        mongo.create_unique_index(mongo_conn, tablename, uniques=[[('objectid',1),('url',1)]])
        mongo.create_index(mongo_conn, tablename, indexs=['updatetime','terrace'])
    return mongo_conn

def create_weixin():
    global mongo_conn
    tablename = 'weixin'
    mongo.create_unique_index(mongo_conn, tablename, uniques=['url'])
    mongo.create_index(mongo_conn, tablename, indexs=['updatetime'])

def create_assemble():
    global mongo_conn
    tablename = 'assemble'
    mongo.create_unique_index(mongo_conn, tablename, uniques=['url'])

def create_comgeneral():
    mongo_conn = mongo.connect('192.168.241.12', 'stream')
    tablename = 'comgeneral'
    mongo.create_unique_index(mongo_conn, tablename, uniques=[[('objectid',1),('url',1)]])
    mongo.create_index(mongo_conn, tablename, indexs=['updatetime','terrace'])

#create_general()
#create_weixin()
#create_assemble()
create_comgeneral()

