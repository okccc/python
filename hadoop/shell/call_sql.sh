#!/usr/bin/env bash

if [ $# -eq 1 ]; then
    sqlfile=$1
    stat_date=`date -d yesterday +%Y%m%d`
	dt=${stat_date:0:8}
	hour=${stat_date:8:2}
elif [ $# -eq 2 ]; then
    sqlfile=$1
    stat_date=$2
else
    echo "wrong arg[] numbers"
    exit 1
fi

CURRENT=`date +'%Y-%m-%d %H:%M:%S'`

logpath=/home/hive/gds/logs/hive/${stat_date}
test ! -d $logpath && mkdir $logpath
hqlpath=/home/hive/gds/hql
ERRORLOG=${logpath}/${sqlfile}_${stat_date}.log

#执行hql文件
hive -hivevar data_date=${stat_date} -hivevar data_date_dt=${dt} -hivevar data_date_hour=${hour} -f ${hqlpath}/${sqlfile}.sql &>> $ERRORLOG

if [ $? -eq 0 ];then
    echo "---call proc succeed at $CURRENT---" >> $ERRORLOG
else
    echo "---call proc failed at $CURRENT---" >>  $ERRORLOG
    exit 1
fi
