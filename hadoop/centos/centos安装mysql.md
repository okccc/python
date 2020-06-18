- [centos7安装mysql5.7](https://juejin.im/post/5d07cf13f265da1bd522cfb6)
```bash
# 查看现有版本  
rpm -qa | grep -i mysql 
# 删掉一切(没有就跳过)
rpm -ev --nodeps mysql-libs-5.1.71-1.el6.x86_64  
# 下载rpm包  
wget https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm
# 安装rpm包,执行成功后会在/etc/yum.repos.d/目录下生成两个repo文件mysql-community.repo及mysql-community-source.repo
rpm -ivh mysql57-community-release-el7-11.noarch.rpm
# 确认mysql仓库添加成功
[root@cdh1 ~]# yum repolist enabled | grep mysql  
mysql-connectors-community/x86_64       MySQL Connectors Community           153
mysql-tools-community/x86_64            MySQL Tools Community                110
mysql57-community/x86_64                MySQL 5.7 Community Server           424
# 切换mysql版本(如有必要)
[root@cdh1 ~]# vim /etc/yum.repos.d/mysql-community.repo
enabled=1
# 安装mysql服务器及所有依赖(包括mysql-community-client、mysql-community-common、mysql-community-libs)
yum -y install mysql-community-server
# 安装mysql驱动
[root@cdh1 ~]# wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.46.tar.gz
[root@cdh1 ~]# tar -xvf mysql-connector-java-5.1.46.tar.gz
[root@cdh1 ~]# mkdir -p /usr/share/java/
[root@cdh1 ~]# cp mysql-connector-java-5.1.46-bin.jar /usr/share/java/mysql-connector-java.jar
# 启动mysql
systemctl start mysqld && systemctl enable mysqld
# 第一次启动会创建超级管理员账号root@localhost,初始密码存储在日志文件中
grep -i 'temporary password' /var/log/mysqld.log
# 首次登陆先修改密码
mysql -uroot -p
# mysql5.6.6版本后增加了密码强度验证插件validate_password
mysql> show variables like 'validate_password%';
# 降低密码强度验证等级(和hive一样set设置是暂时的只对本次连接有效,修改/etc/my.cnf才能永久生效)
mysql> set global validate_password_policy=0;
# 修改密码(包含数字、字母、特殊字符)
mysql> alter user 'root'@'localhost' identified by 'root@123';
# 允许root远程访问(*.*:db.table  'root':账户名  @:赋权  '%':服务器ip '10.2.35.%'表示10.2.35集群上的节点)
mysql> grant all privileges on *.* to 'root'@'%' identified by 'root@123' with grant option;
# 查看root用户权限
mysql> show grants for 'root'@'%';
# 刷新权限
mysql> flush privileges;
# 查看编码
mysql> show variables like 'character%';
# 修改数据库编码
[root@cdh1 ~]# vim /etc/my.cnf && systemctl restart mysqld  # 修改配置文件后要重启mysqld服务
[mysqld]
character-set-server = utf8
init-connect='SET NAMES utf8'
validate_password_policy=0
# 开启日志监控  
mysql> show variables like 'general%';
mysql> set global general_log='on';
mysql> set global general_log_file='/var/log/mysqld.log';
tail -f /var/log/mysqld.log
# 查看mysql连接数  
mysql> show variables like '%max_connections%';  
mysql> show status like 'Thread%';
# 批量插入数据  
mysql> source area.sql;
```