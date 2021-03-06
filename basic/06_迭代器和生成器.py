# coding=utf-8
"""
可迭代对象：可以作用于for循环的对象,包含iter()方法,可用isinstance(**, Iterable)判断
迭代器：有返回值的可迭代对象,包含iter()和next()方法,可用isinstance(**, Iterator)判断
iter()：迭代器一定是可迭代对象但可迭代对象不一定是迭代器,iter函数可以将可迭代对象变成迭代器
生成器：使用yield关键字的函数不再是普通函数,调用该函数不会立即执行而是创建一个生成器对象,调用next()时运行
yield作用：中断函数并返回后面的值,然后在下一次执行next()方法时从当前位置继续运行,减少内存占用
优点：列表和字典等容器是先生成数据再调用,迭代器和生成器不保存数据而是保存数据的生成方式,调用时才生成极大节省内存空间
"""

from collections import Iterable
from collections import Iterator
import sys


def iterator():
    # isinstance()判断是否是可迭代对象
    print(isinstance(100, Iterable))  # False
    print(isinstance('abc', Iterable))  # True
    print(isinstance((), Iterable))  # True
    print(isinstance([], Iterable))  # True
    print(isinstance({}, Iterable))  # True
    print(isinstance((i for i in range(1, 10)), Iterable))  # True
    # isinstance()判断是否是迭代器
    print(isinstance(100, Iterator))  # False
    print(isinstance('abc', Iterator))  # False
    print(isinstance((), Iterator))  # False
    print(isinstance([], Iterator))  # False
    print(isinstance({}, Iterator))  # False
    print(isinstance((i for i in range(1, 10)), Iterator))  # True(生成器一定是迭代器)
    # iter()方法将可迭代对象变成迭代器通过next()不断调用取值,迭代器就是有返回值的可迭代对象
    a = [11, 22, 33]
    print(isinstance(a, Iterator))  # False
    b = iter(a)
    print(isinstance(b, Iterator))  # True
    print(next(b))  # 11
    print(next(b))  # 22
    print(next(b))  # 33


def fibonacci(n):
    a, b, count = 0, 1, 0
    while count < n:
        a, b = b, a + b
        count += 1
        yield a

f = fibonacci(10)
print(f)  # <generator object fibonacci at 0x0000023738144308>
print(isinstance(f, Iterator))  # True --> 说明生成器也是迭代器
while True:
    try:
        print(next(f), end=" ")  # 1 1 2 3 5 8 13 21 34 55
    except StopIteration:  # StopIteration异常用于标识迭代的完成,防止出现无限循环的情况
        sys.exit()  # 退出python解释器,后续代码不会再执行




