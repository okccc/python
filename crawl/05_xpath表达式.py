# coding=utf-8
"""
HTML(Hyper Text Markup Language): 超文本标记语言 ---> 展示数据
XML(Extensible Markup Language): 可扩展标记语言 ---> 传输和存储数据,可以持久化
HTML DOM(Document Object Model for HTML): 文档对象模型 ---> 访问和操作HTML文档
XPath(XML Path Language): 是一种在XML文档中查找信息的语言 ---> 遍历XML文档中的元素和属性
注意: 使用chrome插件Xpath Helper选择标签时,会给选中的标签添加属性class="xh-highlight",并且chrome能匹配到数据但程序可能匹配不到,
     因为有些网站对不同浏览器显示页面略有差异(比如tag标签名称不同),这时可以换个IE内核的浏览器试试 --> IE/遨游/360/搜狗/世界之窗...

lxml库: 是一款高性能的HTML/XML解析器 ---> 用xpath表达式解析并提取HTML/XML数据(可结合XMLQuire或者Chrome插件XPath Helper调试)
lxml库的etree模块
etree.HTML(str): 从字符串常量解析HTML文档,返回节点树(Parses an HTML document from a string constant.Returns the root node)
etree.parse(file): 解析源文件返回一个节点树(Return an ElementTree object loaded with source elements)
etree.tostring(element_or_tree, encoding="utf8").decode("utf8"):  # 此处encoding参数不能省,不然中文乱码
将元素序列化成其xml树编码的字符串(Serialize an element to an encoded string repitementation of its XML tree)

xpath使用路径表达式获取xml文档中的元素和属性
元素: <class 'lxml.etree._Element'> ---> 需要etree.tostring()序列化成字符串输出,不过一般都是取元素的@属性或text
     当xpath表达式返回结果是元素时,可用 text()/.text 获取当前标签的文本内容, tag()/.tag 获取当前标签的名称
属性: <class 'lxml.etree._ElementUnicodeResult'> ---> 可以直接输出(Python里的字符串是Unicode编码)
     当xpath表达式返回结果是属性时,结果就是当前属性的值,也可以用get()方法获取 --> /a/img/@src 等同于 tag = /a/img; tag.get("src")
xpath函数: http://www.w3school.com.cn/xpath/xpath_functions.asp

1.节点:
/ 	从根节点选取
// 	从当前节点选择而不考虑它们的位置
. 	选取当前节点
.. 	选取当前节点的父节点
@ 	选取属性
/bookstore: 选取根元素bookstore
bookstore/book: 选取属于bookstore的子元素的所有book元素
bookstore//book: 选择属于bookstore元素后代的所有book元素,而不管它们位于bookstore下的什么位置
//@lang: 选取名为lang的所有属性

2.谓语: 查找指定条件的节点,嵌在[]中
/bookstore/book[1]: 选取属于bookstore子元素的第一个book元素
/bookstore/book[last()]: 选取属于bookstore子元素的最后一个book元素
/bookstore/book[last()-1]: 选取属于bookstore子元素的倒数第二个book元素
/bookstore/book[position()<3]: 选取属于bookstore子元素的前两个book元素
//title[@lang]: 选取所有具有lang属性的title元素
//title[@lang=’eng’]: 选取所有lang属性值为eng的title元素
/bookstore/book[price>35.00]: 选取bookstore元素下的book元素,且其中的price元素>35.00
/bookstore/book[price>35.00]/title: 选取bookstore元素下的book元素下的title元素,且book元素的price元素>35.00

3.通配符: 用来选取未知的XML元素
*: 匹配任何元素节点
@*: 匹配任何属性节点
node(): 匹配任何类型的节点
/bookstore/*: 选取bookstore元素的所有子元素
//*: 选取文档中的所有元素
//title[@*]: 选取所有带有属性的title元素

4.多路径: 在路径表达式中使用"|"运算符可以选取多个路径
//book/title | //book/price: 选取book元素的所有title和price元素
//title | //price: 选取文档中的所有title和price元素
/bookstore/book/title | //price: 选取属于bookstore元素的book元素的所有title元素和文档中所有的price元素
"""

import requests
from lxml import etree
from w3lib.html import remove_tags

