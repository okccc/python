# coding=utf-8
import pymysql
import logging
import json

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S %p"
)


def insert(values, env):
    """
    将数据插入到mysql
    :return:
    """

    # 读取配置文件
    with open("./conf/" + env + ".conf") as f:
        config = json.loads(f.read())

    # 连接mysql
    conn = pymysql.connect(**config)
    # 创建游标执行crud操作
    cur = conn.cursor()

    try:
        # 插入语句
        sql = "replace into odps_tasks values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
              "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        # 插入多条记录,返回受影响的行数,如果是先删除再插入,res是操作的记录数*2
        res = cur.executemany(sql, values)
        print(res)
        # 提交执行语句
        conn.commit()
    except Exception as e:
        # 回滚
        conn.rollback()
        print(e)
    finally:
        # 关闭连接
        cur.close()
        conn.close()


if __name__ == "__main__":
    # 加载中间件结果
    value_list = json.load(open("value_list.txt", encoding="utf-8"))
    insert(value_list, 'test')
