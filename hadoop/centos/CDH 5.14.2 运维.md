- <font color=red>运行mr涉及join操作时：container is running beyond physical memory limits</font>  
map join：默认情况下,hive会自动将小表加到distribute cache中,然后在map扫描大表的时候,去和distribute cache中的小表做join  
set hive.auto.convert.join=false; -- 关闭自动转化mapjoin,默认为true  
set hive.ignore.mapjoin.hint=false; -- 关闭忽略mapjoin的hints默认为true

- <font color=red>return code 1 from org.apache.hadoop.hive.ql.exec.mr.mapredlocaltask</font>  
local mode：当hive数据量很小时可通过本地模式单节点处理所有任务以减少资源消耗提高效率,数据量很大就必须启用集群模式  
set hive.exec.mode.local.auto=false; -- 关闭本地模式

- <font color=red>hive表解锁</font>  
对hive表执行某个操作时卡死,是因为该表被锁住了  
hive> show locks orders;  -- shared/exclusive 说明该表被锁住了  
hive> unlock table orders;  -- 解锁

- hive分区表某天数据算下来有重复值,可能是因为上游表或者关联表没有加时间分区导致
- hive分区表避免使用current_date作为时间字段,不然回滚历史分区没有数据,可用from_unixtime(unix_timestamp(dt, 'yyyymmdd'),'yyyy-mm-dd')代替
- 夜间批处理调度时间尽量错开,不然连接数超限会导致集群挂掉

- <font color=red>主键冲突：duplicate entry '2017-09-18' for key 'primary'</font>  
mysql表uid字段是主键,而hive表没有主键,所以会有重复数据 "select uid from users where dt='20170918' group by uid having count(1) > 1"

- <font color=red>sqoop往hive抽数据显示数据库不存在</font>  
将hive-site.xml复制到sqoop conf目录下,不然sqoop默认读取内置deby数据库

- sqoop抽数据后ods表和mysql原表字段值对不上,可能是mysql原表新增字段了而ods层表没有这个字段, sqoop这种情况不会报错

- <font color=red>union/join报错</font>  
union：可能是因为各个分段的sql字段数不一样或者某个字段类型不一样  
join：可能是因为"="两边的字段类型不一样

- <font color=red>impala刷新hive(hdfs)数据</font>  
impala-shell -i master2.meihaofenqi.net -q 'invalidate metadata'

- <font color=red>cdh7180端口无法访问(CM界面打不开)</font>  
find / -type f -perm 755 -name 'cloudera*'  
service cloudera-scm-server status  
service cloudera-scm-server restart  
service cloudera-scm-agent status  
service cloudera-scm-agent restart

- <font color=red>cdh集群磁盘扩容后CM界面hdfs/zk/yarn集群启动失败</font>  
解决：因为机器重启后cm服务也要重启,master1节点重启cloudera-scm-server/agent之后,其它节点重启cloudera-scm-agent

- <font color=red>the server is temporarily unable to service your request due to maintenance downtime or capacity problem</font>  
原因：cdh集群master1节点的交换空间满了512Mib/512Mib,导致cloudera挂掉,cm/hive/hue/impala等组件均无法连接使用  
swapon -s 查看交换空间使用情况  
swapoff -a 关闭交换空间  
swapon -a 开启交换空间

- <font color=red>Permission denied: user=yarn, access=EXECUTE, inode="/data":hdfs:supergroup:d-wx------</font>  
原因：yarn用户没有hdfs的/data目录的执行权限  
hadoop fs -chmod -R 755 /data

- <font color=red>master1.meihaofenqi.net: Memory Overcommit Validation Threshold</font>  
示例：主机master1.meihaofenqi.net上的内存被调拨过度,总内存分配额是26.0G,但是RAM只有31.3G(其中6.3G是保留给系统使用的)  
原因：为该节点上的服务分配的总内存大于该节点可用的总内存(其中总内存的20%默认是留给系统使用)  
解决：主机 - 所有主机 - 报警主机 - 资源(检查服务对应实例的内存分配) - 配置(修改memory/heap参数大小) - 重启

- <font color=red>不良: 此角色的事务日志目录所在的文件系统的可用空间小于5.0吉字节 /var/lib/zookeeper(可用4.8吉字节(23.84%),容量20.0吉字节)</font>  
原因：系统盘空间不足  
解决：将/var目录下日积月累的zk/hdfs/hive/mr/yarn等log日志定时删除或者在cdh集群配置更改其保存路径

- cdh界面查看各个组件版本号  
主机 - 所有主机 - 选中主机 - 组件

- <font color=red>org.apache.hadoop.ipc.StandbyException: Operation category READ is not supported in state standby</font>  
原因：主节点是standby状态  
解决：hdfs haadmin -failover nn2 nn1 将nn1切换成active状态

- <font color=red>Initial job has not accepted any resources; check your cluster UI to ensure that workers are registered and have sufficient resources</font>  
原因：内存不足导致spark运行失败  
解决：修改spark-env.sh减小executor默认内存值

- <font color=red>System times on machines may be out of sync. Check system time and time zones.</font>  
原因：集群三台机器时间不同步  
解决：设置系统时间与网络时间同步 - service ntpd stop - ntpdate cn.pool.ntp.org - service ntpd start

- <font color=red>java.io.IOException: Could not locate executable null\bin\winutils.exe in the Hadoop binaries.</font>  
原因：windows缺少hadoop环境  
解决：安装windows版本的hadoop-2.7.2 - Idea - Run - Edit Configurations - Environment variables - 添加HADDOP_HOME 

- 订单表数据抽取：
http://blog.csdn.net/yangtongli2012/article/details/51725408
http://blog.csdn.net/otengyue/article/details/53516028
http://www.cnblogs.com/lcword/p/5508356.html


- 4亿行数据找出前100万大的
其实是topk问题,用ntile分析函数,将数据分成400份,倒序排序取第一份即可

- 同比环比怎么算?
lag(salary, 1, 0) over(partition by employeeno order by yearmonth) as prev_sal -- 环比,与上个月份进行比较 
lag(salary, 12, 0) over(partition by employeeno order by yearmonth) as prev_12_sal -- 同比,与上年度相同月份比较

- 两个数组找出相同元素个数的最优算法？二分查找？冒泡排序？