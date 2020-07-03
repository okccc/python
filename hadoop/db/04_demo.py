# coding=utf-8
import pymysql
import pymongo
import redis
import csv
import codecs

def mysql01():
    """
    注意: sql语句字符串格式化都是%s,没有%d和%f
    """
    # 创建数据库连接
    config = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "root",
        "db": "test",
        "charset": "utf8",
        "cursorclass": pymysql.cursors.DictCursor  # 以dict格式返回数据
    }

    # 连接数据库
    conn = pymysql.connect(**config)
    # 设置自动提交,更新操作(insert,update,delete)都需要commit
    # conn.autocommit(1)
    # 获取游标
    cur = conn.cursor()

    # 要执行的sql语句,python操作数据库时字符串格式化只有%s没有%d%f
    sql = 'replace into positions values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    value = ()
    values = [(), ()]

    try:
        # 插入一条,返回受影响行数
        cur.execute(sql, value)
        # 插入多条(效率高),返回受影响行数
        cur.executemany(sql, values)
        # 提交执行
        conn.commit()

        # 获取上面execute执行结果的所有数据,返回tuple(指定cursorclass = pymysql.cursors.DictCursor就返回dict)
        cur.fetchall()
        # 获取剩余数据第一条数据
        cur.fetchone()
        # 获取剩余数据前2条数据
        cur.fetchmany(2)
    except Exception as e:
        # 发生异常时回滚
        conn.rollback()
        # 捕获异常
        print(e)
    finally:
        # 不论try代码块是否抛出异常,这里都会执行(关闭游标和数据库连接)
        cur.close()
        conn.close()


def mongodb01():
    # 创建数据库连接
    conn = pymongo.MongoClient(host="mongodb://root:lzkhxf3xtewUlctyazH5@10.9.78.195:27017/", connect=False)
    # 指定数据库
    db = conn.stat_dev
    # 指定集合
    collection = db.debitLoanV2
    # print(collection.find().count())  -- 统计记录数

    # 文档查询
    documents = []
    # 将不需要的字段设为0
    for document in collection.find({}, {"_id": 0, "_class": 0}):
        print(document)
        documents.append(document)

    # 按照生成的字段顺序生成csv文件表头
    header = list(documents[0].keys())

    # with open("C://Users/chenqian/Desktop/result.csv", "wb") as file:
    #     file.write(codecs.BOM_UTF8)

    with open("C://Users/chenqian/Desktop/aaa.csv", "w", encoding="utf8", newline="") as file:
        # 创建writer对象
        writer = csv.DictWriter(file, fieldnames=header)
        # 先写入一行表头
        writer.writeheader()
        # 再写入多行数据
        writer.writerows(documents)


def redis01():
    # 连接redis并选择数据库
    sr = redis.StrictRedis(host="localhost", port=6379, db=0)
    # 添加数据
    sr.set(name="orc", value="grubby")
    # 获取数据
    sr.get(name="orc")
