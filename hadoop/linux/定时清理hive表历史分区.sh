#!/usr/bin/env bash

LOG_PATH=/user/hive/warehouse/logs.db
ERRORLOG=/bidata/nginx/webtrace/webtrace/branch/rm_log/hive_partition_clean.log

THREE_DAY_AGO=`date -d "-3 day" +%Y%m%d`
CURRENT=`date +'%Y-%m-%d %H:%M:%S'`

TABLE=(info v40_banner by ky shfw szzs)

run(){

	echo "$CURRENT start"

	for table in ${TABLE[*]}
	do
	   # hadoop fs -rm -r $LOG_PATH/log_record_$table/dt=$THREE_DAY_AGO & >> $ERRORLOG（分区还在，数据为空）
	   hive -e "use logs;alter table log_record_$table drop partition(dt=$THREE_DAY_AGO);" & >> $ERRORLOG
	done

	echo "$CURRENT end"

	if [ $? -eq 0 ] ; then
	        echo "delete data succeed! "
	else
	        echo "delete data failed! "
	        exit 1
	fi

}

run 1 >>$ERRORLOG 2>&1