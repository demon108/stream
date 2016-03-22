#!/bin/python
#encoding:utf-8
import os
import commands

workspace = '/home/dingyong/stream_data_process/comgeneral/'

def get_general_status(terrace):
    process = commands.getoutput("ps aux|grep python|grep 'comgeneral_process.py'|grep %s|grep -v 'grep'|wc -l"%(terrace))
    if int(process)==0:
        return False
    return True

if __name__ == '__main__':
    #new
    if not get_general_status('new'):
	os.chdir(workspace)
	cmd = '/bin/python comgeneral_process.py new &'
	os.system(cmd)
    #old
    if not get_general_status('old'):
        os.chdir(workspace)
        cmd = '/bin/python comgeneral_process.py old &'
        os.system(cmd)
