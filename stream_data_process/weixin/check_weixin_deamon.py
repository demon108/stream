#!/bin/python
#encoding:utf-8
import os
import commands

workspace = '/home/dingyong/stream_data_process/weixin/'

def get_weixin_status():
    process = commands.getoutput("ps aux|grep python|grep 'weixin_process.py'|grep -v 'grep'|wc -l")
    if int(process)==0:
        return False
    return True

if __name__ == '__main__':
    if not get_weixin_status():
	os.chdir(workspace)
	cmd = '/bin/python weixin_process.py > tmp.my &'
	os.system(cmd)
