# coding=utf-8
"""
可迭代对象(Iterable)：可以作用于for循环的对象,可用isinstance(**, Iterable)判断
迭代器(Iterator)：可以不断调用next()返回下一个值的对象,可用isinstance(**, Iterator)判断
iter()函数：'',(),[]等都是Iterable,但不是Iterator,iter()可以将Iterable变成Iterator,生成器一定是迭代器

生成器(generator)：加了yield的函数不再是普通函数,调用该函数不会立即执行而是返回一个生成器,可以不断调用next()获取下一个值
yield作用：中断函数并返回后面的值,然后在下一次执行next()方法时从当前位置继续运行
"""

from collections import Iterable
from collections import Iterator
import sys


def iterator():
    # 判断是否是可迭代对象
    print(isinstance(100, Iterable))  # False
    print(isinstance('abc', Iterable))  # True
    print(isinstance((), Iterable))  # True
    print(isinstance([], Iterable))  # True
    print(isinstance({}, Iterable))  # True
    print(isinstance((i for i in range(1, 10)), Iterable))  # True
    # 判断是否是迭代器
    print(isinstance(100, Iterator))  # False
    print(isinstance('abc', Iterator))  # False
    print(isinstance((), Iterator))  # False
    print(isinstance([], Iterator))  # False
    print(isinstance({}, Iterator))  # False
    print(isinstance((i for i in range(1, 10)), Iterator))  # True
    # 将可迭代对象变成迭代器,通过next()不断调用
    L = [11, 22, 33]
    I = iter(L)
    print(I)  # <list_iterator object at 0x0000020B96AFD198>
    print(next(I))  # 11
    print(next(I))  # 22
    print(next(I))  # 33


def fibonacci(n):
    a, b, count = 0, 1, 0
    while count < n:
        a, b = b, a + b
        count += 1
        yield a

f = fibonacci(10)
print(f)  # <generator object fibonacci at 0x0000023738144308>
print(isinstance(f, Iterator))  # True --> 说明生成器也是迭代器
# while True:
#     try:
#         print(next(f), end=" ")  # 1 1 2 3 5 8 13 21 34 55
#     except StopIteration:  # StopIteration异常用于标识迭代的完成,防止出现无限循环的情况
#         sys.exit()  # 退出python解释器,后续代码不会再执行


"""
多任务: yield可以切换多个任务同时执行
"""
def test1():
    count = 0
    while count < 5:
        count += 1
        yield count

def test2():
    count = 5
    while count > 0:
        count -= 1
        yield count

t1 = test1()
t2 = test2()
print(t1)  # <generator object test1 at 0x000001BF7FA01048>
print(t2)  # <generator object test2 at 0x000001BF7FA016D0>
while True:
    try:
        print(next(t1))
        print(next(t2))
    except StopIteration:
        sys.exit()

