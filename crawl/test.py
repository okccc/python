# coding=utf-8
import requests
from bs4 import BeautifulSoup
import pymysql
import threading
from queue import Queue
import json
import re
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S %p"
)


class Api02(object):
    # 多线程
    def __init__(self):
        self.url = "https://www.baidu.com/s?wd={}&pn={}&gpc={}"
        self.headers = {
            "User-Agent": "Chrome Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
        }
        self.config = {
            "host": "10.9.2.196",
            "port": 3306,
            "user": "meihaodb",
            "password": "Eakgydskaezfl68Eefg:",
            "db": "duckchatdb",
            "charset": "utf8",
            "cursorclass": pymysql.cursors.DictCursor,  # 以dict格式返回数据
        }
        self.negative_words = [
            "110网",
            "骗",
            "忽悠",
            "合法",
            "合理",
            "征信",
            "名声",
            "跑路",
            "违约",
            "不还",
            "起诉",
            "法院",
            "律师",
            "法律",
            "违规",
            "暴力",
            "轰炸",
            "威胁",
            "后悔",
            "反悔",
            "恐吓",
            "服务费",
            "传销",
            "退款",
            "套路",
            "虚假",
            "逾期",
        ]
        self.flag = False
        self.datas = []
        # 构造url队列、请求队列
        self.url_queue = Queue()
        self.soup_queue = Queue()

    def get_hospital(self):
        conn = pymysql.connect(**self.config)
        cur = conn.cursor()
        words = []
        try:
            sql = (
                "select distinct name from shop where online_status=1 and type!='TEST'"
            )
            cur.execute(sql)
            # records = cur.fetchmany(50)
            records = cur.fetchall()
            for record in records:
                hospital = record["name"]
                words.append(hospital)
            words.insert(0, "美好分趣")
            words.insert(0, "美好分期")
            return words
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()

    def get_url(self, words):
        if self.flag:
            # return [self.url.format(word, (i-1)*10, "") for word in words for i in range(1, 20)]
            for word in words:
                for i in range(1, 20):
                    self.url_queue.put(self.url.format(word, (i - 1) * 10, ""))
        else:
            gpc = "stf=%.3f,%.3f|stftype=1" % (time.time() - 86400, time.time())
            # return [self.url.format(word, (i-1)*10, gpc) for word in words for i in range(1, 3)]
            for word in words:
                for i in range(1, 2):
                    # self.url_queue.put(self.url.format(word, (i - 1) * 10, gpc))
                    self.url_queue.put(self.url.format(word, (i - 1) * 10, gpc))

    def get_data(self):
        while True:
            url = self.url_queue.get()
            # print(url)
            response = requests.get(url, headers=self.headers, timeout=5)
            # return BeautifulSoup(response.text, "lxml")
            self.soup_queue.put(BeautifulSoup(response.text, "lxml"))
            self.url_queue.task_done()

    def parse_data(self):
        while True:
            soup = self.soup_queue.get()
            for tag in soup.select("h3 > a"):
                title = tag.text
                link = tag.attrs["href"]
                # 百度搜索的条目都是www.baidu.com域名的地址,点击后会重定向到真实地址,所以需要再次发送请求获取搜索结果的真实url
                real_link = ""
                if link.startswith("http"):
                    response = requests.get(
                        link, headers=self.headers, allow_redirects=False
                    )
                    if response.status_code < 400:
                        # 禁用后status_code是302,通过response.headers["Location"]获取重定向的url
                        real_link = response.headers["Location"]
                        # print(real_link)
                for word in self.negative_words:
                    if word in title:
                        # 有word符合就添加数据
                        data = {"title": title, "link": real_link}
                        print(data)
                        self.datas.append(data)
                        # 结束循环防止一个title多个word重复添加
                        break
            self.soup_queue.task_done()

    def filter_data(self):
        data_new = []
        print(self.datas)
        for data in self.datas:
            for word in ["美好", "医院"]:
                if word in data["title"]:
                    data_new.append(data)
                    break
        # print([dict(t) for t in {tuple(d.items()) for d in data_new}])
        return [dict(t) for t in {tuple(d.items()) for d in data_new}]

    def data(self):
        # 1.获取所有关键字
        words = self.get_hospital()
        print(len(words))
        threads = []
        # 2.获取url列表
        t_url = threading.Thread(target=self.get_url, args=(words,))
        threads.append(t_url)
        for i in range(1, 30):
            # 3.发送请求,获取响应
            t_get = threading.Thread(target=self.get_data)
            threads.append(t_get)
        for i in range(1, 30):
            # 4.解析数据
            t_parse = threading.Thread(target=self.parse_data)
            threads.append(t_parse)
        for t in threads:
            t.setDaemon(True)
            t.start()
        for q in (self.url_queue, self.soup_queue):
            q.join()
        # 5.处理最终结果
        return self.filter_data()


