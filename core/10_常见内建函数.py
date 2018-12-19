# coding=utf-8
"""
内建函数: python解释器启动后默认加载的函数,可通过dir(__builtins__)查找
"""
from functools import reduce

"""
range(): 常用于列表生成器
"""

"""
map(): 对指定序列做映射
格式: map(function, sequence)
     function: 一个函数
     sequence: 一个或多个序列,取决于function需要几个参数
"""
a = map(lambda x: x * x, [1, 2, 3])
print(type(a))  # <class 'map'>
print(list(a))  # [1, 4, 9]

b = map(lambda x, y: x + y, [1, 2, 3], [4, 5, 6])
print(type(b))  # <class 'map'>
print(list(b))  # [5, 7, 9]

"""
filter(): 对指定序列做过滤,返回结果为True的,返回值类型和序列类型相同
格式: filter(function or None, sequence)
     function: 一个函数
     sequence: 序列可以使str,tuple,list
"""
c = filter(lambda x: x % 2, [1, 2, 3, 4])
print(type(c))  # <class 'filter'>
print(list(c))  # [1, 3] python里面0表示False,非0表示True

d = filter(None, "hello")
print(type(d))  # <class 'filter'>
print(list(d))  # ['h', 'e', 'l', 'l', 'o']

"""
reduce(): 对指定序列做累加,存放在functools模块里,要用的话要先导包
格式: reduce(function, sequence, initial)
     function: 一个函数
     sequence: 序列可以使str,tuple,list
     initial: 固定初始值
"""

e = reduce(lambda x, y: x + y, [1, 2, 3, 4])
print(type(e))  # <class 'int'>
print(e)  # 10

f = reduce(lambda x, y: x + y, ['a', 'b', 'c'], 'd')
print(type(f))  # <class 'str'>
print(f)  # dabc

"""
sorted(): 对指定序列排序
格式: sorted(iterable, cmp=None, key=None, reverse=False)
     iterable: 一个可迭代对象
     reverse: 是否倒序(0代表False,非0代表True)
"""
g = sorted([11, 33, 22, 55])
print(g)  # [11, 22, 33, 55]

h = sorted(['a', 'c', 'd', 'b'], reverse=5)
print(h)  # ['d', 'c', 'b', 'a']
