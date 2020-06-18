#!/bin/bash

TODAY=`date -d today +%Y%m%d`

# 每天备份一次
crontab -l > /home/bak/crontab_${TODAY}.bak

# 同时删除3天前的数据
find /home/bak/ -mtime +3 -name '*.bak' -exec rm -rf {} \;