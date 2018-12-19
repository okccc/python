# coding=utf-8
from collections import Iterable
from collections import Iterator

"""
可迭代对象(Iterable): 可以作用于for循环的对象,可用isinstance(**, Iterable)判断
迭代器(Iterator): 可以被next()调用并不断返回下一个值的对象,可用isinstance(**, Iterator)判断
iter()函数: '',(),[]等都是Iterable,但不是Iterator,iter()可以将Iterable变成Iterator,生成器一定是迭代器
"""

print(isinstance(100, Iterable))  # False
print(isinstance('abc', Iterable))  # True
print(isinstance((), Iterable))  # True
print(isinstance([], Iterable))  # True
print(isinstance({}, Iterable))  # True
print(isinstance((i for i in range(1, 10)), Iterable))  # True

print(isinstance(100, Iterator))  # False
print(isinstance('abc', Iterator))  # False
print(isinstance((), Iterator))  # False
print(isinstance([], Iterator))  # False
print(isinstance({}, Iterator))  # False
print(isinstance((i for i in range(1, 10)), Iterator))  # True

a = [11, 22, 33]
b = iter(a)
print(b)  # <list_iterator object at 0x0000020B96AFD198>
print(next(b))  # 11
print(next(b))  # 22
print(next(b))  # 33

print(isinstance(iter([]), Iterator))  # True
