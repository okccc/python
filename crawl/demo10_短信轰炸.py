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


class Api01(object):
    # 多线程
    def __init__(self):
        self.url = "https://www.baidu.com/s?wd={}&pn={}&gpc={}"
        self.headers = {
            "User-Agent": "Chrome Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36"
        }
        self.flag = False
        self.datas = []
        # 构造url队列、请求队列
        self.url_queue = Queue()
        self.soup_queue = Queue()

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
                    self.url_queue.put(self.url.format(word, (i - 1) * 10, gpc))

    def get_data(self):
        while True:
            url = self.url_queue.get()
            # print(url)
            response = requests.get(url, headers=self.headers)
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
                data = {"title": title, "link": real_link}
                print(data)
                self.datas.append(data)
            self.soup_queue.task_done()

    def data(self):
        # 1.获取所有关键字
        words = input("输入查询关键字：")
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
        return self.datas


if __name__ == "__main__":
    res = Api01()
    print(res.data())
