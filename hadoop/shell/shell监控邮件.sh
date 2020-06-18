#!/bin/bash

YESTERDAY=`date -d yesterday +%Y-%m-%d`

# sed可以将表头字段前面的表名去掉
hive -e "set hive.cli.print.header=true;select * from dw.dw_debit_info where dt=${YESTERDAY};" | sed "s/user_info.//g" > /home/aaa.csv
# 中文转码解决windows打开csv文件乱码问题
iconv -f utf-8 -c -t gbk aaa.csv > bbb.csv
# 邮件发送
echo "Hi,附件是昨日数据请查收" | mail -s "app数据" -a /home/bbb.csv chenqian@qbao.com
# 监控报表是否报错
cd /data/logs/hql/${YESTERDAY}/ | grep 'FAILED' *.log