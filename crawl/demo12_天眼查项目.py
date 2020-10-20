# coding=utf-8
import codecs
import csv
import logging
import threading
from queue import Queue
import time

import pymysql
import requests
from lxml import etree

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S %p"
)


class TYC(object):
    def __init__(self):
        # 搜索页
        self.search_url = 'https://www.tianyancha.com/search?key={}'
        # 登录页
        self.login_url = ''
        # 请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
        }
        # 数据库配置
        # self.config = {
        #     "host": "10.9.157.245",
        #     # "host": "localhost",
        #     "port": 3306,
        #     "user": "root",
        #     "password": "ldaI00Uivwp",
        #     # "password": "root",
        #     "db": "hawaiidb",
        #     # "db": "test",
        #     "charset": "utf8",
        #     "cursorclass": pymysql.cursors.DictCursor  # 以dict格式返回数据
        # }
        # csv文件表头
        self.fieldnames = ['register_money', 'actual_money', 'create_date', 'state', 'code1', 'code2', 'code3', 'code4', 'company_type', 'industry',
                    'register_office', 'operate_period', 'taxpayer_qualification', 'staff_num', 'insured_num']
        # 构造url队列、请求响应队列、数据队列
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.items = []
        # 先登录

    # def login(self):
    #     self.session = requests.session()
    #     self.session.post()

    def get_url(self):
        """获取url列表页"""
        # 读取文件获取商户名称
        with open("C://Users/admin/Desktop/shop.txt", encoding="utf8") as f1:
            shops = f1.readlines()
            # print(shops)
        for i in shops:
            response = requests.get(self.search_url.format(i[:-1]))
            html = etree.HTML(response.text)
            urls = html.xpath('//div[@class="header"]/a/@href')
            print(urls)
            if urls:
                for url in urls:
                    print(url)
                    self.url_queue.put(url)

    def get_data(self):
        """发送get请求"""
        while True:
            # 从url_queue获取url
            url = self.url_queue.get()
            response = requests.get(url, headers=self.headers)
            html = etree.HTML(response.text)
            # 将html放入html_queue
            self.html_queue.put(html)
            # 将处理完的url_queue标记为task_done
            self.url_queue.task_done()

    def parse_data(self):
        """解析数据"""
        while True:
            # 从html_queue获取html
            html = self.html_queue.get()
            # 解析数据
            tbody = html.xpath('//table[contains(@class,"border-top-none")]/tbody')[0]
            register_money = tbody.xpath('./tr[1]/td[2]//text()')[0]
            actual_money = tbody.xpath('./tr[1]/td[4]//text()')[0]
            create_date = tbody.xpath('./tr[2]/td[2]//text()')[0]
            state = tbody.xpath('./tr[2]/td[4]//text()')[0]
            code1 = tbody.xpath('./tr[3]/td[2]//text()')[0]
            code2 = tbody.xpath('./tr[3]/td[4]//text()')[0]
            code3 = tbody.xpath('./tr[4]/td[2]//text()')[0]
            code4 = tbody.xpath('./tr[4]/td[4]//text()')[0]
            company_type = tbody.xpath('./tr[5]/td[2]//text()')[0]
            industry = tbody.xpath('./tr[5]/td[4]//text()')[0]
            register_office = tbody.xpath('./tr[6]/td[4]//text()')[0]
            operate_period = tbody.xpath('./tr[7]/td[2]//text()')[0]
            taxpayer_qualification = tbody.xpath('./tr[7]/td[4]//text()')[0]
            staff_num = tbody.xpath('./tr[8]/td[2]//text()')[0]
            insured_num = tbody.xpath('./tr[8]/td[4]//text()')[0]
            item = (register_money, actual_money, create_date, state, code1, code2, code3, code4, company_type, industry,
                    register_office, operate_period, taxpayer_qualification, staff_num, insured_num)
            # 将items放入item_queue
            self.items.append(item)
            # 将处理完的html_queue标记为task_done
            self.html_queue.task_done()

    def save_data(self):
        # 解决excel打开csv文件中文乱码问题
        with open("D://tyc.csv", "wb") as file:
            # 写入windows需要确认编码的字符
            file.write(codecs.BOM_UTF8)
        # 追加写入数据
        with open("D://tyc.csv", "a", encoding="utf-8", newline="") as file:
            # 创建writer对象
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            # 第一行写入表头
            writer.writeheader()
            # 然后写入多行数据
            writer.writerows(self.items)

    def main(self):
        # 线程列表
        threads = []
        # 获取url列表
        self.get_url()
        print(self.url_queue.qsize())
        # 多线程操作部分
        # for i in range(5):
        #     # 2.发送请求获取响应
        #     t_get = threading.Thread(target=self.get_data)
        #     threads.append(t_get)
        # for i in range(5):
        #     # 3.解析响应数据
        #     t_parse = threading.Thread(target=self.parse_data)
        #     threads.append(t_parse)
        # # 4.保存数据
        # self.save_data()
        # for t in threads:
        #     # 由于子线程是死循环,要在开启之前将其设为守护线程表示该线程不重要,当主线程结束时不用等待子线程直接退出
        #     t.setDaemon(daemonic=True)
        #     t.start()
        # for q in (self.url_queue, self.html_queue):
        #     # 让主线程在此处block,等待queue中的items全部处理完
        #     q.join()


if __name__ == '__main__':
    tyc = TYC()
    tyc.main()