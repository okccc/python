# coding=utf-8
"""
类: 大花猫(模型)
对象: 我家里养的那条大花猫(实物)
sys.getrefcount(object): 可以判断对象的引用计数,结果是真实个数+1,对象消失会报错
"""

class Cat:
    # __init__(python内置方法)初始化类,创建对象时自动调用,self就指向该对象的引用
    def __init__(self, name):
        self.name = name
        print("%s 来了" % self.name)

    # __del__(python内置方法)在对象从内存中销毁前自动执行(如果希望对象销毁前做些什么可以写在这里)
    def __del__(self):
        print("%s 走了" % self.name)

    # __str__(python内置方法)可以自定义print方法的输出内容,该方法必须返回一个字符串
    def __str__(self):
        return "我是小猫【%s】" % self.name

    # 自定义方法
    def eat(self):
        # 哪个对象调用该方法,self就是哪个对象的引用
        print("%s 爱吃鱼" % self.name)

# cat01 = Cat("Tom")
# print(cat01)  # 改造__str__方法后,print不再输出地址值而是__str__方法return的值
# cat01.eat()
# # del cat01  # 手动删除对象,提前从内存中销毁,然后执行下方代码
# print("-" * 30)  # cat01是全局变量,所有代码执行完才会从内存中销毁
# print(sys.getrefcount(cat01))
# cat02 = cat01
# print(sys.getrefcount(cat01))
# del cat02
# print(sys.getrefcount(cat01))
# del cat01
# print(sys.getrefcount(cat01))


# 跑步案例
class Person:
    def __init__(self, name, weight):
        # self.属性 = 形参
        self.name = name
        self.weight = weight

    def __str__(self):
        return "我叫 %s,体重 %.1f kg" % (self.name, self.weight)

    def eat(self):
        print("我要吃鸡腿！")
        self.weight += 1

    def run(self):
        print("我要锻炼身体！")
        self.weight -= 0.5

grubby = Person("grubby", 75.0)
print(grubby)
grubby.eat()
print(grubby)
grubby.run()
print(grubby)


# 摆放家具案例
class Furniture:
    def __init__(self, name, area):
        self.name = name
        self.area = area

    def __str__(self):
        return "【%s】 占地面积 %.1f平方米" % (self.name, self.area)

class House:
    def __init__(self, house_type, area):
        # 户型
        self.house_type = house_type
        # 总面积
        self.area = area
        # 剩余面积
        self.free_area = area
        # 家具列表
        self.furniture_list = []

    def __str__(self):
        # python会将()内的内容连接在一起,这样输出内容太长时可以换行
        return ("房子是 【%s】,总面积 %.1f 平米(剩余面积 %.1f 平米),家具列表是 %s" % (self.house_type, self.area,
                                                                 self.free_area, self.furniture_list))

    # 添加家具
    def add_furniture(self, furniture):
        print("要添加的家具是 %s" % furniture)

        # 1、先判断家具面积大小
        if furniture.area > self.free_area:
            print("该家具面积太大 %.1f 平米,放不下！" % furniture.area)
            return

        # 2、添加到家具列表
        self.furniture_list.append(furniture.name)

        # 3、计算房子剩余面积
        self.free_area -= furniture.area

bed = Furniture("床", 4.0)
table = Furniture("桌子", 1.5)
print(bed)
print(table)

my_home = House("两室一厅", 84.00)
print(my_home)
my_home.add_furniture(bed)
print(my_home)
my_home.add_furniture(table)
print(my_home)


# property属性: 对方法进行封装,升级类中getter、setter方法,方便设置/取值
class Test(object):
    def __init__(self):
        self.__num = 100

    @property
    def num(self):
        return self.__num

    @num.setter
    def num(self, value):
        self.__num = value

t = Test()
t.num = 200  # 相当于调用t.setNum(200)
result = t.num  # 相当于调用t.getNum()
print(result)


class Girl:
    """
    私有化: __xx私有化属性/方法,防止与子类名字冲突,不能在类的外部访问,因为名字重整变成了_Class__object
           _xx私有化属性/方法,from A import * 时不能被导入
           xx_避免与关键词冲突
    """
    def __init__(self, name, age):
        self.name = name
        self.__age = age

    def secret(self):
        print("%s 的年龄是 %d" % (self.name, self.__age))

    def __secret(self):
        print("%s 的年龄是 %d" % (self.name, self.__age))

moon = Girl("moon", 18)
moon.secret()
# moon.__secret()  # AttributeError: 'Girl' object has no attribute '__secret'
# 如何访问私有属性和方法呢?
moon._Girl__secret()