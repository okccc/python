# coding=utf-8
"""
开闭原则：对函数开放扩展功能封闭已有功能
装饰器(decorator)：装饰器本质上也是函数,用来装饰被装饰函数从而扩展其功能而不改变已有代码
格式：@deco 等价于 f = deco(f) -->用函数本身接收装饰后的函数
多装饰器：装饰时由内往外,调用时由外往内
应用：插入日志、性能测试、事务处理、缓存、权限校验等有切面需求的场景
"""


def outer(a, b):
    # 闭包：在函数内部继续定义函数,并且内部函数用到了外部函数的变量,最终返回内部函数结果,那么这个内部函数及用到的变量称为闭包
    def inner(x):
        return a * x + b
    return inner

o = outer(3, 5)
print(o(2))  # 11


# 1.装饰器装饰不带参函数
def deco01(func):
    print("正在装饰1")
    def inner():
        print("正在验证权限1")
        func()
    return inner

def deco02(func):
    print("正在装饰2")
    def inner():
        print("正在验证权限2")
        func()
    return inner

# @函数名是python语法糖,只要解释器执行到这里,就会自动装饰,而不用等到调用函数的时候
@deco01  # 等价于 f1 = deco01(f1)
@deco02  # 等价于 f1 = deco02(f1)
def f1():
    print("hello python")

# f1()
"""
正在装饰2
正在装饰1
正在验证权限1
正在验证权限2
hello python
"""


# 2.装饰器装饰带参函数
def deco03(func):
    print("正在装饰3")
    def inner(*args, **kwargs):  # 内置函数的传参和返回值类型要和被装饰函数保持一致
        print("正在验证权限3")
        func(*args, **kwargs)
    return inner

@deco03  # f2 = deco03(f2)
def f2(a, b):
    print("a=%d&b=%d" % (a, b))

f2(10, 20)
"""
正在装饰3
正在验证权限3
a=10&b=20
"""


# 3.装饰器装饰有返回值函数
def deco04(func):
    print("正在装饰4")
    def inner():
        print("正在验证权限4")
        ret = func()
        return ret
    return inner

@deco04  # f3 = deco04(f3)
def f3():
    return "lol"

res = f3()
print("the return value is %s" % res)
"""
正在装饰4
正在验证权限4
the return value is lol
"""


# 4.万能装饰器(不管有没有参数和返回值)
def deco0(func):
    print("正在装饰")
    def inner(*args, **kwargs):
        print("正在验证权限")
        ret = func(*args, **kwargs)
        return ret
    return inner


# 5.带参数的装饰器(通过参数控制装饰不同函数起不同作用)
def deco05_arg(arg):
    def deco05(func):
        print("正在装饰")
        def inner():
            print("正在验证权限")
            if arg == "grubby":
                func()
            else:
                func()
                func()
        return inner
    return deco05

# 先执行deco05_arg("**")函数,返回值是deco05这个函数的引用,再用@deco05对被装饰函数进行装饰
@deco05_arg("grubby")  # f4 = deco05_arg(f4)
def f4():
    print("---f4---")

f4()
"""
正在装饰
正在验证权限
---f4---
"""

@deco05_arg("moon")  # f5 = deco05_arg(f5)
def f5():
    print("---f5---")

f5()
"""
正在装饰
正在验证权限
---f5---
---f5---
"""


# 类装饰器: 用类装饰函数,先创建对象并执行__init__()函数初始化
class Test(object):
    def __init__(self, func):
        print("---正在初始化---")
        print("func name is %s" % func.__name__)
        self.__func = func

    # 如果直接调用对象的话,对象中必须要有callable的函数,即__call__()
    def __call__(self, *args, **kwargs):
        print("---正在装饰---")
        self.__func()


@Test  # test = Test(test) 解释器执行到这里就已经开始装饰,此时test是由Test类创建的对象,而不再是原来的test函数
def test():
    print("---test---")

test()
"""
---正在初始化---
func name is test
---正在装饰---
---test---
"""
