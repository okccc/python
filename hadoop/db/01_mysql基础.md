- [centos7安装mysql5.7](https://juejin.im/post/5d07cf13f265da1bd522cfb6)
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
mysql -u root -p
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
character-set-server=utf8
init-connect='SET NAMES utf8'
validate_password_policy=0
# 开启日志监控
mysql> show variables like 'general%';
mysql> set global general_log='on';
mysql> set global general_log_file='/var/log/mysqld.log';
tail -f /var/log/mysqld.log
# 查看mysql连接数
mysql> show variables like 'max_connections' | select @@max_connections
mysql> show status like 'Thread%';
# 批量插入数据
mysql> source area.sql;
```

## mysql
```sql
/*
e-r模型：当前物理数据库都是按照e-r模型(entry-relationship)进行设计的,关系包括一对一/一对多/多对多
数据库：按照数据结构存储和管理数据的仓库
RDBMS：关系型数据库管理系统
表：按列和行排列的一组数据,列表示特征行表示条目
sql：对数据库做增删改查
三大范式：列不可拆分、唯一标识、引用主键
五大约束：primary key、unique、not null、default、foreign key
逻辑删除：对于重要数据并不希望物理删除,删除后无法恢复,可以设置isdelete列,类型为bit默认值0,要逻辑删除的写1,查询的时候查值为0的即可
*/

-- sql和nosql区别
/*
存储：sql必须先定义表和字段结构才能添加数据,nosql更加灵活和可扩展
关联：sql可以做join操作,nosql不存在
事务：sql支持事务操作,nosql没有事务概念,每个数据集的操作都是原子级的
性能：nosql不需要维护复杂的表关系,性能更好
*/

-- sql：structured query language
-- sql语句分类
DDL(数据定义语言)：create/alter/drop/truncate/rename  -- 针对表
DML(数据操作语言)：insert/delete/update/select        -- 针对数据
DCL(数据控制语言)：commit/rollback/grant/revoke/savepoint

-- 查看当前用户/当前数据库/数据库版本
select user()/database()/version();
-- 查看所有数据库
show databases;
-- 创建数据库
create database java charset=utf8;
-- 选择数据库
use java;
-- 显示默认创建的字符集
show create database java; -- create database `java` /*!40100 default character set utf8 */
-- 修改数据库名(不能直接修改,可以先备份再删除原先的)
/*
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

-- 添加外键约束(在一对多的多方添加)
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
-- 外键的级联操作：在删除students表的数据时,如果这个id值在scores中已经存在会抛异常
-- 级联操作类型包括：
-- restrict(限制)：默认值,抛异常
-- cascade(级联)：如果主表的记录删掉,则从表中相关联的记录都将被删除
-- set null：将外键设置为空
-- no action：什么都不做
-- 删除外键约束
alter table scores drop foreign key stuid;
alter table scores add constraint stu_sco foreign key(stuid) references students(id) on delete cascade;
```

- engine
```sql
-- 查看所有存储引擎
show engines;
-- 查看当前默认存储引擎
mysql> show variables like '%storage_engine%';
+----------------------------------+--------+
| Variable_name                    | Value  |
+----------------------------------+--------+
| default_storage_engine           | InnoDB |
| default_tmp_storage_engine       | InnoDB |
| disabled_storage_engines         |        |
| internal_tmp_disk_storage_engine | InnoDB |
+----------------------------------+--------+
-- 修改表的引擎
alter table test engine=innodb;
-- 存储引擎对比
-- MyISAM：1.不支持事务和外键 2.表级锁,即使操作一条记录也会锁住整个表 3.只缓存索引不缓存数据
-- Innodb(默认)：1.支持事务和外键 2.行级锁,只锁定操作的行,适合高并发操作 3.既缓存索引也缓存数据,对内存要求较高
```

- 事务
```sql
-- 事务就是对表的更新操作(insert/delete/update),使数据从一种状态变换到另一种状态,有acid四大特性
atomicity   -- 原子性：一组事务中的所有操作要么全部成功(commit),要么全部失败(rollback),并且一旦提交就无法回滚
consistency -- 一致性：几个并行执行的事务其执行结果和执行顺序无关
isolation   -- 隔离性：事务的执行不受其他事务的干扰
durability  -- 持久性：已提交的事务对数据库的改变是永久生效的
-- 什么时候会提交数据
a.执行DML操作,默认情况下一旦执行完就会自动提交数据 -> set autocommit = false
b.一旦断开数据库连接,也会提交数据 -> 将获取conn步骤从update方法中剥离出来单独关闭
    
-- 事务隔离：解决脏读、不可重复读、幻读
脏读：读到了别的事务还未提交的数据,这些数据可能会回滚也就是最终不一定存在的数据
可重复读：在一个事务内,最开始读到的数据和事务结束前任意时刻读到的同一批数据是一致的,针对update操作
不可重复读：在一个事务内,不同时刻读到的同一批数据可能不一致,可能会受到别的事务影响,针对update操作
幻读：事务A更新了数据但还未提交,此时事务B插入了与事务A修改之前相同的行数据且提交了,然后在事务A中查询发现刚才的修改好像没起作用,其实是事务B刚插入的,针对insert操作
-- 事务隔离级别：由于事务隔离是通过加锁实现的,所以隔离强度递增性能递减
读未提交：不加锁,性能最好,但是相当于裸奔,连脏读都无法解决(不考虑)
读提交：事务A只能读到事务B已提交的的数据,解决脏读,但是做不到可重复读,也无法解决幻读
可重复读：事务A读不到事务B已提交的数据,事务A开始时数据啥样在事务A提交前都不会变(mysql默认)
串行化：加共享锁,将事务变成顺序执行,相当于单线程,性能最差(不考虑)
-- 查看事务隔离级别
mysql> show variables like 'tx_isolation' | select @@tx_isolation
+-----------------------+-----------------+
| Variable_name         | Value           |
+-----------------------+-----------------+
| transaction_isolation | REPEATABLE-READ |
+-----------------------+-----------------+
-- 修改事务隔离级别,重启生效
mysql> set global transaction isolation level read committed;
-- 查看当前正在运行的事务
mysql> select * from information_schema.innodb_trx;
           脏读    不可重复读    幻读
读未提交    可能    可能         可能
读提交      不可能  可能         可能
可重复读    不可能  不可能        可能
串行化      不可能  不可能       不可能
```

- crud
```sql
-- 创建表5大约束 PRIMARY KEY | UNIQUE | NOT NULL | DEFAULT | FOREIGN KEY 外键是另一个表的主键,用于关联操作,一个表可以有多个外键
create table if not exists `emp` (
`id` int(11) not null auto_increment comment '编号',
`name` varchar(20) not null default '' comment '姓名',
`age` int(11) default null comment '年龄',
`email` varchar(20) default null comment '邮箱',  
`birth` date default null comment '生日',
primary key (`id`),                       -- 主键索引
unique `idx_name` (`name`),               -- 唯一索引
key `idx_age` (`age`),                    -- 单列索引
key `idx_email_birth` (`email`, `birth`)  -- 联合索引
) engine=innodb default charset=utf8 comment='员工表';

-- 删除表
drop table emp;
-- 重命名表
alter table emp rename to emp1;
-- 添加字段
alter table emp add column job varchar(20) after name;
-- 修改字段
-- modify只能修改属性
alter table emp modify column job varchar(60);
-- change既能修改属性也能修改名称
alter table emp change column job job1 varchar(60);
-- 删除字段
alter table emp drop column job1;

-- 插入数据,自增主键给null值
insert into emp values (null, 'grubby', 19, 'orc@163.com', '1990-01-01');
-- 修改字段值
update emp set name='sky',email='hum@123.com' where id = 2;
-- 关闭自动提交事务
set autocommit = false;
-- delete删除数据,在commit之前可以rollback
delete from emp; -- 不加where条件会删除所有数据(慎用!)
-- truncate清空表,相当于自动commit无法rollback
truncate table emp;
-- 回滚数据,只能回滚到最近一次commit后的位置
rollback;
-- 事务一旦提交就不可回滚
commit;

-- 分组过滤
-- where是分组前过滤效率更高,having是分组后过滤
select name, avg(age) age_avg from emp where age > 19 group by name;
-- where不可以接组函数和别名因为where在select之前解析,having可以使用别名因为having在select之后解析
select name, avg(age) age_avg from emp group by name having age_avg > 19;
-- select语句书写规则
select - from - (join) - where - group by - having - order by - limit
-- mysql数据库解析顺序
from - (join) - where - group by - having - select - order by - limit
-- 分页查询
select * from emp limit 0,20;  -- 第一页
select * from emp limit 40,20; -- 第三页
```

- join
```sql
-- a表和b表共有数据
select * from t1 a inner join t2 b on a.id=b.id;
-- a表全集
select * from t1 a left join t2 b on a.id=b.id;
-- b表全集
select * from t1 a right join t2 b on a.id=b.id;
-- a表独有
select * from t1 a left join t2 b on a.id=b.id where b.id is null;
-- b表独有
select * from t1 a right join t2 b on a.id=b.id where a.id is null;
-- a表和b表所有数据
select * from t1 a full join t2 b on a.id=b.id;  -- mysql不支持full join,使用如下方式替代
select * from t1 a left join t2 b on a.id=b.id union select * from t1 a right join t2 b on a.id=b.id;
-- a表独有 + b表独有
select * from t1 a left join t2 b on a.id=b.id where b.id is null union select * from t1 a right join t2 b on a.id=b.id where a.id is null;
-- 笛卡尔积
select * from t1 a join t2 b;

-- left join数据量一定和左表相等吗？
不是的,数据量>=左表,取决于两个表关联的键是一对一还是一对多或者多对多
-- 表关联时on条件和where条件的区别？
如果是inner join效果一样,如果是left join会有区别,数据库表关联时会生成一个临时表,然后将临时表返回给用户
mysql> select * from a left join b on a.id=b.id and a.name='李四' and b.age=18;  -- on是生成临时表时使用的条件,左连接会返回左表所有记录,右表匹配不上就写null
+----+------+------+------+
| id | name | id   | age  |
+----+------+------+------+
|  1 |  张三 | null | null |
|  2 |  李四 |  2   | 18   |
|  3 |  王五 | null | null |
+----+------+------+------+
mysql> select * from a left join b on a.id=b.id where a.name='李四' and b.age=18;  -- where是临时表生成之后再对数据过滤,其实跟left join已经没关系了
+----+------+------+------+
| id | name | id   | age  |
+----+------+------+------+
|  2 |  李四 |  2   | 18   |
+----+------+------+------+
```

- view
```sql
-- 视图：将复杂的查询sql封装成虚拟表
-- 优点：sql语句重用,简化复杂sql(解耦),定制用户数据,安全(read-only)
create view view_name as select * from emp where email is not null;
-- 查看视图
select * from view_name;
-- 更新视图
create or replace view view_name as select * from emp where email is not null;
-- 删除视图
drop view view_name;
```

- explain
```sql
-- 执行计划：可以查看表的读取顺序,索引使用情况,扫描行数等
-- 结合type/key/key_len/rows这些指标判断是否要建索引,如果涉及排序则主要分析Extra指标的Using filesort
mysql> explain select * from emp;
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+-------------+
| id | select_type | table | partitions | type  | possible_keys | key       | key_len | ref  | rows | filtered | Extra       |
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+-------------+
|  1 | SIMPLE      | emp   | NULL       | index | NULL          | idx_a_b_c | 71      | NULL |    1 |   100.00 | Using index |
+----+-------------+-------+------------+-------+---------------+-----------+---------+------+------+----------+-------------+
-- id
id表示查询中执行select子句或操作表的顺序
id相同时执行顺序从上往下,id不同时子查询id序号会递增,id越大执行优先级越高
每个id表示一次独立查询,一个sql的独立查询次数越少越好
-- select_type
select_type表示查询类型,主要用于区别普通查询、关联查询、子查询等
SIMPLE 简单查询, select * from t1 where id=3;
PRIMARY 包含子查询或union的最外层查询, select * from t1 union select * from t2;  -- t1是PRIMARY,t2是UNION
DERIVED from列表中包含的子查询, select * from (select id,count(1) c from t1 group by id) t2 where c>10;  -- t1是DERIVED,t2是PRIMARY
SUBQUERY where列表中包含的第一个子查询, select * from t1 where id in (select id from t2);  -- t1是PRIMARY,t2是SUBQUERY
DEPENDENT SUBQUERY where列表中包含的第一个依赖外部查询的子查询, select * from t1 where exists (select 1 from t2 where t1.id=t2.id);  -- t2是DEPENDENT SUBQUERY 
-- table
table表示查询的表
-- type(重点)
type表示查询类型,system > const > eq_ref > ref > range > index > ALL,一般至少要达到range级别
system 表只有一行记录,不常见
const 通过索引一次就找到了,常见于primary key和unique, select * from t1 where id=1;
eq_ref 唯一性索引扫描,返回匹配的唯一记录,常见于primary key和unique, select * from t1 left join t2 on t1.id=t2.id;
ref 非唯一性索引扫描,返回匹配的所有记录, select * from t1 left join t2 on t1.job=t2.job;
ref_or_null 某个字段既需要指定值也要null值, select * from t1 where t1.name='okc' or t1.name is null;
index_merge 需要多个索引组合使用,常见于or语句, select * from t1 where t1.id=10 or t1.name='okc';
index/unique_subquery 子查询中使用了(唯一)索引, select * from t1 where t1.id in (select t2.id from t2);
range 只检索给定范围的行,key列会显示使用了哪个索引,常见于where语句, select * from t1 where t1.id>10;
index 使用了索引但是没有通过索引进行过滤, select * from t1;
ALL 全表扫描,必须优化
-- possible_keys
possible_keys表示可能用到的索引,某个字段存在索引就会被列出来,但不一定被查询实际使用
-- key(重点)
key表示实际使用的索引
-- key_len(重点)
key_len表示索引中使用的字节数,可以帮助检查是否充分利用了索引
计算规则
1.先看索引列的字段类型+长度, int=4(int占4个字节,最大值2^31 - 1,所以是int(11)) | varchar(20)=20 | char(20)=20  
2.varchar和char要视字符集乘以不同的值(utf-8 * 3 | gbk * 2),varchar是动态字符串要加2个字节,允许为空的字段要加1个字节
-- ref
ref表示索引的哪一列被使用了
-- rows(重点)
rows表示查询时检索的行数,越少越好
-- Extra(针对排序操作,尽量把Using filesort变成Using index)
Using where 表示使用了条件过滤
Using index 表示使用了覆盖索引
Using filesort(重点) 表示排序字段没有通过索引访问,mysql中无法利用索引完成的排序操作称为"文件排序"
Using temporary 表示对查询结果排序或分组时使用了临时表
```

- index
```sql
-- 除了数据以外,数据库还维护着满足特定查找算法的数据结构,以某种方式指向物理数据,从而实现高级查找算法,这种数据结构就是索引
-- 优点：索引是一种排好序的快速查找数据结构,B+树(多路平衡查找树)存储,类似字典目录,可以提高数据检索效率降低IO成本和数据排序成本
-- 缺点：索引本身在insert/update/delete数据时也需要维护,会降低表的更新速度
-- 为什么索引使用B+树？
-- 查询时访问磁盘的次数由树的层数决定,二叉树只能有左右两个子节点而B+树可以有多个子节点,减少树的高度
-- 创建索引
alter table emp add primary key emp (id);      -- 主键索引,设定为主键后数据库会自动创建索引且索引列的值唯一非空
create unique index idx_name on emp (name);    -- 唯一索引,索引列的值必须唯一但允许有空值
create index idx_name on emp (name);           -- 单值索引,索引只包含一个列
create index idx_name_age on emp (name, age);  -- 联合索引,索引包含多个列
create index idx_name on emp (name desc);      -- 倒叙索引
-- 查看索引
show index from emp;
-- 删除索引
drop index idx_name on emp;
-- 查看执行时间
show profiles;
-- 适合建立索引场景
主键 | 频繁查询字段 | 外键(join) | 过滤字段(where) | 分组字段(group) | 排序字段(order),通过索引访问将大大提高排序速度
-- 不适合建立索引场景
表记录数很少(mysql优化器会忽略索引直接全表扫描) | 频繁更新字段
-- 索引失效场景
在索引列上做计算/函数/类型转换等任何操作 price/100 = 3 -> price = 100 * 3 | substr(name,1,3) = 'orc' -> name like 'orc%'
or两边列必须都有索引 | 使用!=或<> | like '..%'可以,like '%..'不行 | is null 可以,is not null 不行

-- 主键索引(聚簇索引)
叶子结点存放整行数据,mysql有且只有一个聚簇索引,通常是主键,没有就唯一键,都没有mysql会创建rowid字段来组织这棵B+树,从而将数据有规律的存储起来,这也是数据库区别于文件系统的地方
-- 非主键索引(二级索引、普通索引)
叶子结点存放主键值,查询时先搜索二级索引树找到主键值,再回到主键索引树搜索整行数据的其它列,该过程叫做回表
-- 覆盖索引
从二级索引就能找到所有查询列,避免回表,减少索引树的搜索次数,explain输出结果Extra=Using index表示使用了覆盖索引
select id,name from emp where name='grubby';  -- create index idx_name on emp (name)
select age from emp where name='grubby';  -- create index idx_name_age on emp (name,age)
-- 最左匹配原则
联合索引的查询是从最左前列开始,并且跳过中间列或使用范围条件(非等值查询)会导致后边的列索引失效,所以尽量将过滤性好的列放前面
create index idx_a_b_c on emp (a,b,c);  -- 联合索引,树上每个节点均同时包含a,b,c字段且a全局有序b局部有序(当a相同时),以此类推
select * from emp where a=3 and b=4 and c=5;  -- Y a,b,c都使用了索引
select * from emp where b=4 and c=5;          -- N 跳过a,后面都断了
select * from emp where a=3 and c=5;          -- Y 只使用了a,跳过b,后面c断了
select * from emp where a=3 and b>4 and c=5;  -- Y 只使用了a,b,联合索引只能保证局部有序,非等值查询的后续字段无法直接通过索引树确定范围,需要回表
-- 索引下推
mysql5.6新特性,将与索引相关的条件判断由mysql服务器向下传递至存储引擎,减少IO次数
主要用来优化联合索引中索引失效的情况,explain输出结果Extra=Using index condition(ICP)表示使用了索引下推
select * from emp where name like '陈%' and age=20;
未开启ICP,存储引擎只会搜索idx_name_age这棵树上的name列,age列需要回表再过滤,如果有10个姓陈的就需要回表10次
开启ICP后,存储引擎在索引内部就过滤了age=20这个条件,减少回表次数,其实就是充分利用索引,尽量在查询出整行数据之前过滤掉无效数据

-- 关联查询优化
left join 左表是主(驱动)表,右表是从(被驱动)表,左连接特点是左表数据全表扫描,关联条件用来确定右表搜索的行,所以尽量将小表放左边
驱动表会全表扫描加索引虽然能用上但扫描行数不变,应当给被驱动表的关联字段建索引,如果是inner join mysql会自动将小表作为驱动表 
select * from a left join b on a.id=b.id;  -- create index idx_id on b (id)
-- 子查询优化
尽量避免使用not in/not exists
select * from a where id not in (select id from b);  -- 改进为 select * from a left join b on a.id=b.id where b.id is null;
-- 排序分组优化
尽量避免Extra出现Using filesort,但是当排序之前有过滤操作时优先给过滤字段加索引
create index idx_a_b_c on emp (a,b,c);    -- 是否出现filesort
select * from emp order by d;             -- Y 排序字段没有索引
select * from emp order by a;             -- Y 排序字段有索引但不是覆盖索引,所以尽量减少select *
select a,b,c from emp order by a,b;       -- N 排序字段有索引且是覆盖索引,很合理
select a,b,c from emp order by a,c;       -- Y 排序字段有索引但跳过了中间列
select a,b,c from emp order by a,b desc;  -- Y 排序字段中同时存在升序(默认)和降序,而索引都是升序的
select a,b,c from emp order by b,a;       -- Y 排序字段顺序和索引顺序不一致,此处mysql优化器也不能调换b和a的位置,会改变排序逻辑
select a,b,c from emp where a<100 order by b;  -- Y 过滤条件是范围查询,但这样是值得的,过滤掉大量数据提升的性能要远远超过使用索引
-- in和exists区别？
主查询和子查询执行顺序不一样
select * from 

-- mysql优化器会改变sql语句中select和where字段的顺序,但是group和order字段的顺序是不能变的,否则业务逻辑就变了
```

- log
```bash
# 慢查询日志
mysql> show variables like 'slow_query_log' | select @@slow_query_log
+---------------------+------------------------------+
| slow_query_log      | OFF                          |
| slow_query_log_file | /var/lib/mysql/cdh1-slow.log |-- 可以监控该文件,将速度慢的sql做相应优化,但是手工查找不方便可借助工具
+---------------------+------------------------------+
mysql> show variables like 'long_query_time' | select @@long_query_time
+-----------------+-----------+
| long_query_time | 10.000000 |
+-----------------+-----------+
mysql> set global slow_query_log = 1;
mysql> set global long_query_time = 5;
[root@cdh1 ~]# vim /etc/my.cnf && systemctl restart mysqld  # 修改配置文件后要重启mysqld服务
[mysqld]
slow_query_log=1
slow_query_log_file=/var/lib/mysql/cdh1-slow.log
long_query_time=5

# mysqldumpslow日志分析工具
-s, --sort  # 排序方式, c 访问次数 | r 返回记录数 | t 查询时间 | l 锁定时间
-t, --top   # 返回前多少条记录
-g, --grep  # 匹配字符串
mysqldumpslow -s c -t 10 /var/lib/mysql/cdh1-slow.log | more                 # 获取访问次数最多的前10条sql,结合more使用防止爆屏
mysqldumpslow -s r -t 10 /var/lib/mysql/cdh1-slow.log | more                 # 获取返回记录最多的前10条sql
mysqldumpslow -s t -t 10 -g "left join" /var/lib/mysql/cdh1-slow.log | more  # 获取耗时最长且包含左连接的前10条sql

# 查询所有用户正在干什么
mysql> show processlist;
+----+------+-----------+------+---------+------+----------+------------------+
| Id | User | Host      | db   | Command | Time | State    | Info             |
+----+------+-----------+------+---------+------+----------+------------------+
| 11 | root | localhost | test | Query   |    0 | starting | show processlist |
+----+------+-----------+------+---------+------+----------+------------------+
# 杀掉进程,重新连接Id会递增
mysql> kill 11;
ERROR 1317 (70100): Query execution was interrupted

# 二进制日志(binlog)
以事件形式记录除select和show以外的所有DDL和DML语句,常用于mysql的主从复制和数据恢复
```

- monitor
```sql
-- 查询数据库有多少张表
select table_schema,count(*) as tables from information_schema.tables group by table_schema;
-- 查询表中有多少字段
select count(*) from information_schema.columns where table_schema = '数据库名' and table_name = '表名';
-- 查询数据库中有多少字段
select count(column_name) from information_schema.columns where table_schema = '数据库名';
-- 查询数据库中所有表、字段、类型和注释
select table_name,column_name,data_type,column_comment from information_schema.columns where table_schema = '数据库名';
```