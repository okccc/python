#!/bin/sh

export JAVA_HOME=/usr/java/jdk1.7.0_67-cloudera/

YESTERDAY=`date -d yesterday +%Y%m%d`  # `date -d '-1 day' +%Y%m%d` 或者 `date +%Y%m%d --date '-1 day'`
TODAY=`date -d today +%Y%m%d`  # `date +%Y%m%d`
CURRENT=`date +'%Y-%m-%d %H:%M:%S'`

ip=$1
port=$2
mysql_db=$3
table=$4
column=$5

username=eadmin
password='EWQTB512Oikf;'  # 密码字符串最好加''防止有$等特殊字符导致access denied

log_path=/home/hive/gds/logs/sqoop/input/${YESTERDAY}
watch_path=/home/hive/gds/filewatch/sqoop/input/${YESTERDAY}

if [[ ! -d ${log_path} ]] ; then
    mkdir ${log_path}
fi

if [[ ! -d ${watch_path} ]] ; then
    mkdir ${watch_path}
fi

echo "${CURRENT} start" >> ${log_path}/${table}.log

# 全量抽数据
sqoop import --connect jdbc:mysql://${ip}:${port}/${mysql_db}?tinyInt1isBit=false
--username ${username} --password ${password} --table ${table} --fields-terminated-by '\001'
--hive-drop-import-delims --hive-import --hive-table base.${table} -m 4 --delete-target-dir --hive-overwrite
--null-string '\\N' --null-non-string '\\N' &>> ${log_path}/${table}.log

# 增量抽数据
sqoop import --connect jdbc:mysql://${ip}:${port}/${mysql_db}?tinyInt1isBit=false
--username ${username} --password ${password} --table ${table} --fields-terminated-by '\001' --where "create_time=${YESTERDAY} or update_time=${YESTERDAY}"
--hive-drop-import-delims --hive-import --hive-table base.${table} -m 4 --delete-target-dir --hive-overwrite --hive-partition-key dt --hive-partition-value ${YESTERDAY}
--null-string '\\N' --null-non-string '\\N' &>> ${log_path}/${table}.log

echo "${CURRENT} end" >> ${log_path}/${table}.log

if [[ $? -eq 0 ]] ; then
     echo ${CURRENT} >> ${watch_path/$table}
     echo "sqoop import data succeed!" >> ${log_path}/${table}.log
else
     echo "sqoop import data failed!" >> ${log_path}/${table}.log
     exit 1
fi

# 参数说明：
sqoop import
--connect jdbc:mysql://${ip}:${port}/${mysql_db}?tinyInt1isBit=false
--username ${username}
--password ${password}
--table ${table}
--fields-terminated-by '\001'                               			    # 设置分隔符
--where "create_time=${YESTERDAY} or update_time=${YESTERDAY}"              # 筛选数据
--hive-drop-import-delims                                   			    # 过滤掉分隔符\n, \r, \01
--hive-import                                               	            # 导入hive,不设置就使用hive默认分隔符
--hive-table base.${table} -m 4                                               # -m表示maptask数量
--delete-target-dir                                                         # 删除已存在的目录
--hive-overwrite                                                            # 覆盖数据
--hive-partition-key dt                                                     # 分区字段dt
--hive-partition-value ${YESTERDAY}                                         # 分区值
--null-string '\\N'                                        			        # 将字符串空值写成\\N
--null-non-string '\\N' &>> ${log_path}/${table}.log                        # 将非字符串空值写成\\N


