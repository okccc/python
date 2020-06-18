#!/bin/bash

if [ $# -eq 2 ]; then
   table="$1"
   stat_date="$2"
elif [ $# -eq 1 ]; then
   table="$1"
   stat_date=`date -d yesterday +%Y%m%d`
else
   echo "wrong args[] number"
   exit 1
fi

flume_date=`date -d ${stat_date} +%Y-%m-%d`
ERRORLOG=/home/dw/hive/flume/youhaohuo/error.log

run(){

# 方式一:加载数据到hive内部表(将某个目录下的数据剪切到/user/hive/warehouse/**.db/**.table目录)
hive -e "LOAD DATA INPATH '/user/flume/qbao_goods_stuff_log/dt=${flume_date}/*' OVERWRITE INTO TABLE bi_rt.$table partition(dt=${stat_date});"

# 方式二:加载数据到hive外部表(建外部表时指定location就不用再load数据了,直接add partition即可)
hive -e "ALTER TABLE bi_rt.qbao_goods_stuff_log ADD IF NOT EXISTS PARTITION (dt='${flume_date}') LOCATION '/user/flume/qbao_goods_stuff_log/dt=${flume_date}';"

if [ $? -eq 0 ] ; then
        echo "load data succeed! "
else
        echo "load data failed! "
        exit 1
fi

}

run 1 >>$ERRORLOG 2>&1