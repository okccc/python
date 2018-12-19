# coding=utf-8
"""
多线程爬虫:
page_queue: 页码队列(page页码)
data_queue: 采集队列(html源码)
CrawlThread: 采集线程
ParseThread: 解析线程

queue部分:
1、Queue(maxsize): 创建一个队列并指定大小(Create a queue object with a given maximum size)
2、queue.put(self, item, block=True, timeout=None): 往队列中添加一个元素(Put an item into the queue)
3、queue.get(self, block=True, timeout=None): 从队列中移除并返回一个元素(Remove and return an item from the queue)
  block=True(默认): 如果对列为空,线程不会结束而是进入阻塞状态,直到队列有新的数据
  block=False: 如果队列为空,就弹出queue.Empty异常

thread部分:
"""

from threading import Thread, Lock
from queue import Queue
import requests
from lxml import etree
import json
import time

# 采集线程类
class CrawlThread(Thread):

    def __init__(self, crawl_name, page_queue, data_queue):
        """
        :param crawl:
        :param page_queue:
        :param data_queue:
        """

        # 调用父类初始化方法
        super(CrawlThread, self).__init__()

        # 线程名
        self.crawl_name = crawl_name
        # 页码队列
        self.page_queue = page_queue
        # 数据队列
        self.data_queue = data_queue

        # 请求头
        self.headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}

    # 重写run方法
    def run(self):
        print("%s 已启动" % self.crawl_name)

        while not crawl_exit:
            try:
                # url前缀
                url = "https://www.qiushibaike.com/8hr/page/"
                # 从page_queue取出一个page
                page = self.page_queue.get(False)
                # 拼接完整url
                full_url = url + str(page)
                print(full_url)

                # 发送get请求
                response = requests.get(full_url, headers=self.headers)
                # 获取html源码
                text = response.text
                # 休眠线程
                time.sleep(1)
                # 将html源码放入data_queue
                self.data_queue.put(text)
            except:
                pass
        print("%s 已结束" % self.crawl_name)


# 解析线程类
class ParseThread(Thread):

    def __init__(self, parse_name, data_queue, filename, lock):
        """
        :param parse_name:
        :param data_queue:
        :param filename:
        :param lock:
        """

        # 调用父类初始化方法
        super(ParseThread, self).__init__()

        # 线程名
        self.parse_name = parse_name
        # 数据队列
        self.data_queue = data_queue
        # 文件名
        self.filename = filename
        # 锁对象
        self.lock = lock

    # 重写run方法
    def run(self):
        print("%s 已启动" % self.parse_name)

        while not parse_exit:
            try:
                # 从date_queue队列取数据
                text = self.data_queue.get(False)
                # 调用解析方法
                self.parse(text)
            except:
                pass

        print("%s 已结束" % self.parse_name)

    def parse(self, text):
        """
        xpath表达式解析html源代码
        :param text:
        :return:
        """

        # 解析HTML文档为HTML DOM(XML)模型
        html = etree.HTML(text)
        # 返回所有段子的节点位置,contains()模糊查询: 第一个参数是要匹配的标签,第二个参数是标签名的部分内容
        node_list = html.xpath('//div[contains(@id, "qiushi_tag")]')
        print(node_list)
        # print(type(node_list))  # <class 'list'>
        # 遍历列表
        for node in node_list:
            # 用户头像链接(xpath表达式返回的是list,根据索引取数据)
            imgurl = node.xpath('.//div[@class="author clearfix"]//img/@src')[0]
            # print(imgurl)
            # 用户姓名
            username = node.xpath('.//div[@class="author clearfix"]//h2')[0].text.replace('\n', '')
            # print(username)
            # 段子内容
            content = node.xpath('.//div[@class="content"]/span')[0].text.replace('\n', '')
            # print(content)
            # 点赞次数
            vote = node.xpath('.//span[@class="stats-vote"]/i')[0].text
            # print(vote)
            # 评论次数
            comments = node.xpath('.//span[@class="stats-comments"]//i')[0].text
            # print(comments)
            # 往字典添加数据
            items = {
                "imgurl": imgurl,
                "username": username,
                "content": content,
                "vote": vote,
                "comments": comments
            }
            # 将Python对象序列化成Json字符串
            data = json.dumps(items, ensure_ascii=False)
            # 写入本地文件
            with self.lock:
                self.filename.write(data + "\n")

crawl_exit = False
parse_exit = False

def main():
    # 页码队列(限定20页)
    page_queue = Queue(maxsize=20)
    # 往队列添加元素
    for i in range(1, 21):
        page_queue.put(i)
    # 采集队列(页面的html源码,参数为空表示不限制大小)
    data_queue = Queue()

    # 创建锁对象
    lock = Lock()
    # 创建存json数据的文件
    filename = open('C://Users/Public/Downloads/qiubai.json', 'a', encoding='utf-8')

    # 采集线程名称
    crawl_list = ['carwl-1', 'carwl-2', 'carwl-3']
    # 存放采集线程对象的列表
    crawl_thread = []
    # 遍历名称
    for crawl_name in crawl_list:
        # 创建采集线程对象
        thread = CrawlThread(crawl_name, page_queue, data_queue)
        # 启动线程
        thread.start()
        # 往列表添加线程对象
        crawl_thread.append(thread)

    # 解析线程名称
    parse_list = ['parse-1', 'parse-2', 'parse-3']
    # 存放解析线程对象的列表
    parse_thread = []
    # 遍历名称
    for parse_name in parse_list:
        # 创建解析线程对象
        thread = ParseThread(parse_name, data_queue, filename, lock)
        # 启动线程
        thread.start()
        # 往列表添加线程对象
        parse_thread.append(thread)

    # 判断page_queue是否为空
    while not page_queue.empty():
        # 不为空就跳过
        pass

    # 如果page_queue为空,采集线程退出循环
    global crawl_exit
    crawl_exit = True
    print("page_queue为空")

    # 给线程加入阻塞
    for thread in crawl_thread:
        thread.join()
        print('1')

    # 判断data_queue是否为空
    while not data_queue.empty():
        # 不为空就跳过
        pass

    # 如果data_queue为空,采集线程退出循环
    global parse_exit
    parse_exit = True
    print("data_queue为空")

    # 给线程加入阻塞
    for thread in parse_thread:
        thread.join()
        print('2')

    with lock:
        # 关闭文件
        filename.close()
    print("thanks for use!")

if __name__ == "__main__":
    main()
