- [centos7安装mysql5.7](https://juejin.im/post/5d07cf13f265da1bd522cfb6)
## mysql
```sql
e-r模型：当前物理数据库都是按照e-r模型(entry-relationship)进行设计的
        实体-->表  关系-->描述两个表之间关系(一对一、一对多、多对多)
数据库：按照数据结构存储和管理数据的仓库
RDBMS：关系型数据库管理系统
表：按列和行排列的一组数据,列表示特征行表示条目
sql：对数据库做增删改查
三大范式：列不可拆分、唯一标识、引用主键
五大约束：primary key、unique、not null、default、foreign key
逻辑删除：对于重要数据并不希望物理删除,删除后无法恢复,可以设置一个isdelete列,类型为bit,默认值0,要逻辑删除的写1,查询的时候查值为0的即可
数据库引擎：默认myisam适用于全文检索,如果需要支持事务手动指定innodb
修改表的引擎: alter table '表名' engine=innodb;

事务：在对数据库做更新操作(insert/update/delete)时要使用事务
开启: begin;       --其实是在一个内存级的临时表里更新数据,begin之后要么commit要么rollback
提交：commit;      --begin后面的所有操作必须commit后才会生效
回滚：rollback;    --begin后面的所有操作在rollback后都不会生效
事务特性(acid)
原子性(atomicity)：事务中的所有操作不可分割,要么全部完成要么全部取消,如果事务崩溃会回滚到之前状态
一致性(consistency)：几个并行执行的事务其执行结果和执行顺序无关
隔离性(isolation)：事务的执行不受其他事务的干扰
持久性(durability)：已提交事务对数据库的改变是永久生效的

join
inner join: 返回关联表中匹配到的值
left join: 返回左表所有行,右表没有匹配到值为null
right join: 返回右表所有行,左表没有匹配到值为null
full join: 会返回左表和右表的所有行,没有匹配到值为null
union all：会列出所有的值(包括重复值)
union：只会列出不同的值(相当于去重)

主键：唯一标识一条记录,保证数据完整性,唯一非空
外键：另一个表的主键,用于关联操作,一个表可以有多个外键
索引：是一种有序的数据结构,b树存储,根节点保存子节点的指针从而避免全表扫描查询

sql和nosql区别
1.存储方式：sql必须先定义表和字段结构才能添加数据,nosql更加灵活和可扩展
2.表关联：sql可以做join操作,nosql不存在
3.事务：sql支持事务操作,nosql没有事务概念,每个数据集的操作都是原子级的
4.性能：nosql不需要维护复杂的表关系性能更好
```

### install
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

### sql
```sql
-- sql：structured结构化、query查询、language语言
-- 查看当前用户
select user();
-- 查看数据库版本
select version();
-- 查看所有数据库
show databases;
-- 查看当前数据库
select database();
-- 创建数据库
create database java charset=utf8;
-- 显示默认创建的字符集
show create database java;-- create database `java` /*!40100 default character set utf8 */
-- 修改数据库名(不能直接修改,可以先备份再删除原先的)
/**
数据备份
    使用超级管理员权限: sudo -s
    进入mysql库目录: cd /var/lib/mysql
    运行mysqldump命令: mysqldump –uroot –p 要备份的数据库 > ~/desktop/bac.sql;(其实就是在新的文件里create和insert)
数据恢复
    连接mysql,先创建一个新的数据库,然后往这个新数据库里恢复数据
    退出重新连接: mysql -uroot –p 新创建的数据库 < ~/desktop/bac.sql
    */
-- 删除数据库
drop database java;

-- 1.表结构
use java; -- (先选择库)
create table if not exists emp(
    empno int primary key auto_increment,
    ename varchar(20),
    email varchar(20) unique not null
);
-- 插入数据,自增主键给null值
insert into emp values(null,'grubby','orc@163.com');
-- 添加列
alter table emp add column job varchar(20) after ename;
-- 修改字段
--  modify：只能修改属性
alter table emp modify column job varchar(60);
--  change：既可以修改属性也可以修改字段名称
alter table emp change column job job1 varchar(60);
-- 修改字段值
update emp set job = '保洁',email = 'haha@itcast.cn' where empno = 2;
-- 删除列
alter table emp drop column job;
-- 删除所有数据(慎用!)
delete from emp;  -- delete：删除数据表还在,可回滚数据
-- 清空表
truncate table emp;  -- truncate：直接删除原表然后按表结构重新创建,不能回滚数据
-- 开启事务
start transaction;
-- 回滚数据操作
rollback;

-- 2.分组
-- 先分组再过滤
select category,sum(price) as totalprice from products group by category having totalprice >100;
-- 先过滤再分组(效率高)
select category,sum(price) as totalprice from products where price >100 group by category;
-- where和having条件语句区别？
-- where是在分组前进行条件过滤,having是在分组后进行条件过滤
-- where不可以接组函数和别名因为where在select之前解析,having可以使用别名因为having在select之后解析
-- select语句书写规则: select(distinct) --> from(join) --> where --> group by --> having --> order by --> limit
-- mysql数据库解析顺序: from(join) --> where --> group by --> select(distinct) --> having --> order by --> limit

-- 3.高级部分
-- 创建索引(索引也是表结构的一部分所以更新操作会变慢,一般只在经常被搜索的列添加索引)
create index pindex on person (name);         -- 普通索引
create index pindex on person (name desc);    -- 倒叙索引
create index pindex on person (name, age);    -- 组合索引
create unique index pindex on person (name);  -- 唯一索引是指一个索引只能用于一个列
-- 查看执行时间
show profiles;
-- 查看索引
show index from person;
-- 删除索引
alter table person drop index pindex;
-- 创建视图(将复杂的查询sql封装成虚拟表)
-- 视图优点：sql语句重用,简化复杂sql(解耦),定制用户数据,安全(只能读不能写)
create view view_name as select id,name,age from person where sex='男';
-- 查看视图
select * from view_name;
-- 更新视图
create or replace view view_name as select id,name,age from person where sex='男';
-- 删除视图
drop view view_name;

-- 添加关系映射(在一对多的多方添加外键约束)
alter table scores add constraint stu_sco foreign key(stuid) references students(id);
-- 也可以在创建表时直接外键约束
create table scores(
id int primary key auto_increment not null,
stuid int,
subid int,
score decimal(5,2),
foreign key(stuid) references students(id),
foreign key(subid) references subjects(id)
);
-- 此时插入或者修改数据时,如果stuid的值在students表中不存在则会报错
-- 外键的级联操作: 在删除students表的数据时,如果这个id值在scores中已经存在,默认会抛异常
-- 级联操作类型包括：
-- restrict(限制)：默认值,抛异常
-- cascade(级联)：如果主表的记录删掉,则从表中相关联的记录都将被删除
-- set null：将外键设置为空
-- no action：什么都不做
alter table scores add constraint stu_sco foreign key(stuid) references students(id) on delete cascade;

-- 4.mysql监控
-- 查询数据库有多少张表
select table_schema,count(*) as tables from information_schema.tables group by table_schema;
-- 查询表中有多少字段
select count(*) from information_schema.columns where table_schema = '数据库名' and table_name = '表名';
-- 查询数据库中有多少字段
select count(column_name) from information_schema.columns where table_schema = '数据库名';
-- 查询数据库中所有表、字段、类型和注释
select table_name,column_name,data_type,column_comment from information_schema.columns where table_schema = '数据库名';

-- 5.mysql优化
-- 添加索引：主键、外键(关联字段)、where/order by子句、选择性高的字段
-- 尽量避免在where子句中使用null值判断,避免使用!=或<>操作符,会导致放弃索引而做全表扫描
-- 尽量避免在where子句中使用or连接条件,如果一个字段有索引另一个没有就会全表扫描
-- 避免在where子句的"="左边进行函数、计算表达式等等,查询时尽量将操作移到等式右边甚至去掉函数,否则无法使用索引
SELECT * from test where substrb(CardNo,1,4) = '5378';                    -- (13秒)
select * from test where amount/30 < 1000;                                -- (11秒)
select * from test where to_char(ActionTime, 'yyyymmdd') = '20191201';    -- (10秒)
-- 由于where子句对列的任何操作都是在sql运行时逐行计算得到的,因此它不得不全表扫描,而没有使用该列的索引
select * from test where CardNo like '5378%';                             -- (< 1秒)
select * from test where amount < 1000*30;                                -- (< 1秒)
select * from test where ActionTime = to_date('20191201', 'yyyymmdd');    -- (< 1秒)

-- 尽可能早地过滤数据,减少每个阶段的数据量
select * from a join b on a.key = b.key where a.id > 10 and b.id < 10;
-- 应该改写为
select * from (select * from a where id > 10) a join (select * from b where id < 10) b on a.key = b.key;

-- 如果union个数大于2,或者每个union数据太大,应该拆成多个insert into
insert overwrite table t1 partition (dt=20180101) select * from (select * from a union select * from b union select * from c) r;
-- 应该改写为
insert into `table` t1 partition (dt=20180101) select * from a;
insert into `table` t1 partition (dt=20180101) select * from b;
insert into `table` t1 partition (dt=20180101) select * from c;
```