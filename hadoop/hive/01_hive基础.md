[参考文档](http://www.cnblogs.com/hpucode/p/5204871.html)  
## basic
- 查看hive版本：hive --version
- 删除库：drop database test cascade(加cascade可以删除含有表的数据库)
- 模糊搜索表：show tables like '*name*'  
- 删除表：drop table table_name  
- 查看表详细信息：desc formatted table_name / show create table table_name    
- 添加新字段：alter table test add columns(order_id int comment '订单id')  
<font color=red>注意：添加新字段后要将原来已经存在的分区先删掉,不然数据加载不进去,如果要调整新字段顺序,可以再用change</font>    
- 修改表字段：alter table test change column column1 column2 string comment '...' first|after column3  
- 删除字段：alter table test replace columns(id int,name string)  
只保留需要的列,不需要的列删掉,同时也可以更换列的顺序(万能版)  
- 删除表分区：  
alter table test drop partition (dt=20160101)  -- 删除单个分区  
alter table test drop partition (dt>=20160101,dt<20170101) -- 删除条件范围内的多个分区  
或者直接去hdfs上删除存储数据的目录(表的分区还在,只是没有数据)  
- 重命名表：alter table table1 rename to table2  
- 复制表结构：create table empty_table1 like table1  
- 查看分区信息：show partitions table_name  
- 查看最小分区：select min(dt) from table_name;
- 查看执行计划：在sql前面加上explain  
- <font color=red>set hive.cli.print.header=true;</font>在输出结果最上面一行打印列名  
- 导出hive数据到本地：hive -e "select * from test;" > /opt/aaa.txt -- (insert overwrite慎用,会覆盖整个目录!)  
- 往mysql插入大量数据：  
load data local infile '/test.txt' replace into table test 	-----覆盖  
load data local infile '/test.txt' into table test          -----追加  
- show functions：查找所有函数  
- desc function extended parse_url：查看某个函数使用案例  
- 视图：create view view01 as select * from debit_ifno where dt=regexp_replace(date_sub(current_date,1),'-','')  
- 注册udf  
将开发的udf打成jar包上传到hdfs指定目录,然后创建函数  
<font color=red>create function default.url_decode as 'com.qbao.udf.decodeurl' using jar '<hdfs:///lib/decodeurl.jar>';</font>  
## load_data
#### <font color=gray>load</font>
- hive> load data <font color=red>[local]</font> inpath '...' <font color=red>[overwrite]</font> into table t1 <font color=red>[partition(...)]</font>      
local表示从linux磁盘复制,否则是从hdfs上剪切;overwrite覆盖/into追加  
#### <font color=gray>insert</font>
- 全量表：hive> insert overwrite/into table t1 select * from t2;
- 分区表：hive> insert overwrite t1 partition(dt=20160412) select ... from t2 where dt=20160412;  
注意：不能用select *,因为分区也是一列,一开始建的是空表没数据,会报错column数量不一致 
#### <font color=gray>as</font>
- hive> create table t2 as select ... from t1 where ...;
#### <font color=gray>hive命令行</font>

| 参数                      | 解释                        |
|:-------------------------|:----------------------------|
|-d,–define <key=value>    |定义变量 -d a=b               |
|-database <databasename>   |指定数据库 默认default         |
|-e <quoted-query-string>   |执行一段sql                   |
|-f <filename>              |执行保存hql语句的文件           |
|-h,–help                  |显示帮助信息                   |
|-h <hostname>              |连接远程hive server           |
|-p <port>                  |连接远程hive server端口号      |
|-hiveconf <property=value> |设置配置参数                   |
|-hivevar <key=value>       |类似define                    |
|-s,–silent                |安静模式 不显示进度只显示结果     |
#### <font color=gray>排序</font>  
- sort by：分区内排序,在每个reduce内部排序
- order by：全局排序,最后会用一个reduce task来完成  
```sql
hive> select * from test;  
5 3 6 2 9 8 1  
hive> select * from test order by id;  
1 2 3 5 6 8 9  
hive> set mapred.reduce.tasks=2;  
hive> select * from test sort by id;  
2 5 6 9 1 3 8  -- 设定了2个reduce,从结果可以看出,在每个reduce内都做了排序,如果reduce数为1,那么两者结果是一样的  
```
## tables
- hive是把除select *以外的sql都翻译成MapReduce程序在yarn集群里跑  
#### <font color=gray>内部表</font>
```sql
create table if not exists dw.inner(  
json string  
)  
comment '内部表'  
row format delimited  
fields terminated by '\t'  
lines terminated by '\n'  
stored as orc tblproperties ("orcompress"="snappy");  
-- orcfile比rcfile在存储结构和存储空间上做了优化
-- 内部表路径默认存放在hdfs的/user/hive/warehouse下,并且还会生成一个tmp目录
```  
#### <font color=gray>外部表</font>  
```sql
create external table if not exists dw.external(
json string  
)  
comment '外部表'  
row format delimited  
fields terminated by '\t'  
lines terminated by '\n'  
stored as orc tblproperties ("orcompress"="snappy")  
location 'hdfs://nameservice1/user/flume/qbao_goods_stuff_log';
-- 外部表路径是自定义的,可以事先在hdfs上创建好
```
#### <font color=gray>分区表</font>  
```sql
create table if not exists base.rec_spu_summary(  
sumary_date         string,  
user_id             int,  
spu_id_list         array<int>  
)  
partitioned by (dt string)  
row format delimited  
fields terminated by '\001'  -- 不同列以'\001'分隔,集合(array,map)元素之间以'\002'分隔,map中key和value以'\003'分隔;  
lines terminated by '\n'  
stored as textfile;  
-- 分区表：创建表的时候可以设置分区(分区表也分内部分区表和外部分区表,如果指定location就是外部分区表)  
```
##### <font color=gray>动态分区</font>
```sql
-- 业务需求：mysql表很大,现在要抽到hive按天分区,保留2016年后的数据,2016年以前的数据都放到20151231这个分区里
-- 解决方法：先将全量数据导入到temp的临时表(不分区),然后使用动态分区插入到ods层的分区表中
-- 注意：动态分区的字段一定位于其他各个字段的最后
set hive.exec.dynamic.partition=true;
set hive.exec.dynamic.partition.mode=nonstrict;       -- 设置允许动态分区 
set hive.optimize.sort.dynamic.partition=true;        -- 设置动态分区排序优化 
set hive.exec.max.dynamic.partitions=10000;            -- 总共的最大动态分区数  
set hive.exec.max.dynamic.partitions.pernode=10000;    -- 每个节点能生成的最大分区数  
insert overwrite table ods.tickets_order partition(dt)
select *,  
       case when create_time >= '2016-01-01' then regexp_replace(substr(create_time,0,10),'-','') else 20151231 end
from temp.tickets_order;
```
#### <font color=gray>mysql表</font>
```sql
create table if not exists app_v40_index_localtion_pvuv_sum (
	stat_date date not null comment '日期',  
	mobile_type varchar (20) not null default '' comment '手机类型',  
	pv int (11) default null,  
	primary key (stat_date)  
) engine = innodb default charset = utf8 comment='呵呵'  
```
## join 
![](images/join.png)  
#### <font color=gray>内连接</font>
```sql  
hive> select * from a join b on(a.id = b.id);  
3   c   1   1   xxx 2  
1   a   3   3   zzz 5  
```
#### <font color=gray>左连接</font>  
```sql
hive> select * from a left join b on(a.id = b.id);  
1   a   3   3   zzz 5  
2   b   4   null    null    null  
3   c   1   1   xxx 2  
```
#### <font color=gray>左半开连接：只显示匹配到的左表数据,比左连接快</font>  
```sql
hive> select * from a left semi join b on(a.id = b.id);  
1   a   3  
3   c   1  
```
#### <font color=gray>右连接</font>  
```sql
hive> select * from a right join b on(a.id = b.id);  
3   c   1   1   xxx 2  
null    null    null    2   yyy 3  
1   a   3   3   zzz 5  
```
#### <font color=gray>全连接</font>
```sql  
hive> select * from a full join b on(a.id = b.id);  
3   c   1   1   xxx 2  
null    null    null    2   yyy 3  
1   a   3   3   zzz 5  
2   b   4   null    null    null  
```
#### <font color=gray>笛卡尔积：m*n</font>  
```sql
hive> select * from a join b;  
1   a   3   1   xxx 2  
2   b   4   1   xxx 2  
3   c   1   1   xxx 2  
1   a   3   2   yyy 3  
2   b   4   2   yyy 3  
3   c   1   2   yyy 3  
1   a   3   3   zzz 5  
2   b   4   3   zzz 5  
3   c   1   3   zzz 5  
```