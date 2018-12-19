"""
25行报错：TypeError: not all arguments converted during string formatting
往mysql插数据时values(%s,%s...)%s数量不能漏写，不然字段对不上
"""

import pymysql
import json
# import logging
#
# logging.basicConfig(
#     level=logging.DEBUG,
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     datefmt="%m/%d/%Y %H:%M:%S %p"
# )


def insert(v1, v2, env):
    with open('./conf/' + env + '.conf') as f:
        config = json.loads(f.read())

    conn = pymysql.connect(**config)
    cur = conn.cursor()

    try:
        sql1 = "replace into user_info values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql2 = "replace into income_pay_detail values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        res1 = cur.executemany(sql1, v1)
        res2 = cur.executemany(sql2, v2)
        print(res1)
        print(res2)
        conn.commit()
    # except Exception as e:
    #     conn.rollback()
    #     print(e)
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    values1 = json.load(open("./value/01.txt", encoding="utf-8"))
    values2 = json.load(open('./value/02.txt', encoding='utf-8'))
    insert(values1, values2, 'test')
