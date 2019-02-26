# coding=utf-8
import urllib.parse
import urllib.request
from lxml import etree
import threading
from queue import Queue
import random
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S %p"
)


class TieBa01(object):
    # 单线程
    def __init__(self, name):
        self.url = "https://tieba.baidu.com/f?{}&pn={}"
        self.name = name
        # urllib和fake_useragent不兼容,还是手写headers吧
        self.ua_list = [
            {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)"},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"},
        ]

    def get_url(self):
        # 对贴吧名称做url转码
        kw = urllib.parse.urlencode({"kw": self.name})
        return [self.url.format(kw, (i-1)*50) for i in range(1, 5)]

    def get_data(self, url):
        print(url)
        # 构造请求对象
        request = urllib.request.Request(url, headers=random.choice(self.ua_list))
        # 发送请求,接受响应
        data = urllib.request.urlopen(request).read()
        html = etree.HTML(data)
        return html

    @staticmethod
    def parse_link(html):
        links = html.xpath('//ul[@id="thread_list"]/li//a[contains(@class, "j_th_tit")]/@href')
        return ["http://tieba.baidu.com" + link for link in links]

    def parse_img(self, link):
        # 构造请求对象
        request = urllib.request.Request(link, headers=random.choice(self.ua_list))
        # 发送请求,接受响应
        response = urllib.request.urlopen(request).read()
        return etree.HTML(response)

    @staticmethod
    def parse_data(html):
        imgs = html.xpath('//div[contains(@id, "post_content")]/img[@class="BDE_Image"]')
        for img in imgs:
            img_url = img.get("src")
            filename = "D://girls/" + img_url[-10:]
            urllib.request.urlretrieve(img_url, filename=filename)
            print("正在下载图片%s" % filename)

    def main(self):
        # 1.获取url列表
        urls = self.get_url()
        print(urls)
        # 2.发送请求,获取响应
        for url in urls:
            html = self.get_data(url)
            # 3.解析数据
            links = self.parse_link(html)
            for link in links:
                html = self.parse_img(link)
                self.parse_data(html)


class TieBa02(object):
    # 多线程
    def __init__(self, name):
        self.url = "https://tieba.baidu.com/f?{}&pn={}"
        self.name = name
        self.ua_list = [
            {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)"},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"},
            {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"},
        ]
        # 构造url队列、请求响应队列、数据队列
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.link_queue = Queue()
        self.data_queue = Queue()

    def get_url(self):
        # 对贴吧名称做url转码
        kw = urllib.parse.urlencode({"kw": self.name})
        for i in range(1, 5):
            # 将url放入url_queue
            self.url_queue.put(self.url.format(kw, (i-1)*50))

    def get_data(self):
        while True:
            # 从url_queue中取出url
            url = self.url_queue.get()
            print(url)
            # 构造请求对象
            request = urllib.request.Request(url, headers=random.choice(self.ua_list))
            # 发送请求,接受响应
            response = urllib.request.urlopen(request)
            # 将html放入html_queue
            self.html_queue.put(etree.HTML(response.read()))
            # 将处理完的url标记为task_done,此时url_queue.size - 1
            self.url_queue.task_done()

    def parse_link(self):
        while True:
            # 从html_queue取出html
            html = self.html_queue.get()
            links = html.xpath('//ul[@id="thread_list"]/li//a[contains(@class, "j_th_tit")]/@href')
            for link in links:
                # 将帖子链接放入link_queue
                self.link_queue.put("http://tieba.baidu.com" + link)
            self.html_queue.task_done()

    def parse_img(self):
        while True:
            # 从link_queue取出link
            link = self.link_queue.get()
            # 构造请求对象
            request = urllib.request.Request(link, headers=random.choice(self.ua_list))
            # 发送请求,接受响应
            response = urllib.request.urlopen(request)
            # 将数据放入data_queue
            self.data_queue.put(etree.HTML(response.read()))
            self.link_queue.task_done()

    def parse_data(self):
        while True:
            # 从data_queue取出data
            html = self.data_queue.get()
            imgs = html.xpath('//div[contains(@id, "post_content")]/img[@class="BDE_Image"]')
            for img in imgs:
                img_url = img.get("src")
                filename = "D://girls/" + img_url[-10:]
                urllib.request.urlretrieve(img_url, filename=filename)
                print("正在下载图片%s" % filename)
            self.data_queue.task_done()

    def main(self):
        threads = []
        # 1.获取url列表
        t_url = threading.Thread(target=self.get_url)
        threads.append(t_url)
        # 2.发送请求,获取响应
        for i in range(1, 5):
            t_link = threading.Thread(target=self.get_data)
            threads.append(t_link)
        # 3.解析数据
        for i in range(1, 5):
            t_img = threading.Thread(target=self.parse_link)
            threads.append(t_img)
            t_html = threading.Thread(target=self.parse_img)
            threads.append(t_html)
            t_parse = threading.Thread(target=self.parse_data)
            threads.append(t_parse)
        for t in threads:
            t.setDaemon(True)
            t.start()
        for q in (self.url_queue, self.html_queue, self.link_queue, self.data_queue):
            q.join()
        print("全部下载完毕！")


if __name__ == "__main__":
    # tb = TieBa01(input("请输入贴吧名称："))
    tb = TieBa02(input("请输入贴吧名称："))
    tb.main()
