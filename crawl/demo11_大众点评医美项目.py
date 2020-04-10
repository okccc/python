import requests
from lxml import etree
from queue import Queue
import pymysql
import time
import threading
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S %p"
)


class DP(object):
    def __init__(self):
        # 城市列表页
        self.city_url = 'http://www.dianping.com/citylist'
        # 医疗健康页
        self.medical_url = 'http://www.dianping.com/shanghai/medical'
        # 医院列表页(城市和分类不确定)
        self.hospital_url = 'http://www.dianping.com/{}/ch85/{}'
        # 请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
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
        # 构造meta队列、url队列、数据队列
        self.meta_queue = Queue()  # (city, code)
        self.url_queue = Queue()
        self.item_queue = Queue()

    def get_city_sort(self):
        """
        获取城市和医院分类编号
        """
        # 城市名称
        citys = []
        response = requests.get(url=self.city_url, headers=self.headers)
        html = etree.HTML(response.text)
        # href_list = html.xpath('//div[@class="main-citylist"]//li//a/@href')
        href_list = html.xpath('//div[contains(@class,"hotcity")]//a/@href')
        for each in href_list:
            city = each.split('/')[-1]
            citys.append(city)
        citys = citys[:-3]
        other = ['changchun', 'changsha', 'changzhou', 'dalian', 'dongguan', 'fuzhou', 'foshan', 'guiyang', 'haikou',
                 'haerbin', 'hefei', 'huhehaote', 'jinan', 'kunming', 'lanzhou', 'ningbo', 'nanchang', 'nanning',
                 'qingdao', 'quanzhou', 'shenyang', 'taiyuan', 'wuxi', 'xiamen', 'zhengzhou']
        citys.extend(other)
        # 医院分类
        codes = ['g183']
        # response = requests.get(url=self.medical_url, headers=self.headers)
        # html = etree.HTML(response.text)
        # href_list = html.xpath('//li[@class="term-list-item"][2]//a/@href')
        # for each in href_list:
        #     code = each.split('/')[-1]
        #     codes.append(code)
        # 放入队列
        for city in citys:
            for code in codes:
                self.meta_queue.put((city, code))

    def get_url(self):
        """
        组合城市和编号获取url列表
        """
        while True:
            city, code = self.meta_queue.get()
            hospital_url = self.hospital_url.format(city, code)
            print(hospital_url)
            self.url_queue.put(hospital_url)
            response = requests.get(url=hospital_url, headers=self.headers)
            html = etree.HTML(response.text)
            # 判断是否有下一页
            next_page = html.xpath('//div[@class="page"]/a[@class="next"]/text()')
            print(next_page)
            if next_page:
                # 倒数第二个链接就是最大页码数
                num = html.xpath('//div[@class="page"]/a[last()-1]/text()')[0]
                for i in range(2, int(num)+1):
                    url_next = hospital_url + 'p' + str(i)
                    print(url_next)
                    self.url_queue.put(url_next)
            self.meta_queue.task_done()

    def parse_url(self):
        """
        解析列表页
        """
        while True:
            url = self.url_queue.get()
            response = requests.get(url, headers=self.headers)
            html = etree.HTML(response.text)
            hospital_list = html.xpath('//div[contains(@class,"shop-list")]//li//a/h4/text()')
            items = []
            for each in hospital_list:
                item = [each, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())]
                items.append(item)
            self.item_queue.put(items)
            self.url_queue.task_done()

    def save_date(self):
        """
        保存数据
        """
        while True:
            items = self.item_queue.get()
            print(items)
            conn = pymysql.connect(**self.config)
            cur = conn.cursor()
            try:
                sql = 'replace into dw_dianping_info values(%s, %s)'
                cur.executemany(sql, items)
                conn.commit()
            except Exception as e:
                print(e)
            finally:
                cur.close()
                conn.close()
                self.item_queue.task_done()

    def main(self):
        # 线程列表
        threads = []
        self.get_city_sort()
        print(self.meta_queue.qsize())
        for i in range(3):
            # 获取url列表
            t_url = threading.Thread(target=self.get_url)
            threads.append(t_url)
        for i in range(3):
            # 解析数据
            t_parse = threading.Thread(target=self.parse_url)
            threads.append(t_parse)
        for i in range(3):
            # 保存数据
            t_save = threading.Thread(target=self.save_date)
            threads.append(t_save)
        for t in threads:
            # 将死循环的线程设置成守护线程,表示该线程不重要,主线程结束子线程也结束
            t.setDaemon(daemonic=True)
            t.start()
        for q in (self.meta_queue, self.url_queue, self.item_queue):
            # 让主线程在此处block,等待队列中的items全部处理完
            q.join()


if __name__ == '__main__':
    dp = DP()
    dp.main()