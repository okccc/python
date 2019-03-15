# coding=utf-8
import requests
from lxml import etree
from selenium import webdriver
import json
import time
import pymysql
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S %p"
)


class LaGou01(object):
    # 1.抓接口,使用requests模块发送网络请求,需要伪造请求头(反爬虫很容易识别伪造的headers,指不定少了哪个参数就不行)
    def __init__(self):
        # 抓包分析获取接口、请求头、请求数据
        self.url = "https://www.lagou.com/jobs/positionAjax.json?city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false"
        # 请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
            "Cookie": "_ga=GA1.2.1632229811.1551433595; user_trace_token=20190301174634-e6860271-3c06-11e9-88dd-5254005c3644; LGUID=20190301174634-e6860baf-3c06-11e9-88dd-5254005c3644; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216938a748a5c4-0f51663fd41519-3d644701-1327104-16938a748a6941%22%2C%22%24device_id%22%3A%2216938a748a5c4-0f51663fd41519-3d644701-1327104-16938a748a6941%22%7D; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=205; gate_login_token=be26ff66f397b706256aefb504fb3ce03c809505678707fb; index_location_city=%E4%B8%8A%E6%B5%B7; JSESSIONID=ABAAABAAAIAACBIAEB1C6DEE2DCA456D6063E2CF66D39D3; WEBTJ-ID=20190304111617-16946b3b88d416-079994951d3bce-3d644601-1327104-16946b3b88e52b; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1551433595,1551669377; _gid=GA1.2.1726247041.1551669378; _putrc=01A61E721A07441C; login=true; unick=1573976179%40qq.com; TG-TRACK-CODE=search_code; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1551669963; LGRID=20190304112602-3ca124f6-3e2d-11e9-89d2-5254005c3644; SEARCH_ID=6d3fb33e50d74a218fb79c49aa6a739e",
            "Referer": "https://www.lagou.com/jobs/list_java?labelWords=&fromSearch=true&suginput=",
            # ...
        }
        self.proxies = {"https": "https://222.170.101.98:37025"}

    def get_ids(self, i):
        # 请求数据
        form_data = {"first": "true", "pn": i, "kd": "java"}
        # 获取请求数据
        response = requests.post(self.url, data=form_data, headers=self.headers, proxies=self.proxies, timeout=5)
        # 将json字符串转成dict
        data = json.loads(response.text)
        print(data)
        # 获取所有job编号
        position_ids = data["content"]["hrInfoMap"].keys()
        # position_ids = [d['positionId'] for d in data['content']['positionResult']['result']]
        return position_ids

    def parse_detail(self, id):
        """
        解析每个职位的详细信息
        """

        # 详情页链接
        url = "https://www.lagou.com/jobs/" + str(id) + ".html"
        # 请求头
        headers = {
            "User-Agent": "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Referer": "https://www.lagou.com/jobs/list_java?labelWords=&fromSearch=true&suginput=",
            "Cookie": "JSESSIONID=ABAAABAABEEAAJA6EA181175874A387649B864C48AE01AA; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1537253504; _ga=GA1.2.1735615114.1537253505; user_trace_token=20180918145145-4ebed506-bb0f-11e8-baf2-5254005c3644; LGUID=20180918145145-4ebed7dd-bb0f-11e8-baf2-5254005c3644; _gid=GA1.2.1064196434.1537253505; index_location_city=%E4%B8%8A%E6%B5%B7; TG-TRACK-CODE=search_code; SEARCH_ID=f52a4cd1d6dd4e50b78974df963ce515; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1537258174; LGSID=20180918160935-2e005133-bb1a-11e8-baf2-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_java%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; LGRID=20180918160935-2e0053c0-bb1a-11e8-baf2-5254005c3644",
        }
        # 发送get请求
        response = requests.get(url, headers=headers)
        html = etree.HTML(response.text)
        # 解析字段
        name = html.xpath('//div[@class="job-name"]/@title')[0]
        address = "-".join(html.xpath('//div[@class="work_addr"]//a/text()')[:-1])
        address_detail = html.xpath('//input[@name="positionAddress"]/@value')[0]
        address = address + "-" + address_detail
        salary = html.xpath('//dd[@class="job_request"]//span[1]/text()')[0][:-1]
        experience = html.xpath('//dd[@class="job_request"]//span[3]/text()')[0][:-2]
        education = html.xpath('//dd[@class="job_request"]//span[4]/text()')[0][:-2]
        label = " ".join(html.xpath('//li[@class="labels"]/text()'))
        company = html.xpath('//div[@class="company"]/text()')[0]
        temptation = html.xpath('//dd[@class="job-advantage"]/p')[0].text
        description = "".join(html.xpath('//dd[@class="job_bt"]//*/text()')).strip()

        position = {
            "id": id,
            "name": name,
            "address": address,
            "salary": salary,
            "experience": experience,
            "education": education,
            "label": label,
            "company": company,
            "temptation": temptation,
            "description": description,
        }
        self.insert(position)

    def insert(self, position):
        """
        将职位信息插入数据库
        """

        config = {
            "host": "localhost",
            "port": 3306,
            "user": "root",
            "password": "root",
            "db": "test",
            "charset": "utf8"
        }

        conn = pymysql.connect(**config)
        cur = conn.cursor()

        value = []
        for field in ["id", "name", "address", "salary", "experience", "education", "label", "company", "temptation",
                      "description"]:
            value.append(position[field])
        print(value)

        try:
            sql = "REPLACE INTO positions VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql, value)
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()

    def main(self):
        # 遍历所有页面
        for i in range(1, 2):
            # 1.发送请求接受响应
            position_ids = self.get_ids(i)
            print(position_ids)
            for position_id in position_ids:
                # 2.解析数据
                item = self.parse_data(position_id)
                # 3.保存数据
                self.save_data(item)


