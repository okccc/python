# coding=utf-8
"""
错误: 92行--UnicodeEncodeError: 'gbk' codec can't encode character '\ue415' in position 275: illegal multibyte sequence
原因: windows文件默认gbk编码,Python解释器会用gbk编码去解析爬取的网络数据流data,然而此时data是已经decode过的Unicode编码,导致报错
解决方案: 使用open()函数时,应该指定参数encoding='utf-8'
"""

import requests
from lxml import etree
import json
import logging
import threading
from queue import Queue

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S %p"
)


class QiuBai01(object):
    # 单线程爬虫
    def __init__(self):
        self.url = "https://www.qiushibaike.com/hot/page/{}/"
        self.headers = {"User-Agent": "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11"}

    def get_url(self):
        return [self.url.format(i) for i in range(1, 14)]

    def parse_url(self, url):
        print(url)
        response = requests.get(url, headers=self.headers)
        return etree.HTML(response.text)

    @staticmethod
    def extract_data(html):
        # contains()模糊查询: 第一个参数是要匹配的标签,第二个参数是标签名的部分内容
        nodes = html.xpath('//div[contains(@id, "qiushi_tag")]')
        items = []
        for node in nodes:
            # 用户头像链接
            img_url_temp = node.xpath('.//div[@class="author clearfix"]//img/@src')
            img_url = "https:" + img_url_temp[0]
            # 用户姓名
            username_temp = node.xpath('.//div[@class="author clearfix"]//h2/text()')
            username = username_temp[0].replace("\n", "")
            # 段子内容
            contents = node.xpath('.//div[@class="content"]/span/text()')
            content = [content.replace("\n", "") for content in contents]
            # 段子图片
            content_img_url_temp = node.xpath('.//div[@class="thumb"]/a/img/@src')
            content_img_url = "https:" + content_img_url_temp[0] if len(content_img_url_temp) > 0 else None
            # 点赞次数
            vote = node.xpath('.//span[@class="stats-vote"]/i/text()')[0]
            # 评论次数
            comments = node.xpath('.//span[@class="stats-comments"]//i/text()')[0]
            item = {
                "img_url": img_url,
                "username": username,
                "content": content,
                "content_img_url": content_img_url,
                "vote": vote,
                "comments": comments,
            }
            items.append(item)
        return items

    @staticmethod
    def save_data(items):
        with open("./result.json", "a", encoding="utf8") as f:
            for item in items:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    def main(self):
        # 1.获取url
        urls = self.get_url()
        # 2.发送请求,获取响应
        for url in urls:
            html = self.parse_url(url)
            # 3.提取数据
            items = self.extract_data(html)
            # 4.保存数据
            self.save_data(items)


class QiuBai02(object):
    # 多线程爬虫
    def __init__(self):
        self.url = "https://www.qiushibaike.com/hot/page/{}/"
        self.headers = {"User-Agent": "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11"}
        # 构造url队列、请求队列、数据队列
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.item_queue = Queue()

    def get_url(self):
        # return [self.url.format(i) for i in range(1, 14)]
        for i in range(1, 14):
            # 将url放入队列
            self.url_queue.put(self.url.format(i))

    def parse_url(self):
        # 写死循环让该线程一直做这件事
        while True:
            # 从url_queue取出url
            url = self.url_queue.get()
            print(url)
            response = requests.get(url, headers=self.headers)
            # return etree.HTML(response.text)

            # 将html源码放入队列
            self.html_queue.put(etree.HTML(response.text))
            # 队列task_done()后get()才会减1
            self.url_queue.task_done()

    def extract_data(self):
        while True:
            # 从html_queue取出html
            html = self.html_queue.get()
            # contains()模糊查询: 第一个参数是要匹配的标签,第二个参数是标签名的部分内容
            nodes = html.xpath('//div[contains(@id, "qiushi_tag")]')
            items = []
            for node in nodes:
                # 用户头像链接
                img_url_temp = node.xpath('.//div[@class="author clearfix"]//img/@src')
                img_url = "https:" + img_url_temp[0]
                # 用户姓名
                username_temp = node.xpath('.//div[@class="author clearfix"]//h2/text()')
                username = username_temp[0].replace("\n", "")
                # 段子内容
                contents = node.xpath('.//div[@class="content"]/span/text()')
                content = [content.replace("\n", "") for content in contents]
                # 段子图片
                content_img_url_temp = node.xpath('.//div[@class="thumb"]/a/img/@src')
                content_img_url = "https:" + content_img_url_temp[0] if len(content_img_url_temp) > 0 else None
                # 点赞次数
                vote = node.xpath('.//span[@class="stats-vote"]/i/text()')[0]
                # 评论次数
                comments = node.xpath('.//span[@class="stats-comments"]//i/text()')[0]
                item = {
                    "img_url": img_url,
                    "username": username,
                    "content": content,
                    "content_img_url": content_img_url,
                    "vote": vote,
                    "comments": comments,
                }
                items.append(item)
            # return items

            # 将items放入队列
            self.item_queue.put(items)
            self.html_queue.task_done()

    def save_data(self):
        while True:
            # 从item_queue取出item
            items = self.item_queue.get()
            with open("D://result.json", "a", encoding="utf8") as f:
                for item in items:
                    f.write(json.dumps(item, ensure_ascii=False) + "\n")
            self.item_queue.task_done()

    def main(self):
        threads = []
        # 1.获取url列表
        t_url = threading.Thread(target=self.get_url)
        threads.append(t_url)
        # 2.发送请求,获取响应
        for i in range(1, 10):
            # 爬虫速度主要慢在网络传输,可以使用多线程发送请求
            t_html = threading.Thread(target=self.parse_url)
            threads.append(t_html)
        # 3.提取数据
        for i in range(1, 3):
            # 使用多线程提取数据
            t_item = threading.Thread(target=self.extract_data)
            threads.append(t_item)
        # 4.保存数据
        t_save = threading.Thread(target=self.save_data)
        threads.append(t_save)
        for t in threads:
            # 由于子线程是while死循环将线程设置为守护线程
            t.setDaemon(True)
            t.start()
        for q in [self.url_queue, self.html_queue, self.item_queue]:
            # 让主线程阻塞,等待队列中的任务完成
            q.join()
        print("任务全部结束,主线程over!")


if __name__ == "__main__":
    # qb = QiuBai01()
    qb = QiuBai02()
    qb.main()
