- [VMware Workstation 15 Pro 破解版](https://www.jianshu.com/p/2d00763a8605)
- [SecureCRT 64位 破解版](https://www.jianshu.com/p/f61a4f1f4405)
- [VMvare安装Centos7](https://zhangweisep.github.io/2019/03/02/VM%E8%99%9A%E6%8B%9F%E6%9C%BA%E5%AE%89%E8%A3%85Centos-7/)
- [cm官方下载地址](https://archive.cloudera.com/cm6/6.2.1/redhat7/yum/RPMS/x86_64/)
- [cdh官方下载地址](https://archive.cloudera.com/cdh6/6.2.1/parcels/)
- [cdh6.2官方安装文档](https://docs.cloudera.com/documentation/enterprise/6/6.2/topics/installation.html)

### CentOs7
```bash
# 安装虚拟机 - 手动分区 - 挂载点/ - 期望容量20GB

# yum安装 -y表示不询问安装 Is this ok [y/d/N]: y
[root@cdh1 ~]# yum -y install vim wget lrzsz
# 修改ip地址  
[root@cdh1 ~]# vim /etc/sysconfig/network-scripts/ifcfg-ens33
BOOTPROTO="static"
ONBOOT="yes"
IPADDR=192.168.189.11
GATEWAY=192.168.189.2  # 编辑 - 虚拟网络编辑器 - NAT设置
NETMASK=255.255.255.0
DNS1=8.8.8.8
[root@cdh1 ~]# service network restart && ifconfig/ip addr && ping www.baidu.com
# 修改主机名
[root@cdh1 ~]# vim /etc/hostname && reboot
# 修改hosts
[root@cdh1 ~]# vim /etc/hosts
192.168.189.11  cdh1
192.168.189.12  cdh2
192.168.189.13  cdh3

# 禁用selinux  
[root@cdh1 ~]# vim /etc/sysconfig/selinux
SELINUX=disabled 
# 防火墙
[root@cdh1 ~]# firewall-cmd --state && systemctl stop firewalld && systemctl disable firewalld
Removed symlink /etc/systemd/system/multi-user.target.wants/firewalld.service.
Removed symlink /etc/systemd/system/dbus-org.fedoraproject.FirewallD1.service.

# 开启ntp服务
[root@cdh1 ~]# yum -y install ntp
[root@cdh1 ~]# vim /etc/ntp.conf
# server 0.centos.pool.ntp.org iburst
# server 1.centos.pool.ntp.org iburst
# server 2.centos.pool.ntp.org iburst
# server 3.centos.pool.ntp.org iburst
# 主节点 | 其它节点
server cn.pool.ntp.org | server cdh1
[root@cdh1 ~]# systemctl start ntpd && systemctl enable ntpd
Created symlink from /etc/systemd/system/multi-user.target.wants/ntpd.service to /usr/lib/systemd/system/ntpd.service

# 开启http服务
[root@cdh1 ~]# yum -y install httpd
[root@cdh1 conf]# vim /etc/httpd/conf/httpd.conf
AddType application/x-gzip .gz .tgz .parcel
[root@cdh1 ~]# systemctl start httpd && systemctl enable httpd
Created symlink from /etc/systemd/system/multi-user.target.wants/httpd.service to /usr/lib/systemd/system/httpd.service

# Cloudera建议将/proc/sys/vm/swappiness设置为最大值10
[root@cdh1 ~]# echo 10 > /proc/sys/vm/swappiness  # 临时生效
[root@cdh1 ~]# vim /etc/sysctl.conf  # 永久生效
vm.swappiness=10

# Cloudera建议禁用大页面压缩
[root@cdh1 ~]# vim /etc/rc.local
echo never > /sys/kernel/mm/transparent_hugepage/defrag
echo never > /sys/kernel/mm/transparent_hugepage/enabled

# 安装jdk
[root@cdh1 ~]# wget https://archive.cloudera.com/cm6/6.2.1/redhat7/yum/RPMS/x86_64/oracle-j2sdk1.8-1.8.0+update181-1.x86_64.rpm
[root@cdh1 ~]# vim /etc/profile
export JAVA_HOME=/usr/java/jdk1.8.0_181-cloudera
export PATH=$PATH:$JAVA_HOME/bin
[root@cdh1 ~]# source /etc/profile && java -version

# 克隆虚拟机,然后配置ssh免密登录
[root@cdh1 ~]# ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/root/.ssh/id_rsa): 
Created directory '/root/.ssh'.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /root/.ssh/id_rsa.
Your public key has been saved in /root/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:/Mn1qHwR9YqRt98GwwI4Rxhyb+pjPGYjM2x7NRVViOs root@cdh1
[root@cdh1 ~]# ssh-copy-id cdh2/cdh3
```

### CM
```bash
# 安装Cloudera-Manager-Server
# 方式一：构建本地仓库源使用yum安装
[root@cdh1 ~]# vim /etc/yum.repos.d/cloudera-manager.repo
[cloudera-manager]
name=Cloudera Manager 6.2.1
baseurl=http://cdh1/cloudera-repos/cm6/6.2.1
gpgcheck=0  # yum安装或升级软件包时是否开启gpg校验 0关闭1开启 
enabled=1   # yum安装或升级软件包时是否将该仓库做为软件包提供源 0禁用1启用
autorefresh=0
type=rpm-md
# 将cloudera-manager.repo复制到cdh2和cdh3
[root@cdh1 ~]# scp -r /etc/yum.repos.d/cloudera-manager.repo cdh2:/etc/yum.repos.d
# 通过http服务构建本地仓库地址
[root@cdh1 ~]# mkdir -p /var/www/html/cloudera-repos/cm6/6.2.1/RPMS/x86_64/
[root@cdh1 ~]# mkdir -p /var/www/html/cloudera-repos/cm6/6.2.1/repodata
# 可以通过浏览器查看本地源 http://192.168.189.11/cloudera-repos/cm6/6.2.1/RPMS/x86_64/
[root@cdh1 6.2.1]# pwd
/var/www/html/cloudera-repos/cm6/6.2.1
[root@cdh1 6.2.1]# ll
总用量 20
-rw-r--r-- 1 root root 14041 9月  17 2019 allkeys.asc
drwxr-xr-x 2 root root  4096 5月  31 14:23 repodata
drwxr-xr-x 3 root root    20 5月  31 14:11 RPMS
# 只在cdh1节点安装,其它节点后续在CM界面里Install Agents,yum会自动解决依赖问题
[root@cdh1 ~]# yum install cloudera-manager-daemons cloudera-manager-agent cloudera-manager-server

# 方式二：使用rpm命令手动安装(推荐)
# 安装依赖(所有节点)
[root@cdh1 opt]# yum -y install bind-utils openssl-devel psmisc cyrus-sasl-plain cyrus-sasl-gssapi portmap /lib/lsb/init-functions httpd mod_ssl python-psycopg2 MySQL-python
# 安装cloudera-manager-daemons(所有节点)
[root@cdh1 opt]# rpm -ivh cloudera-manager-daemons-6.2.1-1426065.el7.x86_64.rpm  # 新增目录/opt/cloudera/cm
# 安装cloudera-manager-server(master节点)
[root@cdh1 opt]# rpm -ivh cloudera-manager-server-6.2.1-1426065.el7.x86_64.rpm  # 新增目录/opt/cloudera/parcel-repo(csd) /etc/cloudera-scm-server /var/log/cloudera-scm-server
Created symlink from /etc/systemd/system/multi-user.target.wants/cloudera-scm-server.service to /usr/lib/systemd/system/cloudera-scm-server.service
# 安装cloudera-manager-agent(所有节点)
[root@cdh1 opt]# rpm -ivh cloudera-manager-agent-6.2.1-1426065.el7.x86_64.rpm  # 新增目录/opt/cloudera/cm-agent /etc/cloudera-scm-agent /var/log/cloudera-scm-agent
Created symlink from /etc/systemd/system/multi-user.target.wants/cloudera-scm-agent.service to /usr/lib/systemd/system/cloudera-scm-agent.service
Created symlink from /etc/systemd/system/multi-user.target.wants/supervisord.service to /usr/lib/systemd/system/supervisord.service

# package包以.rpm结尾,数量多下载不方便
# parcel包以.parcel结尾,相当于压缩包,一个包对应一个系统版本,方便下载
# cloudera推荐使用parcel安装,方便Cloudera Manager自动化部署和滚动升级
# 将CDH Parcel文件和manifest.json上传到 /opt/cloudera/parcel-repo/
# 修改文件所有者
[root@cdh1 parcel-repo]# chown -R cloudera-scm:cloudera-scm /opt/cloudera/parcel-repo/*
[root@cdh1 parcel-repo]# ll -h
总用量 2.0G
-rw-r--r-- 1 cloudera-scm cloudera-scm 2.0G 5月  29 13:12 CDH-6.2.1-1.cdh6.2.1.p0.1425774-el7.parcel
-rw-r--r-- 1 cloudera-scm cloudera-scm   40 12月  4 21:35 CDH-6.2.1-1.cdh6.2.1.p0.1425774-el7.parcel.sha
-rw-r--r-- 1 cloudera-scm cloudera-scm  34K 12月  4 21:37 manifest.json
# CDH会被安装在/opt/cloudera/parcels目录
[root@cdh1 parcels]# ll
总用量 0
lrwxrwxrwx  1 root root  31 5月  31 15:21 CDH -> CDH-6.2.1-1.cdh6.2.1.p0.1425774
drwxr-xr-x 11 root root 119 9月  11 2019 CDH-6.2.1-1.cdh6.2.1.p0.1425774

# 安装mysql,创建cdh各组件的数据库
CREATE DATABASE scm DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
GRANT ALL ON scm.* TO 'scm'@'%' IDENTIFIED BY 'scm@1234';
CREATE DATABASE amon DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
GRANT ALL ON amon.* TO 'amon'@'%' IDENTIFIED BY 'amon@123';
CREATE DATABASE rman DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
GRANT ALL ON rman.* TO 'rman'@'%' IDENTIFIED BY 'rman@123';
CREATE DATABASE hue DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
GRANT ALL ON hue.* TO 'hue'@'%' IDENTIFIED BY 'hue@1234';
CREATE DATABASE metastore DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
GRANT ALL ON metastore.* TO 'metastore'@'%' IDENTIFIED BY 'metastore@123';
CREATE DATABASE sentry DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
GRANT ALL ON sentry.* TO 'sentry'@'%' IDENTIFIED BY 'sentry@123';
CREATE DATABASE nav DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
GRANT ALL ON nav.* TO 'nav'@'%' IDENTIFIED BY 'nav@1234';
CREATE DATABASE navms DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
GRANT ALL ON navms.* TO 'navms'@'%' IDENTIFIED BY 'navms@123';
CREATE DATABASE oozie DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
GRANT ALL ON oozie.* TO 'oozie'@'%' IDENTIFIED BY 'oozie@123';
CREATE DATABASE hive DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
GRANT ALL ON hive.* TO 'hive'@'%' IDENTIFIED BY 'hive@123';
flush privileges;
# 初始化CM数据库,密码是刚才创建的scm用户密码scm@1234
[root@cdh1 ~]# /opt/cloudera/cm/schema/scm_prepare_database.sh mysql scm scm
# 查看CM数据库配置
[root@cdh1 ~]# cat /etc/cloudera-scm-server/db.properties

# 启动CM服务,scm库会生成很多表,/var/log/cloudera-scm-server会生成cloudera-scm-server.log
[root@cdh1 ~]# systemctl start cloudera-scm-server && systemctl enable cloudera-scm-server
[root@cdh1 ~]# tail -f /var/log/cloudera-scm-server/cloudera-scm-server.log  # 时间略久
INFO WebServerImpl:com.cloudera.server.cmf.WebServerImpl: Started Jetty server.  # 说明启动成功

# 访问CM WEB界面 http://192.168.189.11:7180 admin/admin,登录后scm库的USERS表多了admin账号
# Install Agents可能会失败多试几次
# 安装完CDH要将mysql驱动放到hive和oozie的lib目录下不然创建数据库失败,因为hive和oozie使用mysql做metastore
[root@cdh1 ~]# cp /usr/share/java/mysql-connector-java.jar /opt/cloudera/parcels/CDH/lib/hive/lib
[root@cdh1 ~]# cp /usr/share/java/mysql-connector-java.jar /opt/cloudera/parcels/CDH/lib/oozie/lib
# 数据库设置Hive -> JDBC URL
jdbc:mysql://cdh1:3306/hive?createDatabaseIfNotExist=true
# 如果安装失败,卸载CDH环境重新部署
[root@cdh1 ~]# yum -y remove 'cloudera-manager-*' && yum clean all
```

### db
```sql
-- 通过CM安装CDH默认使用内嵌的PostgreSQL数据库
postgres    -- 管理员cloudera-scm    /var/lib/cloudera-scm-server-db/data/generated_password.txt
scm         -- cdh的metastore       /etc/cloudera-scm-server/db.properties
hive        -- hive的metastore          
hue         -- hue的metastore
amon        -- activity monitor     /etc/cloudera-scm-server/db.mgmt.properties
smon        -- service monitor
rmon        -- report monitor
hmon        -- host monitor
nav         -- cloudera navigator

-- 使用管理员账号cloudera-scm登录,不然查询表没有权限
[root@master1 ~]# psql -h 127.0.0.1 -p 7432 -U cloudera-scm -d postgres
Password for user cloudera-scm:9BQ2Ep4fYm
postgres=> \l
                                                List of databases
        Name        |       Owner        | Encoding |  Collate   |   Ctype    |         Access privileges         
--------------------+--------------------+----------+------------+------------+-----------------------------------
 amon               | amon               | UTF8     | en_US.UTF8 | en_US.UTF8 | 
 hive               | hive               | UTF8     | en_US.UTF8 | en_US.UTF8 | 
 hue                | hue                | UTF8     | en_US.UTF8 | en_US.UTF8 | =Tc/hue                          +
                    |                    |          |            |            | hue=CTc/hue
 nav                | nav                | UTF8     | en_US.UTF8 | en_US.UTF8 | 
 navms              | navms              | UTF8     | en_US.UTF8 | en_US.UTF8 | 
 oozie_oozie_server | oozie_oozie_server | UTF8     | en_US.UTF8 | en_US.UTF8 | 
 postgres           | cloudera-scm       | UTF8     | en_US.UTF8 | en_US.UTF8 | 
 rman               | rman               | UTF8     | en_US.UTF8 | en_US.UTF8 | 
 scm                | scm                | UTF8     | en_US.UTF8 | en_US.UTF8 | 
 template0          | cloudera-scm       | UTF8     | en_US.UTF8 | en_US.UTF8 | =c/"cloudera-scm"                +
                    |                    |          |            |            | "cloudera-scm"=CTc/"cloudera-scm"
 template1          | cloudera-scm       | UTF8     | en_US.UTF8 | en_US.UTF8 | =c/"cloudera-scm"                +
                    |                    |          |            |            | "cloudera-scm"=CTc/"cloudera-scm"
(11 rows)
postgres=> 

-- 常用指令
\q                -- 退出psql客户端
\l                -- 列出所有的数据库
\c database_name  -- 连接到指定的数据库
\d                -- 列出当前数据库下所有表
\d table_name     -- 显示指定表的结构信息
\?                -- 列出所有sql的命令列表
\h sql            -- 查看sql命令的解释,比如\h select 

-- hive库下表名都是大写,查询时要加""不然报错
hive=# select * from "DBS";
-- 做crud操作时,字符串只能用'',""会被认为是column,添加新用户后要通过admin激活
hue=# update auth_user set password=md5('admin@123') where username='admin';
```

### cdh运维
```bash
# CDH安装成功后,hadoop/hdfs/hive/impala/java/mapred/spark/sqoop/yarn/zookeeper等组件的命令在/etc/alternatives目录
# 在CM界面重启yarn后,8088页面的applications也会清零
```
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

- <font color=red>升级python3后执行impala-shell报错</font>  
原因：impala-shell.py是python2写的,还得用python2调用  
解决：vim impala-shell -> 将最后一行的exec python ${SHELL_HOME}/impala_shell.py "$@"改成python2

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
解决：安装windows版本的hadoop-2.7.2 - Idea - Run - Edit Configurations - Environment variables - 添加HADOOP_HOME=C:\hadoop-2.7.2

- <font color=red>执行hql报错 FAILED: ParseException line 321:8 character ' ' not supported here</font>  
原因：windows的UTF-8 BOM格式会带有一些隐藏的特殊符号,切换成以ANSI格式编码就能看到有些空格是特殊字符,导致在linux环境下乱码  
解决：notepad++ - 格式 - 以UTF-8无BOM格式编码  
保护色：设置 - 语言格式设置 - 背景色 - more colors - 80/97/205

- <font color=red>Display all 478 possibilities? (y or n)</font>  
原因：windows系统中的tab键在linux里无法识别,要替换成空格