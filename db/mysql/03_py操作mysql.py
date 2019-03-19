# coding=utf-8
"""
注意: sql语句字符串格式化都是%s,没有%d和%f
"""

import pymysql

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

# 要执行的sql语句
sql = "replace into positions values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
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
