#!/bin/bash
ps -efw |grep scrapy |grep stream_spider|awk '{print "kill -9 "$2}' |bash
