#!/bin/bash

if [ $# -eq 1 ]; then
    sqlfile=$1
    stat_date=`date -d yesterday +%Y%m%d`
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

# hive shell -> sql对应的dt=${hivevar:dt}
hive -hivevar dt=${stat_date} -f ${hqlpath}/${sqlfile}.sql &>> ${ERRORLOG}
# impala-shell -> sql对应的dt='${var:dt}'
impala-shell -i master2 --var=dt=${stat_date} -f ${hqlpath}/${sqlfile}.sql &>> ${ERRORLOG}

if [ $? -eq 0 ];then
    echo "---call proc succeed at $CURRENT---" >> ${ERRORLOG}
else
    echo "---call proc failed at $CURRENT---" >>  ${ERRORLOG}
    exit 1
fi
