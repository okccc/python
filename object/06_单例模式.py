# coding=utf-8
"""
单例模式: 不管类创建多少次对象,在内存中只有一个实例

python创建对象时默认调用：
1、__new__(cls): 创建对象,返回对象引用
2、__init__(self): 初始化对象,定义实例属性   (__new__ + __init__相当于java构造方法)
"""


class Single(object):
    instance = None
    init_flag = False

    # 重写__new__方法
    def __new__(cls, *args, **kwargs):

        if cls.instance is None:
            cls.instance = object.__new__(cls)

        return cls.instance

    # 只初始化一次
    def __init__(self, name):

        if not Single.init_flag:
            self.name = name

        Single.init_flag = True


s1 = Single("grubby")
print(id(s1))
print(s1.name)
s2 = Single("moon")
print(id(s2))
print(s2.name)
