[参考文档](https://www.cnblogs.com/freeweb/p/5276558.html)
## redis
```bash
# redis是一个高性能的key-value数据库

# redis三大特点  
1.数据完全基于内存所以读写速度极快,每秒约10万条,为防数据丢失会定期往磁盘写数据持久化  
2.支持多种数据类型(字符串、list、set/zset、hash...)  
3.分布式集群

# nosql对比
mongodb：文档存储,类json格式的数据
redis：key-value存储,通过key快速查询value
hbase：列存储,结构化和半结构化数据

# 下载压缩包  
[root@cdh1 ~]# wget http://download.redis.io/releases/redis-4.0.10.tar.gz
# 解压  
[root@cdh1 ~]# tar -xvf redis-4.0.10.tar.gz  
# 切换到redis目录  
[root@cdh1 ~]# cd /usr/local/redis-4.0.10  
# 编译安装  
[root@cdh1 ~]# make && make install  --> 安装完发现/usr/local/bin下多了几个可执行文件
# 修改redis.conf  
daemonize yes  --> 允许redis后台运行  
将bind 127.0.0.1改成bind 192.168.19.11/0.0.0.0  --> 这样其他机器可以通过ip连接该redis,不然只能本地连接  
将requirepass放开并设置登录密码  --> redis-cli -h 192.168.19.11 -p 6379 -a ***  
# 进入redis目录,启动redis服务  
[root@cdh1 ~]# redis-server ./redis.conf
# 修改配置文件时要先redis-cli shutdown关闭redis服务再重启
```


#### db
- flushdb：清空当前数据库  
- flushall：清空所有数据库  
- select 0：选择第一个数据库  
- del key_name：删除键值对  
- <font color=red>keys *</font>：查看所有key
- type key_name：查看key的类型
#### string
- set uname grubby ex 60：设置键值对(ex过期时间)  
- get uname：根据key获取value
- ttl uname：查看生命周期  
#### list  
- <font color=red>llen websites</font>：求list长度  
- lpush websites baidu.com：往列表左边插入值  
- rpush websites google.com：往列表右边插入值  
- <font color=red>lrange websites 0 -1</font>：遍历list  
- lpop websites：从左边删除列表值  
- rpop websites：从右边删除列表值  
- lrem websites 2 qq.com：删除指定值(count>0从上往下删,count<0从下往上删,count=0删除所有)  
- lindex websites 1：根据索引求值  
#### set(无序)  
- <font color=red>scard team1</font>：求set长度  
- sadd team1 kobe：往集合添加元素  
- <font color=red>smembers team1</font>：遍历set  
- srem team1 kobe：删除集合元素  
- sinter team1 team2：求两个集合交集  
- sunion team1 team2：求两个集合并集  
- sdiff team1 team2：求两个集合差集  
#### zset(有序)  
- <font color=red>zcard myzset</font>：求zset长度  
- zadd myzset 10 a 11 b 12 c：往zset添加值和分数,值存在就更新分数,分数可以相同  
- <font color=red>zrange myzset 0 -1</font>：遍历zset不带分数  
- zrange myzset 0 -1 withscores：遍历zset带分数  
#### hash(字典)  
- <font color=red>hlen website</font>：求hash长度  
- hset website baidu baidu.com：往字典存键值对  
- hget website baidu：根据键获取值  
- <font color=red>hgetall website</font>：遍历  
- hkeys website：获取所有键  
- hvals website：获取所有值  
- hdel website baidu：删除指定键值对  
- hexists website baidu：判断键是否存在：0不存在,1存在  
