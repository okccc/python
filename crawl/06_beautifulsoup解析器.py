# coding=utf-8
"""
Beautiful Soup: 也是一个HTML/XML的解析器
lxml是局部遍历,而Beautiful Soup基于HTML DOM,会载入整个文档,解析整个DOM树,因此时间和内存开销大很多,所以性能要低于lxml
BeautifulSoup用来解析HTML比较简单,API非常人性化,支持CSS选择器、Python标准库中的HTML解析器,也支持lxml的XML解析器
抓取工具 	  运行速度 	使用难度
regexp 	    最快 	 很复杂(不建议使用)
bs4 	     慢 	     简单
xpath 	     快 	     简单(scrapy框架支持)
"""

from bs4 import BeautifulSoup
import re
import requests
import json
import csv
import codecs
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S %p"
)


text1 = '''
    <html><head><title>The Dormouse's story</title></head>
    <body>
    <p class='title' name='dromouse'><b>The Dormouse's story</b></p>
    <p class='story'>Once upon a time there were three little sisters; and their names were
    <a href='http://example.com/elsie' class='sister' id='link1'><!-- Elsie --></a>,
    <a href='http://example.com/lacie' class='sister' id='link2'>Lacie</a> and
    <a href='http://example.com/tillie' class='sister' id='link3'>Tillie</a>;
    and they lived at the bottom of a well.</p>
    <p class='story'>...</p>
'''

# 解析字符串：创建beautiful soup对象并指定lxml解析器
soup = BeautifulSoup(text1, 'lxml')  # lxml/html5lib

# 解析html文件：open()
# soup = BeautifulSoup(open('hello.html'), 'lxml')

# 格式化输出
# print(soup.prettify())


'''
搜索文档树: find_all(arg)返回列表 --> tag有两个属性name(标签名称)和attrs(属性字典)
'''
def find_all():
    # 1.标签名查找(字符串、正则、列表)
    for tag in soup.find_all('p'):
        print(tag)  # <p class="title" name="dromouse"><b>The Dormouse's story</b></p>
        print(type(tag))  # <class 'bs4.element.Tag'>
        print(tag.name)  # p
        print(tag.text)  # The Dormouse's story
        print(tag.attrs)  # {'class': ['title'], 'name': 'dromouse'}
        print(tag.attrs['class'])  # ['title']

    for tag in soup.find_all(re.compile('^b')):
        print(tag.name)  # body b

    for tag in soup.find_all(['a', 'b']):
        print(tag)

    print("=" * 50)

    # 2.关键字查找
    for tag in soup.find_all(id='link1'):
        print(tag)  # <a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>

    for tag in soup.find_all(href='http://example.com/lacie'):
        print(tag)  # <a class="sister" href="http://example.com/lacie" id="link2">Lacie</a>

    print("=" * 50)

    # 3.获取标签里的内容(字符串、正则、列表)
    for text in soup.find_all(text='Lacie'):
        print(text)  # Lacie

    for text in soup.find_all(text=re.compile('^L')):
        print(text)  # Lacie

    for text in soup.find_all(text=['Lacie', 'Tillie']):
        print(text)  # Lacie Tillie


'''
CSS选择器: soup.select(arg)返回列表 --> 标签名不加修饰/类名前加./id名前加#
'''
def css():
    # 1.标签名查找
    for tag in soup.select('title'):
        print(tag)  # <title>The Dormouse's story</title>

    # 2.类名查找
    for tag in soup.select('.sister'):
        print(tag)  # <a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>
        print(tag.name)  # a
        print(tag.attrs)  # {'id': 'link1', 'class': ['sister'], 'href': 'http://example.com/elsie'}

    # 3.id查找
    for tag in soup.select('#link1'):
        print(tag)  # <a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>

    # 4.组合(父子标签)查找
    for tag in soup.select('p #link1'):
        print(tag)  # <a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>

    # 直接子标签查找 >
    for tag in soup.select('head > title'):
        print(tag)  # <title>The Dormouse's story</title>

    # 5.属性查找(类似xpath但是不写@)
    for tag in soup.select('a[href="http://example.com/elsie"]'):
        print(tag)  # <a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>

    # 6.获取标签里的内容
    for tag in soup.select('title'):
        print(tag.get_text())  # The Dormouse's story


def tencent():
    # 初始页面
    url = "https://hr.tencent.com/position.php?&start="
    # 请求头
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1"}
    # 发送请求
    response = requests.get(url, headers=headers)
    # 创建bs解析器对象
    soup = BeautifulSoup(response.text, 'lxml')
    # 获取该网站的最大页数
    end = soup.find_all(text=re.compile('\d+'))[-2]

    # 存放所有职位的列表
    items = []

    # 循环所有页面
    for i in range(1, int(end)+1):
        page = (i-1) * 10
        full_url = url + str(page)

        # 向新的页面发起请求
        response = requests.get(full_url, headers=headers)
        # 创建bs解析器对象
        soup = BeautifulSoup(response.text, 'lxml')
        # 获取当前页面的职位列表
        positions = soup.select('tr[class="even"]') + soup.select('tr[class="odd"]')

        # 遍历该页面所有职位
        for each in positions:
            # 职位名称
            name = each.select('a')[0].get_text()
            # 详细链接
            link = each.select('a')[0].attrs['href']
            # 职位类别
            sort = each.select('td')[1].get_text()
            # 招聘人数
            num = each.select('td')[2].get_text()
            # 工作地点
            site = each.select('td')[3].get_text()
            # 发布时间
            publishtime = each.select('td')[4].get_text()

            item = {
                "name": name,
                "link": "https://hr.tencent.com/" + link,
                "sort": sort,
                "num": num,
                "site": site,
                "publishtime": publishtime,
            }
            print(item)
            items.append(item)

            # with open("D://tencent.json", "a", encoding="utf8") as file:
            #     file.write(json.dumps(item, ensure_ascii=False) + "\n")

    # csv文件的表头
    header = ['name', 'link', 'sort', 'num', 'site', 'publishtime']

    # 解决excel打开csv文件中文乱码问题
    with open("D://tencent.csv", "wb") as file:
        # 写入windows需要确认编码的字符
        file.write(codecs.BOM_UTF8)

    # 追加写入数据
    with open("D://tencent01.csv", "a", encoding="utf-8", newline="") as file:
        # 创建writer对象
        writer = csv.DictWriter(file, fieldnames=header)
        # 第一行写入表头
        writer.writeheader()
        # 然后写入多行数据
        writer.writerows(items)


if __name__ == '__main__':
    find_all()
    # css()
    # tencent()