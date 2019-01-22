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


if __name__ == '__main__':
    variable()
