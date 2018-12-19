# coding=utf-8
import copy

"""
浅拷贝与深拷贝:
浅拷贝: 指向同一个内存地址
深拷贝: 指向不同内存地址
"""


def test01():
    a = [11, 22, 33]
    b = a
    print(id(a))  # 14265288
    print(id(b))  # 14265288
    c = copy.deepcopy(a)
    print(id(c))  # 14263880


# test01()

"""
2种深拷贝:
deepcopy: 反复拷贝过程中拷贝的是上一层,且与数据类型无关
copy: 反复拷贝过程中只拷贝第一层,但如果是不可变类型(tuple),就不拷贝而是指向当前这一层的内存地址
"""


def test02():
    a = [11, 22, 33]
    b = [44, 55, 66]
    c1 = [a, b]
    c2 = (a, b)
    print(c1)  # [[11, 22, 33], [44, 55, 66]]
    print(c2)  # ([11, 22, 33], [44, 55, 66])
    d1 = copy.deepcopy(c1)
    d2 = copy.deepcopy(c2)
    print(id(c1))  # 14526536
    print(id(d1))  # 14528264
    print(id(c2))  # 10623560
    print(id(d2))  # 10623624
    a.append(77)
    print(c1[0])  # [11, 22, 33, 77]
    print(d1[0])  # [11, 22, 33]
    print(c2[0])  # [11, 22, 33, 77]
    print(d2[0])  # [11, 22, 33]


# test02()


def test03():
    a = [11, 22, 33]
    b = [44, 55, 66]
    c1 = [a, b]
    c2 = (a, b)
    print(c1)  # [[11, 22, 33], [44, 55, 66]]
    print(c2)  # ([11, 22, 33], [44, 55, 66])
    d1 = copy.copy(c1)
    d2 = copy.copy(c2)
    print(id(c1))  # 12232776
    print(id(d1))  # 11852616
    print(id(c2))  # 6822472
    print(id(d2))  # 6822472
    a.append(77)
    print(c1[0])  # [11, 22, 33, 77]
    print(d1[0])  # [11, 22, 33, 77]
    print(c2[0])  # [11, 22, 33, 77]
    print(d2[0])  # [11, 22, 33, 77]


# test03()
