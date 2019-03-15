# coding=utf-8
import requests
from bs4 import BeautifulSoup
import pymysql
import threading
from queue import Queue
import logging
import time
from fake_useragent import UserAgent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S %p"
)


class BaiDu01(object):
    # 单线程
    def __init__(self):
        self.url = "https://www.baidu.com/s?wd={}&pn={}&gpc={}"
        self.ua = UserAgent()
        self.config = {
            "host": "10.9.2.196",
            "port": 3306,
            "user": "meihaodb",
            "password": "Eakgydskaezfl68Eefg:",
            "db": "duckchatdb",
            "charset": "utf8",
            "cursorclass": pymysql.cursors.DictCursor  # 以dict格式返回数据
        }
        self.negative_words = ["110网", "骗", "忽悠", "合法", "合理", "征信", "名声", "跑路", "违约", "不还", "起诉", "法院", "律师", "法律",
                               "正规", "违规", "暴力", "轰炸", "威胁", "后悔", "反悔", "恐吓", "服务费", "传销", "退款", "套路", "虚假", "逾期"]
        self.flag = False
        self.datas = []

    def get_hospital(self):
        conn = pymysql.connect(**self.config)
        cur = conn.cursor()
        words = []
        try:
            sql = "select distinct name from shop where online_status=1 and type!='TEST'"
            cur.execute(sql)
            # records = cur.fetchmany(50)
            records = cur.fetchall()
            for record in records:
                hospital = record["name"]
                words.append(hospital)
            words.insert(0, "美好分趣")
            words.insert(0, "美好分期")
            return words
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()

    def get_url(self, words):
        if self.flag:
            return [self.url.format(word, (i-1)*10) for word in words for i in range(1, 20)]
        else:
            gpc = "stf=%.3f,%.3f|stftype=1" % (time.time() - 86400, time.time())
            return [self.url.format(word, (i-1)*10, gpc) for word in words for i in range(1, 3)]

    def get_data(self, url):
        # print(url)
        response = requests.get(url, headers={"User-Agent": self.ua.random})
        return BeautifulSoup(response.text, "lxml")

    def parse_data(self, soup):
        for tag in soup.select("h3 > a"):
            title = tag.text
            link = tag.attrs["href"]
            # 百度搜索的条目都是www.baidu.com域名的地址,点击后会重定向到真实地址,所以需要再次发送请求获取搜索结果的真实url
            real_link = ""
            if link.startswith("http"):
                # requests默认会自动处理302跳转,经过跳转的请求返回的url/status_code/headers都是跳转后的信息,可用response.history追踪跳转情况
                # 如果请求跳转过多可能会报错：TooManyRedirects: Exceeded 30 redirects 禁用重定向还可以减少网络消耗提高访问速度
                response = requests.get(link, headers={"User-Agent": self.ua.random}, allow_redirects=False)
                if response.status_code < 400:
                    # 禁用后status_code是302,通过response.headers["Location"]获取重定向的url
                    real_link = response.headers["Location"]
            for word in self.negative_words:
                if word in title:
                    # 有word符合就添加数据
                    data = {"title": title, "link": real_link}
                    self.datas.append(data)
                    # 结束循环防止一个title多个word重复添加
                    break

    def filter_data(self):
        filter_words = ["美好", "美容", "医院", "医疗", "医美", "祛痘", "植发", "整形", "门诊", "诊所"]
        data_new = []
        for data in self.datas:
            for word in filter_words:
                if word in data["title"]:
                    data_new.append(data)
                    break
        print([dict(t) for t in {tuple(d.items()) for d in data_new}])
        # return [dict(t) for t in {tuple(d.items()) for d in data_new}]

    def main(self):
        # 1.获取所有关键字
        words = self.get_hospital()
        # 2.获取url列表
        urls = self.get_url(words)
        print(len(urls))
        # 遍历url
        for url in urls:
            # 3.发送请求,获取响应
            soup = self.get_data(url)
            # 4.解析数据
            self.parse_data(soup)
        # 5.处理最终结果
        self.filter_data()


