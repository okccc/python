## mysql常见问题
***
- "data truncated for column"错误
一、添加字符长度（varchar改成text）
二、更改字符类型为utf8（已经是utf8）
最后终于发现mysql还有一种字段类型为longtext，原来我插入的字符串太长了，连text都接受不了，要设置为longtext.
***
- navicat中文乱码：
右键数据库→连接属性→高级，将编码选为自动即可！
***
- connection to mysql failed. [hy000][1130] null,  message from server: "host '192.168.19.1' is not allowed to connect to this mysql server"
mysql>grant all on *.* to 'root'@'%'  identified by 'root' with grant option;
参数解析：'root'：账户名       @：赋权        '%'：随便一台机器        '10.2.35.%'：10.2.35集群的某个节点
mysql>show grants for root@'10.2.35.%' ;    可查看账号权限
***
- [err] 1396 - operation create user failed for 'test'@'%'
该用户已存在或者曾经存在被删除后没有刷新权限导致,可以flush privileges或者drop user test
***
- error 1045 (28000): access denied for user 'hive'@'localhost' (using password: yes)
mysql有个用户名为空的账户,mysql会先匹配它,导致root以外的账户匹配不上,删掉它即可
delete from user where user='' and host='localhost';
flush privileges;
