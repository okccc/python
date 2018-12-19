#!/usr/bin/env bash

YESTERDAY=`date -d yesterday +%Y-%m-%d`

# sed可以将表头字段前面的表名去掉
hive -e "set hive.cli.print.header=true;select * from bi_dm.t_app_v40_index_localtion_d where dt='$YESTERDAY';" | sed "s/user_info.//g" > /home/aaa.csv
# 中文转码解决windows打开csv文件乱码问题
iconv -f utf-8 -c -t gbk aaa.csv > bbb.csv

echo "Hi ：

附件是昨日app数据，请查收" |mail -s "app数据"
-a /home/dw/hive/flume/v40_banner/data/app楼层数据.xlsx
-a /home/dw/hive/flume/v40_banner/data/app旧模块数据.xlsx
-a /home/dw/hive/flume/v40_banner/data/app新模块数据.xlsx
chenqian@qbao.com zhubaojin@qbao.com wangzhengcai@qbao.com

rm -f /home/dw/hive/flume/v40_banner/data/*