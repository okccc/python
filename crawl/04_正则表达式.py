# coding=utf-8
"""
正则表达式 :用于操作字符串

pattern = re.compile("")
pattern.match(): 从起始位置往后查找,返回第一个符合的字符串
pattern.search(): 从任意位置往后查找,返回第一个符合的字符串
pattern.findall(): 所有的全部匹配,返回列表
pattern.split(): 分割字符串,返回列表
pattern.sub(): 替换,返回字符串
re.I表示忽略大小写;re.S表示全文匹配而不是只匹配当前这一行

* : 零次或多次,等同于{0,}
? : 零次或一次,等同于{0,1}
+ : 一次或多次,等同于{1,}
^ : 字符串开头,如果在[]内表示取反
$ : 字符串结尾
. : 匹配除\n以外的任意单个字符
[] : 匹配内容
{} : 限定次数
() : 子表达式
\ : 转义下一个字符,在字符串里要写双斜杠\\

\d : 匹配任意数字,等同于[0-9]
\D : 匹配任意非数字,等同于[^0-9]
\w : 匹配任意字符,等同于[a-zA-Z0-9_]
\W : 匹配任意非字符,等同于[^a-zA-Z0-9_]
\s : 匹配任意空白字符,等同于[\t\n\r\f]
\S : 匹配任意非空字符,等同于[^\t\n\r\f]
\b : 匹配任意边界,例如：er\b与never中er匹配,但与verb中er不匹配
\B : 匹配任意非边界

{n} : 刚好n次
{n,} : 至少n次
{n,m} : 至少n次至多m次

组 : ((A)(B(C)))

在线正则表达式: http://tool.oschina.net/regex/
参考文档：http://www.runoob.com/python3/python3-reg-expressions.html
"""

import re
import urllib.request

def regex():
    # match()
    pattern = re.compile(r"\d+")
    m = pattern.match("aaa123bbb456")
    print(m)  # None
    m = pattern.match("aaa123bbb456", 2, 5)
    print(m)  # None
    m = pattern.match("aaa123bbb456", 3, 5)
    print(m)  # <_sre.SRE_Match object; span=(3, 5), match='12'>
    print(m.group())  # 12

    pattern = re.compile(r"([a-z]+) ([a-z]+)", re.I)  # re.I表示忽略大小写;re.S表示全文匹配
    m = pattern.match("Hello World Hello python")
    # group()方法返回符合规则的组,不写默认0
    print(m.group(0))  # Hello World
    print(m.group(1))  # Hello
    print(m.group(2))  # World
    # print(m.group(3))  # IndexError: no such group

    # span()方法返回符合规则的第n个串的索引区间
    print(m.span())  # (0, 11)
    print(m.span(1))  # (0, 5)
    print(m.span(2))  # (6, 11)

    # search()
    pattern = re.compile(r"\d+")
    s = pattern.search("aaa123bbb456")
    print(s.group())  # 123
    s = pattern.search("aaa123bbb456", 2, 5)
    print(s.group())  # 12
    s = pattern.search("aaa123bbb456", 3, 5)
    print(s.group())  # 12

    # findall()
    pattern = re.compile(r"\d+")
    f = pattern.findall("abc 123 def 456")
    # findall()返回的是列表,不需要调用group()
    print(f)  # ['123', '456']
    pattern = re.compile(r"\d*")  # *表示贪婪模式: 尽可能获取多的
    f = pattern.findall("abc 123 def 456")
    print(f)  # ['', '', '', '', '123', '', '', '', '', '', '456', '']
    pattern = re.compile(r"\d?")  # ?表示非贪婪模式: 尽可能获取少的
    f = pattern.findall("abc 123 def 456")
    print(f)  # ['', '', '', '', '1', '2', '3', '', '', '', '', '', '4', '5', '6', '']

    # split()
    s = re.split("[\s\d\\\;]+", "abc12 de;34\fg")
    print(s)  # ['abc', 'de', 'g']

    # sub()
    str1 = "abc123def"
    s1 = re.sub("\d+", "emmm", str1)
    print(s1)  # abcemmmdef
    str2 = "     hello   python  "
    s2 = re.sub("\s", "", str2)
    print(s2)  # hellopython
    print(len(s2))  # 11

class NeihanduanziSpider(object):
    """
    用正则表达式爬内涵段子
    """

    # 初始化
    def __init__(self):
        self.page = 1
        self.switch = True

    # 爬取数据
    def loadPage(self):

        # 待爬取url
        url = "http://www.neihanpa.com/article/list_5_" + str(self.page) + ".html"
        # http请求头
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"}
        # 创建请求对象
        request = urllib.request.Request(url, headers=headers)

        # 使用代理IP
        # proxy_list = [
        #     {"http": "113.89.54.209:9999"},
        #     {"http": "61.50.244.179:808"},
        #     {"http": "58.220.95.107:8080"}
        # ]
        # proxy = random.choice(proxy_list)
        # proxy_handler = urllib.request.ProxyHandler(proxy)
        # opener = urllib.request.build_opener(proxy_handler)
        # response = opener.open(request)

        # 发送请求
        response = urllib.request.urlopen(request)

        # chardet可以测试网页编码
        # res = chardet.detect(response.read())
        # print(res)  # {'language': 'Chinese', 'confidence': 0.99, 'encoding': 'GB2312'}

        # 爬网页的时候要注意网页源码的charset,乱码时要用decode()做解码
        # ignore参数表示忽略非gb2312编码的字符,因为网站可能会注入少量其它字符
        html = response.read().decode("gb2312", "ignore")
        print(type(html))  # <class 'str'>
        # print(html)

        # 使用正则过滤数据
        pattern = re.compile('<div class="f18 mb20">(.*?)</div>', re.S)
        result = pattern.findall(html)
        print(type(result))  # <class 'list'>
        # print(result)
        print("*****正在爬取第 %d 页数据*****" % self.page)
        for item in result:
            item = item.replace("<p>", "").replace("</p>", "").replace("<br />", "")
            self.writeToFile(item)

    # 保存到本地
    def writeToFile(self, item):
        f = open("D://data.txt", "a", encoding="utf-8")
        f.write(item)
        f.write("=" * 100)
        f.close()

    # 循环爬取
    def work(self):
        while self.switch:
            self.loadPage()
            self.page += 1


if __name__ == "__main__":
    # regex()

    s = NeihanduanziSpider()
    s.work()