def xpath01():
    # 1、etree读取字符串 ---> python的3引号可用于表示多行字符串或者函数下方的注释
    text = """
        <div>
            <ul>
                 <li class="item-0"><a href="link1.html">first item</a></li>
                 <li class="item-1"><a href="link2.html">second item</a></li>
                 <li class="item-inactive"><a href="link3.html">third item</a></li>
                 <li class="item-1"><a href="link4.html">fourth item</a></li>
                 <li class="item-0"><a href="link5.html">fifth item</a> # 注意，此处缺少一个 </li> 闭合标签
            </ul>
        </div>
     """
    # 将字符串解析为HTML文档
    data = etree.HTML(text)
    print(type(data))  # <class 'lxml.etree._ElementTree'>
    # 将HTML文档序列化成字符串(etree可以自动修正html代码)
    data_new = etree.tostring(data, encoding="utf8").decode("utf-8")
    print(type(data_new))  # <class 'str'>
    # xpath表达式解析
    items = data.xpath('//li')
    # 遍历列表
    for item in items:
        print(type(item))  # <class 'lxml.etree._Element'>
        # 将元素序列化成字符串
        item = etree.tostring(item, encoding="utf8").decode("utf-8")
        print(item)  # <li class="item-0"><a href="link1.html">first item</a></li>


def xpath02():
    # 2、etree读取文件
    html = etree.parse("images/hello.html")
    print(type(html))  # <class 'lxml.etree._ElementTree'>
    datas = etree.tostring(html, encoding="utf8").decode("utf-8")
    print(type(datas))  # <class 'str'>

    # 获取所有的<li>标签: 当xpath表达式返回结果是元素时,text获取当前标签的文本内容,tag获取当前标签的名称
    items = html.xpath('//li')
    for item in items:
        print(type(item))  # <class 'lxml.etree._Element'>
        print(item)  # <Element li at 0x22772f98e08>
        print(item.text)
        print(item.tag)  # li
        # 将元素序列化成字符串
        item1 = etree.tostring(item, encoding="utf8").decode("utf-8")
        print(type(item1))  # <class 'str'>
        print(item1)  # <li class="item-0"><a href="link1.html">first item</a></li>

    # 获取<li>标签下href为link1.html的<a>标签
    items = html.xpath('//li/a[@href="link1.html"]')
    for item in items:
        print(type(item))  # <class 'lxml.etree._Element'>
        # 将元素序列化成字符串
        item = etree.tostring(item).decode("utf-8")
        print(item)  # <a href="link1.html">first item</a>

    # 获取<li>标签下的所有<span>标签
    items = html.xpath('//li//span')
    for item in items:
        print(type(item))  # <class 'lxml.etree._Element'>
        # 将元素序列化成字符串
        item = etree.tostring(item).decode("utf-8")
        print(item)  # <span class="bold">third item</span>

    # 获取倒数第二个元素的内容
    items = html.xpath('//*[last()-1]')
    for item in items:
        print(type(item))  # <class 'lxml.etree._Element'>
        # 将元素序列化成字符串
        item = etree.tostring(item).decode("utf-8")
        print(item)  # <li class="item-1"><a href="link4.html">fourth item</a></li>

    # 获取class值为bold的标签名称
    items = html.xpath('//*[@class="bold"]')
    for item in items:
        print(type(item))  # <class 'lxml.etree._Element'>
        print(item.text)  # third item
        print(item.tag)  # span
        # 将元素序列化成字符串
        item = etree.tostring(item).decode("utf-8")
        print(item)  # <span class="bold">third item</span>

    # 获取<li>标签的所有class属性
    items = html.xpath('//li/@class')
    print(items)  # ['item-0', 'item-1', 'item-inactive', 'bold', 'item-1', 'item-0']
    for item in items:
        print(type(item))  # <class 'lxml.etree._ElementUnicodeResult'>
        # item = etree.tostring(item).decode("utf-8")
        # TypeError: Type 'lxml.etree._ElementUnicodeResult' cannot be serialized
        print(item)  # item-0

    # 获取<li>标签下的<a>标签里的所有class属性
    items = html.xpath('//li/a//@class')
    for item in items:
        print(type(item))  # <class 'lxml.etree._ElementUnicodeResult'>
        print(item)  # bold

    # 获取最后一个<li>的<a>的href属性
    items = html.xpath('//li[last()]/a/@href')
    for item in items:
        print(type(item))  # <class 'lxml.etree._ElementUnicodeResult'>
        print(item)  # link5.html


def xpath03():
    datas = []
    url = "https://www.baidu.com/s?"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1"}
    params = {"wd": "美好分期", "pn": 10}
    response = requests.get(url, params=params, headers=headers)
    html = etree.HTML(response.text)
    # contains()模糊查询: 第一个参数是要匹配的标签, 第二个参数是标签名的部分内容
    items = html.xpath("//div[@id='content_left']/div[contains(@class, 'result')]/h3/a")
    for each in items:
        # text被<br>分成了好几段导致xpath无法直接获取,可用remove_tags去除碍事标签直接获取文本
        title = remove_tags(etree.tostring(each, encoding="utf8").decode("utf8"))
        link = each.get("href")
        data = {"title": title, "link": link}
        datas.append(data)
    print(datas)


if __name__ == "__main__":
    # xpath01()
    # xpath02()
    xpath03()
