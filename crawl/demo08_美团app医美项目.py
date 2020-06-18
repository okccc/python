# coding=utf-8
import requests
from lxml import etree
from selenium import webdriver
from queue import Queue
import time
import pymysql
import threading
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S %p"
)


class MT(object):
    def __init__(self):
        # 抓包分析出请求url(挨个调试WebForms参数,过程略复杂,也是爬虫关键所在)
        self.addr_url = "https://i.meituan.com/cosmetology/wiki.html?cityid={}&tagid={}&wkwebview=1"
        self.ajax_url = "https://i.meituan.com/beauty/medical/channel/shop/ajax/getshops?cityid={}&tagid={}&pageno={}"
        # 请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Host": "i.meituan.com",
        }
        # 数据库配置
        self.config = {
            # "host": "10.9.157.245",
            "host": "localhost",
            "port": 3306,
            "user": "root",
            # "password": "ldaI00Uivwp",
            "password": "root",
            # "db": "hawaiidb",
            "db": "test",
            "charset": "utf8",
            "cursorclass": pymysql.cursors.DictCursor  # 以dict格式返回数据
        }
        # 构造meta队列、url队列、请求响应队列、数据队列
        self.city_tag_queue = Queue()  # (cityid, tagid)
        self.meta_queue = Queue()  # (cityid, tagid, count)
        self.url_queue = Queue()
        self.data_queue = Queue()
        self.item_queue = Queue()

    def get_city_tag(self):
        """获取城市和类目信息"""
        # 城市编号
        cityids = [1, 10, 20, 30, 40, 42, 44, 45, 50, 51, 52, 55, 56, 57, 59, 60, 62, 65, 66, 70, 73, 76, 80, 82, 83, 89, 91]
        # cityids = [1]
        # 医学美容分类编号
        tagids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 54, 123, 156, 157, 158]
        # tagids = [1, 2]
        for cityid in cityids:
            for tagid in tagids:
                # 将所有(cityid, tagid)组合放入city_tag_queue
                self.city_tag_queue.put((cityid, tagid))

    def scroll(self):
        """控制滚动条统计每个cityid的tagid对应的下拉次数count(pageno)"""
        # 创建Chrome对象
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        driver = webdriver.Chrome(executable_path="D://chromedriver/chromedriver.exe", options=options)
        while True:
            if not self.city_tag_queue.empty():
                # 从city_tag_queue取出元组(cityid, tagid)并拆包
                cityid, tagid = self.city_tag_queue.get()
                # 打开页面
                driver.get(self.addr_url.format(cityid, tagid))
                # 新页面刷新很慢,等待3秒
                time.sleep(5)
                # 获取body对象高度的js
                js1 = 'return document.body.scrollHeight'
                # 下拉滚动条的js
                js2 = 'window.scrollTo(0, document.body.scrollHeight)'
                # 先手动往下拉一下,不然while循环条件不成立
                driver.execute_script(js2)
                time.sleep(3)
                # 记录初始高度和循环次数
                old_scroll_height, count = 0, 1
                # 只要往下拉body高度发生变化说明还没到底
                while driver.execute_script(js1) > old_scroll_height:
                    # 给高度重新赋值
                    old_scroll_height = driver.execute_script(js1)
                    # 继续往下拉
                    driver.execute_script(js2)
                    # 等待刷新完成(这个时间根据实际情况设定)
                    time.sleep(1)
                    count += 1
                # 统计每个cityid的tagid对应的下拉次数count
                self.meta_queue.put((cityid, tagid, count))
                # 将处理完的city_tag_queue标记为task_done
                self.city_tag_queue.task_done()
                time.sleep(0.5)
            else:
                break
        # 退出浏览器
        driver.quit()

    def get_url(self):
        """获取所有url"""
        while True:
            # 从meta_queue取出元组(city, tag, count)并拆包
            cityid, tagid, count = self.meta_queue.get()
            for i in range(1, count):
                url = self.ajax_url.format(cityid, tagid, i)
                # 将url放入url_queue
                self.url_queue.put(url)
            # 将处理完的meta_queue标记为task_done
            self.meta_queue.task_done()

    def get_data(self):
        """请求数据"""
        while True:
            # 从url_queue取出url
            url = self.url_queue.get()
            response = requests.get(url, headers=self.headers)
            dict_data = response.json()
            shops = dict_data['data']['shops']
            # 将shops放入data_queue
            if len(shops) > 0:
                self.data_queue.put(shops)
            # 将处理完的url标记为task_done
            self.url_queue.task_done()

    def parse_data(self):
        """解析数据"""
        while True:
            # 从data_queue取出shops
            shops = self.data_queue.get()
            items = []
            for shop in shops:
                shop_id = shop['shopId']
                shop_name = shop['name']
                link = shop['url']
                response = requests.get(link, headers=self.headers)
                html = etree.HTML(response.text)
                address_tmp = html.xpath('//div[@class="poi-address"]/text()')
                address = address_tmp[0] if len(address_tmp) > 0 else ''
                expend_tmp = html.xpath('//span[@class="avg-price"]/text()')
                expend = expend_tmp[0][3:] if len(expend_tmp) > 0 else ''
                star_tmp = html.xpath('//a[@class="react"]//em[@class="star-text"]/text()')
                star = star_tmp[0] if len(star_tmp) > 0 else 0
                num_tmp = html.xpath('//span[@class="pull-right"]/text()')
                num = num_tmp[0][:-3] if len(num_tmp) > 0 else 0
                item = [shop_id, shop_name, address, expend, star, num, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())]
                items.append(item)
                # if ext_infos:
                #     for info in ext_infos:
                #         info_id = info['id']
                #         info_title = info['title']
                #         price = info['price']
                #         saled = info['saledTimeDesc'] if info['saledTimeDesc'] else '已售0'
                #         item = [shop_id, shop_name, info_id, info_title, price, saled,
                #                 time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())]
                #         items.append(item)
                # elif product_infos:
                #     for info in product_infos:
                #         info_id = info['infoId']
                #         info_title = info['title']
                #         price = info['currentPrice']
                #         saled = info['saledTimeDesc'] if info['saledTimeDesc'] else '已售0'
                #         item = [shop_id, shop_name, info_id, info_title, price, saled,
                #                 time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())]
                #         items.append(item)
                # else:
                #     continue
            # 将items放入item_queue
            if len(items) > 0:
                self.item_queue.put(items)
            # 将处理完的shops标记为task_done
            self.data_queue.task_done()

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
                sql = "replace into dw_meituan_shop values(%s,%s,%s,%s,%s,%s,%s)"
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
        # 先获取城市和类目信息
        self.get_city_tag()
        print(self.city_tag_queue.qsize())
        # 线程列表
        thread_list = []
        # 多线程操作部分
        for i in range(10):
            # 1.下拉滚动条获取(cityid, tagid, count)
            t_scroll = threading.Thread(target=self.scroll)
            thread_list.append(t_scroll)
        for i in range(5):
            # 2.获取url列表
            t_url = threading.Thread(target=self.get_url)
            thread_list.append(t_url)
        for i in range(10):
            # 3.发送请求,获取响应
            t_get = threading.Thread(target=self.get_data)
            thread_list.append(t_get)
        for i in range(10):
            # 4.解析数据
            t_parse = threading.Thread(target=self.parse_data)
            thread_list.append(t_parse)
        for i in range(15):
            # 5.保存数据
            t_save = threading.Thread(target=self.save_data)
            thread_list.append(t_save)
        for t in thread_list:
            # 将死循环的子线程设置成守护线程
            t.setDaemon(daemonic=True)
            t.start()
            time.sleep(0.5)
        for q in (self.city_tag_queue, self.meta_queue, self.url_queue, self.data_queue, self.item_queue):
            q.join()


