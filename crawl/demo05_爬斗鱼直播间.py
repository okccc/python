# coding=utf-8
import requests
import json
import threading
from queue import Queue
from selenium import webdriver
import time
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S %p"
)

class DouYu01(object):
    # 1.抓接口之PC端：chrome抓包斗鱼电脑版页面的Network做分析找出请求url
    def __init__(self):
        # 数据接口
        self.url = "https://www.douyu.com/gapi/rkc/directory/0_0/{}"
        # 请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "referer": "https://www.douyu.com/directory/all",
            "x-requested-with": "XMLHttpRequest",
            "accept": "application/json, text/plain, */*",
        }
        # 构造url队列、请求响应队列、数据队列
        self.url_queue = Queue()
        self.room_queue = Queue()
        self.item_queue = Queue()

    def get_url(self):
        # 先求出最大页数
        response = requests.get(self.url.format(1), headers=self.headers)
        dict_data = json.loads(response.text)
        max_page = dict_data["data"]["pgcnt"]
        # 将url放入url_queue
        for i in range(max_page):
            self.url_queue.put(self.url.format(i))

    def get_data(self):
        while True:
            # 从url_queue取出url
            url = self.url_queue.get()
            response = requests.get(url, headers=self.headers)
            dict_data = json.loads(response.text)
            rooms = dict_data["data"]["rl"]
            # 将rooms放入room_queue
            self.room_queue.put(rooms)
            # 将处理完的url标记为task_done,此时url_queue.qsize -1
            self.url_queue.task_done()

    def parse_data(self):
        while True:
            items = []
            # 从room_queue取出rooms
            rooms = self.room_queue.get()
            # 遍历当前页的所有房间
            for room in rooms:
                # 字典生成式取room的部分key和value
                item = {key: room[key] for key in ["rid", "uid", "nn", "rn", "ol", "url", "c2name", "c2url"]}
                item["url"] = "https://www.douyu.com" + item["url"]
                items.append(item)
            # 将items放入itme_queue
            self.item_queue.put(items)
            # 将处理完的rooms标记为task_done
            self.room_queue.task_done()

    def save_data(self):
        while True:
            # 从item_queue取出items
            items = self.item_queue.get()
            with open("images/douyu.json", "a", encoding="utf8") as f:
                for item in items:
                    print(item)
                    f.write(json.dumps(item, ensure_ascii=False, indent=2) + ", ")
            # 将处理完的items标记为task_done
            self.item_queue.task_done()

    def main(self):
        threads = []
        # 1.获取url列表
        self.get_url()
        print(self.url_queue.qsize())
        # 2.发送请求,获取响应
        for i in range(10):
            t1 = threading.Thread(target=self.get_data)
            threads.append(t1)
        # 3.解析数据
        for i in range(10):
            t2 = threading.Thread(target=self.parse_data)
            threads.append(t2)
        # 4.保存数据
        for i in range(10):
            t3 = threading.Thread(target=self.save_data)
            threads.append(t3)
        for t in threads:
            # 由于该子线程是死循环,需要在调用start()之前将其设置为守护线程,表示该线程不重要,当主线程结束时不用等待该子线程直接退出
            t.setDaemon(daemonic=True)
            t.start()
        for q in [self.url_queue, self.room_queue, self.item_queue]:
            # 让主线程block,等待queue中的items全部处理完
            q.join()
        print("任务全部结束,主线程over！")


