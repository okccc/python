# coding=utf-8
import json
import requests
import sys


def generate(filename, sync_type):
    # 获取key
    d = json.load(open(filename), strict=False)
    apollo_key = d["job"]["apollo_key"]
    # print(type(d["job"]["content"][0]["reader"]["parameter"]["connection"][0]["jdbcUrl"][0]))

    # apoll地址
    apoll_url = "http://apollo-config-dev.jlgltech.com/configs/bdp_db_conn_config/default/application"
    # 发送请求
    response = requests.get(url=apoll_url)
    # print(response.text)
    # 加载所有配置
    d1 = json.loads(response.text)
    config = d1["configurations"]
    # 获取指定key的value
    apollo_value = config[apollo_key]
    # print(apollo_value)
    # 解析用户/密码/连接
    d2 = json.loads(apollo_value)
    username = d2["username"]
    password = d2["password"]
    url = d2["url"]

    # 往字典填充数据库连接信息并写入新的文件
    if sync_type == "mysqltohive":
        param = d["job"]["content"][0]["reader"]["parameter"]
        param["username"] = username
        param["password"] = password
        param["connection"][0]["jdbcUrl"][0] = url
        json.dump(d, open(filename + "_new", "w"), ensure_ascii=False)
    else:
        param = d["job"]["content"][0]["writer"]["parameter"]
        param["username"] = username
        param["password"] = password
        param["connection"][0]["jdbcUrl"] = url
        json.dump(d, open(filename + "_new", "w"), ensure_ascii=False)


if __name__ == '__main__':
    # 参数解析
    generate(sys.argv[1], sys.argv[2])
