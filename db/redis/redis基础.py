# coding=utf-8
"""
NoSQL(Not Only SQL): 非关系型数据库
随着访问量的上升,网站的数据库性能出现了问题,于是nosql被设计出来,nosql不需要维护复杂的数据关系
常用nosql：
hbase：列存储,结构化和半结构化数据
mongodb：文档存储,类json格式的数据
redis：k-v存储,可以通过key快速查询value

redis三大特点：
1、Redis数据库完全存在于内存中,使用磁盘仅用于持久化,所以读写速度极快,每秒约10万左右集合或者记录
2、Redis数据类型非常丰富(字符串、list、set、hash...)
3、Redis有良好的集群支持,可以将数据复制到任意数量的从服务器

flushdb  删除当前数据库
flushall  删除所有数据库
select 0  选择第一个数据库
del key_name  删除键值对

-- 字符串操作
192.168.19.11:6379> set uname grubby ex 60  --> ex设置过期时间
OK
192.168.19.11:6379> get uname
"grubby"
192.168.19.11:6379> ttl uname
(integer) 53

-- list操作
192.168.19.11:6379> lpush websites baidu.com  --> 往列表左边插入值
(integer) 1
192.168.19.11:6379> rpush websites google.com  --> 往列表右边插入值
(integer) 2
192.168.19.11:6379> lrange websites 0 -1  --> 遍历list
1) "baidu.com"
2) "google.com"
192.168.19.11:6379> lpop websites  --> 从左边删除列表值
"baidu.com"
192.168.19.11:6379> rpop websites  --> 从右边删除列表值
"google.com"
192.168.19.11:6379> lrem websites 2 qq.com  --> 删除指定值：count>0表示从上往下删除指定个数
(integer) 2
192.168.19.11:6379> lrem websites -2 qq.com  --> 删除指定值：count<0表示从下往上删除指定个数
(integer) 2
192.168.19.11:6379> lrem websites 0 qq.com  --> 删除指定值：count=0表示删除所有指定值
(integer) 2
192.168.19.11:6379> lindex websites 1  --> 根据索引求值
"google.com"
192.168.19.11:6379> llen websites   --> 求列表长度
(integer) 2

-- set操作(去重,无序)
192.168.19.11:6379> sadd team1 kobe  --> 往集合添加元素
(integer) 1
192.168.19.11:6379> sadd team1 james
(integer) 1
192.168.19.11:6379> smembers team1  --> 遍历set
1) "james"
2) "kobe"
192.168.19.11:6379> scard team1  --> set长度
(integer) 2
192.168.19.11:6379> srem team1 kobe  --> 删除集合元素
(integer) 1
192.168.19.11:6379> smembers team1
1) "james"
192.168.19.11:6379> sadd team1 kobe
(integer) 1
192.168.19.11:6379> sadd team2 wade
(integer) 1
192.168.19.11:6379> sadd team2 james
(integer) 1
192.168.19.11:6379> smembers team2
1) "wade"
2) "james"
192.168.19.11:6379> sinter team1 team2  --> 求两个集合交集
1) "james"
192.168.19.11:6379> sunion team1 team2  --> 求两个集合并集
1) "wade"
2) "james"
3) "kobe"
192.168.19.11:6379> sdiff team1 team2  --> 求两个集合差集
1) "kobe"
192.168.19.11:6379> sdiff team2 team1
1) "wade"

-- zset操作(去重,有序)
192.168.19.11:6379> zadd myzset 10 a 11 b 12 c  --> 往zset添加值和分数,值存在就更新分数,分数可以相同
(integer) 3
192.168.19.11:6379> zadd myzset 10 a 15 b 20 d
(integer) 1
192.168.19.11:6379> zcard myzset  --> zset长度
(integer) 4
192.168.19.11:6379> zrange myzset 0 -1  --> 遍历zset不带分数
1) "a"
2) "c"
3) "b"
4) "d"
192.168.19.11:6379> zrange myzset 0 -1 withscores  --> 遍历zset带分数
1) "a"
2) "10"
3) "c"
4) "12"
5) "b"
6) "15"
7) "d"
8) "20"

-- hash操作(字典)
192.168.19.11:6379> hset website baidu www.baidu.com  -- 往字典存键值对
(integer) 1
192.168.19.11:6379> hset website google www.google.com
(integer) 1
192.168.19.11:6379> hget website baidu  -- 根据键获取值
"www.baidu.com"
192.168.19.11:6379> hgetall website  -- 获取所有键值对
1) "baidu"
2) "www.baidu.com"
3) "google"
4) "www.google.com"
192.168.19.11:6379> hkeys website  -- 获取所有键
1) "baidu"
2) "google"
192.168.19.11:6379> hvals website  -- 获取所有值
1) "www.baidu.com"
2) "www.google.com"
192.168.19.11:6379> hdel website baidu  -- 删除指定键值对
(integer) 1
192.168.19.11:6379> hgetall website
1) "google"
2) "www.google.com"
192.168.19.11:6379> hexists website baidu  -- 判断键是否存在：0不存在,1存在
(integer) 0
192.168.19.11:6379> hexists website google
(integer) 1
192.168.19.11:6379> hlen website  -- 求字典长度
(integer) 1

-- type查看key的类型
192.168.19.11:6379> keys *
1) "websites"
2) "team1"
3) "website"
192.168.19.11:6379> type team1
set
192.168.19.11:6379> type website
hash
192.168.19.11:6379> type websites
list
"""
