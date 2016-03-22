#!/bin/python
#encoding:utf-8
import os
import commands

workspace = '/home/dingyong/stream_data_process/general/'

def get_general_status():
    process = commands.getoutput("ps aux|grep python|grep 'dispatcher.py'|grep -v 'grep'|wc -l")
    if int(process)==0:
        return False
    return True

if __name__ == '__main__':
    if not get_general_status():
	os.chdir(workspace)
	cmd = '/bin/python dispatcher.py &'
	os.system(cmd)
