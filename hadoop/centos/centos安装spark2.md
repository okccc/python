[Scala下载地址](http://www.scala-lang.org/)  
[Spark下载地址](http://spark.apache.org/)
- spark是基于内存的快速、通用、可扩展的大数据计算引擎

## local
- 解压安装包  
tar -xvf spark-2.1.1-bin-hadoop2.7.tgz  
mv spark-2.1.1-bin-hadoop2.7 spark-2.1.1

- run-example  
./bin/run-example org.apache.spark.examples.SparkPi  

## on yarn
- 解压安装包  
tar -xvf spark-2.1.1-bin-hadoop2.7.tgz  
mv spark-2.1.1-bin-hadoop2.7 spark-2.1.1

- 添加到环境变量/etc/profile  
export SPARK_HOME=/home/project/spark-2.1.1  
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

- spark-env.sh  
```bash
# on yarn模式从hdfs上获取数据,local/standalone模式从本地加载数据
YARN_CONF_DIR=/home/project/hadoop-2.7.2/etc/hadoop
# jdk
JAVA_HOME=/home/project/jdk1.8
# master节点地址
SPARK_MASTER_HOST=centos01
SPARK_MASTER_PORT=7077
# 如果使用HA的话添加以下配置
SPARK_DAEMON_JAVA_OPTS="
-Dspark.deploy.recoveryMode=ZOOKEEPER 
-Dspark.deploy.zookeeper.url=centos01,centos02,centos03 
-Dspark.deploy.zookeeper.dir=/spark"
# worker节点核数和实例数
SPARK_WORKER_CORES=1
SPARK_WORKER_INSTANCES=1
# spark-submit提交任务默认是1024m(可根据实际情况调整)
SPARK_WORKER_MEMORY=512m  
SPARK_EXECUTOR_MEMORY=512m
# spark历史日志的web页面端口号18080
# 内存中保存application历史记录上限30个,超过这个值会删除旧的应用
# spark历史日志在hdfs上的位置
SPARK_HISTORY_OPTS="
-Dspark.history.ui.port=18080
-Dspark.history.retainedApplications=30
-Dspark.history.fs.logDirectory=hdfs://centos01:9000/user/spark/history
"
```
- spark-defaults.conf
```bash
# 开启日志
spark.eventLog.enabled     true
# application在运行过程中所有的信息均记录在该路径下
spark.eventLog.dir         hdfs://centos01:9000/user/spark/history   
# 压缩日志为snappy格式
spark.eventLog.compress    true
```

- 拷贝spark到其它节点  
scp -r spark-2.1.1/ centos02:/home/project  
scp -r spark-2.1.1/ centos03:/home/project

- 一键启动zk、hdfs、yarn、spark  
```bash
#!/bin/bash

# 启动zookeeper
for i in centos01 centos02 centos03
do
    # ssh后面的命令是未登录执行,需要先刷新系统环境变量
    ssh $i "source /etc/profile && zkServer.sh start"
done
# 启动hdfs
start-dfs.sh
# 启动yarn
start-yarn.sh
# centos02要手动启动
ssh centos02 "source /etc/profile && yarn-daemon.sh start resourcemanager"
# 开启jobhistory
mr-jobhistory-daemon.sh start historyserver
# 启动spark
/home/project/spark-2.1.1/sbin/start-all.sh
# 开启spark的history-server
/home/project/spark-2.1.1/sbin/start-history-server.sh
```
- spark-shell  
./bin/spark-shell  
scala> val count = sc.textFile("README.md").filter(line=>line.contains("Spark")).count()  
count: Long = 20 

- spark-submit  
./bin/spark-submit \
--class org.apache.spark.examples.mllib.RandomRDDGeneration \
--master yarn \
--deploy-mode cluster \
./examples/jars/spark-examples_2.11-2.1.1.jar  
```angular2html
spark-submit \
--class <main-class>               -- 应用的启动类
--master <master-url> \            -- master地址,local/yarn
--deploy-mode <deploy-mode> \      -- 部署模式,client/cluster
--conf <key>=<value> \             -- spark配置属性
<application-jar> \                -- 打包好的jar包依赖
[application-arguments]            -- 传给main方法的参数
--driver-memory 512M \             -- Driver内存,默认1G
--executor-memory 512M \           -- 每个executor内存,默认1G
```

- web页面监控  
http://centos01:8080 (master)  
http://centos01:4040 (spark-shell)  
http://centos01:18080 (history server)
