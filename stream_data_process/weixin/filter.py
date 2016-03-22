#encoding:utf-8

def parse_config_info(name,limiter,synonyms,exclude_limiter):
    limiter_parse=[]
    if limiter:
        limiter_parse_tmps = limiter.split(',')
        for limiter_parse_tmp in limiter_parse_tmps:
            limiter_parse_tmp2 = limiter_parse_tmp.split('#$!#')
            limiter_parse.append(limiter_parse_tmp2)
    if synonyms:
        synonyms_parse_tmp = synonyms.split('#$!#')
	synonyms_parse = []
	for s in synonyms_parse_tmp:
	    if not s.strip():
		continue
	    synonyms_parse.append(s)
    else:
        synonyms_parse = []
    synonyms_parse.append(name)
    if exclude_limiter:
        exclude_limiter_tmp = exclude_limiter.split('#$!#')
        exclude_limiter_parse = []
        for ex in exclude_limiter_tmp:
            if not ex.strip():
                continue
            exclude_limiter_parse.append(ex)
    else:
        exclude_limiter_parse = []
    return limiter_parse,synonyms_parse,exclude_limiter_parse

# def interpose_mongo(raw_qualified):
#     handle = get_mongo_conn()
#     tablename = 'datas'
#     for qualified in raw_qualified:
#         objectid = qualified['objectid']
#         data = qualified['data']
#         data.update({'objectid':objectid})
#         mongo.insert(handle, tablename, data)

#weixin rawdatas:  [{'title':title,'url':url,'pubtime':pubtime,'author':author}]
def filter(cinfos,rawdatas):
    raw_qualified = []
    total = 0
    for cinfo in cinfos:
        objectid = cinfo[0]
        name = cinfo[1]
        limiter = cinfo[2]
        synonyms = cinfo[3]
        exclude_limiter = cinfo[4]
        if not name.strip() and not synonyms.strip():
	    continue
	#open('cinfos.my','a+').write(str(objectid)+','+str(name)+','+str(limiter)+','+str(synonyms)+','+str(exclude_limiter)+'\n')
        limiter_parse,synonyms_parse,exclude_limiter_parse = parse_config_info(name,limiter,synonyms,exclude_limiter)
        #rawdatas:  [{'title':title,'url':url,'pubtime':pubtime,'author':author}]
        for data in rawdatas:
	    #print data['pubtime'].strftime('%Y-%m-%d')
            title = data['title']
            content = title
            #tag：该条数据是否上前台的标志
            tag = False
            #判断同义词：出现一个则为真
	    #print synonyms_parse
            for synonym in synonyms_parse:
                if content.find(synonym)!=-1:
                    tag = True
                    break
            if not tag:
                continue
            #判断反向限定词：出现一个则为假
            for exclude_limit in exclude_limiter_parse:
                if content.find(exclude_limit)!=-1:
                    tag = False
                    break
            if not tag:
                continue
            #判断限定词：[[1,2,3],[4,5,6]]
            #列表中的子列表为或的关系，只要出现一个即为真
            #子列表中的每项为与的关系，必须全部出现才为真
            for limite in limiter_parse:
                tag = True
                for lim in limite:
                    if content.find(lim)==-1:
                        tag = False
                        break 
                if tag:
                    break
            if not tag:
                continue
	    #open('result.my','a+').write(str(objectid)+','+str(name)+','+str(synonyms)+'######'+str(exclude_limiter)+'\n')
	    #open('result.my','a+').write(title+'\n')
	    #open('result.my','a+').write('\n')
            data.update({'objectid':objectid,'type':'weixin'})
            raw_qualified.append(data)
            total += 1
    return raw_qualified



