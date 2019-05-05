/**
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
原子性(atomicity)：事务中的全部操作不可分割,要么全部完成要么均不执行
一致性(consistency)：几个并行执行的事务其执行结果和执行顺序无关
隔离性(isolation)：事务的执行不受其他事务的干扰
持久性(durability)：已提交事务对数据库的改变是一直生效的

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
 */

-- sql:  structed结构化 query查询 language语言
-- 查看当前用户
select user();
-- 查看当前数据库版本
select version();
-- 查看当前所有数据库
show databases;
-- 查看当前选择的数据库
select database();
-- 创建自己的数据库
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

-- 创建表(先选择库)
use java;
create table if not exists emp(
empno int primary key auto_increment,
ename varchar(20),
email varchar(20) unique not null
);
-- 插入数据
insert into emp values(null,'grubby','orc@163.com');
insert into emp values(null,'moon','hum@163.com');
insert into emp values(null,'sky','ud@163.com');

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
-- 删除所有数据
delete from emp;  -- delete：删除数据表还在,可回滚数据
-- 按照一定条件删除
delete from emp where empno = 1;
-- 清空表
truncate table emp;  -- truncate：直接删除原表然后按表结构重新创建,不能回滚数据
-- 开启事务
start transaction;
-- 回滚数据操作
rollback;

-- 分组和过滤
drop table if exists products;
create table if not exists products(
id int primary key,
pname varchar(20),
price double(10,2),
category varchar(20) --  类别
);
insert into products values(1,'电视',900,'电器');
insert into products values(2,'洗衣机',100,'电器');
insert into products values(3,'洗衣粉',90,'日用品');
insert into products values(5,'洗衣粉',90,'日用品');
insert into products values(4,'桔子',9,'水果');

-- 商品归类后,显示每一类商品的总价
select category,sum(price) as totalprice from products group by category;
--  先分组再过滤
select category,sum(price) as totalprice from products group by category having totalprice >100;
--  先过滤再分组(效率高)
select category,sum(price) as totalprice from products where price >100 group by category;
-- where 和 having 条件语句的区别？
-- where 是在分组前进行条件过滤,having 是在分组后进行条件过滤
-- where 不可以接组函数和别名因为where在select之前解析,having 可以使用别名因为having在select之后解析

-- select语句书写的规则: select (distinct) --> from (join) --> where --> group by --> having --> order by --> limit;
-- mysql数据库解析的顺序: from (join) --> where --> group by --> select (distinct) --> having --> order by --> limit;


-- 创建索引(有索引的表更新操作会变慢,因为索引本身也需要更新,一般只在经常被搜索的列/表创建索引)
create index pindex on person (name);       -- 普通索引
create index pindex on person (name desc);  -- 倒叙索引
create index pindex on person (name, age);  -- 组合索引
create unique index pindex on person (name);  -- 唯一索引是指一个索引只能用于一个列
-- 查看执行时间
show profiles;
-- 查看索引
show index from person;
-- 删除索引
alter table person drop index pindex;
-- 添加主键、索引
alter table tbl_name add primary key (column_list);              -- 添加主键(唯一且不为null)
alter table tbl_name add index index_name (column_list);         -- 普通索引
alter table tbl_name add unique index_name (column_list);        -- 唯一索引
alter table tbl_name add fulltext index_name (column_list);      -- 全文索引

-- 创建视图(对于很复杂的查询sql,经常使用的话维护起来很麻烦,可以定义成视图,视图的本质就是对查询的封装,生成一个新的表)
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

-- 查询数据库有多少张表
select table_schema,count(*) as tables from information_schema.tables group by table_schema;
-- 查询表中有多少字段
select count(*) from information_schema.columns where table_schema = '数据库名' and table_name = '表名';
-- 查询数据库中有多少字段
select count(column_name) from information_schema.columns where table_schema = '数据库名';
-- 查询数据库中所有表、字段、类型和注释
select table_name,column_name,data_type,column_comment from information_schema.columns where table_schema = '数据库名';