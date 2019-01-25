# coding=utf-8
"""
开闭原则：已经实现的功能代码不要修改,可以扩展;即开放扩展功能封闭已实现功能代码
装饰器(decorator)：用来装饰函数,可以扩展函数功能,函数有多个装饰器时要注意执行流程(装饰时由内往外,调用时由外往内)
格式: @deco 等价于 f = deco(f) --->用函数本身接收装饰后的函数
"""


# 1、装饰器装饰不带参函数
def deco01(func):
    print("---正在装饰1---")
    def inner():
        print("---正在验证权限1---")
        func()
    return inner

def deco02(func):
    print("---正在装饰2---")
    def inner():
        print("---正在验证权限2---")
        func()
    return inner

# @函数名是python语法糖,只要解释器执行到这里,就会自动装饰,而不用等到调用函数的时候
@deco01  # 等价于 f1 = deco01(f1)
@deco02  # 等价于 f1 = deco02(f1)
def f1():
    print("hello python")
f1()

print("=" * 50)

# 2、装饰器装饰带参函数(内部函数inner和指向被装饰函数的函数func都要跟随被装饰函数f2一样带参数)
def deco03(func):
    print("---正在装饰3---")
    def inner(*args, **kwargs):  # 此处也要定义参数
        print("---正在验证权限3---")
        func(*args, **kwargs)  # 此处要拆包
    return inner

@deco03  # f2 = deco03(f2)
def f2(a, b):
    print("a=%d;b=%d" % (a, b))

f2(10, 20)

print("=" * 50)

# 3、装饰器装饰有返回值函数(指向被装饰函数的函数要接收返回值,并将返回值作为内部函数的结果返回给被装饰函数)
def deco04(func):
    print("---正在装饰4---")
    def inner():
        print("---正在验证权限4---")
        ret = func()  # 保存返回来的lol
        return ret  # 将lol返回给83行的调用
    return inner

@deco04  # f3 = deco04(f3)
def f3():
    return "lol"

res = f3()
print("the return value is %s" % res)

print("=" * 50)

# 4、通用装饰器(不管有没有参数和返回值)
def deco0(func):
    print("---正在装饰---")
    def inner(*args, **kwargs):
        print("---正在验证权限---")
        ret = func(*args, **kwargs)
        return ret
    return inner

# 5、带参数的装饰器(在装饰不同函数时能起到不同作用)
def deco05_arg(arg):
    def deco05(func):
        print("---正在装饰---")
        def inner():
            print("---正在验证权限---")
            if arg == "grubby":
                func()
            else:
                func()
                func()
        return inner
    return deco05

# 1、先执行deco05_arg("**")函数,返回值是deco05这个函数的引用
# 2、再用@deco05对被装饰函数进行装饰
@deco05_arg("grubby")  # f4 = deco05_arg(f4)
def f4():
    print("---f4---")

@deco05_arg("moon")  # f5 = deco05_arg(f5)
def f5():
    print("---f5---")

f4()
f5()

print("=" * 50)

"""
类装饰器: 用类装饰函数,先创建对象并执行__init__()函数初始化
"""
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

