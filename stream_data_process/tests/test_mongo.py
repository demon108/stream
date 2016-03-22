import mongo_util as mongo

conn = mongo.connect('192.168.241.12','stream')
url = 'http://mp.weixin.qq.com/s?__biz=MjM5ODU4OTkxNQ==&mid=401347170&idx=2&sn=2efdb73104dd08c6422d53a4efd09ccc&scene=4#wechat_redirect'
#url = 'weixin'
result = mongo.find_one(conn,'weixin',query_dict={'url':url})
print result['url']
if not result:
    print 333
print 2222