class LaGou02(object):
    # 2.使用selenium模拟浏览器操作(推荐)
    def __init__(self):
        # 创建浏览器对象
        self.driver = webdriver.Chrome(executable_path="D://chromedriver/chromedriver.exe")
        # 地址栏url
        self.url = "https://www.lagou.com/jobs/list_java?labelWords=&fromSearch=true&suginput="
        # 数据库连接信息
        self.config = {
            "host": "localhost",
            "port": 3306,
            "user": "root",
            "password": "root",
            "db": "test",
            "charset": "utf8"
        }

    def open_page(self):
        # 第一步、打开初始页面
        self.driver.get(self.url)
        # 循环点击下一页
        while True:
            # 获取当前页面源码
            source = self.driver.page_source
            # 将字符串解析为HTML文档
            html = etree.HTML(source)
            # xpath解析获取当前页面所有job页面链接
            links = html.xpath('//a[@class="position_link"]/@href')
            # 遍历所有链接
            for link in links:
                # 切换窗口打开job详情页
                self.switch_window(link)
            # 获取下一页按钮标签(注意：find_element_by_xpath只能获取元素不能获取元素里的text)
            tag = self.driver.find_element_by_xpath('//div[@class="pager_container"]/span[last()]')
            # 判断下一页能否继续点击
            if tag.get_attribute("class") == "pager_next pager_next_disabled":
                break
            else:
                tag.click()
            # 设置翻页时间间隔
            time.sleep(10)

    def switch_window(self, link):
        # 第二步、在job列表页和job详情页之间来回切换,解析完的详情页就关掉并切回列表页,始终保持只有两个窗口
        # 在新窗口打开job详情页
        self.driver.execute_script("window.open('%s')" % link)
        # 跳到详情页
        self.driver.switch_to_window(self.driver.window_handles[1])
        # 获取详情页源码
        source = self.driver.page_source
        # 解析源码
        self.parse_detail(source)
        time.sleep(3)
        # 关掉详情页
        self.driver.close()
        # 再回到列表页
        self.driver.switch_to_window(self.driver.window_handles[0])

    def parse_detail(self, source):
        # 第三步、解析详情页
        # 将字符串解析为HTML文档
        html = etree.HTML(source)
        # 解析字段
        id = html.xpath('//input[@id="jobid"]/@value')[0]
        name = html.xpath('//div[@class="job-name"]/@title')[0]
        address = "-".join(html.xpath('//div[@class="work_addr"]//a/text()')[:-1])
        address_detail = html.xpath('//input[@name="positionAddress"]/@value')[0]
        address = address + "-" + address_detail
        salary = html.xpath('//dd[@class="job_request"]//span[1]/text()')[0][:-1]
        experience = html.xpath('//dd[@class="job_request"]//span[3]/text()')[0][:-2]
        education = html.xpath('//dd[@class="job_request"]//span[4]/text()')[0][:-2]
        label = " ".join(html.xpath('//li[@class="labels"]/text()'))
        company = html.xpath('//div[@class="company"]/text()')[0]
        temptation = html.xpath('//dd[@class="job-advantage"]/p')[0].text
        description = "".join(html.xpath('//dd[@class="job_bt"]//*/text()')).strip()
        position = {
            "id": id,
            "name": name,
            "address": address,
            "salary": salary,
            "experience": experience,
            "education": education,
            "label": label,
            "company": company,
            "temptation": temptation,
            "description": description,
        }
        self.insert(position)

    def insert(self, position):
        # 第四步、数据入库
        conn = pymysql.connect(**self.config)
        cur = conn.cursor()
        value = []
        for field in ["id", "name", "address", "salary", "experience", "education", "label", "company", "temptation",
                      "description"]:
            value.append(position[field])
        print(value)
        try:
            sql = "REPLACE INTO positions VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql, value)
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()

    def main(self):
        self.open_page()


if __name__ == '__main__':
    ls = LaGou01()
    # ls = LaGou02()
    ls.main()
