# coding=utf-8
import requests
from lxml import etree
import urllib.request
import threading
from queue import Queue
import os
import re

class DouTu01(object):
    def __init__(self):
        self.url = "https://www.doutula.com/photo/list/?page={}"
        self.headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"}

    def get_url(self):
        return [self.url.format(i) for i in range(1, 100)]

    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        return etree.HTML(response.text)

    @staticmethod
    def parse_data(html):
        imgs = html.xpath('//div[@class="page-content text-center"]//a/img[@class!="gif"]')
        for img in imgs:
            # 如果当前标签已经是最内层标签,建议用get()获取属性值,因为xpath返回的列表可能会list index out of range,而get()返回None
            img_url = img.get("data-original")
            alt = img.get("alt")
            # 使用正则将特殊字符替换掉
            alt = re.sub(r"[/?!.*,]", "", alt)
            # splitext()：将path切割成root + extension
            suffix = os.path.splitext(img_url)[1][0:4]
            filename = "D://doutu/" + alt + suffix
            print(filename)
            # urlretrieve()：如果被检索的url是个文件可以直接将其复制到本地
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
        self.headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"}
        # 构造url队列、请求响应队列
        self.url_queue = Queue()
        self.html_queue = Queue()

    def get_url(self):
        for i in range(1, 100):
            # 将url放入url_queue
            self.url_queue.put(self.url.format(i))

    def get_data(self):
        while True:
            # 从url_queue取出url
            url = self.url_queue.get()
            response = requests.get(url, headers=self.headers)
            # 将html源码放入html_queue
            self.html_queue.put(etree.HTML(response.text))
            self.url_queue.task_done()

    def parse_data(self):
        while True:
            html = self.html_queue.get()
            imgs = html.xpath('//div[@class="page-content text-center"]//a/img[@class!="gif"]')
            for img in imgs:
                # 如果当前标签已经是最内层标签,建议用get()获取属性值,因为xpath返回的列表可能会list index out of range,而get()返回None
                img_url = img.get("data-original")
                alt = img.get("alt")
                # 使用正则将特殊字符替换掉
                alt = re.sub(r"[/?!.*,]", "", alt)
                # splitext()：将path切割成root + extension
                suffix = os.path.splitext(img_url)[1][0:4]
                filename = "D://doutu/" + alt + suffix
                print(filename)
                # urlretrieve()：如果被检索的url是个文件可以直接将其复制到本地
                urllib.request.urlretrieve(img_url, filename=filename)
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
        for i in range(1, 20):
            t_parse = threading.Thread(target=self.parse_data)
            threads.append(t_parse)
        for t in threads:
            t.setDaemon(True)
            t.start()
        for q in (self.url_queue, self.html_queue):
            q.join()
        print("表情包下载完毕!")


if __name__ == '__main__':
    # dt = DouTu01()
    dt = DouTu02()
    dt.main()
