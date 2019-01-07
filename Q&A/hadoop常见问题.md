## hadoop常见问题  
- <font color=red>运行mr涉及join操作时：container is running beyond physical memory limits</font>  
map join：默认情况下,hive会自动将小表加到distributecache中,然后在map扫描大表的时候,去和distributecache中的小表做join  
set hive.auto.convert.join=false; 关闭自动转化mapjoin,默认为true;  
set hive.ignore.mapjoin.hint=false; 关闭忽略mapjoin的hints(不忽略,hints有效),默认为true(忽略hints)
***
- <font color=red>failed: execution error, return code 1 from org.apache.hadoop.hive.ql.exec.mr.mapredlocaltask</font>  
local mode：当hive输入数据量非常小时,可通过本地模式在单台机器上处理所有任务以减少资源消耗提高效率,数据量太大就必须启用集群模式了  
set hive.exec.mode.local.auto=false;
***
- <font color=red>hive表解锁</font>  
对hive表执行某个操作时卡死,是因为该表被锁住了  
hive>show locks tablename;  -->  shared/exclusive   说明该表被锁住了  
hive>unlock table tablename;  -->  解锁
***
- hive表往mysql导数据报错主键冲突：duplicate entry '2017-09-18 00:00:07-1597658' for key 'primary'
因为mysql表create_time和userid字段是主键,而hive表没有主键,所以会有数据重复插入,可以先在hive表里查询重复数据："select create_time,userid from test where dt='20170918' group  by create_time,userid having count(1) > 1"

- hive分区表某天数据算下来有重复值,可能是因为上游表或者关联表没有加时间分区导致

- <font color=red>hive分区表尽量避免使用current_date作为时间字段,不然回滚历史分区会没数据,可用select from_unixtime(unix_timestamp(dt, 'yyyymmdd'),'yyyy-mm-dd')代替</font>  

- 订单表数据抽取：  
http://blog.csdn.net/yangtongli2012/article/details/51725408
http://blog.csdn.net/otengyue/article/details/53516028
http://www.cnblogs.com/lcword/p/5508356.html

- [数据库三范式](http://www.cnblogs.com/linjiqin/archive/2012/04/01/2428695.html)

- sqoop往hive抽数据显示数据库不存在
将hive-site.xml复制到sqoop conf目录下,如果在sqoop的conf目录下找不到hive-site.xml,sqoop默认读取内置deby数据库

- sqoop抽数据后ods表和mysql原表字段值对不上, 可能是mysql原表新增字段了而ods层表没有这个字段, sqoop这种情况不会报错  

- union/join报错
union：可能是因为各个分段的sql字段数不一样或者某个字段类型不一样
join：可能是因为"="两边的字段类型不一样

- 4亿行数据找出前100万大的
其实是topk问题,用ntile分析函数,将数据分成400份,倒序排序取第一份即可

- 从access.log中取出1~2点的数据
代理ip原理？

- 同比环比怎么算?
lag(salary, 1, 0) over(partition by employeeno order by yearmonth) as prev_sal -- 环比,与上个月份进行比较 
lag(salary, 12, 0) over(partition by employeeno order by yearmonth) as prev_12_sal -- 同比,与上年度相同月份比较   

- 两个数组找出相同元素个数的最优算法？二分查找？冒泡排序？  

- impala刷新hive数据  
impala-shell -i master2.meihaofenqi.net -q 'invalidate metadata'

 
