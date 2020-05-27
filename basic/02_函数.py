# coding=utf-8
"""
函数: 封装具有独立功能的代码块;func表示这是一个函数,func()表示调用这个函数
区别: 方法在类里面,第一个参数默认self;函数在类外面,没有默认参数
python函数中参数的传递方式：
值传递：数字、字符串等不可变对象是值传递,在函数内部无法改变
引用传递：列表、字典等可变对象是引用传递,在函数内部可以改变
"""


def test01(name, gender=True):
    """
    缺省参数: 当某个参数多数情况下都是固定值时就可以设置成缺省参数,比如列表的sort方法(默认升序,指定reverse=Ture才是降序)
    注意: 缺省参数要放在参数列表的末尾
    """
    gender_value = "男生"
    if not gender:
        gender_value = "女生"
    print("%s是%s" % (name, gender_value))

def cumulate01(n):
    # 累加案例
    if n == 1:
        return 1
    else:
        return cumulate01(n - 1) + n

def fibonacci(n):
    # 菲波那切数列
    if n == 1 or n == 2:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def input01():
    # input(): 键盘录入只能输入字符串,数字类型要用int,float等函数转换
    price = float(input("请输入单价:"))
    weight = int(input("请输入重量:"))
    money = price * weight
    print(money)

def eval01():
    # eval(): 可以将input输入的字符串当成有效表达式(取字符串里的内容)并返回计算结果
    result = eval(input("输入算术题:"))
    print(result)

def id01():
    # id(): 可以查看变量在内存中的地址值
    num = 10
    print("%d" % id(num))  # 1537823824 (%d以十进制输出结果)
    print("%x" % id(num))  # 5ba95450 (%x以十六进制输出结果)

def print01():
    """
    print(): 默认换行,在结尾添加end=""可以不换行接着输出
    %表示格式化输出符: 当print输出内容包不同数据类型的变量时要对变量格式化
    %s:字符串  %d:整数  %f:小数  %%:输出%
    print(f'')表示格式化,相当于print(''.format())
    """
    # 格式化输出字符串
    print("大家好我叫 %s" % "小花")  # 大家好我叫 小花
    # 格式化输出整数(06控制长度,不满6位以0补全)
    print("我的学号是 %06d" % 19)  # 我的学号是 000019
    # 格式化输出小数(.2控制长度,小数点后面保留2位)
    print("苹果单价 %.2f 元/斤,重量 %d 斤,总价 %.2f 元" % (4.5, 5, 4.5*5))  # 多个变量放()用逗号隔开
    # 格式化输出百分比
    print("数据比例是 %.2f%%" % (0.25 * 100))

def high_order():
    """
    高阶函数：一个函数接收另一个函数作为参数
    map(function, sequence)：对sequence中的item依次执行function后将结果组成迭代器返回
    reduce(function, sequence[, initial])：先对sequence中前两个item执行function得到的结果再与下一个item执行function如此迭代
                                           如果有initial则作为初始值调用
    filter(function, sequence)：对sequence中的item依次执行function后将结果值返回True的组成迭代器返回
    """
    from functools import reduce

    res1 = list(map(lambda x: x * x, [1, 2, 3]))
    print(res1)  # [1, 4, 9]
    res2 = reduce(lambda x, y: x + y, [1, 2, 3, 4])
    print(type(res2))  # <class 'int'>
    print(res2)  # 10
    res3 = reduce(lambda x, y: x * y, [1, 2, 3], 5)
    print(res3)  # 30
    res4 = reduce(lambda x, y: x * 10 + y, [1, 3, 5, 7, 9])
    print(res4)  # 13579
    res5 = reduce(lambda a, b: a if (a > b) else b, [23, 11, 59, 42, 100])
    print(res5)  # 100
    res6 = list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4]))
    print(res6)  # [2, 4]

def enumerate01():
    # enumerate()：将可迭代对象(字符串/列表/元组/字典key)组合为索引序列,同时列出数据和下标,一般用在for循环中
    L = ["aa", "bb", "cc"]
    for i in L:
        print(i)  # aa bb cc
    for i in enumerate(L):
        print(i)  # (0, 'aa') (1, 'bb') (2, 'cc')
    # 拆包：将元祖/列表中的数据拆分成多个单独变量
    for i, l in enumerate(L):
        print(i, l)  # 0 aa 1 bb 2 cc

def zip01():
    names = ["grubby", "moon", "sky"]
    races = ["orc", "ne", "human"]
    ages = [18, 19, 20]
    # enumerate()
    for index, name in enumerate(names):
        race = races[index]
        age = ages[index]
        # print((name, race, age))
    # zip()：将一系列可迭代对象中的元素打包成一个个tuple,并返回由这些tuple组成的list
    for name, race, age in zip(names, races, ages):
        print((name, race, age))
zip01()