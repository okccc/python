# coding=utf-8
"""
算法复杂度
基本操作(赋值/加减乘除)：只有常数项,O(1)
顺序结构(代码移到下一行)：时间复杂度按加法计算
循环结构(for/while)：时间复杂度按乘法计算
分支结构(if)：时间复杂度取最大值
时间消耗：O(1) < O(logn) < O(n) < O(nlogn) < O(n2) < O(n3) < O(2n) < O(n!) < O(nn)
大O记法：处理规模为n的数据所用时间T(n)即是算法复杂度,一般只看最高次项,比如3n^2和10n^2是一个级别,复杂度默认指最坏复杂度
程序 = 算法 + 数据结构 --> 算法是解决问题的设计思想,数据结构描述了数据元素之间的关系,是算法处理问题的载体

timeit模块：可以测试一段Python程序的运行速度
t = Timer(stmt='pass', setup='pass', timer=<timer function>)
t.timeit(n)   -- 测试n次代码结果取平均值
然而程序的算法复杂度不能只看时间,因为不同性能的机器运行时间不一样,应该根据程序的运算数量来判断

线性表：某类元素的一个集合,记录着元素之间的顺序关系线性表是最基本的数据结构之一
根据存储方式不同分为:
顺序表：将元素顺序的存放在一块连续的存储区里
链表：将元素存放在通过链接构造起来的一系列存储块中

顺序表两种基本实现方式:
一体式结构：表信息(容量+元素个数)和元素存放在同一个存储区
分离式结构(常用)：表信息(容量+元素个数)和元素存放在不同的存储区
Python中list就是采用分离式技术实现的动态顺序表

顺序表操作:
增加元素：1、尾部追加,时间复杂度O(1)
         2、非保序的加入元素(不常用),时间复杂度O(1)
         3、保序的加入元素,时间复杂度O(n)
删除元素：1、删除尾部元素,时间复杂度O(1)
         2、非保序的元素删除(不常用),时间复杂度O(1)
         3、保序的元素删除,时间复杂度O(n)

顺序表的构建需要预先知道数据大小来申请连续的存储空间,而且在扩充时又需要进行数据的搬迁,很不灵活
链表结构可以充分利用计算机内存空间,实现灵活的内存动态管理
链表：属于线性表的一种,是一种常见的数据结构,它不像顺序表一样连续存储数据,而是在每一个节点(数据存储单元)
     存放下一个节点的位置信息(地址)
"""

import time
from timeit import Timer

def test():
    # 如果 a+b+c=N且 a^2+b^2=c^2(a,b,c 为自然数)，如何求出所有a、b、c可能的组合？
    start_time = time.time()
    for a in range(0, 1001):  # 循环结构
        for b in range(0, 1001):  # 循环结构
            # for c in range(0, 1001):
            c = 1000 - a - b  # 循环结构内部的基本操作
            if a + b + c == 1000 and a ** 2 + b ** 2 == c ** 2:  # 循环结构内部的分支结构
                print("a=%d,b=%d,c=%d" % (a, b, c))
    # 该函数算法复杂度：T(n) = n * n * (1 + max(0, 1)) = 2n^2 = O(n^2)
    end_time = time.time()
    print("time:%d" % (end_time - start_time))


def test01():
    L = []
    for i in range(10000):
        L += [i]

def test02():
    L = []
    for i in range(10000):
        L.append(i)

def test03():
    L = [i for i in range(10000)]

def test04():
    L = []
    for i in range(10000):
        L.extend([i])

t1 = Timer(stmt="test01()", setup="from __main__ import test01")
print("+=", t1.timeit(10000))
t2 = Timer(stmt="test02()", setup="from __main__ import test02")
print("append", t2.timeit(10000))
t3 = Timer(stmt="test03()", setup="from __main__ import test03")
print("generator", t3.timeit(10000))
t4 = Timer(stmt="test04()", setup="from __main__ import test04")
print("extend", t4.timeit(10000))
