## hive优化
[参考文档](http://www.cnblogs.com/xd502djj/p/3799432.html)  
***  
#### 如何提高hdfs文件上传效率
1. 文件不要太大(测试用文件从200m到1g不均)，启动多个客户端并行上传文件
2. 考虑减少hive数据副本为2
3. 优化mapreduce及hadoop集群，提高i/o，减少内存使用
***
#### 基本原则
1、尽量尽早地过滤数据，减少每个阶段的数据量
select ... from a  
join b  
on a.key = b.key  
where a.userid>10  
     and b.userid<10  
        and a.dt='20120417'  
        and b.dt='20120417';  
应该改写为：  
select .... from (select .... from a  
                  where dt='201200417'  
                                    and userid>10  
                              ) a  
join ( select .... from b  
       where dt='201200417'  
                     and userid < 10  
     ) b  
on a.key = b.key;  
2、如果union all的部分个数大于2，或者每个union部分数据量大，应该拆成多个insert into 语句  
insert overwite table tablename partition (dt= ....)  
select ..... from (  
                   select ... from a  
                   union all  
                   select ... from b  
                   union all  
                   select ... from c  
                               ) r  
where ...;  
可以改写为：  
insert into table tablename partition (dt= ....)  
select .... from a  
where ...;  
insert into table tablename partition (dt= ....)  
select .... from b  
where ...;  
insert into table tablename partition (dt= ....)  
select .... from c  
where ...;  
3、map join：小表放左边，会被加载到内存，在map端做join操作而不是reduce端，可以省去shuffle过程大量的io操作  
      但是要慎用map join，一般行数<2000行，大小<1m的表(具体看集群配置)建议使用，否则会引起内存的大量消耗  
4、控制map数和reduce数遵循两个原则：使大数据量利用合适的map/reduce数；  
                                                                     使单个map/reduce任务处理合适的数据量；  
控制hive任务map数:  
通常情况下，作业会通过input文件产生一个或多个map任务  
影响因素：输入文件大小，输入文件个数，文件块大小(默认128m, 可在hive中通过set dfs.block.size;查看)；  
举例：  
a)input目录下有1个文件a,大小为780m,那么hadoop会将该文件a分隔成7个块(6个128m的块和1个12m的块)，从而产生7个map数  
b)input目录下有3个文件a,b,c,大小分别为10m，20m，130m，那么hadoop会分隔成4个块(10m,20m,128m,2m),从而产生4个map数  
map数不是越多越好：如果一个任务有很多小文件(<<128m),则每个小文件也会被当做一个块，用一个map任务来完成，而map任务启动和初始化的时间远远大于逻辑处理的时间，就会造成很大的资源浪费，而且，同时可执行的map数也是受限的；  
是不是保证每个map处理接近128m的文件块就行了？  
不一定：比如有一个127m的文件，正常会用一个map去完成，但如果这个文件只有一个或者两个字段，却有几千万的记录，但是map处理的逻辑却很复杂，只用一个map任务做的话就会很耗时；  
综上：要根据实际情况适当减少或增加map数；  
1、减少map数  
假设一个sql任务：  
select count(1) from test where dt=20170101;  
该任务的inputdir  /user/hive/warehouse/test/dt=20170101  
共有194个文件，其中很多是远远小于128m的小文件，总大小9g，正常执行会用194个map任务；  
map总共消耗的计算资源： slots_millis_maps= 623,020  
可以通过以下方法来在map执行前合并小文件，减少map数：  
set mapred.max.split.size=100000000;  
set mapred.min.split.size.per.node=100000000;  
set mapred.min.split.size.per.rack=100000000;  
set hive.input.format=org.apache.hadoop.hive.ql.io.combinehiveinputformat;  
再执行上面的语句，用了74个map任务，map消耗的计算资源：slots_millis_maps= 333,500  
对于这个简单sql任务，执行时间上可能差不多，但节省了一半的计算资源。  
大概解释一下，100000000表示100m,  
set hive.input.format=org.apache.hadoop.hive.ql.io.combinehiveinputformat;     //表示执行前进行小文件合并  
前面三个参数确定合并文件块的大小，>128m按128m切割，100~128m按100m切割，<100m的(包括小文件和分隔大文件剩下的)，进行合并，最终生成了74个块；  
2、增加map数  
当input的文件都很大，任务逻辑复杂，map执行非常慢的时候，可以考虑增加map数，来使得每个map处理的数据量减少，从而提高任务的执行效率；  
假设有这样一个任务：  
select data_desc,  
count(1),  
count(distinct id),  
sum(case when …),  
sum(case when …),  
sum(…)  
from a group by data_desc  
如果表a只有一个文件，大小为120m，但包含几千万的记录，如果用1个map去完成这个任务，肯定是比较耗时的，这种情况下，可以考虑将这一个文件合理的拆分成多个，然后用多个map任务去完成；  
set mapred.reduce.tasks=10;  
create table a1 as  
select * from a  
distribute by rand(123);  
这样会将a表的记录，随机的分散到包含10个文件的a1表中，再用a1代替上面sql中的a表，则会用10个map任务去完成，每个map任务处理大于12m(几百万记录)的数据，效率高很多；  
看上去，貌似这两种有些矛盾，一个是要合并小文件，一个是要把大文件拆成小文件，这正是重点需要关注的地方，  
根据实际情况，控制map数量需要遵循两个原则：使大数据量利用合适的map数；使单个map任务处理合适的数据量；  
控制hive任务reduce数：  
reduce个数的设定极大影响任务执行效率  
影响因素：  
参数1：hive.exec.reducers.bytes.per.reducer(每个reduce处理的数据量，默认1g)  
参数2：hive.exec.reducers.max(每个任务最大的reduce数，默认为999)  
reducer数计算公式：n=min(参数2，总输入数据量/参数1)  
如果reduce端输入(map端输出)总大小小于1g,那么只会有一个reduce任务；  
如：select dt,count(1) from test where dt=20170101 group by dt;  
/user/hive/warehouse/test/dt=20170101 总大小为9g多，因此这句有10个reduce  
适当调整reduce个数：  
1、改变参数1的值  
set hive.exec.reducers.bytes.per.reducer=500000000; (500m)  
select dt,count(1) from test where dt=20170101 group by dt; 这次有20个reduce  
2、设定reduce个数  
set mapred.reduce.tasks = 15;  
select dt,count(1) from test where dt=20170101 group by dt;这次有15个reduce  
reduce数也不是越多越好：同map一样，启动和初始化reduce也会消耗时间和资源；  
另外，有多少个reduce，就会有多少个输出文件，在迭代计算过程中，如果生成了很多个小文件，  
那么这些小文件会作为下一个任务的输入，又会出现小文件过多的问题；  
只有一个reduce的情况：  
a)数据量小于hive.exec.reducers.bytes.per.reducer参数值(1g)  
b)没有group by操作：把select dt,count(1) from test where dt=20170101 group by dt; 写成 select count(1) from test where dt=20170101;  
c)有order by操作：select dt,count(1) from log_record_info where dt>=20170115 group by dt order by dt;该任务会执行2个job，第二个job是order by，只有一个reduce  
d)有笛卡尔积：这些操作都是全局的，所以hadoop不得不用一个reduce去完成；  
<font color=red>5、数据倾斜问题：</font>    
set mapred.reduce.tasks= 200；---  增大reduce个数  
set hive.optimize.skewjoin=true；---  如果是join 过程出现倾斜 应该设置为true  
set hive.groupby.skewindata=true； ---  如果是group by过程出现倾斜 应该设置为true  
set hive.skewjoin.key=100000；---  join的键对应的记录条数超过设定值(具体看集群配置)则会进行分拆  
set hive.groupby.mapaggr.checkinterval=100000；---  groupby的键对应的记录条数超过设定值则会进行分拆  
1、空值导致数据倾斜：  
方案一：  
select * from log a  join users b  on a.user_id is not null  and a.user_id = b.user_id  
union all  
select * from log a where a.user_id is null;  
方案二：  
select *  from log a  left join users b  on case when a.user_id is null then concat(‘hive’,rand() ) else a.user_id = b.user_id;  
方案一是2个job，方案二是1个job且io更少，所以方案二更好  
2、不同数据类型关联导致数据倾斜  
比如 users表user_id是int类型，而logs表user_id有int和string类型，这样join的时候，hash操作默认会按int类型的user_id分配，string类型的记录都会被分配在一个reduce中  
select * from users a  left join logs b  on a.user_id = cast(b.user_id as string) ;  
其它参数设置：  
1、 并发执行  
set hive.exec.parallel=true; 默认为false  
set hive.exec.parallel.thread.number=8; 线程数  
2、数据倾斜(大量key被shuffle到 某一个reduce)  
set hive.groupby.skewindata=true;  
join、group by、count distinct 操作都可能会引起数据倾斜问题  
数据倾斜时负载均衡，当选项设定为true，生成的查询计划会有两个mrjob。第一个mrjob 中，map的输出结果集合会随机分布到reduce中，每个reduce做部分聚合操作，并输出结果，这样处理的结果是相同的groupby key有可能被分发到不同的reduce中，从而达到负载均衡的目的；第二个mrjob再根据预处理的数据结果按照groupby key分布到reduce中(这个过程可以保证相同的groupby key被分布到同一个reduce中)，最后完成最终的聚合操作。  
3、聚合操作  
set hive.map.aggr=true;  
在map中会做部分聚集操作，效率更高但需要更多的内存  
