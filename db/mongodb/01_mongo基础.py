# coding=utf-8
"""
MongoDB是一个基于分布式文件存储的NoSQL数据库
优点：可以存储不同结构的文档数据(json格式)、支持mapreduce处理海量数据性能优越
缺点：nosql不支持事务和表关联等操作、占用空间大

SQL术语	        MongoDB术语	    解释说明
database	    db       	    数据库
table	        collection	    数据库表/集合(储存多个文档且结构不固定)
row	            document	    数据记录行/文档(json格式)
column	        field	        数据字段/域
index	        index	        索引
table joins	    // (nosql数据库不维护表之间的关系)
primary key	    primary key(MongoDB自动将_id字段设置为主键)

安装mongodb:
wget http://fastdl.mongodb.org/other/mongodb-other-x86_64-2.2.3.tgz
tar zxvf mongodb-other-x86_64-2.2.3.tgz
mkdir -p /data/db/   # mongodb需要自定义数据目录
服务端：mongod
客户端：mongo

数据库操作：
db：查看当前数据库名称
db.stats()：查看当前数据库信息
show dbs：查看所有数据库
use test：切换数据库(如果数据库不存在则指向数据库但不创建,直到插入数据或创建集合时数据库才被创建)
db.dropDatabase()：删除当前数据库

集合操作：
show collections：查看当前数据库所有集合
db.createCollection(name, options)：创建集合
    --name：集合名称
    --options：指定集合配置的文档
db.createCollection("stu")
db.createCollection("sub", {capped : true, size : 10})
    --capped：默认false表示不设置上限
    --size：当capped为true时要指定size大小;当文档达到上限时会将之前的数据覆盖,单位为字节
db.集合名称.drop()：删除集合

数据类型：
Object ID：文档ID
-- 每个文档都有一个_id属性保证其唯一性,也可以自己设置_id插入文档
-- objectID是一个12字节的十六进制数：当前时间戳(4) + 机器ID(3) + 服务进程id(2) + 增量值(3)
String：字符串
Boolean：true/false
Integer：32/64位整数(取决于服务器)
Double：浮点值
Arrays：数组/列表
Object：用于嵌入式的文档,即一个值为一个文档
Null：存储Null值
Timestamp：时间戳
Date：存储当前日期或时间的UNIX格式

文档操作：
1、db.集合名称.insert(document)：插入
db.stu.insert({name:'gj',gender:1})：如果不指定_id参数,MongoDB会为文档分配一个唯一的ObjectId
2、db.集合名称.update(
   <query>,  # 类似sql语句update中where部分
   <update>,  # 类似sql语句update中set部分
   {multi: <boolean>}  # 默认false只更新满足条件的第一个文档,true全部更新
)：更新
db.stu.update({name:'hr'},{name:'mnc'})  -- 全文档更新
db.stu.insert({name:'hr',gender:0})
db.stu.update({name:'hr'},{$set:{name:'hys'}})  -- 通过操作符$set指定属性更新
db.stu.update({},{$set:{gender:0}},{multi:true})  -- 修改多条匹配到的数据
3、db.集合名称.save(document)：保存  -- 如果文档的_id存在则修改,不存在则添加
db.stu.save({_id:'20160102','name':'yk',gender:1})
4、db.集合名称.remove(
   <query>,  # 删除文档的条件
   {
     justOne: <boolean>  # 默认false删除多条,true只删除匹配到的第一条
   }
)：删除
db.stu.remove({gender:0},{justOne:true})
db.stu.remove({})  -- 全部删除

数据查询：
db.集合名称.find({条件文档})：查询全部
db.集合名称.findOne({条件文档})：查询返回第一个
db.集合名称.find({条件文档}).pretty()：格式化查询结果

比较运算符：
默认是等于判断, $lt < ; $lte <= ; $gt > ; $gte >= ; $ne !=
db.stu.find({name:'gj'})：查询名字=gj的
db.stu.find({age:{$gte:18}})：查询年龄>=18的

逻辑运算符：
默认是逻辑与; $or 表示逻辑或
db.stu.find({age:{$gte:18},gender:1})：查询年龄>=18且性别=1的
db.stu.find({$or:[{age:{$gt:18}},{gender:1}]})：查询年龄>=18或性别=1的
db.stu.find({$or:[{age:{$gte:18}},{gender:1}],name:'gj'})：查询年龄>=18或性别=1且名字=gj的

范围运算符：
使用"$in"和"$nin"判断是否在某个范围内
db.stu.find({age:{$in:[18,28]}})：查询年龄为18/28的

支持正则表达式：
使用//或$regex编写正则表达式
db.stu.find({name:/^黄/})
db.stu.find({name:{$regex:'^黄'}})：查询姓黄的

自定义查询：
使用$where后面写一个函数返回满足条件的数据
db.stu.find({$where:function(){return this.age>20}})：查询年龄>20的

limit()：db.集合名称.find().limit(10)
skip()：db.集合名称.find().skip(2)  -- 从第3条开始查询
for(i=0;i<15;i++){db.t1.insert({_id:i})}
db.stu.find().limit(4).skip(5)
db.stu.find().skip(5).limit(4)  # limit和skip结合使用时不分先后顺序

投影：返回指定key的文档查询结果
db.集合名称.find({},{字段名称:1,...})
-- 在第二个参数中将需要显示的字段设置为1即可,不设置就不显示;_id列默认是显示的,如果不想显示需要明确设置为0
db.stu.find({},{"name":1, "gender":1})  -- 如果要选取的字段很少就将需要的字段指定为1
db.stu.find({},{"_id":0, "age":0})  -- 如果要选取的字段太多可以将不需要的字段设为0

排序：
db.集合名称.find().sort.md({字段:1,...})
db.stu.find().sort.md({gender:-1,age:1})  # 1升序-1降序

统计：
db.集合名称.find({条件}).count() 等价于 db.集合名称.count({条件})
db.stu.find({gender:1}).count()
db.stu.count({age:{$gt:20},gender:1})

去重：
db.集合名称.distinct('去重字段',{条件})
db.stu.distinct('gender',{age:{$gt:18}})

aggregate聚合操作：
db.集合名称.aggregate([{管道:{表达式}}])

常用管道
$group：将集合中的文档分组统计结果
$match：过滤数据
$project：修改输入文档的结构,如重命名、增加、删除字段、创建计算结果
$sort.md：将输入文档排序后输出
$limit：限制聚合管道返回的文档数
$skip：跳过指定数量的文档,并返回余下的文档
$unwind：将数组类型的字段进行拆分

常用表达式
$sum：计算总和,$sum:1同count表示计数
$avg：计算平均值
$min：获取最小值
$max：获取最大值
$push：在结果文档中插入值到一个数组中
$first：根据资源文档的排序获取第一个文档数据
$last：根据资源文档的排序获取最后一个文档数据

$group
1、db.stu.aggregate([
    {$group:
        {
            _id:'$gender',  # _id表示分组依据: 使用某个字段的格式为'$字段'
            counter:{$sum:1}
        }
    }
])：统计男/女生总人数
2、db.stu.aggregate([
    {$group:
        {
            _id:null,  # group by null表示将所有文档分为一组
            counter:{$sum:1},
            avgAge:{$avg:'$age'}
        }
    }
])：统计所有学生总人数、平均年龄
3、db.stu.aggregate([
    {$group:
        {
            _id:'$gender',
            name:{$push:'$name'}  # 透视数据
        }
    }
])：统计学生性别和姓名
4、db.stu.aggregate([
    {$group:
        {
            _id:'$gender',
            name:{$push:'$$ROOT'}  # 使用$$ROOT可以将文档内容加入到结果集的数组中
        }
    }
])

$match
1、db.stu.aggregate([
    {$match:{age:{$gt:20}}}
])：查询年龄>20的
2、db.stu.aggregate([
    {$match:{age:{$gt:20}}},
    {$group:{_id:'$gender',counter:{$sum:1}}}
])：查询年龄>20的男/女生人数

$project
修改输入文档的结构: 如重命名、增加、删除字段、创建计算结果
1、db.stu.aggregate([
    {$project:{_id:0,name:1,age:1}}
])：查询学生姓名、年龄
2、db.stu.aggregate([
    {$group:{_id:'$gender',counter:{$sum:1}}},
    {$project:{_id:0,counter:1}}
])：查询男/女生人数,输出人数

$sort.md
1、db.stu.aggregate([{$sort.md:{age:1}}])：按年龄升序排序
2、db.stu.aggregate([
    {$group:{_id:'$gender',counter:{$sum:1}}},
    {$sort.md:{counter:-1}}
])：查询男/女生人数然后降序排序

$limit、$skip
1、db.stu.aggregate([{$limit:2}])
2、db.stu.aggregate([{$skip:2}])
3、db.stu.aggregate([
    {$group:{_id:'$gender',counter:{$sum:1}}},
    {$sort.md:{counter:1}},
    {$skip:1},
    {$limit:1}
])：先统计男/女生人数,升序排序,取第二条数据

$unwind
将文档中某个数组类型的字段拆分成多条,每条包含数组中的一个值
语法1：db.集合名称.aggregate([{$unwind:'$字段名称'}])
db.t2.insert({_id:1,item:'t-shirt',size:['S','M','L']})
db.t2.aggregate([{$unwind:'$size'}])
语法2：db.inventory.aggregate([{
    $unwind:{
        path:'$字段名称',
        preserveNullAndEmptyArrays:<boolean>  # 防止数据丢失
    }
}])：处理空数组、非数组、无字段、null情况
db.t3.insert([
{ "_id" : 1, "item" : "a", "size": [ "S", "M", "L"] },
{ "_id" : 2, "item" : "b", "size" : [ ] },
{ "_id" : 3, "item" : "c", "size": "M" },
{ "_id" : 4, "item" : "d" },
{ "_id" : 5, "item" : "e", "size" : null }
])
db.t3.aggregate([{$unwind:'$size'}])  -- 空数组、无字段、null的文档都被丢弃了
db.t3.aggregate([{$unwind:{path:'$sizes',preserveNullAndEmptyArrays:true}}])  -- 不丢弃

python操作mongo：
# 创建MONGODB数据库链接
conn = pymongo.MongoClient(host="", port=27017)
# 指定数据库
db = conn.dbname
# 指定集合
collection = db.collectionname
# 插入文档数据
collection.insert()
"""