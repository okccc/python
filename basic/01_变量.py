# coding=utf-8
"""
python六大数据类型:
不可变类型: 数字(int float bool)、字符串、元组
可变类型: 列表、集合、字典(key必须是不可变类型,value任意;因为python设置键值对时会先对key做hash处理,而hash()函数只能接受不可变类型)
   注意: 变量的CUD操作改变的是list/dict的内容,而list/dict在内存中引用的地址值并不变,重新赋值才会改变变量在内存中引用的地址值

LEGB规则: python使用LEGB的顺序来查找符号对应的对象
locals: 局部变量
enclosing: 外部嵌套函数(闭包中常见)
globals: 全局变量
builtins: python内置的,与之对应的是像os、random这些要导入的模块
"""


def hash01():
    # 判断对象是否可哈希
    print(int.__hash__)  # <slot wrapper '__hash__' of 'int' objects>
    print(str.__hash__)  # <slot wrapper '__hash__' of 'str' objects>
    print(bool.__hash__)  # <slot wrapper '__hash__' of 'int' objects>
    print(tuple.__hash__)  # <slot wrapper '__hash__' of 'tuple' objects>
    print(list.__hash__)  # None
    print(set.__hash__)  # None
    print(dict.__hash__)  # None
    print(object.__hash__)  # <slot wrapper '__hash__' of 'object' objects>


def equal():
    """
    is: 比较内存地址(是否引用同一个对象),是身份运算符(is/is not)
    ==: 比较内容
    """
    a = [1, 2, 3]
    b = [1, 2, 3]
    c = a
    print(a is b)  # False
    print(a == b)  # True
    print(a is c)  # True
    print(a == c)  # True


def exchange():
    # 交换两个变量值
    a, b = 100, 200

    # 通用写法
    # c = b
    # b = a
    # a = c
    # print(a, b)

    # python写法
    # a, b = (b, a)  # 当返回结果是元组时,()可以省略
    a, b = b, a
    print(a, b)  # 200 100


def variable():
    global province
    address = ["江苏", "", "安徽", "", "上海"]
    for each in address:
        if each:
            province = each
            print(province)  # 江苏 安徽 上海
        # print(province)  # 江苏 江苏 安徽 安徽 上海


"""
浅拷贝: 普通赋值操作拷贝的是变量在内存中的引用,指向同一个内存地址,所以a变b也跟着变
深拷贝: 为了使赋值操作中a的变化不影响b,得重新开辟内存空间,即拷贝时指向不同内存地址
2种深拷贝:
deepcopy: 反复拷贝过程中拷贝的是上一层,且与数据类型无关
copy: 反复拷贝过程中只拷贝第一层,但如果是不可变类型(tuple),就不拷贝而是指向当前这一层的内存地址
"""
import copy


def shallowcopy():
    a = [11, 22, 33]
    b = a
    print(id(a))  # 1561934426952
    print(id(b))  # 1561934426952
    a.append(44)
    print(id(a))  # 1561934426952
    print(id(b))  # 1561934426952
    print(a)  # [11, 22, 33, 44]
    print(b)  # [11, 22, 33, 44]


def deepcopy01():
    a = [11, 22, 33]
    b = [44, 55, 66]
    c1 = [a, b]
    c2 = (a, b)
    print(c1)  # [[11, 22, 33], [44, 55, 66]]
    print(c2)  # ([11, 22, 33], [44, 55, 66])
    d1 = copy.deepcopy(c1)
    d2 = copy.deepcopy(c2)
    print(id(c1))  # 2135784678856
    print(id(d1))  # 2135784652360
    print(id(c2))  # 2136070554120
    print(id(d2))  # 2135786326920
    a.append(77)
    print(c1[0])  # [11, 22, 33, 77]
    print(d1[0])  # [11, 22, 33]
    print(c2[0])  # [11, 22, 33, 77]
    print(d2[0])  # [11, 22, 33]


def deepcopy02():
    a = [11, 22, 33]
    b = [44, 55, 66]
    c1 = [a, b]
    c2 = (a, b)
    print(c1)  # [[11, 22, 33], [44, 55, 66]]
    print(c2)  # ([11, 22, 33], [44, 55, 66])
    d1 = copy.copy(c1)
    d2 = copy.copy(c2)
    print(id(c1))  # 2425713124808
    print(id(d1))  # 2425714771144
    print(id(c2))  # 2425714883848
    print(id(d2))  # 2425714883848
    a.append(77)
    print(c1[0])  # [11, 22, 33, 77]
    print(d1[0])  # [11, 22, 33, 77]
    print(c2[0])  # [11, 22, 33, 77]
    print(d2[0])  # [11, 22, 33, 77]


"""
python有很多内建属性
常用属性            说明               触发方式
__init__          初始化函数          创建实例后赋值时使用,在__new__后面
__new__           生成实例所需属性     创建实例时
__class__         实例所在的类        实例.__class__
__str__           实例字符串表示       print()
__del__           析构               del删除实例
__dict__          实例自定义属性       vars(实例.__dict__)
__doc__           类文档              help(类/实例)
__getattribute__  属性访问拦截器       访问实例属性时
__bases__         类的所有父类         类名.__bases__
"""


class Test(object):
    def __init__(self, param1):
        self.param1 = param1
        self.param2 = "orc"

    # 属性访问拦截器
    def __getattribute__(self, item):
        print("---属性访问权限设置---")
        if item == "param1":
            return "不好意思,没有访问该属性权限！"
        else:
            temp = object.__getattribute__(self, item)
            print("the value is %s" % temp)
            return temp

    def show(self):
        print("欢迎来到召唤师峡谷！")

t = Test("grubby")
print(t.param1)
print(t.param2)

# 调用show方法的过程其实分两步,先获取show属性的对应return结果值,再调用该方法
# 如果18行没有return值的话,28行调用方法会报错 TypeError: 'NoneType' object is not callable
# 总结: 不管调用的是属性还是方法,都会经过__getattribute__拦截器判断
t.show()
