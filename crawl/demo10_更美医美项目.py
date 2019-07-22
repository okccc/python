# coding=utf-8
import requests
from lxml import etree
from queue import Queue
import time
import pymysql
import threading
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S %p"
)


class GM(object):
    def __init__(self):
        # 请求地址
        self.url = 'https://www.igengmei.com/hospital_list/?page={}'
        # 请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
        }
        # 数据库配置
        self.config = {
            "host": "10.9.157.245",
            # "host": "localhost",
            "port": 3306,
            "user": "root",
            "password": "ldaI00Uivwp",
            # "password": "root",
            "db": "hawaiidb",
            # "db": "test",
            "charset": "utf8",
            "cursorclass": pymysql.cursors.DictCursor  # 以dict格式返回数据
        }
        # 构造队列
        self.url_queue = Queue()
        self.link_queue = Queue()
        self.item_queue = Queue()

    def get_url(self):
        for i in range(1, 150):
            # 将列表页url放入url_queue
            self.url_queue.put(self.url.format(i))

    def get_list_data(self):
        while True:
            # 从url_queue获取列表页url
            url = self.url_queue.get()
            print(url)
            # 获取医院连接
            response = requests.get(url, headers=self.headers)
            html = etree.HTML(response.text)
            # 获取当前页所有医院链接
            links = html.xpath('//div[@class="expert-info-tag"]//a/@href')
            for link in links:
                # 将link放入link_queue
                self.link_queue.put("https://www.igengmei.com" + link)
            self.url_queue.task_done()

    def get_detail_data(self):
        while True:
            # 从link_queue取出link
            link = self.link_queue.get()
            # 获取医美项目
            response = requests.get(link, headers=self.headers)
            html = etree.HTML(response.text)
            # 获取医院名称
            hospital_id = html.xpath('//div[@class="expert-info"]/@data-id')[0]
            hospital_name = html.xpath('//h1/text()')[0]
            items = []
            # 检查该医院是否有查看更多按钮
            promotion_list_links = html.xpath('//div[@class="promotion-content content"]//p[@class="more f-right"]/a/@href')
            if len(promotion_list_links) > 0:
                # 获取点击查看更多按钮后的页面
                promotion_list_link = "https://www.igengmei.com" + promotion_list_links[0]
                response = requests.get(promotion_list_link, headers=self.headers)
                html = etree.HTML(response.text)
                a_list = html.xpath('//a[@class="commodity"]')
                for a in a_list:
                    product_id = a.xpath('./@href')[0].split('/')[-2]
                    product_title = a.xpath('.//p/text()')[0].split('】')[-1]
                    price = a.xpath('.//em[@class="num-price"]/text()')[0]
                    order_cnt_temp = a.xpath('.//em[@class="green-color"]/text()')
                    order_cnt = '已预约' + order_cnt_temp[0] if order_cnt_temp else '已预约0'
                    item = [hospital_id, hospital_name, product_id, product_title, price, order_cnt,
                            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())]
                    items.append(item)
            else:
                div_list = html.xpath('//div[@class="promotion-item"]/div')
                for div in div_list:
                    product_id = div.xpath('./a/@href')[0].split('/')[-2]
                    product_title = div.xpath('./p[1]/text()')[0].split('】')[-1]
                    price = div.xpath('./p[2]/text()')[0]
                    order_cnt = div.xpath('.//span/text()')[0]
                    item = [hospital_id, hospital_name, product_id, product_title, price, order_cnt, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())]
                    items.append(item)
            # 将items放入item_queue
            self.item_queue.put(items)
            self.link_queue.task_done()

    def save_data(self):
        """保存数据"""
        while True:
            # 从item_queue取出items
            items = self.item_queue.get()
            print(items)
            conn = pymysql.connect(**self.config)
            cur = conn.cursor()
            try:
                # 往数据库写数据(覆盖)
                sql = "REPLACE INTO dw_gengmei_info VALUES(%s,%s,%s,%s,%s,%s,%s)"
                cur.executemany(sql, items)
                conn.commit()
            except Exception as e:
                print(e)
            finally:
                cur.close()
                conn.close()
                # 将处理完的items标记为task_done
                self.item_queue.task_done()

    def main(self):
        # 线程列表
        thread_list = []
        # 1.获取url列表
        self.get_url()
        print(self.url_queue.qsize())
        for i in range(5):
            # 2.请求列表页数据
            t_page = threading.Thread(target=self.get_list_data)
            thread_list.append(t_page)
        for i in range(5):
            # 3.请求详情页数据
            t_detail = threading.Thread(target=self.get_detail_data)
            thread_list.append(t_detail)
        for i in range(10):
            # 4.保存数据
            t_save = threading.Thread(target=self.save_data)
            thread_list.append(t_save)
        for t in thread_list:
            # 将死循环的子线程设置成守护线程,表示该线程不重要,主线程结束子线程也结束
            t.setDaemon(daemonic=True)
            t.start()
        for q in (self.url_queue, self.link_queue, self.item_queue):
            # 让主线程在此处block,等待queue中的items全部处理完
            q.join()


if __name__ == '__main__':
    gm = GM()
    gm.main()