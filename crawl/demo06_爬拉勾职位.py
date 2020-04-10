# coding=utf-8
import requests
from selenium import webdriver
import json
import time
import csv
import codecs
import pymysql
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S %p"
)

class LaGou01(object):
    # 1.抓接口：使用requests模块请求,需要伪造请求头(拉勾反爬虫有点东西,能轻松识别伪造的headers,指不定少了哪个参数就不行)
    def __init__(self):
        # 抓包分析获取接口、请求头、请求数据
        self.url = "https://www.lagou.com/jobs/positionAjax.json?city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false"
        # 请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Cookie": "_ga=GA1.2.1632229811.1551433595; user_trace_token=20190301174634-e6860271-3c06-11e9-88dd-5254005c3644; LGUID=20190301174634-e6860baf-3c06-11e9-88dd-5254005c3644; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216938a748a5c4-0f51663fd41519-3d644701-1327104-16938a748a6941%22%2C%22%24device_id%22%3A%2216938a748a5c4-0f51663fd41519-3d644701-1327104-16938a748a6941%22%7D; _gid=GA1.2.81669527.1552786672; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=205; gate_login_token=72b21e037a0b076f0f0f0a7878f6dced1a117ae4e212831f; index_location_city=%E4%B8%8A%E6%B5%B7; WEBTJ-ID=20190318095637-1698e83d28a69d-007b37cccff29f-3d644509-1327104-1698e83d28b456; _putrc=01A61E721A07441C; JSESSIONID=ABAAABAAAIAACBI6A186064BFF78580C26C24595F21C2A7; login=true; unick=1573976179%40qq.com; _gat=1; PRE_UTM=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1552819562,1552874198,1552960185,1552962642; LGSID=20190319103043-feba9dfe-49ee-11e9-a333-5254005c3644; PRE_HOST=www.google.com; PRE_SITE=https%3A%2F%2Fwww.google.com%2F; TG-TRACK-CODE=index_hotsearch; LGRID=20190319103048-0181f0f9-49ef-11e9-aac9-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1552962647; SEARCH_ID=b954989dca554359b06fdbf5781e33bc",
            "Referer": "https://www.lagou.com/jobs/list_java?labelWords=&fromSearch=true&suginput=?labelWords=hot",
            "X-Requested-With": "XMLHttpRequest",
            "Origin": "https://www.lagou.com",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }

    def get_data(self, i):
        # 请求数据
        form_data = {"first": "false", "pn": i, "kd": "java"}
        # 获取请求数据
        response = requests.post(self.url, data=form_data, headers=self.headers)
        # 将json字符串转成dict
        data = json.loads(response.text)
        print(data)
        # 获取当前所有职位信息
        position_list = data["content"]["positionResult"]["result"]
        positions = []
        keys = ["positionId","companyId","positionName","salary","companyShortName","companySize","district","linestaion",
                "workYear","education","positionLables","industryField","hitags","companyLabelList","positionAdvantage"]
        for position in position_list:
            # 字典生成式取部分字段
            position = {key: position[key] for key in keys}
            positions.append(position)
        return positions

    def save_data(self, positions):
        with open("D://lagou.json", "a", encoding="utf8") as f:
            for position in positions:
                print(position)
                f.write(json.dumps(position, ensure_ascii=False, indent=2))

    def main(self):
        # 遍历所有页面
        for i in range(1, 31):
            # 1.获取当前页数据
            positions = self.get_data(i)
            # 2.保存数据
            self.save_data(positions)
            # 翻页时间间隔设置长一点
            time.sleep(5)


