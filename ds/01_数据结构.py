# coding=utf-8
"""
1.数组(Arrays)
数组是固定大小结构,容纳相同类型数据,可通过索引随机访问,可以遍历/插入/删除/更新/搜索
数组可用作其它数据结构的基础,还可用于 冒泡/选择/快速/插入/二分 等排序查找算法

2.链表(Linked Lists)
链表是一种顺序结构,由相互链接的线性序列组成,必须按照顺序访问数据
链表中的元素称为节点,每个节点包含一个密钥key和一个指向next节点的指针
链表的第一个元素叫head,最后一个元素叫tail
head -> key|next -> key|next -> key|next -> null
单链列表只能正向遍历,双链表可以在前进和后退方向上遍历,循环链表头的上一个指针指向尾部,尾的下一个指针指向头
搜索：通过简单的线性搜索在给定的链表中找到键为k的第一个元素并返回指向该元素的指针
插入：在链表中插入一个密钥,可以在列表的开头、末尾、中间插入
删除：从链表中删除元素x,可以从列表的开头、末尾、中间删除

3.堆栈(Stack)
堆栈是一种先进后出的结构,可用于在递归中实现函数调用
push推送：在堆栈顶部插入一个元素
pop弹出：删除最上面的元素并返回

4.队列(Queue)
队列是一种先进先出的结构,可用于管理多线程中的线程
进队列：将元素插入队列末尾
出队列：从队列开头删除元素

5.哈希表(Hash)
哈希表采用映射函数f: key -> address将关键字映射到该记录在表中的位置,给定任意key都能通过hash函数计算出记录在表中的位置
有序数组使用二分查找复杂度是O(log2n),无序数组只能遍历查找复杂度是O(n),哈希表查找任意元素复杂度是O(1)

6.树(Tree)
树是一种层次结构,数据按层次组织并链接在一起,包括二叉搜索树、B树、红黑树等

算法复杂度
基本操作(赋值/加减乘除)：只有常数项,O(1)
顺序结构(代码移到下一行)：时间复杂度按加法计算
循环结构(for/while)：时间复杂度按乘法计算
分支结构(if)：时间复杂度取最大值
时间消耗：O(1) < O(logn) < O(n) < O(nlogn) < O(n^2) < O(n^3) < O(2^n) < O(n!) < O(n^n)
大O记法：处理规模为n的数据所用时间T(n)即是算法复杂度,一般只看最高次项,比如3n^2和10n^2是一个级别,复杂度默认指最坏复杂度
程序 = 算法 + 数据结构 --> 算法是解决问题的设计思想,数据结构描述了数据元素之间的关系,是算法处理问题的载体

timeit模块：可以测试一段Python程序的运行速度
t = Timer(stmt='pass', setup='pass', timer=<timer function>)
t.timeit(n)   -- 测试n次代码结果取平均值
然而程序的算法复杂度不能只看时间,因为不同性能的机器运行时间不一样,应该根据程序的运算数量来判断

线性表(一维)：线性表是最基本的数据结构之一,是某类元素的一个集合,记录着元素之间的顺序关系,包括顺序表和链表
顺序表：将元素顺序的存放在一块连续的存储区里
    一体式结构：表头信息(容量、元素个数)和元素存放在同一个存储区
    分离式结构：表头信息(容量、元素个数)和元素存放在不同的存储区 ---> Python中list就是采用分离式技术实现的动态顺序表
链表：不像顺序表那样连续存储数据,而是将元素存放在包含数据区和链接区的节点中
区别：
顺序表构建需要预先知道数据大小来申请连续的存储空间,而且在扩充时又需要进行数据的搬迁,很不灵活
链表结构可以充分利用计算机内存空间,实现灵活的内存动态管理
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
