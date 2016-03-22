#!/bin/python
#encoding:utf-8
import os
import commands
import datetime

workspace = '/home/dingyong/stream_spider/conf'

def get_general_status():
    process = commands.getoutput("ps aux|grep scrapy|grep 'stream_spider'|grep -v 'grep'|wc -l")
    if int(process)==0:
        return False
    return True

if __name__ == '__main__':
    os.chdir(workspace)
    if not get_general_status():
	timeflag = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
	cmd = 'mv total.dat total.dat.%s'%(timeflag)
	os.system(cmd)
	os.chdir(workspace)
	cmd = '/bin/sh run.sh &'
	os.system(cmd)
