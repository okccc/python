# coding=utf-8
"""
JSON(JavaScript Object Notation):
1、JavaScript对象表示法,独立于语言和平台
2、轻量级的文本数据交换格式(比如网站前后台的数据交换)
3、类似xml且比xml更小更快更易解析
json简单说就是javascript中的对象和数组,通过这两种结构可以表示各种复杂的结构
对象: 在js中用{}表示,数据结构为{key: value}键值对,通过key取值;key是字符串,value可以是字符串、数字、数组、对象等
数组: 在js中用[]表示,数据结构为["python", "java"],通过索引取值;字段值类型可以是字符串、数字、数组、对象等
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
"""

import json
import jsonpath
import chardet
import requests

"""
json.dumps(obj): 将Python对象序列化成Json格式的字符串(Serialize obj to a JSON formatted str)
序列化: 把变量从内存中变成可存储或传输的过程,延长生命周期
注意: json.dumps()序列化默认使用ascii编码,处理中文时要添加参数ensure_ascii=False禁用ascii编码,按utf-8编码
chardet.detect(byte_str)可以测试网页编码,参数类型必须是bytes or bytearray
"""
def dumps():
    tuple = (1, 2, 3, 4)
    list = [1, 2, 3, 4]
    dict = {"city": "上海", "name": "grubby"}
    print(json.dumps(tuple))  # [1, 2, 3, 4]
    print(type(json.dumps(tuple)))  # <class 'str'>
    print(json.dumps(list))  # [1, 2, 3, 4]
    print(type(json.dumps(list)))  # <class 'str'>

    print(json.dumps(dict))  # {"city": "\u4e0a\u6d77", "name": "grubby"}
    print(type(json.dumps(dict)))  # <class 'str'>
    # 将str编码成bytes
    res = json.dumps(dict).encode('utf-8')
    print(type(res))  # <class 'bytes'>
    print(chardet.detect(res))  # {'encoding': 'ascii', 'confidence': 1.0, 'language': ''}

    print(json.dumps(dict, ensure_ascii=False))  # {"name": "grubby", "city": "上海"}
    # 将str编码成bytes
    res = json.dumps(dict, ensure_ascii=False).encode('utf-8')
    print(type(res))  # <class 'bytes'>
    print(chardet.detect(res))  # {'encoding': 'utf-8', 'language': '', 'confidence': 0.7525}


"""
json.loads(): 将包含Json文档的字符串实例反序列化成Python对象
(Deserialize s (a str instance containing a JSON document) to a python object)
注意: a str是一个整块,不能是多个小的块(loads/load does not decode multiple json object)
"""
def loads():
    list_str = '[1, 2, 3, 4]'
    dict_str = '{"city": "上海", "name": "grubby"}'
    print(json.loads(list_str))  # [1, 2, 3, 4]
    print(type(json.loads(list_str)))  # <class 'list'>
    print(json.loads(dict_str))  # {'name': 'grubby', 'city': '上海'}
    print(type(json.loads(dict_str)))  # <class 'dict'>


"""
json.dump(): 将Python对象序列化成json字符串后写入文件
(Serialize obj as a JSON formatted stream to fp (a .write()-supporting file-like object).)
"""
def dump():
    list = [{"city": "上海"}, {"name": "grubby"}]
    dict = {"city": "上海", "name": "grubby"}
    json.dump(list, open("C://Users/Public/list.json", "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(dict, open("C://Users/Public/dict.json", "w", encoding="utf-8"), ensure_ascii=False)


"""
json.load(): 将文件中json字符串反序列化成python对象
(Deserialize fp (a .read()-supporting file-like object containing a JSON document) to a python object)
"""
def load():
    list_str = json.load(open("C://Users/Public/list.json", encoding="utf-8"))
    dict_str = json.load(open("C://Users/Public/dict.json", encoding="utf-8"))
    print(list_str)  # [{'city': '上海'}, {'name': 'grubby'}]
    print(type(list_str))  # <class 'list'>
    print(dict_str)  # {'city': '上海', 'name': 'grubby'}
    print(type(dict_str))  # <class 'dict'>


"""
需求: 获取拉勾网城市Json文件http://www.lagou.com/lbs/getAllCitySearchLabels.json的所有城市
jsonpath.jsonpath(obj, express): traverse JSON object using jsonpath expr, returning values or paths
"""
def lagou():
    # 文件链接
    url = "http://www.lagou.com/lbs/getAllCitySearchLabels.json"
    # 请求头
    headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"}
    # 发送get请求
    response = requests.get(url, headers=headers)
    # 获取数据
    text = response.text
    print(type(text))  # <class 'str'>
    # 将json格式的字符串转换成Python对象
    dict = json.loads(text)
    print(type(dict))  # <class 'dict'>
    # 通过JsonPath表达式解析
    city_list = jsonpath.jsonpath(dict, '$..name')
    print(type(city_list))  # <class 'list'>
    # for city in city_list:
    #     print(city)

    # 将list序列化成json数组
    array = json.dumps(city_list, ensure_ascii=False)
    # print(type(array))  # <class 'str'>
    # print(chardet.detect(array.encode('utf-8')))  # {'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}

    # 写入本地文件
    with open("C://Users/qmtv/Documents/city.txt", "w") as f:
        f.write(array)


if __name__ == "__main__":
    dumps()
    # loads()
    # dump()
    # load()
    # lagou()
