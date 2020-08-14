[hadoop官网](http://hadoop.apache.org/)  
[scala官网](http://www.scala-lang.org/)  
[spark官网](http://spark.apache.org/)

### zookeeper3.6
```bash
# 每次都要先启动zookeeper,因为hdfs和yarn都依赖zk管理
# 解压安装包并添加到环境变量
[root@cdh1 opt]# tar -xvf zookeeper-3.6.1.tar.gz -C /opt/module
# 添加到环境变量
[root@cdh1 ~]# vim /etc/profile
export ZK_HOME=/opt/module/zookeeper-3.6.1
export PATH=$PATH:$ZK_HOME/bin
# 在data目录下创建myid文件
echo '1' > myid
# 拷贝到其它节点(要先创建/opt/module目录,不然传输的文件都会存放在module目录而不是zookeeper目录)并修改myid
[root@cdh1 module]# scp -r zookeeper-3.6.1/ cdh2:/opt/module
[root@cdh1 module]# scp -r zookeeper-3.6.1/ cdh3:/opt/module
# 启动/停止/状态
[root@cdh1 ~]# zkServer.sh start-foreground/stop/status
# 打开客户端
[root@cdh1 ~]# zkCli.sh -server host:port
# 查看事务日志
[root@cdh1 version-2]# zkTxnLogToolkit.sh log.100000001
# 查看快照文件
[root@cdh1 version-2]# zkSnapShotToolkit.sh snapshot.0
```

```bash
[root@cdh1 conf]# vim zoo.cfg
# The number of milliseconds of each tick
# ZK服务器或客户端与服务器之间维持心跳的时间间隔,每隔tickTime发送一个心跳,以毫秒为单位  
tickTime=2000  
# leader与follower之间初始连接能容忍的最多心跳数(tickTime数量)  
initLimit=10  
# leader与follower之间请求应答能容忍的最多心跳数(tickTime数量) 
syncLimit=5
# 存储快照
dataDir=/opt/module/zookeeper-3.6.1/data
# 存储事务日志
dataLogDir=/opt/module/zookeeper-3.6.1/logs
# the port at which the clients will connect  
clientPort=2181  
# 服务器名称与地址：集群信息(服务器编号,服务器地址,LF通信端口,选举端口)  
server.1=cdh1:2888:3888
server.2=cdh2:2888:3888
server.3=cdh3:2888:3888
```

```bash
# zookeeper是一个分布式应用程序协调服务,zk=文件系统+通知机制
# 分布式系统：利用更多机器处理更多数据,协调就是让各个节点的信息能够同步和共享
# 应用场景
1.统一命名服务
2.统一配置管理
工程中的很多配置信息比如数据库连接一般写在配置文件中,单节点机器没啥问题
分布式集群还是需要一个集中管理配置的地方,可以将配置信息写进znode,相关应用程序监听这个znode,zk依赖ZAB协议可以保证主从数据一致性
Hadoop使用zk做namenode的高可用
Hbase的客户端就是连接zk获取集群配置信息再进行后续操作
Kafka也是用zk维护broker信息
3.统一集群管理
# zk数据结构
数据结构通常是K-V或者树形结构两种,ZK是类似linux的树形结构,每个节点叫znode,可通过其路径唯一标识
znode并不存储大规模业务数据,而是存储不少量状态和配置信息,每个znode默认能存储1M数据,适用于读多写少场景
# zk三个状态
Looking(选举状态): 当前节点不知道谁是leader,正在搜寻
Leading(主节点): 当前节点即选出来的leader
Following(从节点): leader已经选好,当前节点与之同步
# ZAB协议(Zookeeper Atomic Broadcast)
恢复模式(选leader): 当启动服务或leader出现异常时会通过半数机制选举新的leader并同步状态到follower,然后退出恢复模式
广播模式(干活): 保证主从节点数据一致
# zk事务操作
zxid: 当zookeeper服务器状态发生变化时(insert/update/delete znode)会对应一个事务请求,zk会为其分配一个全局的事务id,编号越大说明事务越新
# zk选举机制
全新集群: 比较myid(半数机制)  
非全新集群(有机器中途宕机): 先比较zxid再比较myid 
# znode两种类型
持久的(persistent): 即使zk集群宕机也不会丢失
临时的(ephemeral): 断开连接就会丢失
# znode四种目录节点(默认持久非序列化)  
PERSISTENT  
PERSISTENT_SEQUENTIAL(持久序列化/test0000000019)  
EPHEMERAL  
EPHEMERAL_SEQUENTIAL 
# Watcher
zk允许用户在指定znode注册watcher,当触发特定事件时zk服务端会将事件通知到客户端,以此实现分布式协调服务

# zk实现分布式锁: 当锁的持有者断开时锁会自动释放,zk的临时znode可以实现这个功能
# 在cli1创建临时znode
[zk: localhost:2181(CONNECTED) 0] create -e /lock 'lock'  # -e表示临时,此时cli2无法创建/lock会显示已存在
# 在cli2监控该znode
[zk: localhost:2181(CONNECTED) 0] stat -w /lock  # 当cli1断开连接时/lock自动丢失,此时cli2可以创建/lock

# zk实现master-worker协同: 要求系统中只能有一个master,且master能实时监控worker情况
# 在cli1创建临时znode
[zk: localhost:2181(CONNECTED) 0] create -e /master 'master:8888'
# 在cli1创建持久znode并监控该znode
[zk: localhost:2181(CONNECTED) 0] create /workers && ls -w /workers
# 在cli2的/workers节点下创建临时znode并观察监控变化
[zk: localhost:2181(CONNECTED) 0] create -e /workers/w1 'w1:8888'
```

- zk启动报错
```bash
org.apache.zookeeper.server.quorum.QuorumPeerConfig$ConfigException: Address unresolved: cdh1:3888
原因：3888后面有空格导致无法识别端口号,linux复制文件时要注意空格

Caused by: java.lang.IllegalArgumentException: myid file is missing
原因：data目录下缺少myid文件

Cannot open channel to 3 at election address cdh3/192.168.152.13:3888
原因：有的节点还没启动,已经启动的节点会努力寻找其它节点进行leader选举,正常现象等节点都启动就好了
```

### hadoop2.7
```bash
# 解压安装包
[root@cdh1 opt]# tar -xvf hadoop-2.7.2.tar.gz -C /opt/module
[root@cdh1 opt]# tar -xvf apache-hive-1.2.1-bin.tar.gz -C /opt/module

# bin目录是一些原始命令  hadoop/hdfs/yarn/mapred/run-eample/spark-shell/spark-submit/spark-sql
# sbi目录是一些服务(启动/停止)命令  start/stop

# 添加到环境变量
[root@cdh1 ~]# vim /etc/profile
export HADOOP_HOME=/opt/module/hadoop-2.7.2
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin
export HIVE_HOME=/opt/module/hive-1.2.1
export PATH=$PATH:$HIVE_HOME/bin:$HIVE_HOME/sbin

[root@cdh1 hadoop]# vim hadoop-env.sh
export JAVA_HOME=/usr/java/jdk1.8.0_181-cloudera

[root@cdh1 hadoop]# vim slaves
cdh1
cdh2
cdh3

[root@cdh1 conf]# vim hive-env.sh
export HADOOP_HOME=/opt/module/hadoop-2.7.2
export HIVE_CONF_DIR=/opt/module/hive-1.2.1/conf

# 配置hive元数据到mysql,在hive的conf目录新增hive-site.xml
[root@cdh1 ~]# cp /usr/share/java/mysql-connector-java-5.1.46.jar /opt/module/hive-1.2.1/lib/

# 修改完全部配置文件后拷贝到其它节点
[root@cdh1 module]# scp -r hadoop-2.7.2/ cdh2:/opt/module/
[root@cdh1 module]# scp -r hadoop-2.7.2/ cdh3:/opt/module/
```

- hive-site.xml
```xml
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
	<property>
	  <name>javax.jdo.option.ConnectionURL</name>
	  <value>jdbc:mysql://cdh1:3306/metastore?createDatabaseIfNotExist=true</value>
	  <description>JDBC connect string for a JDBC metastore</description>
	</property>
	<property>
	  <name>javax.jdo.option.ConnectionDriverName</name>
	  <value>com.mysql.jdbc.Driver</value>
	  <description>Driver class name for a JDBC metastore</description>
	</property>
	<property>
	  <name>javax.jdo.option.ConnectionUserName</name>
	  <value>root</value>
	  <description>username to use against metastore database</description>
	</property>
	<property>
	  <name>javax.jdo.option.ConnectionPassword</name>
	  <value>root</value>
	  <description>password to use against metastore database</description>
	</property>
	<property>
      <name>hive.server2.thrift.port</name>
      <value>10000</value>
      <description>HiveServer2 listen port</description>
    </property>
</configuration>
```

- core-site.xml
```xml
<configuration>  
    <!-- 指定hdfs的nameservice为ns1 -->  
    <property>  
        <name>fs.defaultFS</name>  
        <value>hdfs://ns1/</value>  
    </property>  
    <!-- 指定hadoop临时目录 -->  
    <property>  
        <name>hadoop.tmp.dir</name>  
        <value>/opt/module/hadoop-2.7.2/tmp</value>  
    </property>  
    <!-- 指定zookeeper地址 -->  
    <property>  
        <name>ha.zookeeper.quorum</name>  
        <value>cdh1:2181,cdh2:2181,cdh3:2181</value>  
    </property>
    <!-- 文件删除后保留时长(分钟),默认0表示关闭回收站,安全起见还是打开防止误删数据 -->
    <property>  
        <name>fs.trash.interval</name>  
        <value>1440</value>  
    </property>
</configuration> 
``` 

- hdfs-site.xml
```xml
<configuration>  
    <!--指定hdfs的nameservice为ns1,需要和core-site.xml中的保持一致 -->  
    <property>  
        <name>dfs.nameservices</name>  
        <value>ns1</value>  
    </property>  
    <!-- ns1下面有两个NameNode,分别是nn1,nn2 -->  
    <property>  
        <name>dfs.ha.namenodes.ns1</name>  
        <value>nn1,nn2</value>  
    </property>  
    <!-- nn1的RPC通信地址 -->  
    <property>  
        <name>dfs.namenode.rpc-address.ns1.nn1</name>  
        <value>cdh1:9000</value>  
    </property>  
    <!-- nn1的http通信地址 -->  
    <property>  
        <name>dfs.namenode.http-address.ns1.nn1</name>  
        <value>cdh1:50070</value>  
    </property>  
    <!-- nn2的RPC通信地址 -->  
    <property>  
        <name>dfs.namenode.rpc-address.ns1.nn2</name>  
        <value>cdh2:9000</value>  
    </property>  
    <!-- nn2的http通信地址 -->  
    <property>  
        <name>dfs.namenode.http-address.ns1.nn2</name>  
        <value>cdh2:50070</value>  
    </property>  
    <!-- 指定NameNode的元数据在JournalNode上的存放位置 -->  
    <property>  
        <name>dfs.namenode.shared.edits.dir</name>  
        <value>qjournal://cdh1:8485;cdh2:8485;cdh3:8485/ns1</value>  
    </property>  
    <!-- 指定JournalNode在本地磁盘存放数据的位置 -->  
    <property>  
        <name>dfs.journalnode.edits.dir</name>  
        <value>/opt/module/hadoop-2.7.2/journaldata</value>  
    </property>  
    <!-- 开启NameNode失败自动切换 -->  
    <property>  
        <name>dfs.ha.automatic-failover.enabled</name>  
        <value>true</value>  
    </property>  
    <!-- 配置失败自动切换实现方式 -->  
    <property>  
        <name>dfs.client.failover.proxy.provider.ns1</name>
        <value>org.apache.hadoop.hdfs.server.namenode.ha.ConfiguredFailoverProxyProvider</value>
    </property>  
    <!-- 配置隔离机制方法,防止脑裂split-brain-->  
    <property>  
        <name>dfs.ha.fencing.methods</name>  
        <value>  
            sshfence
            shell(/bin/true)  
        </value>  
    </property>  
    <!-- 使用sshfence隔离机制时需要ssh免登陆 -->  
    <property>  
        <name>dfs.ha.fencing.ssh.private-key-files</name>  
        <value>/opt/module/hadoop-2.7.2/.ssh/id_rsa</value>  
    </property>  
    <!-- 配置sshfence隔离机制超时时间 -->  
    <property>  
        <name>dfs.ha.fencing.ssh.connect-timeout</name>  
        <value>30000</value>  
    </property>  
    <!-- 指定hdfs副本数量 -->
    <property>
        <name>dfs.replication</name>
        <value>3</value>
    </property>
</configuration> 
``` 

- mapred-site.xml
```xml
<configuration>  
    <!-- 指定mr框架为yarn方式 -->  
    <property>  
        <name>mapreduce.framework.name</name>  
        <value>yarn</value>  
    </property>  
    <!-- mr历史服务器端地址 -->
    <property>
        <name>mapreduce.jobhistory.address</name>
        <value>cdh1:10020</value>
    </property>
    <!-- mr历史服务器web端地址 -->
    <property>
        <name>mapreduce.jobhistory.webapp.address</name>
        <value>cdh1:19888</value>
    </property>
</configuration>  
```

- yarn-site.xml
```xml
<configuration>  
    <!-- 开启RM高可用 -->  
    <property>  
       <name>yarn.resourcemanager.ha.enabled</name>  
       <value>true</value>  
    </property>  
    <!-- 指定RM的cluster id -->  
    <property>  
       <name>yarn.resourcemanager.cluster-id</name>  
       <value>yrc</value>  
    </property>  
    <!-- 指定RM的名字 -->  
    <property>  
       <name>yarn.resourcemanager.ha.rm-ids</name>  
       <value>rm1,rm2</value>  
    </property>  
    <!-- 分别指定RM的地址 -->  
    <property>  
       <name>yarn.resourcemanager.hostname.rm1</name>  
       <value>cdh1</value>  
    </property>  
    <property>  
       <name>yarn.resourcemanager.hostname.rm2</name>  
       <value>cdh2</value>  
    </property>  
    <!-- 指定zk集群地址 -->  
    <property>  
       <name>yarn.resourcemanager.zk-address</name>  
       <value>cdh1:2181,cdh2:2181,cdh3:2181</value>  
    </property>  
    <!-- Reducer获取数据的方式 -->
    <property>  
       <name>yarn.nodemanager.aux-services</name>  
       <value>mapreduce_shuffle</value>  
    </property>  
    <!-- 使用日志聚集功能 -->
    <property>
        <name>yarn.log-aggregation-enable</name>
        <value>true</value>
    </property>
    <!-- 日志保留时间设置7天 -->
    <property>
        <name>yarn.log-aggregation.retain-seconds</name>
        <value>604800</value>
    </property>
    <!-- spark和mr历史日志路径 -->
    <property>
        <name>yarn.log.server.url</name>
        <value>http://cdh1:19888/jobhistory/logs</value>
    </property>
    
    <!-- 下面两项配置是防止spark运行时内存不足导致报错-->
    <!--是否启动一个线程检查每个任务正使用的物理内存量,如果任务超出分配值则直接将其杀掉,默认true -->
    <property>
        <name>yarn.nodemanager.pmem-check-enabled</name>
        <value>false</value>
    </property>
    <!--是否启动一个线程检查每个任务正使用的虚拟内存量,如果任务超出分配值则直接将其杀掉,默认true -->
    <property>
        <name>yarn.nodemanager.vmem-check-enabled</name>
        <value>false</value>
    </property>
</configuration>  
```  

```bash
# 手动启动集群
# 启动zk
[root@cdh1 ~]# zkServer.sh start
# 格式化namenode
[root@cdh1 ~]# hdfs namenode -format
# 把tmp拷到nn2下面
[root@cdh1 hadoop-2.7.2]# scp -r hadoop-2.7.2/tmp cdh2:/opt/module/hadoop-2.7.2
# 格式化ZKFC
[root@cdh1 ~]# hdfs zkfc -formatZK
# 启动hdfs
[root@cdh1 ~]# start-dfs.sh
# 启动yarn
[root@cdh1 ~]# start-yarn.sh
# cdh2要手动启
[root@cdh2 ~]# yarn-daemon.sh start resourcemanager
# 启动mr历史日志
[root@cdh1 ~]# mr-jobhistory-daemon.sh start historyserver

# 一键启动/停止集群
[root@cdh1 ~]# cd /usr/bin -> vim start-cluster -> chmod +x start-cluster
#!/bin/bash
# 启动zk
for i in cdh1 cdh2 cdh3
do
    echo ==================== ${i} ====================
    # ssh后面的命令是未登录执行,需要先刷新系统环境变量
    ssh ${i} "source /etc/profile && zkServer.sh start"
    echo ${?}
done
# 启动hdfs
start-dfs.sh
# 启动yarn
start-yarn.sh
# cdh2要手动启动
ssh cdh2 "source /etc/profile && yarn-daemon.sh start resourcemanager"
# 开启mr的jobhistory
mr-jobhistory-daemon.sh start historyserver
# 启动spark
/opt/module/spark-2.1.1-bin-hadoop2.7/sbin/start-all.sh
# 开启spark的history-server
/opt/module/spark-2.1.1-bin-hadoop2.7/sbin/start-history-server.sh

# 一键查看进程
[root@cdh1 ~]# cd /usr/bin --> vim jpsall --> chmod +x jpsall
#!/bin/bash
for i in cdh1 cdh2 cdh3
do
    echo ==================== ${i} ====================
    # ssh后面的命令是未登录执行,需要先刷新系统环境变量
    ssh ${i} "source /etc/profile && jps | grep -v Jps"
done
```

```bash
# 集群命令
/opt/cloudera/parcels/CDH/bin目录存放了hadoop/hdfs/yarn/zookeeper等一系列集群命令
# 查看hadoop版本
hadoop version
# 查看hdfs的各节点状态信息
hdfs dfsadmin -report
# 刷新节点
hdfs dfsadmin -refreshNodes
# 查看hdfs是否是安全模式(无法修改和删除数据)
hdfs dfsadmin -safemode
# 获取namenode节点的HA状态
hdfs haadmin -getServiceState nn1
# 切换状态(将nn2变为active)
hdfs haadmin -failover nn1 nn2
# 检测节点健康状况
hdfs haadmin -checkHealth nn1
# 单独启动一个zkfc进程
hadoop-daemon.sh start zkfc

# yarn
# 查看yarn应用列表
yarn application -list
# 杀掉指定yarn应用
yarn application -kill application_id
# 查看yarn应用状态
yarn application -status application_id

# hdfs
# 修改目录权限
hadoop fs -chmod 777 /user
# 查看文件列表以时间倒序排序
hadoop fs -ls -t -r /
# 查看文件内容
hadoop fs -cat <hdfs文件>
# 上传下载
hadoop fs -put <Linux文件> <hdfs路径>
hadoop fs -get <hdfs路径> <Linux文件>
# 创建文件夹(级联)
hadoop fs -mkdir -p <path>  
# 设置/取消该文件夹上传文件数限制
hdfs dfsadmin -setQuota | -clrQuota 3 /test
# 设置/取消该文件夹大小
hdfs dfsadmin -setSpaceQuota | -clrSpaceQuota 1g /test
# 在hdfs上移动文件
hadoop fs -mv /aaa/* /bbb/  
# 删除hdfs文件
hadoop fs -rm /aaa/angela.txt  
# 删除hdfs文件夹
hadoop fs -rm -r /aaa  
# hdfs总空间大小
hadoop fs -df -h /
Filesystem    Size   Used  Available  Use%
hdfs://ns1  93.5 T  66.2 T   20.4 T    71%
# hdfs某个目录大小
hadoop fs -du -s -h /user/hive/warehouse
31.6T  64.7T  /user/hive/warehouse  # 说明是2个副本,小文件也会被当成128m切块大小,所以不是刚刚好2倍关系 
# hdfs某个目录下所有文件大小
hadoop fs -du -h /user/hive/warehouse
5.2 G    12.7 G   /user/hive/warehouse/dm.db
104.5 G  240.2 G  /user/hive/warehouse/dw.db
320.7 G  671.3 G  /user/hive/warehouse/ods.db
# hdfs文件大小排序
hadoop fs -du /user/hive/warehouse/ods.db | awk '{print int($1/1024/1024/1024) "G",int($2/1024/1024/1024) "G",$3}' OFS="  " | sort -nr  
72G  167G  /user/hive/warehouse/ods.db/debit_detail
54G  110G  /user/hive/warehouse/ods.db/urge_record
51G  105G  /user/hive/warehouse/ods.db/pay_repayment_detail
48G  97G  /user/hive/warehouse/ods.db/debit_order
23G  47G  /user/hive/warehouse/ods.db/debit_order_ext

# trash
# 类似linux系统回收站,hdfs会为每个用户创建一个回收站目录/user/当前用户/.Trash/
# hdfs内部实现是在namenode开启一个后台线程Emptier专门管理和监控系统回收站,将超过生命周期的数据删除并释放关联的数据块
# 防止误删数据,删除的文件不会立即清除而是转移到/user/当前用户/.Trash/Current并保留一段时间(fs.trash.interval),所以hdfs磁盘空间不会立即增加
# 手动清空回收站
hadoop fs -expunge  # 会将当前目录/user/用户名/.Trash/current重命名为/user/用户名/.Trash/yyMMddHHmmSS,再次执行就彻底删除了

# web页面监控
http://cdh1:50070    # active
http://cdh2:50070    # standby
http://cdh1:8088     # yarn  
http://cdh1:19888    # job history
```

### spark2.1
```bash
# 解压安装包
[root@cdh1 ~]# tar -xvf spark-2.1.1-bin-hadoop2.7.tgz -C /opt/module
# 添加到环境变量
[root@cdh1 ~]# vim /etc/profile
export SPARK_HOME=/opt/module/spark-2.1.1-bin-hadoop2.7
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

# This file is sourced when running various Spark programs.
[root@cdh1 ~]# vim spark-env.sh
# java环境
JAVA_HOME=/usr/java/jdk1.8.0_181-cloudera
# on yarn模式,只能从hdfs读数据,通过yarn管理资源和任务监控(8088端口)
HADOOP_CONF_DIR=/opt/module/hadoop-2.7.2/etc/hadoop
SPARK_DRIVER_MEMORY=512M
SPARK_EXECUTOR_CORES=1
SPARK_EXECUTOR_INSTANCES=2
SPARK_EXECUTOR_MEMORY=512M
SPARK_HISTORY_OPTS="-Dspark.history.fs.logDirectory=hdfs://cdh1:9000/user/spark/history"

# standalone模式,只能从本地读数据,spark自己管理资源和任务监控(8080端口)
SPARK_MASTER_HOST=cdh1
SPARK_MASTER_PORT=7077
SPARK_WORKER_CORES=1
SPARK_WORKER_INSTANCES=1
SPARK_WORKER_MEMORY=512M
SPARK_DAEMON_JAVA_OPTS="
-Dspark.deploy.recoveryMode=ZOOKEEPER
-Dspark.deploy.zookeeper.url=cdh1,cdh2,cdh3
-Dspark.deploy.zookeeper.dir=/spark"
SPARK_HISTORY_OPTS="-Dspark.history.fs.logDirectory=hdfs://cdh1:9000/user/spark/history"

# Default system properties included when running spark-submit.
[root@cdh1 ~]# vim spark-defaults.conf
spark.eventLog.enabled     true
# 日志目录需提前创建好
spark.eventLog.dir         hdfs://cdh1:9000/user/spark/history

# 拷贝到其它节点
[root@cdh1 opt]# scp -r spark-2.1.1/ cdh2:/opt/module  
[root@cdh1 opt]# scp -r spark-2.1.1/ cdh3:/opt/module

# 一键启动/关闭集群
[root@cdh1 ~]# start-cluster

# 本地测试(日志格式：local-timestamp)
[root@cdh1 ~]# run-example org.apache.spark.examples.streaming.NetworkWordCount localhost 9999
[root@cdh1 ~]# spark-shell
Spark context Web UI available at http://192.168.152.11:4040
Spark context available as 'sc' (master = local[*], app id = local-1594958655022).
Spark session available as 'spark'.
Using Scala version 2.11.8 (Java HotSpot(TM) 64-Bit Server VM, Java 1.8.0_181)
scala> sc
res0: org.apache.spark.SparkContext = org.apache.spark.SparkContext@236f3885
scala> val count = sc.textFile("README.md").filter(line=>line.contains("Spark")).count()
count: Long = 20
scala> spark
res1: org.apache.spark.sql.SparkSession = org.apache.spark.sql.SparkSession@31aa9b01
scala> spark.read.
csv   format   jdbc   json   load   option   options   orc   parquet   schema   table   text   textFile
scala> spark.sql("show databases").show()
+------------+
|databaseName|
+------------+
|     default|
+------------+

# 提交任务到yarn(日志格式：application_timestamp_0001)
[root@cdh1 spark-2.1.1-bin-hadoop2.7]# spark-submit --class org.apache.spark.examples.SparkPi --master yarn --deploy-mode client ./examples/jars/spark-examples_2.11-2.1.1.jar
[root@cdh1 spark-2.1.1-bin-hadoop2.7]# spark-submit --class org.apache.spark.examples.mllib.LinearRegression --master yarn --deploy-mode cluster --jars ./examples/jars/*  hdfs://cdh1:9000/data/sample_linear_regression_data.txt
# 参数解析
--class <main-class>           # application的启动类
--master <master-url>          # master地址,local/yarn
--deploy-mode <deploy-mode>    # 部署模式,client(将driver作为外部客户端本地部署,默认)/cluster(将driver部署到worker节点)
--conf <key>=<value>           # 配置属性
--verbose                      # 输出额外的debug信息
<application-jar>              # 包含application和dependencies的jar包路径
[application-arguments]        # 传给main方法的参数
--driver-memory 512M           # driver可用内存,默认1G
--executor-memory 512M         # executor可用内存,默认1G

# client/cluster对比
1.submit your application from a gateway machine that is physically co-located with your worker machines(e.g. Master node in a standalone EC2 cluster). In this setup, client mode is appropriate, the driver is launched directly within the spark-submit process which acts as a client to the cluster. The input and output of the application is attached to the console. Thus, this mode is especially suitable for applications that involve the REPL (e.g. Spark shell).
2.if your application is submitted from a machine far from the worker machines (e.g. locally on your laptop), it is common to use cluster mode to minimize network latency between the drivers and the executors
In client mode, the driver runs in the client process, and the application master is only used for requesting resources from YARN.
In cluster mode, the driver runs inside an application master process which is managed by YARN on the cluster, and the client can go away after initiating the application. 

# web页面监控
http://cdh1:8080    # master(如果8080端口被占用,MasterUI会尝试8081端口,WorkerUI会顺延到8082端口,可通过spark启动日志查看)
http://cdh1:4040    # spark-shell
http://cdh1:18080   # history server
```

### hue
```bash
# 解决hue10万行下载限制
# 以管理员账号admin登录查看配置信息
Hue Administration - Configuration - beeswax - download_cell_limit(默认100000行*100列=10000000)
[root@master1 ~]# find / -name beeswax
/opt/cloudera/parcels/CDH-5.14.2-1.cdh5.14.2.p0.3/lib/hue/apps/beeswax
/opt/cloudera/parcels/CDH-5.14.2-1.cdh5.14.2.p0.3/lib/hue/apps/beeswax/src/beeswax
/opt/cloudera/parcels/CDH-5.14.2-1.cdh5.14.2.p0.3/lib/hue/apps/beeswax/src/beeswax/static/beeswax
/opt/cloudera/parcels/CDH-5.14.2-1.cdh5.14.2.p0.3/lib/hue/build/static/beeswax
[root@master1 ~]# vim /opt/cloudera/parcels/CDH-5.14.2-1.cdh5.14.2.p0.3/lib/hue/apps/beeswax/src/beeswax/conf.py
DOWNLOAD_CELL_LIMIT = Config(
  key='download_cell_limit',
  default=100000000,
  
# hue查询结果字段带有表名
CM - Hive - 配置 - hiveserver2 - hive-site.xml的HiveServer2高级配置代码段(安全阀) - hive.resultset.use.unique.column.names=false

# hue添加spark查询接口
CM - Hue - 配置 - safe - hue_safety_valve.ini的Hue服务高级配置代码段(安全阀) - 
[desktop]
  app_blacklist=
[notebook]
 show_notebooks=true
 enable_batch_execute=true
 enable_query_builder=true
[[interpreters]]
  [[[hive]]]
    name=Hive
    interface=hiveserver2
  [[[impala]]]
    name=Impala
    interface=hiveserver2
  [[[sparksql]]]
    name=SparkSql
    interface=hiveserver2
  [[[spark]]]
    name=Scala
    interface=livy
  [[[pyspark]]]
    name=PySpark
    interface=livy
  [[[r]]]
    name=R
    interface=livy
  [[[jar]]]
    name=Spark Submit Jar
    interface=livy-batch
  [[[py]]]
    name=Spark Submit Python
    interface=livy-batch
[spark]
  livy_server_host=master1.meihaofenqi.net
  livy_server_port=8998
  livy_server_session_kind=yarn
 
# 安装spark的REST服务livy
# REST是一种服务架构,将web服务视为资源由url唯一标识,明确使用http方法来表示不同操作的调用,get检索/post新增/put修改/delete删除
# REST服务是跨平台的(java/ios/android)且高度可重用,因为它们都依赖基本的http协议
[root@master1 ~]# unzip livy-0.5.0-incubating-bin.zip
# 修改配置
[root@master1 conf]# vim livy-env.sh
export JAVA_HOME=/usr/java/jdk1.8.0_151/
export SPARK_HOME=/opt/cloudera/parcels/CDH/lib/spark
export SPARK_CONF_DIR=/etc/spark/conf
export HADOOP_CONF_DIR=/etc/hadoop/conf
[root@master1 conf]# vim livy.conf
# What host address to start the server on. By default, Livy will bind to all network interfaces.
livy.server.host = master1.meihaofenqi.net
# What port to start the server on.
livy.server.port = 8998
# What spark master Livy sessions should use.
livy.spark.master = yarn
# What spark deploy mode Livy sessions should use.
livy.spark.deploy-mode = cluster
# Enabled to check whether timeout Livy sessions should be stopped.
livy.server.session.timeout-check = true
# Time in milliseconds on how long Livy will wait before timing out an idle session.
livy.server.session.timeout = 1h
# How long a finished session state should be kept in LivyServer for query.
livy.server.session.state-retain.sec = 600s
# 创建存放日志目录
[root@master1 livy]# mkdir logs
# 启动livy-server
[root@master1 bin]# ./livy-server (start/stop/status)
# hue打开Scala报错：The Spark session could not be created in the cluster
# 查看livy日志发现错误：Permission denied: user=root, access=WRITE, inode="/user":hdfs:supergroup:drwxr-xr-x
sudo -u hdfs hadoop fs -chmod 777 /user
# UI监控 http://master1.meihaofenqi.net:8998
```

### mapreduce
```java
public class WordCount {  
    public static class WordCountMapper extends Mapper<LongWritable, Text, Text, IntWritable>{  
        private final static IntWritable one = new IntWritable(1);  
        private Text text = new Text();  
        @Override  
        protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {  
            // 将value(一行数据)转换成string
            String line = value.toString();  
            // 切分
            String[] words = line.split(" ");  
            // 遍历words,输出一个个<word,1>
            for (String word : words) {  
                text.set(word);  
                context.write(text, one);  
            }  
        }  
    }  
    public static class WordCountReducer extends Reducer<Text, IntWritable, Text, IntWritable>{  
        @Override  
        protected void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {  
            int count = 0;  
            for (IntWritable value : values) {  
                count += value.get();  
            }  
            context.write(key, new IntWritable(count));  
        }  
    }  
    public static void main(String[] args) throws Exception {  
        Configuration conf = new Configuration();  
        Job job = Job.getInstance(conf);  
        job.setMapperClass(WordCountMapper.class);  
        job.setReducerClass(WordCountReducer.class);  
        job.setMapOutputKeyClass(Text.class);  
        job.setMapOutputValueClass(IntWritable.class);  
        job.setOutputKeyClass(Text.class);  
        job.setOutputValueClass(IntWritable.class);  
        String input = "hdfs://ubuntu:8020/user/mapreduce/wc.txt";  
        String output = "hdfs://ubuntu:8020/user/mapreduce/output";  
        FileInputFormat.setInputPaths(job, new Path(input));  
        FileOutputFormat.setOutputPath(job, new Path(output));  
        System.exit(job.waitForCompletion(true) ? 0 : 1);  
    }  
}  
```