class BaiDu02(object):
    # 多线程
    def __init__(self):
        self.url = "https://www.baidu.com/s?wd={}&pn={}&gpc={}"
        self.ua = UserAgent()
        self.config = {
            "host": "10.9.2.196",
            "port": 3306,
            "user": "meihaodb",
            "password": "Eakgydskaezfl68Eefg:",
            "db": "duckchatdb",
            "charset": "utf8",
            "cursorclass": pymysql.cursors.DictCursor  # 以dict格式返回数据
        }
        self.negative_words = ["110网", "骗", "忽悠", "合法", "合理", "征信", "名声", "跑路", "违约", "不还", "起诉", "法院", "律师", "法律",
                               "正规", "违规", "暴力", "轰炸", "威胁", "后悔", "反悔", "恐吓", "服务费", "传销", "退款", "套路", "虚假", "逾期"]
        self.flag = False
        self.datas = []
        # 构造url队列、请求响应队列
        self.url_queue = Queue()
        self.soup_queue = Queue()

    def get_hospital(self):
        conn = pymysql.connect(**self.config)
        cur = conn.cursor()
        words = []
        try:
            sql = "select distinct name from shop where online_status=1 and type!='TEST'"
            cur.execute(sql)
            # records = cur.fetchmany(50)
            records = cur.fetchall()
            for record in records:
                hospital = record["name"]
                words.append(hospital)
            words.insert(0, "美好分趣")
            words.insert(0, "美好分期")
            return words
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()

    def get_url(self, words):
        if self.flag:
            # return [self.url.format(word, (i-1)*10, "") for word in words for i in range(1, 20)]
            for word in words:
                for i in range(1, 20):
                    self.url_queue.put(self.url.format(word, (i-1)*10, ""))
        else:
            gpc = "stf=%.3f,%.3f|stftype=1" % (time.time() - 86400, time.time())
            # return [self.url.format(word, (i-1)*10, gpc) for word in words for i in range(1, 3)]
            for word in words:
                for i in range(1, 2):
                    self.url_queue.put(self.url.format(word, (i-1)*10, gpc))

    def get_data(self):
        while True:
            # 从url_queue取出url
            url = self.url_queue.get()
            response = requests.get(url, headers={"User-Agent": self.ua.random})
            # return BeautifulSoup(response.text, "lxml")
            # 将html源码放入soup_queue
            self.soup_queue.put(BeautifulSoup(response.text, "lxml"))
            # 将处理完的url标记为task_done,此时url_queue.qsize - 1
            self.url_queue.task_done()

    def parse_data(self):
        while True:
            # 从soup_queue取出soup
            soup = self.soup_queue.get()
            for tag in soup.select("h3 > a"):
                title = tag.text
                link = tag.attrs["href"]
                # 百度搜索的条目都是www.baidu.com域名的地址,点击后会重定向到真实地址,所以需要再次发送请求获取搜索结果的真实url
                real_link = ""
                if link.startswith("http"):
                    response = requests.get(link, headers={"User-Agent": self.ua.random}, allow_redirects=False)
                    if response.status_code < 400:
                        # 禁用后status_code是302,通过response.headers["Location"]获取重定向的url
                        real_link = response.headers["Location"]
                        # print(real_link)
                for word in self.negative_words:
                    if word in title:
                        # print(word)
                        # 有word符合就添加数据
                        data = {"title": title, "link": real_link}
                        print(data)
                        self.datas.append(data)
                        # 结束循环防止一个title多个word重复添加
                        break
            # 将处理完的soup标记为task_done,此时soup_queue.qsize - 1
            self.soup_queue.task_done()

    def filter_data(self):
        print(self.datas)
        data_new = []
        for data in self.datas:
            for word in ["美好", "医院"]:
                if word in data["title"]:
                    data_new.append(data)
                    break
        print([dict(t) for t in {tuple(d.items()) for d in data_new}])
        # return [dict(t) for t in {tuple(d.items()) for d in data_new}]

    def main(self):
        # 1.获取所有关键字
        words = self.get_hospital()
        print(len(words))
        threads = []
        # 2.获取url列表
        t_url = threading.Thread(target=self.get_url, args=(words,))
        threads.append(t_url)
        for i in range(1, 20):
            # 3.发送请求,获取响应
            t_html = threading.Thread(target=self.get_data)
            threads.append(t_html)
        for i in range(1, 20):
            # 4.解析数据
            t_parse = threading.Thread(target=self.parse_data)
            threads.append(t_parse)
        for t in threads:
            # 由于该子线程是死循环,需要在调用start()之前将其设置为守护线程,表示该线程不重要,当主线程结束时不用等待该子线程直接退出
            t.setDaemon(daemonic=True)
            t.start()
        for q in (self.url_queue, self.soup_queue):
            # 让主线程block,等待queue中的items全部处理完
            q.join()
        # 5.处理最终结果
        self.filter_data()


if __name__ == '__main__':
    # bd = BaiDu01()
    bd = BaiDu02()
    bd.main()




