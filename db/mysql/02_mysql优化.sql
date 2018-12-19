-- 1、表的主键、外键必须有索引;
-- 3、经常与其他表进行连接的表,在连接字段上应该建立索引;
-- 4、经常出现在Where子句中的字段,特别是大表的字段,应该建立索引;
-- 5、索引应该建在选择性高的字段上;
-- 6、索引应该建在小字段上,对于大的文本字段甚至超长字段,不要建索引;

-- 第一掌 避免对列的操作
-- 任何对列的操作都可能导致全表扫描,包括数据库函数、计算表达式等等,查询时尽量将操作移到等式右边甚至去掉函数
-- 例1：下列SQL条件语句中的列都建有恰当的索引,但30万行数据情况下执行速度却非常慢：
select * from record where substrb(CardNo,1,4) = '5378';                -- (13秒)
select * from record where amount/30 < 1000;                            -- (11秒)
select * from record where to_char(ActionTime, 'yyyymmdd') = '19991201';   -- (10秒)
-- 由于where子句中对列的任何操作结果都是在SQL运行时逐行计算得到的,因此它不得不进行表扫描,而没有使用该列上面的索引
select * from record where CardNo like '5378%';                         -- (< 1秒)
select * from record where amount  < 1000*30;                           -- (< 1秒)
select * from record where ActionTime = to_date('19991201', 'yyyymmdd'); -- (< 1秒)
-- 差别是很明显的！
