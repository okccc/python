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
        # 登录页
        self.login_url = 'https://account.dianping.com/login?redir=http://www.dianping.com'
        # 城市列表页
        self.city_url = 'http://www.dianping.com/citylist'
        # 医院列表页
        self.hospital_url = 'http://www.dianping.com/{}/ch85/{}'  # 城市 分类
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
        # 构造url队列、请求响应队列、数据队列
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.item_queue = Queue()

    def get_url(self):
        """获取url列表页"""
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
        # 放入url队列
        for city in citys:
            for code in codes:
                # 根据city和code拼接url
                url = self.hospital_url.format(city, code)
                self.url_queue.put(url)
                # # 解析当前页面
                # response = requests.get(url=url, headers=self.headers)
                # html = etree.HTML(response.text)
                # # 判断是否有下一页
                # next_page = html.xpath('//div[@class="page"]/a[@class="next"]/text()')
                # if next_page:
                #     # 倒数第二个链接就是最大页码数
                #     num = html.xpath('//div[@class="page"]/a[last()-1]/text()')[0]
                #     for i in range(2, int(num) + 1):
                #         url_next = url + 'p' + str(i)
                #         self.url_queue.put(url_next)

    def get_data(self):
        """发送get请求"""
        while True:
            # 从url_queue获取url
            url = self.url_queue.get()
            # url = 'http://www.dianping.com/shanghai/ch85/g183p3'
            response = requests.get(url, headers=self.headers)
            html = etree.HTML(response.text)
            # 将html放入html_queue
            self.html_queue.put(html)
            # 判断是否有下一页
            next_page = html.xpath('//div[@class="page"]/a[@class="next"]/text()')
            if next_page:
                # 倒数第二个链接就是最大页码数
                num = html.xpath('//div[@class="page"]/a[last()-1]/text()')[0]
                for i in range(2, int(num) + 1):
                    url_next = url + 'p' + str(i)
                    self.url_queue.put(url_next)
            # 将处理完的url_queue标记为task_done
            self.url_queue.task_done()

    def parse_data(self):
        """解析数据"""
        while True:
            # 从html_queue获取html
            html = self.html_queue.get()
            href_list = html.xpath('//div[contains(@class,"shop-list")]//li/div[2]/div[1]/a[@title]/@href')
            items = []
            # 遍历所有shop
            for href in href_list:
                print(href)
                # 解析详情页
                response = requests.get(url=href, headers=self.headers)
                html = etree.HTML(response.text)
                shop_tmp = html.xpath('//div[@class="breadcrumb"]/a[last()]/text()')
                shop = shop_tmp[0].strip() if len(shop_tmp) > 0 else ''
                city_tmp = html.xpath('//div[@class="breadcrumb"]/a[1]/text()')
                city = city_tmp[0].strip()[:-2] + "市" if len(city_tmp) > 0 else ''
                district_tmp = html.xpath('//span[@itemprop="locality region"]/text()')
                district = district_tmp[0] if len(district_tmp) > 0 else ''
                address_tmp = html.xpath('//span[@itemprop="street-address"]/text()')
                address = address_tmp[0].strip() if len(address_tmp) > 0 else ''
                insert_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                item = (shop, city, district, address, insert_time)
                print(item)
                items.append(item)
            # 将items放入item_queue
            self.item_queue.put(items)
            # 将处理完的html_queue标记为task_done
            self.html_queue.task_done()

    def save_date(self):
        """保存数据"""
        while True:
            # 从item_queue获取item
            items = self.item_queue.get()
            conn = pymysql.connect(**self.config)
            cur = conn.cursor()
            try:
                sql = 'replace into dw_dianping_shop values(%s, %s, %s, %s, %s)'
                cur.executemany(sql, items)
                conn.commit()
            except Exception as e:
                print(e)
            finally:
                cur.close()
                conn.close()
                # 将处理完的item_queue标记为task_done
                self.item_queue.task_done()

    def main(self):
        # 线程列表
        threads = []
        # 1.获取url列表
        self.get_url()
        # 多线程操作部分
        for i in range(5):
            # 2.发送请求获取响应
            t_get = threading.Thread(target=self.get_data)
            threads.append(t_get)
        for i in range(5):
            # 3.解析响应数据
            t_parse = threading.Thread(target=self.parse_data)
            threads.append(t_parse)
        for i in range(5):
            # 4.保存数据
            t_save = threading.Thread(target=self.save_date)
            threads.append(t_save)
        for t in threads:
            # 由于子线程是死循环,要在开启之前将其设为守护线程表示该线程不重要,当主线程结束时不用等待子线程直接退出
            t.setDaemon(daemonic=True)
            t.start()
        for q in (self.url_queue, self.html_queue, self.item_queue):
            # 让主线程在此处block,等待queue中的items全部处理完
            q.join()


if __name__ == '__main__':
    dp = DP()
    dp.main()