## mongodb基础
- MongoDB是一个基于分布式文件存储的NoSQL数据库,旨在为web应用提供可扩展的高性能数据存储解决方案  
- 优点：数据结构灵活(类json格式)、高性能(支持mr处理海量数据)、扩展性好  
- 缺点：nosql不支持事务和表关联等操作、占用空间大  
- 安装  
wget http://fastdl.mongodb.org/other/mongodb-other-x86_64-2.2.3.tgz  
tar zxvf mongodb-other-x86_64-2.2.3.tgz  
mkdir -p /data/db/   # mongodb需要自定义数据目录  
- 服务端：mongod  
- 客户端：mongo  
- 查看帮助：mongod –help  
- 启动：sudo service mongod start  
- 停止：sudo service mongod stop  
- 重启：sudo service mongod restart  
- 默认端⼝：27017  
- 查看是否启动成功：ps ajx|grep mongod  
- 配置文件位置：/etc/mongod.conf  
- 日志位置：/var/log/mongodb/mongod.log  
- 数据备份：mongodump -h hostname -d test -o output_path  
- 数据恢复：mongorestore -h hostname -d test --dir input_path  
- 导入数据：/usr/bin/mongoimport -d tencent -c position --file ./position.json(csv)  
## type
- Object ID：文档ID保证唯一性,是一个12字节的十六进制数：当前时间戳(4) + 机器ID(3) + mongodb服务进程id(2) + 增量值(3)  
- String：字符串  
- Boolean：true/false  
- Integer：32/64位整数(取决于服务器)  
- Double：双精度浮点值  
- Arrays：数组/列表  
- Object：嵌入式文档,一个值即一个文档  
- Null：空值 
- Timestamp：时间戳  
- Date：存储当前日期或时间的UNIX格式  

SQL术语|MongoDB术语|说明
 :---: | :---: | :---: 
database|db|数据库
table|collection|表/集合(存储多个文档且结构不固定)
row|document|行/文档
column|field|字段/域
index|index|索引
joins|/|nosql数据库不维护表之间的关系
primary key|primary key|MongoDB自动将_id字段设置为主键
## db  
- db：当前数据库名称  
- show dbs：查看所有数据库  
- use test：切换- 数据库(如果数据库不存在则指向数据库但不创建,直到插入数据或创建集合时数据库才被创建)  
- db.version()：当前数据库版本  
- <font color=red>db.stats()</font>：当前数据库信息  
- db.dropDatabase()：删除当前数据库  
- db._adminCommand("connPoolStats")：当前正在使用的链接  
## collection  
- show collections：查看当前数据库所有集合  
- db.createCollection(name, options)：创建集合  
- db.createCollection("position")  
- db.createCollection("sub", {capped : true, size : 10})  // capped默认false不设置上限,true要指定size,文档达到上限会覆盖之前数据 
- db.集合.drop()：删除集合 
- db.help()：数据库相关帮助命令
- db.集合.help()：集合相关帮助命令 
## crud 
#### <font color=gray>增</font>
- <font color=red>db.集合.insert({})</font>  // insert：_id存在会报错 save：_id存在会更新
- 造数据：for(i=1;i<=100;i++){db.position.insert({name:"test"+i,age:i})}  
#### <font color=gray>删(慎用!)</font>
- <font color=red>db.集合.remove({query}, {justOne:true})</font>  // justOne默认false删除所有,true只删除第一条  
- db.position.remove({gender:0}, {justOne:true})  
- db.position.remove({})  # 清空集合
#### <font color=gray>改</font>
- <font color=red>db.集合.update({query}, {update}, {multi:true})</font>  // query相当于where、update相当于set、multi默认false只更新第一条,true更新所有  
- db.position.update({category:"技术"},{$set:{location:"上海"}},{multi:true})  // 将所有category为"技术"的文档的location改成"上海"
- db.position.update({},{$set:{category:"研发"}},{multi:true})  // 将所有文档的category改成"研发"  
#### <font color=gray>查</font>
- <font color=red>db.集合.find({query})</font>  
- db.集合.findOne({query})  
- db.集合.find({query}).pretty()
- db.集合.find({query}).explain()
## mongodb高级查询
#### <font color=gray>索引</font>
- 查看索引：<font color=red>db.集合.getIndexes()</font>
- 创建单列索引：<font color=red>db.集合.ensureIndex({field:1/-1})</font>  // 1是升序,-1是降序
- 创建多列索引(复合索引)：db.集合.ensureIndex({field1:1/-1,field2:1/-1})
- 创建子文档索引：db.集合.ensureIndex({field.subfield:1/-1})
- 唯一索引：db.集合.ensureIndex({field:-1},{unique:true})
- 删除单个索引：db.集合.dropIndex({field:1/-1})
- 删除所有索引：db.集合.dropIndexes()
#### <font color=gray>比较运算符</font>
- <font color=red>默认=, $lt < | $lte <= | $gt > | $gte >= | $ne !=</font>  
db.position.find({category:"技术"})  // category=技术  
db.position.find({update_time:{$gte:"2019年05月08日"}})  // 更新时间>=20190508  
db.position.find({location:{$ne:null}})  // 地址非空  
#### <font color=gray>逻辑运算符</font> 
- <font color=red>默认$and逻辑与,$or表示逻辑或</font>  
db.position.find({category:"技术",location:"上海"})  // 类别是技术并且地址在上海  
db.position.find({$or:[{category:"技术"},{location:"上海"}]})  // 类别是技术或者地址在上海  
db.position.find({$or:[{category:"技术"},{location:"上海"}],update_time:{$gte:"2019年05月08日"}})  // 类别是技术或者地址在上海,并且更新时间>=20190508
#### <font color=gray>范围运算符</font>
- <font color=red>使用$in和$nin判断是否在某个范围内</font>  
db.position.find({category:{$in:["技术","产品"]}})  // 类别属于技术或产品  
#### <font color=gray>正则表达式</font> 
- <font color=red>使用//或$regex查找</font>  
db.position.find({title:/算法/})  // 标题中包含"算法"  
db.position.find({title:{$regex:'专家$'}})  // 标题以专家结尾  
#### <font color=gray>自定义查询</font>
- db.position.find().limit(4).skip(5)  // limit和skip不分先后  
#### <font color=gray>投影(指定字段查询)</font>  
- <font color=red>db.集合.find({query},{field:1/0})</font>  // 1显示0不显示,_id字段默认显示  
db.position.find({},{category:1,location:1})  // 如果要选取的字段很少就将需要的字段指定为1  
db.position.find({},{_id:0,responsibility:0})  // 如果要选取的字段很多就将不需要的字段设为0  
#### <font color=gray>排序</font>
- <font color=red>db.集合.find().sort({field:1/-1})</font>  # 1升序-1降序  
db.position.find().sort({update_time:-1})    
#### <font color=gray>统计</font>  
- <font color=red>db.集合.find({query}).count() | db.集合.count({query})</font>  
db.position.find({location:"北京"}).count()  
db.position.count({location:"北京"})  
#### <font color=gray>去重</font>
- <font color=red>db.集合.distinct('去重字段',{query})</font>  
db.position.distinct('category')  
db.position.distinct('category',{update_time:{$gte:"2019年05月08日"}})
## mongodb聚合操作
- <font color=red>db.集合.aggregate({管道:{表达式}},{管道:{表达式}}...)</font> 

