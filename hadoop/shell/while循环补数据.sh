#!/bin/bash

table=$1
partitions=$2

num=1

while [${num} -lt ${partitions}]
do
    echo ${num}
    stat_date=`date -d "-${num} day" +%Y%m%d`  # (注意：是" ",不是' ')
    echo "当前分区是: ${stat_date}"

    # 要执行的代码部分
    hive -hivevar data_date=${stat_date} -f /data/hive/hqls/${table}.sql

    let num+=1

done