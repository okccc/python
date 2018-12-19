# coding=utf-8
import requests
import json
import jsonpath
import logging
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S %p"
)

data_list = []

s = requests.session()
url_login = "https://signin.aliyun.com/1065151969971491/login.htm"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"}
with open("./conf/user.conf") as f:
    data = json.loads(f.read())
s.post(url_login, data=data, headers=headers)


@retry(retry=retry_if_exception_type(json.decoder.JSONDecodeError), wait=wait_fixed(5), stop=stop_after_attempt(3))
def parse(ids):
    """
    解析获取的请求数据
    :param ids: id列表
    :return: json字符串里的data字段
    """

    for i in ids:
        data = getfile(i)

        # 是脚本就直接取数据
        if data is not None:
            data_list.append(data)
        # 是文件夹就继续循环
        else:
            ids2 = getdir(i)
            if ids2 is not False:
                parse(ids2)
            else:
                pass

    return data_list


def getfile(i):
    # 脚本接口
    url = "https://ide-cn-shanghai.data.aliyun.com/web/flow/loadProp?objectId=" + str(
        i) + "&projectId=29820&tenantId=171224272675329"
    # 获取请求数据
    res = s.get(url, headers=headers)
    # 转成Python对象
    dict1 = json.loads(res.text)
    # 获取data字段
    data = dict1.get('data')
    return data


def getdir(i):
    # 文件夹接口
    url = "https://ide-cn-shanghai.data.aliyun.com/web/folder/listObject?objectId=" + str(
        i) + "&projectId=29820&tenantId=171224272675329&type=1"
    res = s.get(url, headers=headers)
    dict2 = json.loads(res.text)
    ids2 = jsonpath.jsonpath(dict2, '$..id')
    return ids2


if __name__ == "__main__":
    id_list = [-1]
    res = parse(id_list)
    # 将结果缓存到中间件
    json.dump(res, open("data_list.txt", "w", encoding="utf-8"), ensure_ascii=False)
