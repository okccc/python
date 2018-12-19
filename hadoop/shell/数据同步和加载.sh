#!/usr/bin/env bash

if [ $# -eq 2 ]; then
    table_name="$1"
    stat_date="$2"
elif [ $# -eq 1 ]; then
    table_name="$1"
    stat_date=`date -d yesterday +%Y%m%d`
else
    echo "wrong arg[] number"
    exit 1
fi

flume_date=`date -d ${stat_date} +%Y-%m-%d`
current_date=`date +'%Y-%m-%d %H:%M:%S'`

ERRORLOG=/bidata/nginx/webtrace/webtrace/branch/shfw/shfw_error.log

run(){

    #同步数据到30
    echo "$current_date start" >> $ERRORLOG

    scp root@172.16.3.23:/Data/LOG/nginx/qianbao_webtrace/${stat_date}/da_v40_banner_dig_json.access.log*.gz /bidata/nginx/webtrace/webtrace/${stat_date}/
    zcat /bidata/nginx/webtrace/webtrace/${stat_date}/da_v40_banner_dig_json.access.log*.gz | grep '"status": 200' > /bidata/nginx/webtrace/webtrace/branch/shfw/da_v40_banner_${stat_date}.log
    rm -rf /bidata/nginx/webtrace/webtrace/${stat_date}/da_v40_banner_dig_json.access.log*.gz

    echo "$current_date end" >> $ERRORLOG

    if [ $? -eq 0 ] ; then
            echo "sync data succeed! "
    else
            echo "sync data failed! "
            exit 1
    fi

    #加载数据到hive(local表示linux本地,没有local表示hdfs)
    hive -e "LOAD DATA LOCAL INPATH 'bidata/nginx/webtrace/webtrace/branch/shfw/da_v40_banner_${stat_date}.log' OVERWRITE INTO TABLE logs.${table_name} partition(dt=${stat_date});"

    if [ $? -eq 0 ] ; then
            echo "load data succeed! "
    else
            echo "load data failed! "
            exit 1
    fi
}

run 1 >>$ERRORLOG 2>&1