class MT2(object):
    def __init__(self):
        # 列表页
        self.url = 'https://{}.meituan.com/jiankangliren/pn{}/'
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
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
        # 构造url队列,请求响应队列,数据队列
        self.url_queue = Queue()
        self.html_queue = Queue()
        self.item_queue = Queue()

    def get_url(self):
        """获取url列表"""
        # 城市名称
        # citys = ['bj', 'sh', 'gz', 'sz', 'tj', 'xa', 'cq', 'hz', 'nj', 'wh', 'cd', 'cz', 'cc', 'chs', 'dl', 'dg', 'fz', 'fs',
        #          'gy', 'hf', 'hrb', 'jn', 'km', 'nb', 'nn', 'nc', 'qd', 'qz', 'sjz', 'su', 'sy', 'ty', 'wz', 'xm', 'zz']
        citys = ['gz', 'sz']
        for city in citys:
            # 每个城市首页
            url_full = self.url.format(city, 1)
            print(url_full)
            response = requests.get(url_full, headers=self.headers)
            html = etree.HTML(response.text)
            # 判断最大页数
            num = html.xpath('//nav[@class="mt-pagination"]//li[last()-1]//text()')
            print(num)
            if num:
                for i in range(1, int(num[0])+1):
                    # 将url放入url_queue
                    self.url_queue.put(self.url.format(city, i))

    def get_data(self):
        """发送get请求"""
        while True:
            # 从url_queue获取url
            url = self.url_queue.get()
            print(url)
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
            divs = html.xpath('//div[contains(@class,"abstract-item")]')
            items = []
            for each in divs:
                shop = each.xpath('.//a[@class="item-title"]/text()')[0]
                classify_tmp = each.xpath('.//div[@class="item-site-info"]/span[1]/text()')
                print(classify_tmp)
                classify = classify_tmp[0] if len(classify_tmp) > 0 else ''
                address_tmp = each.xpath('.//div[@class="item-site-info"]/span[2]/text()')
                print(address_tmp)
                address = address_tmp[0] if len(address_tmp) > 0 else ''
                try:
                    expend = each.xpath('.//div[@class="item-price-info"]/span/text()')[0]
                except:
                    expend = ''
                star_tmp = each.xpath('.//div[contains(@class,"item-eval-info")]/span[1]/text()')
                star = star_tmp[0] if len(star_tmp) > 0 else ''
                num_tmp = each.xpath('.//div[contains(@class,"item-eval-info")]/span[2]/text()')
                num = num_tmp[0] if len(num_tmp) > 0 else 0
                item = [shop, classify, address, expend, star, num, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())]
                print(item)
                items.append(item)
            # 将items放入item_queue
            self.item_queue.put(items)
            # 将处理完的html_queue标记为task_done
            self.html_queue.task_done()

    def save_date(self):
        """保存数据"""
        while True:
            # 从item_queue获取items
            items = self.item_queue.get()
            print(items)
            conn = pymysql.connect(**self.config)
            cur = conn.cursor()
            try:
                # 往数据库写数据(覆盖)
                sql = "REPLACE INTO dw_meituan_shop VALUES(%s,%s,%s,%s,%s,%s,%s)"
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
        print(self.url_queue.qsize())
        # 多线程操作部分
        for i in range(5):
            # 2.发送请求获取响应
            t_get = threading.Thread(target=self.get_data)
            threads.append(t_get)
        for i in range(5):
            # 3.解析数据
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
        for q in [self.url_queue, self.html_queue, self.item_queue]:
            # 让主线程在此处block,等待queue中的items全部处理完
            q.join()


if __name__ == '__main__':
    mt = MT()
    mt.main()