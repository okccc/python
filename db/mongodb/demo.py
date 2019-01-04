# coding=utf-8
import pymongo


def test():
    # 参考文档 https://www.jianshu.com/p/c9777b063593
    conn = pymongo.MongoClient("mongodb://root:lzkhxf3xtewUlctyazH5@10.9.78.195:27017/", connect=False)
    db = conn["stat_dev"]
    collection = db["debitLoanV2"]
    with open("C://Users/chenqian/Desktop/result.json", "w") as f:
        for i in collection.find():
            f.write(str(i) + "\n")


if __name__ == '__main__':
    test()