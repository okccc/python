# coding=utf-8
import requests
from bs4 import BeautifulSoup
import time
import pymysql
import logging
import gevent
from gevent import monkey

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S %p"
)


monkey.patch_all()

def shop():
    config = {
        "host": "10.9.2.196",
        "port": 3306,
        "user": "meihaodb",
        "password": "Eakgydskaezfl68Eefg:",
        "db": "duckchatdb",
        "charset": "utf8",
        "cursorclass": pymysql.cursors.DictCursor  # 以dict格式返回数据
    }
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    hospitals = []
    try:
        sql = "select name from shop where online_status=1 and type!='TEST'"
        cur.execute(sql)
        # records = cur.fetchmany(5)
        records = cur.fetchall()
        for record in records:
            hospital = record["name"]
            hospitals.append(hospital)
        data(hospitals)
    except Exception as e:
        print(e)
    finally:
        cur.close()
        conn.close()

def data(words, flag=False):
    # 负面消息关键字
    negative_words = ["110网", "骗", "忽悠", "合法", "合理", "征信", "名声", "跑路", "违约", "不还", "起诉", "法院", "律师", "法律",
                      "正规", "违规", "暴力", "轰炸", "威胁", "后悔", "反悔", "恐吓", "服务费", "传销", "退款", "套路", "虚假", "逾期"]
    datas = []
    # words.extend(['美好分期', '美好分趣'])
    words.insert(0, "美好分趣")
    words.insert(0, "美好分期")
    print(len(words))
    for wd in words:
        print(wd)
        if flag:
            for page in range(1, 20):
                pn = (page - 1) * 10
                params = {"wd": wd, "pn": pn}
                # parse(datas, negative_words, params)
                g1 = gevent.spawn(parse, datas, negative_words, params)
                g1.join()
                time.sleep(1)
        else:
            for page in range(1, 3):
                pn = (page - 1) * 10
                params = {"wd": wd, "pn": pn, "gpc": "stf=1546743776.63,1546830176.63|stftype = 1"}
                # parse(datas, negative_words, params)
                g2 = gevent.spawn(parse, datas, negative_words, params)
                g2.join()
            # time.sleep(0.5)
    filter_words = ["美好", "美容", "医院", "医疗", "医美", "祛痘", "植发", "整形", "门诊", "诊所"]
    data_new = []
    for data in datas:
        for word in filter_words:
            if word in data["title"]:
                data_new.append(data)
                break
    print([dict(t) for t in {tuple(d.items()) for d in data_new}])
    # return [dict(t) for t in {tuple(d.items()) for d in data_new}]

def parse(datas, negative_words, params):
    name = params["wd"]
    url = "https://www.baidu.com/s?"
    headers = {
        "User-Agent": "Chrome Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"}
    response = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    for tag in soup.select("h3 > a"):
        title = tag.text
        link = tag.attrs["href"]
        # 百度搜索的条目都是www.baidu.com域名的地址,点击后会重定向到真实地址,所以需要再次发送请求获取搜索结果的真实url
        real_link = ""
        if link.startswith("http"):
            response = requests.get(link, headers=headers, allow_redirects=False)
            if response.status_code < 400:
                # 禁用后status_code是302,通过response.headers["Location"]获取重定向的url
                real_link = response.headers["Location"]
                # if "www.zhihu.com" in real_link:
                #     real_link = real_link.replace("https", "http")
        for word in negative_words:
            if word in title:
                # 有word符合就添加数据
                data = {"name": name, "title": title, "link": real_link}
                # data = {"title": title, "link": real_link}
                datas.append(data)
                # 结束循环防止一个title多个word重复添加
                break


if __name__ == '__main__':
    shop()