class LaGou02(object):
    # 2.selenium模拟浏览器操作 --> 抓详情页(意味着要多访问很多页面,原则上能爬列表页就不爬详情页,当然详情页能获取更多数据)
    def __init__(self):
        # 初始url
        self.url = "https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?city=%E8%8B%8F%E5%B7%9E&cl=false&fromSearch=true&labelWords=&suginput="
        # 详情页url
        self.detail_url = "https://www.lagou.com/jobs/{}.html"
        # 创建Chrome对象
        self.driver = webdriver.Chrome(executable_path="D://chromedriver/chromedriver.exe")
        # 创建数据库连接
        self.config = {
            "host": "localhost",
            "port": 3306,
            "user": "root",
            "password": "root",
            "db": "test",
            "charset": "utf8",
            "cursorclass": pymysql.cursors.DictCursor  # 以dict格式返回数据
        }

    def get_page(self):
        # 存放当前列表页数据的list
        items = []

        # # 获取源码
        # source = self.driver.page_source
        # # 将source解析为HTML文档
        # html = etree.HTML(source)

        # 获取当前页的所有职位id
        job_ids = []
        tags = self.driver.find_elements_by_xpath('//ul[@class="item_con_list"]/li')
        for tag in tags:
            job_ids.append(tag.get_attribute("data-positionid"))
        # 获取下一页标签 --> find_element()空值会报错,要用find_elements()
        next_page = self.driver.find_elements_by_xpath('//span[@class="pager_next"] | //span[@class="pager_next "]')
        next_page = next_page[0] if len(next_page) > 0 else None
        # 返回结果
        return items, job_ids, next_page

    def get_detail(self, job_id):
        # 在新窗口打开详情页
        self.driver.execute_script("window.open('%s')" % self.detail_url.format(job_id))
        # 获取所有窗口
        windows = self.driver.window_handles
        # 跳转到新打开的窗口
        self.driver.switch_to_window(windows[1])
        # 取数据前等3秒
        time.sleep(3)

        # # 获取source
        # source = self.driver.page_source
        # # 解析为HTML文档
        # html = etree.HTML(source)

        # 获取该职位信息
        item = {
            "id": job_id,
            "name": self.driver.find_element_by_xpath('//div[@class="job-name"]').get_attribute("title"),
            "address": self.driver.find_element_by_xpath('//div[@class="work_addr"]').text[:-4],
            "salary": self.driver.find_element_by_xpath('//dd[@class="job_request"]//span[@class="salary"]').text,
            "experience": self.driver.find_element_by_xpath('//dd[@class="job_request"]//span[3]').text[:-2],
            "education": self.driver.find_element_by_xpath('//dd[@class="job_request"]//span[4]').text[:-2],
            "label": "".join([tag.text+"," for tag in self.driver.find_elements_by_xpath('//li[@class="labels"]')])[:-1],
            "company": self.driver.find_element_by_xpath('//div[@class="company"]').text,
            "temptation": self.driver.find_element_by_xpath('//dd[@class="job-advantage"]/p').text,
            "description": "".join([tag.text for tag in self.driver.find_elements_by_xpath('//div[@class="job-detail"]//*')]).replace("\n", ""),
        }
        # 关窗口前等3秒
        time.sleep(3)
        # 处理完数据后关闭窗口
        self.driver.close()
        # 跳回到列表页
        self.driver.switch_to_window(windows[0])
        # 返回结果
        return item

    def save_data(self, items):
        # 连接数据库
        conn = pymysql.connect(**self.config)
        # 获取游标
        cur = conn.cursor()
        # 当前列表页的结果数据
        values = []
        for item in items:
            value = list(item.values())
            print(value)
            values.append(value)
        # 插入语句
        sql = "REPLACE INTO positions VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        try:
            cur.executemany(sql, values)
            conn.commit()
        except Exception as e:
            print(e)
        finally:
            cur.close()
            conn.close()

    def main(self):
        # 1.先打开首页
        self.driver.get(self.url)
        # 等待页面加载完
        time.sleep(3)
        # 2.获取首页数据
        items, job_ids, next_page = self.get_page()
        print(job_ids)
        for job_id in job_ids:
            item = self.get_detail(job_id)
            items.append(item)
        print(items)
        # 3.保存首页数据
        self.save_data(items)
        # 4.判断是否有下一页
        while next_page is not None:
            # 有就点击下一页
            next_page.click()
            # 等待页面加载完
            time.sleep(3)
            # 继续循环取数据存数据
            items, job_ids, next_page = self.get_page()
            for job_id in job_ids:
                item = self.get_detail(job_id)
                items.append(item)
            self.save_data(items)
            # 翻页时间间隔设置长一点
            time.sleep(10)
        # 最后退出浏览器
        self.driver.quit()


