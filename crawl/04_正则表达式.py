# coding=utf-8
"""
re(regular expression)：用于匹配字符串,r""表示忽视\的转义效果("aaa\tbbb" --> "aaa bbb" | r"aaa\tbbb" --> "aaa\tbbb")
pattern = re.compile(r"...")：预编译正则表达式生成pattern对象放到内存中,然后再与目标字符串匹配,可以提升效率

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
import chardet

def regex01():
    # 1.match()：只匹配字符串的开始,返回第一个符合的字符串,不符合就返回None
    pattern = re.compile("\d+")
    m = pattern.match("aaa123bbb456")
    print(m)  # None
    m = pattern.match("aaa123bbb456", 2, 5)
    print(m)  # None
    m = pattern.match("aaa123bbb456", 3, 5)
    print(m)  # <_sre.SRE_Match object; span=(3, 5), match='12'>
    print(m.group())  # 12

    pattern = re.compile("([a-z]+) ([a-z]+)", re.I)  # re.I表示忽略大小写
    m = pattern.match("Hello World Hello python")
    # group()方法返回符合规则的组,不写默认0
    print(m.group(0))  # Hello World
    print(m.group(1))  # Hello
    print(m.group(2))  # World
    # print(m.group(3))  # IndexError: no such group

    # span()方法返回符合规则的第n个子串的索引区间
    print(m.span())  # (0, 11)
    print(m.span(1))  # (0, 5)
    print(m.span(2))  # (6, 11)

    # 2.search()：匹配整个字符串,返回第一个符合的字符串
    pattern = re.compile("\d+")
    s = pattern.search("aaa123bbb456")
    print(s.group())  # 123
    s = pattern.search("aaa123bbb456", 2, 5)
    print(s.group())  # 12
    s = pattern.search("aaa123bbb456", 3, 5)
    print(s.group())  # 12

    # 3.findall()：匹配所有的,返回列表 --> 爬虫常用
    pattern = re.compile("\d+")  # re默认是贪婪模式,尽可能匹配多的内容
    f = pattern.findall("abc 123 def 456")
    print(f)  # ['123', '456']
    pattern = re.compile("\d+?")  # 在+/*后面加上?表示非贪婪模式,尽可能匹配少的内容
    f = pattern.findall("abc 123 def 456")
    print(f)  # ['1', '2', '3', '4', '5', '6']

    # 4.split()：切割,返回列表
    s = re.split("[\d\s\;]+", "abc12 de;34\fg")
    print(s)  # ['abc', 'de', 'g']

    # 5.sub()：替换,返回字符串
    str1 = "abc123def"
    s1 = re.sub("\d+", "emmm", str1)
    print(s1)  # abcemmmdef
    str2 = "     hello   python  "
    s2 = re.sub("\s", "", str2)
    print(s2)  # hellopython


def regex02():
    # 请求地址
    url = "http://www.neihanpa.com/article/list_5_1.html"
    # http请求头
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"}
    # 创建请求对象
    request = urllib.request.Request(url, headers=headers)
    # 发送请求
    response = urllib.request.urlopen(request)
    # chardet测试网页编码
    res = chardet.detect(response.read())
    print(res)  # {'language': 'Chinese', 'confidence': 0.99, 'encoding': 'GB2312'}
    # 爬网页的时候要注意网页源码的charset,乱码时要用decode()做解码;ignore参数表示忽略非gb2312编码的字符,因为网站可能会注入少量其它字符
    html = response.read().decode("gb2312", "ignore")
    print(type(html))  # <class 'str'>
    # re.findall("a(.*?)b", "str")能返回()中的内容,()前后内容起到定位和过滤作用 --> 抓网页常用
    pattern = re.compile('<div class="f18 mb20">(.*?)</div>', re.S)  # re.S表示将"."的作用扩展到整个字符串,包括"\n"
    items = pattern.findall(html)
    print(type(items))  # <class 'list'>
    for item in items:
        item = item.replace("<p>", "").replace("</p>", "").replace("<br />", "")
        with open("D://data.txt", "a", encoding="utf-8") as f:
            f.write(item)


if __name__ == "__main__":
    regex01()
    # regex02()
