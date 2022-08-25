#!/bin/bash


if [[ $# -eq 3 ]]; then
    # 表名称
    table_name=$1
    # 同步类型,mysqltohive/hivetomysql
    sync_type=$2
    store_type=$3
    # 是否分区表
    is_par_table=N
elif [[ $# -eq 4 ]]; then
    # 表名称
    table_name=$1
    # 同步类型,mysqltohive/hivetomysql
    sync_type=$2
    store_type=$3
    # 是否分区表
    is_par_table=Y
    dt=$4
else
    echo "wrong args[] number"
    exit 1
fi


#库名称
db_name=ods

#文件夹名称
if [[ ${sync_type} == "mysqltohive" ]]; then
    folder_name=MysqlToHive
else
    folder_name=HiveToMysql
fi

#文件名称
file_name=${table_name}
#环境dev/fat/prod
env_type=fat
#文件类型
file_type=txt
#存储类型
table_type=${store_type}

#####以下为抽取脚本，请勿修改
exist_file=${file_name}.${file_type}
comm_path=/data1/projects-app/ChartSync/datax/job/${sync_type}/${env_type}/
if [ "${sync_type}" == "mysqltohive" ]
    then
        echo "mysqltohive"
        #1.添加分区/清空分区
        param="${dt}"
        if [ "${is_par_table}" == "Y" ]
            then
                hive --database ${db_name} -e "alter table ${table_name} drop if exists partition (dt='${dt}')"
                hive --database ${db_name} -e "alter table ${table_name} add if not exists partition (dt='${dt}')"
                echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
            else hive --database ${db_name} -e "truncate table ${table_name}"
        fi
        #！2.判文件是否存在，存在时需要先进行删除，再进行get，不存在时，直接get下来
        if [ -f ${comm_path}${exist_file} ]
            then
                rm -f ${comm_path}${exist_file}
        fi
        hdfs dfs -get /dolphinscheduler/bigdata/resources/${folder_name}/${env_type}/${file_name}.${file_type} ${comm_path}${exist_file}
        python /data1/projects-app/ChartSync/datax/bin/apollo.py ${comm_path}${exist_file} ${sync_type} ${table_type} ${param}
        python /data1/projects-app/ChartSync/datax/bin/datax.py -p "-Dparam=${param}"  ${comm_path}${exist_file}_new
        if [ $? -eq 0 ] ; then
            echo "import data succeed! "
        else
            echo "import data failed! "
            exit 1
        fi
fi
if [ "${sync_type}" == "hivetomysql" ]
    then
        echo "hivetomysql"
        param="${dt}"
        if [ -f ${comm_path}${exist_file} ];
            then
                rm -f ${comm_path}${exist_file}
        fi
        hdfs dfs -get /dolphinscheduler/bigdata/resources/${folder_name}/${env_type}/${file_name}.${file_type} ${comm_path}${exist_file}
        python /data1/projects-app/ChartSync/datax/bin/apollo.py ${comm_path}${exist_file} ${sync_type} ${table_type}
        python /data1/projects-app/ChartSync/datax/bin/datax.py -p "-Dparam=${param}"  ${comm_path}${exist_file}_new
        if [ $? -eq 0 ] ; then
            echo "export data succeed! "
        else
            echo "export data failed! "
            exit 1
        fi
fi