class LaGou03(object):
    # 3.selenium模拟浏览器操作 --> 抓列表页(推荐)
    def __init__(self):
        # 初始url
        # self.url = "https://www.lagou.com/jobs/list_java?px=default&city=%E4%B8%8A%E6%B5%B7#filterBox"
        self.url = "https://www.lagou.com/jobs/list_sql?city=%E8%8B%8F%E5%B7%9E&cl=false&fromSearch=true&labelWords=&suginput="
        # 创建Chrome对象
        self.driver = webdriver.Chrome(executable_path="D://chromedriver/chromedriver.exe")
        # csv文件的表头
        self.fieldnames = ['id', 'link', 'name', 'address', 'salary', 'experience', 'company', 'mark', 'category', 'attract']

    def get_data(self):
        # 存放当前列表页数据的list
        items = []

        # # 获取源码
        # source = self.driver.page_source
        # # 将source解析为HTML文档
        # html = etree.HTML(source)

        # 获取当前页所有职位
        li_list = self.driver.find_elements_by_xpath('//ul[@class="item_con_list"]/li')
        for li in li_list:
            item = {
                # 取单个标签的text用find_element(),取多个标签的text用find_elements()
                "id": li.find_element_by_xpath('.//a[@class="position_link"]').get_attribute("data-lg-tj-cid"),
                "link": li.find_element_by_xpath('.//a[@class="position_link"]').get_attribute("href"),
                "name": li.find_element_by_xpath('.//h3').text,
                "address": li.find_element_by_xpath('.//span[@class="add"]/em').text,
                "salary": li.find_element_by_xpath('.//span[@class="money"]').text,
                "experience": li.find_element_by_xpath('.//div[@class="p_bot"]/div[@class="li_b_l"]').text[7:],
                "company": li.find_element_by_xpath('.//div[@class="company_name"]/a').text,
                "mark": li.find_element_by_xpath('.//div[@class="industry"]').text,
                "category": " ".join([tag.text for tag in li.find_elements_by_xpath('.//div[@class="list_item_bot"]/div[@class="li_b_l"]/span')]),
                "attract": li.find_element_by_xpath('.//div[@class="li_b_r"]').text,
            }
            items.append(item)
        # 获取下一页标签 --> find_element()空值会报错,要用find_elements()
        next_page = self.driver.find_elements_by_xpath('//span[@class="pager_next"] | //span[@class="pager_next "]')
        next_page = next_page[0] if len(next_page) > 0 else None
        # 返回结果
        return items, next_page

    def save_data_first(self, items):
        # 解决excel打开csv文件中文乱码问题
        with open("D://lagou.csv", "wb") as file:
            # 写入windows需要确认编码的字符
            file.write(codecs.BOM_UTF8)
        # 追加写入数据
        with open("D://lagou.csv", "a", encoding="utf-8", newline="") as file:
            # 创建writer对象
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            # 第一行写入表头
            writer.writeheader()
            # 然后写入多行数据
            writer.writerows(items)

    def save_data_after(self, items):
        # 追加写入数据
        with open("D://lagou.csv", "a", encoding="utf-8", newline="") as file:
            # 创建writer对象
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            # 然后写入多行数据
            writer.writerows(items)

    def main(self):
        # 1.先打开首页
        self.driver.get(self.url)
        # 等待页面加载完
        time.sleep(10)
        # 2.获取首页数据
        items, next_page = self.get_data()
        print(items)
        # 3.保存首页数据
        self.save_data_first(items)
        # 4.判断是否有下一页
        while next_page is not None:
            # 有就点击下一页
            next_page.click()
            # 翻页时间间隔设置长一点
            time.sleep(10)
            # 继续循环取数据存数据
            items, next_page = self.get_data()
            # 追加写入csv文件
            self.save_data_after(items)
        # 最后退出浏览器
        self.driver.quit()


if __name__ == '__main__':
    # lg = LaGou01()
    lg = LaGou02()
    # lg = LaGou03()
    lg.main()