管道|作用|表达式|作用
:---:|:---:|:---:|:---:
$group|分组|$sum|求和
$match|过滤|$avg|平均值
$project|修改文档结构|$min|最小值
$sort|排序|$max|最大值
$limit|限制条数|$push|往一个数组中插入值
$skip|跳过指定文档条数|$first|排序后第一条文档
$unwind|拆分数组类型字段|$last|排序后最后一条文档
 
#### <font color=gray>$group</font>
- <font color=red>_id:'$field'指定分组字段,_id:null表示不分组</font>  
db.position.aggregate({$group:{_id:'$location', sum:{$sum:1}}})  
db.position.aggregate({$group:{_id:null, min:{$min:'$update_time'},max:{$max:'$update_time'}}}) 
#### <font color=gray>$match</font>
- <font color=red>先过滤数据再分组聚合(前面管道的结果交给下一个管道)</font>  
db.position.aggregate({$match:{update_time:{$gte:"2019年05月08日"}}},{$group:{_id:"$category",sum:{$sum:1}}})  
#### <font color=gray>$project</font>
- 先分组再修改文档结构  
db.position.aggregate({$group:{_id:"$category",sum:{$sum:1}}},{$project:{_id:0,sum:1}})  
#### <font color=gray>$sort</font>
- <font color=red>分组聚合后对结果排序</font>  
db.position.aggregate({$group:{_id:"$category",sum:{$sum:1}}},{$sort:{sum:-1}})
])：查询男/女生人数然后降序排序  
#### <font color=gray>$limit(skip) </font>
- 限制条数  
db.position.aggregate({$group:{_id:"$category",sum:{$sum:1}}},{$sort:{sum:-1}},{$skip:1},{$limit:3}) 
])：先统计男/女生人数,升序排序,取第二条数据  
#### <font color=gray>$unwind</font>
- <font color=red>将数组类型字段拆分成多条文档</font>  
db.position.insert({_id:1,title:["开发","产品","销售"]})  
db.position.aggregate({$match:{_id:1}},{$unwind:'$title'})
