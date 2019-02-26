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
    """
    方式一：抓接口,使用requests模块发送网络请求,需要伪造请求头(反爬虫很容易识别伪造的headers,指不定少了哪个参数就不行)
    """

    def parse_page(self):
        """
        获取每页所有职位信息的id
        """

        # 调用接口
        url = "https://www.lagou.com/jobs/positionAjax.json?city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false"
        # 请求头
        headers = {
            "User-Agent": "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
            "Cookie": "JSESSIONID=ABAAABAABEEAAJA6EA181175874A387649B864C48AE01AA; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1537253504; _ga=GA1.2.1735615114.1537253505; user_trace_token=20180918145145-4ebed506-bb0f-11e8-baf2-5254005c3644; LGUID=20180918145145-4ebed7dd-bb0f-11e8-baf2-5254005c3644; _gid=GA1.2.1064196434.1537253505; index_location_city=%E4%B8%8A%E6%B5%B7; TG-TRACK-CODE=search_code; SEARCH_ID=f52a4cd1d6dd4e50b78974df963ce515; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1537258174; LGSID=20180918160935-2e005133-bb1a-11e8-baf2-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_java%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; LGRID=20180918160935-2e0053c0-bb1a-11e8-baf2-5254005c3644",
            "Referer": "https://www.lagou.com/jobs/list_java?labelWords=&fromSearch=true&suginput=",
            # ...
        }
        # 请求数据
        formdata = {
            "first": "false",
            "pn": 1,
            "kd": "java"
        }
        # 发送post请求
        for i in range(1, 31):
            formdata["pn"] = i
            # 获取请求数据
            response = requests.post(url, data=formdata, headers=headers)
            # 转成python对象(dict)
            data = json.loads(response.text)
            # 获取所有职位信息的编号
            ids = data['content']['hrInfoMap'].keys()
            for id in ids:
                self.parse_detail(id)
                time.sleep(1)
            time.sleep(10)

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
        for field in ["id", "name", "address", "salary", "experience", "education", "label", "company", "temptation", "description"]:
            value.append(position[field])
        print(value)

        try:
            sql = "replace into position values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql, value)
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()


class LaGou02(object):
    """
    方式二：使用selenium模拟浏览器操作(推荐)
    """

    def __init__(self):
        # 创建浏览器对象
        self.driver = webdriver.Chrome(executable_path="D://chromedriver/chromedriver.exe")
        # 初始页面
        self.url = "https://www.lagou.com/jobs/list_java?labelWords=&fromSearch=true&suginput="

    def parse_page(self):
        """
        获取详情页链接
        """

        # 打开初始页面
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
                # 切换窗口打开链接
                self.switch_window(link)
                time.sleep(1)
            # 获取下一页按钮标签(注意：find_element_by_xpath只能获取元素不能获取元素里的text)
            tag = self.driver.find_element_by_xpath('//div[@class="pager_container"]/span[last()]')
            # 判断下一页能否继续点击
            if tag.get_attribute("class") == "pager_next pager_next_disabled":
                break
            else:
                tag.click()
            # 设置翻页时间间隔
            time.sleep(10)

    def switch_window(self, url):
        """
        在job列表页和job详情页之间来回切换,解析完的详情页就关掉并切回列表页,始终保持只有两个窗口
        """

        # self.driver.get(url)  # 直接打开会覆盖原页面

        # 在新窗口打开job详情页
        self.driver.execute_script("window.open('%s')" % url)
        # 跳到详情页
        self.driver.switch_to_window(self.driver.window_handles[1])
        # 获取详情页源码
        source = self.driver.page_source
        # 解析源码
        self.parse_detail(source)
        # 关掉详情页
        self.driver.close()
        # 再回到列表页
        self.driver.switch_to_window(self.driver.window_handles[0])

    def parse_detail(self, source):
        """
        解析详情页
        """

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
        """
        数据入库
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
            sql = "replace into position values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql, value)
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()


if __name__ == '__main__':
    ls = LaGou01()
    # ls = LaGou02()
    ls.parse_page()