class DouYu02(object):
    # 2.抓接口之App端：chrome抓包斗鱼手机版页面的Network做分析找出请求url
    def __init__(self):
        # 数据接口
        self.url = "https://m.douyu.com/api/room/list?page={}&type="
        # 请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Mobile Safari/537.36",
            "Referer": "https://m.douyu.com/list/room",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json"
        }
        # 构造url队列、请求响应队列、数据队列
        self.url_queue = Queue()
        self.room_queue = Queue()
        self.item_queue = Queue()

    def get_url(self):
        # 先求出最大页数
        response = requests.get(self.url.format(1), headers=self.headers)
        dict_data = json.loads(response.text)
        max_page = dict_data["data"]["pageCount"]
        # 将url放入url_queue
        for i in range(max_page):
            self.url_queue.put(self.url.format(i))

    def get_data(self):
        while True:
            # 从url_queue取出url
            url = self.url_queue.get()
            response = requests.get(url, headers=self.headers)
            dict_data = json.loads(response.text)
            rooms = dict_data["data"]["list"]
            # 将rooms放入room_queue
            self.room_queue.put(rooms)
            # 将处理完的url标记为task_done,此时url_queue.qsize -1
            self.url_queue.task_done()

    def parse_data(self):
        while True:
            items = []
            # 从room_queue取出rooms
            rooms = self.room_queue.get()
            # 遍历当前页的所有房间
            for room in rooms:
                # 字典生成式取room的部分key和value
                item = {key: room[key] for key in ["rid", "roomName", "roomSrc", "nickname", "hn"]}
                items.append(item)
            # 将items放入itme_queue
            self.item_queue.put(items)
            # 将处理完的rooms标记为task_done
            self.room_queue.task_done()

    def save_data(self):
        while True:
            # 从item_queue取出items
            items = self.item_queue.get()
            with open("images/douyu.json", "a", encoding="utf8") as f:
                for item in items:
                    print(item)
                    f.write(json.dumps(item, ensure_ascii=False, indent=2) + ", ")
            # 将处理完的items标记为task_done
            self.item_queue.task_done()

    def main(self):
        threads = []
        # 1.获取url列表
        self.get_url()
        print(self.url_queue.qsize())
        # 2.发送请求,获取响应
        for i in range(10):
            t1 = threading.Thread(target=self.get_data)
            threads.append(t1)
        # 3.解析数据
        for i in range(10):
            t2 = threading.Thread(target=self.parse_data)
            threads.append(t2)
        # 4.保存数据
        for i in range(10):
            t3 = threading.Thread(target=self.save_data)
            threads.append(t3)
        for t in threads:
            # 由于该子线程是死循环,需要在调用start()之前将其设置为守护线程,表示该线程不重要,当主线程结束时不用等待该子线程直接退出
            t.setDaemon(daemonic=True)
            t.start()
        for q in [self.url_queue, self.room_queue, self.item_queue]:
            # 让主线程block,等待queue中的items全部处理完
            q.join()
        print("任务全部结束,主线程over！")


class DouYu03(object):
    """
    3.使用selenium模拟浏览器操作
      html = etree.HTML(driver.page_source)-->html.xpath()不能和driver.find_elements_by_xpath()混着用
      driver.page_source速度更快但是html.xpath()有时候取数据莫名其妙报错,可以用driver.find_elements_by_xpath()
    """
    def __init__(self):
        self.url = "https://www.douyu.com/directory/all"
        self.driver = webdriver.Chrome(executable_path="D://chromedriver/chromedriver.exe")

    def get_data(self):
        # # 获取浏览器渲染后的网页elements
        # elements = self.driver.page_source
        # # 将字符串解析为HTML文档
        # html = etree.HTML(elements)
        # # xpath解析
        # room_list = html.xpath('//div[contains(@class,"ListContent")]/ul/li')
        li_list = self.driver.find_elements_by_xpath('//div[contains(@class,"ListContent")]/ul/li')
        items = []
        for li in li_list:
            item = {
                "link": li.find_element_by_xpath('.//a[last()]').get_attribute("href"),
                "anchor": li.find_element_by_xpath('.//h2').text,
                "title": li.find_element_by_xpath('.//h3').text,
                "category": li.find_element_by_xpath('.//span[@class="DyListCover-zone"]').text,
                "online": li.find_element_by_xpath('.//span[@class="DyListCover-hot"]').text
            }
            items.append(item)
        # 获取下一页按钮的input标签
        next_page = self.driver.find_elements_by_xpath('//li[@class=" dy-Pagination-next"]')
        next_page = next_page[0] if len(next_page) > 0 else None
        return items, next_page

    @staticmethod
    def save_data(items):
        with open("./douyu.json", "a", encoding="utf8") as f:
            for item in items:
                print(item)
                f.write(json.dumps(item, ensure_ascii=False, indent=2) + ", ")

    def main(self):
        # 1.先打开斗鱼首页
        self.driver.get(self.url)
        # 注意：有些页面加载比较慢,直接获取数据可能会报错：element is not attached to the page document
        time.sleep(3)
        # 2.获取首页数据
        items, next_page = self.get_data()
        # 3.保存首页数据
        self.save_data(items)
        # 4.判断是否有下一页
        while next_page:
            # 有就点击下一页
            next_page.click()
            # 此处也需要等待页面加载完
            time.sleep(3)
            # 继续获取数据并保存
            items, next_page = self.get_data()
            self.save_data(items)
        self.driver.quit()


if __name__ == '__main__':
    # dy = DouYu01()
    # dy = DouYu02()
    dy = DouYu03()
    dy.main()
