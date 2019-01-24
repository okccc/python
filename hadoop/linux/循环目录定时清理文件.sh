#!/usr/bin/env bash

LOG_PATH=/bidata/nginx/webtrace/webtrace/branch
ERRORLOG=/bidata/nginx/webtrace/webtrace/branch/rm_log/log_clean.log

TWO_DAY=`date -d "2 day ago" +%Y%m%d`
TWO_DAY1=`date -d "2 day ago" +%Y-%m-%d`
CURRENT=`date +'%Y-%m-%d %H:%M:%S'`

LOG_DIR=(by m_qianbao qianbao)
LOG_DIR1=(qhb szzs)

run(){
    echo "$CURRENT start"

    cd $LOG_PATH
    for log_dir in ${LOG_DIR[*]}
    do
       rm -rf $LOG_PATH/$log_dir/$TWO_DAY
    done

    for log_dir in ${LOG_DIR1[*]}
    do
       rm -rf $LOG_PATH/$log_dir/rsync_log_path/$TWO_DAY1
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