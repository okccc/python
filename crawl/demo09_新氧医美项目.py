# coding=utf-8
import requests
from lxml import etree
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


class SY(object):
    """
    多线程爬虫：
    1.线程安全：Queue的put/get方法默认阻塞,所以是线程安全的
    2.解耦：整个流程中各个模块直接与队列交互,相互之间没有关联,提高代码容错率
    3.速度：对于耗时较长的环节可以多开几个线程并发处理
    """
    def __init__(self):
        # Network-->Headers分析出请求url
        self.home = 'https://y.soyoung.com/yuehui/beijing/'
        self.addr_url = 'https://y.soyoung.com/{}/{}/'  # 省份 类目
        self.ajax_url = 'https://y.soyoung.com/yuehui/shop'
        # 请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Host": "y.soyoung.com",
        }
        # post请求数据
        self.form_data = {
            "district_id": {},  # 省份id: 1~34
            "sort": 0,  # 排序方式: 默认值0
            "menu1_id": {},  # 类目id: [10001, 10020...]
            "index": {}  # shop页码: 对应滚动条下拉次数
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
        # 构造url队列、form_data队列、请求响应队列、数据队列
        self.district_menu1_queue = Queue()  # ((district_name, district_id) (menu1_name, menu1_id))
        self.meta_queue = Queue()  # (district_id, menu1_id, count)
        self.data_queue = Queue()
        self.item_queue = Queue()

    def get_district_menu(self):
        """获取区域和类目信息"""
        response = requests.get(self.home, headers=self.headers)
        html = etree.HTML(response.text)
        # 区域和类目
        districts, menu1s = [], []
        # 区域名称和编号
        district_names = html.xpath('//div[@class="provinces-cape"]/a/@data-pinyin')
        district_ids = html.xpath('//div[@class="provinces-cape"]/a/@data-id')
        for district_name, district_id in zip(district_names, district_ids):
            if district_id not in ['26', '29', '30', '32', '33', '34', '35']:
            # if district_id == '1':
                districts.append((district_name, district_id))
        # 类目名称和编号
        menu1_names = html.xpath('//div[@class="menu-box menu1"]//a/@data-menu1-pinyin')[1:]
        menu1_ids = html.xpath('//div[@class="menu-box menu1"]//a/@data-menu1')[1:]
        for menu1_name, menu1_id in zip(menu1_names, menu1_ids):
            menu1s.append((menu1_name, menu1_id))
        # 返回结果
        return districts, menu1s

    def get_district_menu1(self, districts, menu1s):
        for district in districts:
            for menu1 in menu1s:
                # 将所有(district, menu1)组合放入district_menu1_queue
                self.district_menu1_queue.put((district, menu1))

    def scroll(self):
        """控制滚动条统计每个district_id的menu1_id对应的下拉次数count(index)"""
        # 创建Chrome对象：该方法是多线程并发执行,每个线程都会创建一个driver对象
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
        driver = webdriver.Chrome(executable_path="D://chromedriver/chromedriver.exe", options=options)
        while True:
            if not self.district_menu1_queue.empty():
                # 从url_queue取出元组(district, menu1)并拆包
                district, menu1 = self.district_menu1_queue.get()
                print(district, menu1)
                # 打开页面
                driver.get(self.addr_url.format(district[0], menu1[0]))
                # 新页面刷新很慢,等待3秒
                time.sleep(5)
                # 获取body对象高度的js
                js1 = 'return document.body.scrollHeight'
                # 下拉滚动条的js
                js2 = 'window.scrollTo(0, document.body.scrollHeight)'
                # 先手动往下拉一下,不然while循环条件不成立
                driver.execute_script(js2)
                time.sleep(2)
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
                # 统计每个district_id的menu1_id对应的下拉次数count
                self.meta_queue.put((district[1], menu1[1], count))
                # 将处理完的district_menu1标记为task_done
                self.district_menu1_queue.task_done()
                time.sleep(1)
            else:
                break
        # 退出浏览器
        driver.quit()

    def post_data(self):
        """获取form_data并发送post请求"""
        while True:
            # 从meta_queue获取meta
            meta = self.meta_queue.get()
            print(meta)
            for i in range(meta[2]):
                # post请求数据
                form_data = {
                    "district_id": int(meta[0]),  # 省份id: 1~34
                    "sort": 0,  # 排序方式: 默认值0
                    "menu1_id": int(meta[1]),  # 类目id: [10001, ]
                    "index": i  # shop页码: 对应滚动条下拉次数
                }
                print(form_data)
                # 发送post请求
                response = requests.post(self.ajax_url, data=form_data, headers=self.headers)
                if response.text:
                    dict_data = json.loads(response.text)
                    products = dict_data['responseData']['product_info']
                    # 将products放入data_queue
                    self.data_queue.put(products)
            # 将处理完的form_data标记为task_done
            self.meta_queue.task_done()

    def parse_data(self):
        """解析数据"""
        while True:
            items = []
            # 从data_queue取出data
            products = self.data_queue.get()
            for product in products:
                hospital_id = product['hospital_id']
                hospital_name = product['hospital_name']
                product_id = product['pid']
                product_title = product['title']
                price = product['price_online']
                order_cnt = product['order_cnt']
                item = [hospital_id, hospital_name, product_id, product_title, price, order_cnt,
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())]
                items.append(item)
            # 将items放入item_queue
            self.item_queue.put(items)
            # 将处理完的data_queue标记为task_done
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
                sql = "REPLACE INTO dw_xinyang_info VALUES(%s,%s,%s,%s,%s,%s,%s)"
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
        # 先获取省份和类目信息
        districts, menu1s = self.get_district_menu()
        print(districts, menu1s)
        self.get_district_menu1(districts, menu1s)
        print(self.district_menu1_queue.qsize())
        # 多线程操作部分
        for i in range(10):
            # 1.下拉滚动条获取(district_id, menu1_id, index)
            t_scroll = threading.Thread(target=self.scroll)
            thread_list.append(t_scroll)
        for i in range(10):
            # 2.发送请求,获取响应
            t_post = threading.Thread(target=self.post_data)
            thread_list.append(t_post)
        for i in range(5):
            # 3.解析数据
            t_parse = threading.Thread(target=self.parse_data)
            thread_list.append(t_parse)
        for i in range(5):
            # 4.保存数据
            t_save = threading.Thread(target=self.save_data)
            thread_list.append(t_save)
        for t in thread_list:
            # 将死循环的子线程设置成守护线程,表示该线程不重要,主线程结束子线程也结束
            t.setDaemon(daemonic=True)
            t.start()
            time.sleep(0.5)
        for q in (self.district_menu1_queue, self.meta_queue, self.data_queue, self.item_queue):
            # 让主线程在此处block,等待queue中的items全部处理完
            q.join()


if __name__ == '__main__':
    sy = SY()
    sy.main()