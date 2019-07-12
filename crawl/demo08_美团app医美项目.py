# coding=utf-8
import requests
from selenium import webdriver
from queue import Queue
import time
import json
import pymysql
import threading
import logging

logging.basicConfig(
    level=logging.INFO,
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
            "host": "10.9.157.245",
            "port": 3306,
            "user": "root",
            "password": "ldaI00Uivwp",
            "db": "hawaiidb",
            "charset": "utf8",
            "cursorclass": pymysql.cursors.DictCursor  # 以dict格式返回数据
        }
        # 构造url队列、请求响应队列、数据队列
        self.url_queue = Queue()
        self.data_queue = Queue()
        self.item_queue = Queue()

    def scroll(self):
        """控制滚动条统计每个cityid的tagid对应的下拉次数count(pageno)"""
        # 创建Chrome对象
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        driver = webdriver.Chrome(executable_path="D://chromedriver/chromedriver.exe", options=options)
        # 城市编号
        cityids = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90]
        # 医学美容分类编号
        tagids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 54, 123, 156, 157, 158]
        metas = []
        for cityid in cityids:
            for tagid in tagids:
                # 打开页面
                driver.get(self.addr_url.format(cityid, tagid))
                # 新页面刷新很慢,等待3秒
                time.sleep(3)
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
                    time.sleep(0.5)
                    count += 1
                # 统计每个cityid的tagid对应的下拉次数count
                metas.append((cityid, tagid, count))
                time.sleep(0.5)
        # 退出浏览器
        driver.quit()
        return metas

    def get_url(self, metas):
        """获取所有url"""
        for meta in metas:
            for i in range(1, meta[2]):
                url = self.ajax_url.format(meta[0], meta[1], i)
                # 将url放入url_queue
                self.url_queue.put(url)

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
                ext_infos = shop['extInfo']
                product_infos = shop['productInfos']
                if ext_infos:
                    for info in ext_infos:
                        info_id = info['id']
                        info_link = info['linkUrl']
                        info_title = info['title']
                        info_price = info['price']
                        info_saled = info['saledTimeDesc'] if info['saledTimeDesc'] else '已售0'
                        item = [shop_id, shop_name, info_id, info_link, info_title, info_price, info_saled,
                                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())]
                        items.append(item)
                elif product_infos:
                    for info in product_infos:
                        info_id = info['infoId']
                        info_link = info['linkUrl']
                        info_title = info['title']
                        info_price = info['currentPrice']
                        info_saled = info['saledTimeDesc'] if info['saledTimeDesc'] else '已售0'
                        item = [shop_id, shop_name, info_id, info_link, info_title, info_price, info_saled,
                                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())]
                        items.append(item)
                else:
                    continue
            print(items)
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
            conn = pymysql.connect(**self.config)
            cur = conn.cursor()
            try:
                # 往数据库写数据(覆盖)
                sql = "replace into dw_meituan_info values(%s,%s,%s,%s,%s,%s,%s,%s)"
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
        # 1.下拉滚动条获取(cityid, tagid, count)
        metas = self.scroll()
        # 2.获取url列表
        t_url = threading.Thread(target=self.get_url, args=(metas,))
        thread_list.append(t_url)
        print(self.url_queue.qsize())
        for i in range(20):
            # 3.发送请求,获取响应
            t_get = threading.Thread(target=self.get_data)
            thread_list.append(t_get)
        for i in range(10):
            # 4.解析数据
            t_parse = threading.Thread(target=self.parse_data)
            thread_list.append(t_parse)
        for i in range(10):
            # 5.保存数据
            t_save = threading.Thread(target=self.save_data)
            thread_list.append(t_save)
        for t in thread_list:
            # 将死循环的子线程设置成守护线程
            t.setDaemon(daemonic=True)
            t.start()
        for q in (self.url_queue, self.data_queue, self.item_queue):
            q.join()


if __name__ == '__main__':
    mt = MT()
    mt.main()