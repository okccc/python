# coding=utf-8
import pymongo
import csv
import codecs


def test():
    # 创建数据库连接
    conn = pymongo.MongoClient("mongodb://root:lzkhxf3xtewUlctyazH5@10.9.78.195:27017/", connect=False)
    # 库
    db = conn.stat_dev
    # 集合
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


if __name__ == '__main__':
    test()