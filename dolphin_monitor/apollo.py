# coding=utf-8
import json
import requests
import sys


def generate(filename, sync_type, table_type, param):
    # 获取数仓配置信息
    d = json.load(open(filename), strict=False)
    apollo_key = d["dsn"]
    # print(type(d["job"]["content"][0]["reader"]["parameter"]["connection"][0]["jdbcUrl"][0]))

    # apoll地址
    login_url = "http://apollo.xxx.com/signin"
    config_url = "http://apollo.xxx.com/apps/bdp_db_conn_config/envs/FAT/clusters/default/namespaces"
    s = requests.session()
    headers = {"User-Agent": "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11"}
    data = {"username": "tim_chen", "password": "tim_chen"}
    s.post(login_url, data, headers)
    response = s.get(config_url, headers=headers)
    # print(response.text)

    # 获取该环境的所有key-value
    dict01 = dict()
    items = json.loads(response.text)[0]["items"]
    for item in items:
        key = item["item"]["key"]
        value = item["item"]["value"]
        dict01[key] = value
    # 获取指定key的value
    apollo_value = dict01[apollo_key]
    # 解析用户/密码/连接
    username = json.loads(apollo_value)["username"]
    password = json.loads(apollo_value)["password"]
    url = json.loads(apollo_value)["url"]

    # 加载模板并填充空缺值
    if sync_type == "mysqltohive":
        query_sql = d["querySql"][0]
        # print(query_sql)
        column = d["column"]
        file_name = d["fileName"]
        d1 = json.load(open("temp01.txt"), strict=False)
        # d1 = json.load(open("/data1/projects-app/ChartSync/datax/job/mysqltohive/prod/template.txt"), strict=False)
        p1 = d1["job"]["content"][0]["reader"]["parameter"]
        p1["username"] = username
        p1["password"] = password
        p1["connection"][0]["querySql"][0] = query_sql
        p1["connection"][0]["jdbcUrl"][0] = url
        p2 = d1["job"]["content"][0]["writer"]["parameter"]
        p2["column"] = column
        p2["fileName"] = file_name
        p2["fileType"] = table_type
        if len(param) == 8:
            p2["path"] = "/data/hive/warehouse/ods.db/" + file_name + "/dt=" + param
        else:
            p2["path"] = "/data/hive/warehouse/ods.db/" + file_name
        # 生成新文件
        json.dump(d1, open(filename + "_new", "w"), ensure_ascii=False)
    else:
        column1 = d["column1"]
        column2 = d["column2"]
        path = d["path"]
        table = d["table"]
        d2 = json.load(open("temp02.txt"), strict=False)
        # d2 = json.load(open("/data1/projects-app/ChartSync/datax/job/hivetomysql/prod/template.txt"), strict=False)
        p1 = d2["job"]["content"][0]["reader"]["parameter"]
        p1["column"] = column1
        p1["fileType"] = table_type
        p1["path"] = path
        p2 = d2["job"]["content"][0]["writer"]["parameter"]
        p2["column"] = column2
        p2["connection"][0]["jdbcUrl"] = url
        p2["connection"][0]["table"][0] = table
        p2["username"] = username
        p2["password"] = password
        json.dump(d2, open(filename + "_new", "w"), ensure_ascii=False)


if __name__ == '__main__':
    # 参数解析
    # generate("a.txt", "mysqltohive", "text", "20210101")
    generate("b.txt", "hivetomysql", "text", "20210101")
    # generate(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
