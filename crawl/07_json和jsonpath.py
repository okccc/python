# coding=utf-8
"""
JSON(JavaScript Object Notation):
1.JavaScript对象表示法,独立于语言和平台
2.轻量级的文本数据交换格式(比如网站前后台不同语言之间的数据交换)
3.类似xml且比xml更小更快更易解析
json其实就是javascript中的数组和对象,通过这两种结构可以表示各种复杂的结构
数组array --> python中list,数据结构为["python", "java"],通过索引取值;字段值类型可以是字符串、数字、数组、对象等
对象object --> python中dict,数据结构为{key: value}键值对,通过key取值;key是字符串,value可以是字符串、数字、数组、对象等
空值null --> python中None
json模块提供了四个功能: dumps、dump、loads、load,用于Json字符串和Python对象之间的序列化/反序列化

JsonPath: 遍历Json对象中的节点;JsonPath之于Json相当于XPath之于XML
XPath    JsonPath       描述
/	        $	        根节点
.	        @	        当前节点
/	        .or[]	    取子节点
..	        n/a	        取父节点,JsonPath未支持
//	        ..	        就是不管位置,选择所有符合条件的内容
*	        *	        匹配所有元素节点
@	        n/a	        根据属性访问,JsonPath不支持,因为Json是Key-value递归结构,不需要
[]	        []	        迭代器标示(可以在里边做简单的迭代操作,如数组下标,根据内容选值等)
|	        [,]	        支持迭代器中做多选
[]	        ?()	        支持过滤操作
n/a	        ()	        支持表达式计算
()	        n/a	        分组,JsonPath不支持

抓包技巧：
1.有些网站pc端数据很难获取(加密、反爬...)可以尝试app端,很多直接返回json数据
2.在Network查找真实url时,***?callback=jsonp或者***?callback=jQuery这种格式的请求会返回类json数据,去掉callback函数就是json
url = "https://tousu.sina.com.cn/api/index/s?callback=jQuery&keywords=%E4%B8%8A%E6%B5%B7&page_size=10&page=1&_=1552983689513"
url = "https://m.douban.com/rexxar/api/v2/subject_collection/movie_showing/items?os=android&for_mobile=1&callback=jsonp2&start=18&count=18&loc_id=108288&_=1552985740409"
上述url中的callback=jQuery、callback=jsonp2以及末尾的时间戳都可以去掉
"""

import json
import requests
import jsonpath
import chardet
from pprint import pprint
import re

def dumps():
    """
    json.dumps(obj)：将Python对象序列化成Json格式的字符串(Serialize obj to a JSON formatted str)
    序列化：把变量从内存中变成可存储或传输的过程,延长生命周期
    注意：json.dumps()序列化默认使用ascii编码,处理中文时要添加参数ensure_ascii=False禁用ascii编码,按utf-8编码
    chardet.detect(byte_str)可以测试网页编码,参数类型必须是bytes or bytearray
    """
    T = (1, 2, 3, 4)
    L = [1, 2, 3, 4]
    D = {"city": "上海", "name": "grubby"}
    print(json.dumps(T))  # [1, 2, 3, 4]
    print(type(json.dumps(T)))  # <class 'str'>
    print(json.dumps(L))  # [1, 2, 3, 4]
    print(type(json.dumps(L)))  # <class 'str'>
    print(json.dumps(D))  # {"city": "\u4e0a\u6d77", "name": "grubby"}
    print(type(json.dumps(D)))  # <class 'str'>

    # 将str编码成bytes
    res = json.dumps(D).encode('utf-8')
    print(type(res))  # <class 'bytes'>
    print(chardet.detect(res))  # {'encoding': 'ascii', 'confidence': 1.0, 'language': ''}

    print(json.dumps(D, ensure_ascii=False))  # {"name": "grubby", "city": "上海"}
    # 将str编码成bytes
    res = json.dumps(D, ensure_ascii=False).encode('utf-8')
    print(type(res))  # <class 'bytes'>
    print(chardet.detect(res))  # {'encoding': 'utf-8', 'language': '', 'confidence': 0.7525}

def dump():
    """
    json.dump()：将Python对象序列化成json字符串后写入文件(Serialize obj as a JSON formatted stream to fp (a .write()-supporting file-like object).)
    """
    L = [{"city": "上海"}, {"name": "grubby"}]
    D = {"city": "上海", "name": "grubby"}
    json.dump(L, open("C://Users/Public/list.json", "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(D, open("C://Users/Public/dict.json", "w", encoding="utf-8"), ensure_ascii=False)

def loads():
    """
    json.loads()：将包含Json文档的字符串实例反序列化成Python对象(Deserialize s (a str instance containing a JSON document) to a python object)
    """
    list_str = '[1, 2, 3, 4]'
    dict_str = '{"city": "上海", "name": "grubby"}'
    print(json.loads(list_str))  # [1, 2, 3, 4]
    print(type(json.loads(list_str)))  # <class 'list'>
    print(json.loads(dict_str))  # {'name': 'grubby', 'city': '上海'}
    print(type(json.loads(dict_str)))  # <class 'dict'>

def load():
    """
    json.load()：将文件中json字符串反序列化成python对象(Deserialize fp (a .read()-supporting file-like object containing a JSON document) to a python object)
    """
    list_str = json.load(open("C://Users/Public/list.json", encoding="utf-8"))
    dict_str = json.load(open("C://Users/Public/dict.json", encoding="utf-8"))
    print(list_str)  # [{'city': '上海'}, {'name': 'grubby'}]
    print(type(list_str))  # <class 'list'>
    print(dict_str)  # {'city': '上海', 'name': 'grubby'}
    print(type(dict_str))  # <class 'dict'>

def json01():
    # 获取拉勾城市信息
    url = "http://www.lagou.com/lbs/getAllCitySearchLabels.json"
    # 请求头
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"}
    # 发送get请求
    response = requests.get(url, headers=headers)
    # 将json格式的字符串转换成Python对象
    data = json.loads(response.text)
    # pprint可以格式化输出内容,使dict等数据格式看着更美观
    pprint(data)
    # 通过JsonPath解析出目标字段
    citys = jsonpath.jsonpath(data, '$..name')
    print(citys)  # <class 'list'>
    # 保存数据
    with open("./city.json", "w", encoding="utf8") as f:
        # dumps()可以设置换行时的缩进,这样json字符串就不是一整行而是json格式
        f.write(json.dumps(data, ensure_ascii=False, indent=4))

def json02():
    # 抓取36kr上的文章
    url = "https://36kr.com/"
    # 请求头
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"}
    # 发送请求获取响应
    response = requests.get(url, headers=headers)
    # 通过在response中搜索文章标题发现数据在第69行的<script></script>标签里面,正则匹配取出数据
    # res = re.findall("<script>var props=(.*?)</script>", response.text)[0]
    res = re.findall("<script>var props=(.*?),locationnal=", response.text)[0]
    # 将json字符串转换成dict
    data = json.loads(res)  # json.decoder.JSONDecodeError: Extra data: line 1 column 144652 (char 144651)
    print(data)
    # 将数据写入本地分析错误原因,发现1:144652处有个,locationnal={...},说明这是用逗号隔开的两个json串,经取舍取前面部分即可
    with open("images/36kr.json", "w", encoding="utf8") as f:
        f.write(res)


if __name__ == "__main__":
    # dumps()
    # loads()
    # dump()
    # load()
    # json01()
    json02()