class Api01(object):
    # 多线程
    def __init__(self):
        self.url = "https://tousu.sina.com.cn/api/index/s?keywords={}&page_size=10&page=1"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
        }
        self.config = {
            "host": "10.9.2.196",
            "port": 3306,
            "user": "meihaodb",
            "password": "Eakgydskaezfl68Eefg:",
            "db": "duckchatdb",
            "charset": "utf8",
            "cursorclass": pymysql.cursors.DictCursor,  # 以dict格式返回数据
        }
        self.negative_words = [
            "110网",
            "骗",
            "忽悠",
            "合法",
            "合理",
            "征信",
            "名声",
            "跑路",
            "违约",
            "不还",
            "起诉",
            "法院",
            "律师",
            "法律",
            "违规",
            "暴力",
            "轰炸",
            "威胁",
            "后悔",
            "反悔",
            "恐吓",
            "服务费",
            "传销",
            "退款",
            "套路",
            "虚假",
            "逾期",
        ]
        self.datas = []
        # 构造url队列、请求队列
        self.url_queue = Queue()
        self.data_queue = Queue()

    def get_hospital(self):
        conn = pymysql.connect(**self.config)
        cur = conn.cursor()
        words = []
        try:
            sql = (
                "select distinct name from shop where online_status=1 and type!='TEST'"
            )
            cur.execute(sql)
            # records = cur.fetchmany(50)
            records = cur.fetchall()
            for record in records:
                hospital = record["name"]
                words.append(hospital)
            words.insert(0, "美好分趣")
            words.insert(0, "美好分期")
            return words
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()

    def get_url(self, words):
        for word in words:
            self.url_queue.put(self.url.format(word))
        print(self.url_queue.qsize())

    def get_data(self):
        while True:
            url = self.url_queue.get()
            response = requests.get(url, headers=self.headers, timeout=5)
            data = json.loads(response.text)
            contents = data["result"]["data"]["lists"]
            if contents is not None:
                self.data_queue.put(contents)
            self.url_queue.task_done()

    def parse_data(self):
        while True:
            contents = self.data_queue.get()
            for content in contents:
                title = content["main"]["title"]
                title = "".join(re.compile("[\u4e00-\u9fa5]").findall(title))
                link = "https:" + content["main"]["url"]
                # timestamp = content["main"]["timestamp"]
                # if float(timestamp) > time.time() - 86400:
                for word in self.negative_words:
                    if word in title:
                        # 有word符合就添加数据
                        data = {"title": title, "link": link}
                        print(data)
                        self.datas.append(data)
                        # 结束循环防止一个title多个word重复添加
                        break
            self.data_queue.task_done()

    def filter_data(self):
        data_new = []
        print(self.datas)
        for data in self.datas:
            for word in ["美好", "医院"]:
                if word in data["title"]:
                    data_new.append(data)
                    break
        # print([dict(t) for t in {tuple(d.items()) for d in data_new}])
        return [dict(t) for t in {tuple(d.items()) for d in data_new}]

    def data(self):
        # 1.获取所有关键字
        words = self.get_hospital()
        # print(len(words))
        threads = []
        # 2.获取url列表
        t_url = threading.Thread(target=self.get_url, args=(words,))
        threads.append(t_url)
        for i in range(1, 20):
            # 3.发送请求,获取响应
            t_get = threading.Thread(target=self.get_data)
            threads.append(t_get)
        for i in range(1, 20):
            # 4.解析数据
            t_parse = threading.Thread(target=self.parse_data)
            threads.append(t_parse)
        for t in threads:
            t.setDaemon(True)
            t.start()
        for q in (self.url_queue, self.data_queue):
            q.join()
        # 5.处理最终结果
        return self.filter_data()


class Api(object):
    @staticmethod
    def data():
        res01 = Api01().data()
        print(res01)
        print("=" * 30)
        time.sleep(3)
        res02 = Api02().data()
        print(res02)
        return res01 + res02


if __name__ == "__main__":
    res = Api()
    print(res.data())
