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
from queue import Queue  # 线程安全
from fake_useragent import UserAgent

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S %p"
)


class QiuBai01(object):
    # 单线程
    def __init__(self):
        self.url = "https://www.qiushibaike.com/hot/page/{}/"
        self.ua = UserAgent()

    def get_url(self):
        return [self.url.format(i) for i in range(1, 14)]

    def get_data(self, url):
        print(url)
        response = requests.get(url, headers={"User-Agent": self.ua.random})
        return etree.HTML(response.text)

    @staticmethod
    def parse_data(html):
        # contains()模糊查询: 参数一是属性,参数二是属性值包含的部分内容
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
        with open("D://qiubai.json", "a", encoding="utf8") as f:
            for item in items:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

    def main(self):
        # 1.获取url
        urls = self.get_url()
        # 遍历url
        for url in urls:
            # 2.发送请求,获取响应
            html = self.get_data(url)
            # 3.解析数据
            items = self.parse_data(html)
            # 4.保存数据
            self.save_data(items)


class QiuBai02(object):
    # 多线程
    def __init__(self):
        self.url = "https://www.qiushibaike.com/hot/page/{}/"
        self.ua = UserAgent()
        # 构造url队列、请求响应队列、解析数据队列
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.item_queue = Queue()

    def get_url(self):
        # return [self.url.format(i) for i in range(1, 14)]
        for i in range(1, 14):
            # 将url放入队列
            self.url_queue.put(self.url.format(i))

    def get_data(self):
        # 写死循环让该线程一直做这件事
        while True:
            # 从url_queue取出url
            url = self.url_queue.get()
            print(url)
            response = requests.get(url, headers={"User-Agent": self.ua.random})
            # return etree.HTML(response.text)

            # 将html源码放入html_queue
            self.html_queue.put(etree.HTML(response.text))
            # 将处理完的url标记为task_done,此时url_queue.qsize - 1
            self.url_queue.task_done()

    def parse_data(self):
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

            # 将items放入item_queue
            self.item_queue.put(items)
            # 将处理完的html标记为task_done
            self.html_queue.task_done()

    def save_data(self):
        while True:
            # 从item_queue取出item
            items = self.item_queue.get()
            with open("D://qiubai.json", "a", encoding="utf8") as f:
                for item in items:
                    f.write(json.dumps(item, ensure_ascii=False) + "\n")
            # 将处理完的items标记为task_donen
            self.item_queue.task_done()

    def main(self):
        threads = []
        # 1.获取url列表
        t_url = threading.Thread(target=self.get_url)
        threads.append(t_url)
        # 2.发送请求,获取响应
        for i in range(10):
            # 爬虫速度主要慢在网络传输,可以使用多线程发送请求
            t_html = threading.Thread(target=self.get_data)
            threads.append(t_html)
        # 3.解析数据
        for i in range(10):
            # 使用多线程提取数据
            t_parse = threading.Thread(target=self.parse_data)
            threads.append(t_parse)
        # 4.保存数据
        t_save = threading.Thread(target=self.save_data)
        threads.append(t_save)
        for t in threads:
            # 由于该子线程是死循环,需要在调用start()之前将其设置为守护线程,表示该线程不重要,当主线程结束时不用等待该子线程直接退出
            t.setDaemon(daemonic=True)
            t.start()
        for q in [self.url_queue, self.html_queue, self.item_queue]:
            # 让主线程block,等待queue中的items全部处理完
            q.join()
        print("任务全部结束,主线程over!")
        # while True:
        #     print(threading.enumerate())
        #     time.sleep(1)


if __name__ == "__main__":
    # qb = QiuBai01()
    qb = QiuBai02()
    qb.main()
