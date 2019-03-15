# coding=utf-8
import requests
from lxml import etree
import urllib.request
from fake_useragent import UserAgent
import threading
from queue import Queue
import os
import re
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S %p"
)


class DouTu01(object):
    def __init__(self):
        self.url = "https://www.doutula.com/photo/list/?page={}"
        self.ua = UserAgent()

    def get_url(self):
        return [self.url.format(i) for i in range(1, 30)]

    def get_data(self, url):
        response = requests.get(url, headers={"User-Agent": self.ua.random})
        return etree.HTML(response.text)

    @staticmethod
    def parse_data(html):
        imgs = html.xpath('//div[@class="page-content text-center"]//a/img[@class!="gif"]')
        for img in imgs:
            # 如果当前标签已经是最内层标签,建议用get()获取属性值,因为xpath返回的是列表,可能会索引越界,而get()则返回None
            img_url = img.get("data-original")
            alt = img.get("alt")
            # 使用正则将特殊字符替换掉,r""表示取原生字符串而不对字符串内部的特殊字符转义
            alt = re.sub(r"[?？!！]", "", alt)
            # splitext()：将path切割成root + extension
            suffix = os.path.splitext(img_url)[1][0:4]
            filename = "D://doutu/" + alt + suffix
            print(filename)
            # 如果被检索的url是个文件可以直接将其复制到本地 --> 快速保存图片
            urllib.request.urlretrieve(img_url, filename=filename)

    def main(self):
        # 1.获取url列表
        urls = self.get_url()
        for url in urls:
            # 2.发送请求,接受响应
            html = self.get_data(url)
            # 3.解析数据
            self.parse_data(html)


class DouTu02(object):
    def __init__(self):
        self.url = "https://www.doutula.com/photo/list/?page={}"
        self.ua = UserAgent()
        # 构造url队列、请求响应队列
        self.url_queue = Queue()
        self.html_queue = Queue()

    def get_url(self):
        for i in range(1, 30):
            # 将url放入url_queue
            self.url_queue.put(self.url.format(i))

    def get_data(self):
        while True:
            # 从url_queue取出url
            url = self.url_queue.get()
            response = requests.get(url, headers={"User-Agent": self.ua.random})
            # 将html源码放入html_queue
            self.html_queue.put(etree.HTML(response.text))
            # 将处理完的url标记为task_done,此时url_queue.qsize - 1
            self.url_queue.task_done()

    def parse_data(self):
        while True:
            # 从html_queue取出html
            html = self.html_queue.get()
            imgs = html.xpath('//div[@class="page-content text-center"]//a/img[@class!="gif"]')
            for img in imgs:
                # 如果当前标签已经是最内层标签,建议用get()获取属性值,因为xpath返回的列表可能会list index out of range,而get()返回None
                img_url = img.get("data-original")
                alt = img.get("alt")
                # 使用正则将特殊字符替换掉
                alt = re.sub(r"[?？!！]", "", alt)
                # splitext()：将path切割成root + extension
                suffix = os.path.splitext(img_url)[1][0:4]
                filename = "D://doutu/" + alt + suffix
                print(filename)
                # 如果被检索的url是个文件可以直接将其复制到本地 --> 快速保存图片
                urllib.request.urlretrieve(img_url, filename=filename)
            # 将处理完的html标记为task_done
            self.html_queue.task_done()

    def main(self):
        threads = []
        # 1.获取url列表
        t_url = threading.Thread(target=self.get_url)
        threads.append(t_url)
        # 2.发送请求,接受响应
        for i in range(1, 20):
            t_html = threading.Thread(target=self.get_data)
            threads.append(t_html)
        # 3.解析数据
        for i in range(1, 5):
            t_parse = threading.Thread(target=self.parse_data)
            threads.append(t_parse)
        for t in threads:
            # 由于该子线程是死循环,需要在调用start()之前将其设置为守护线程,表示该线程不重要,当主线程结束时不用等待该子线程直接退出
            t.setDaemon(daemonic=True)
            t.start()
        for q in (self.url_queue, self.html_queue):
            # 让主线程block,等待queue中的items全部处理完
            q.join()
        print("表情包下载完毕!")


if __name__ == '__main__':
    # dt = DouTu01()
    dt = DouTu02()
    dt.main()
