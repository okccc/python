[参考文档](https://blog.csdn.net/Dog_Lea/article/details/52729726)
- 查看现有版本  
rpm -qa | grep -i mysql 
- 删掉一切  
rpm -ev --nodeps mysql-libs-5.1.71-1.el6.x86_64  
- 下载rpm包  
wget http://repo.mysql.com/mysql-community-release-el6-5.noarch.rpm
- 安装rpm包  
rpm -ivh mysql-community-release-el6-5.noarch.rpm
- 安装mysql服务及其依赖关系   
yum install mysql-server 
- 安装成功后开启mysql服务  
/etc/init.d/mysqld start    其他mysqld用法: /etc/init.d/mysqld {start|stop|status|restart|condrestart|try-restart|reload|force-reload}
- 首次登陆密码为空   
mysql -u root
- 设置密码  
mysql> use mysql;    
mysql> update user set password=Password("你要修改的root密码") where User='root';  
<font color=red>注意：每次操作完user表要刷新权限</font>  
mysql> flush privileges;  
mysql> quit  
- 创建新用户并赋权  
mysql> create user 'hive'@'%' identified by 'hive';  
mysql> grant all privileges on *.* to 'hive'@'%' identified by 'hive' with grant option;  
<font color=red>参数解析：'hive'：账户名   @：赋权 '%'：随便一台机器  '10.2.35.%'：10.2.35集群的某个节点</font>  
mysql> show grants for hive@'10.2.35.%' ;  
mysql> flush privileges;  
mysql> quit;
- 开启日志监控  
mysql> show variables like 'general%';  
mysql> set global general_log='on';  
mysql> set global general_log_file='/var/log/mysqld.log';  
tail -f /var/log/mysqld.log
- 批量插入数据  
mysql> source area.sql;