# coding=utf-8
import types
"""
静态语言: java/c++-->编译时就已经声明好变量的数据类型,先编译好再运行
动态语言: python-->运行时才确定变量的数据类型,变量类型即是被赋值的那个值的类型,可以在运行过程中修改代码
"""

class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def eat(self):
        print("%s 正在吃饭" % self.name)


# 给类动态添加属性
Person.num = 10

# 给类动态添加实例方法
def run(self):
    print("%s 正在跑步" % self.name)

# 给类动态添加静态方法
@staticmethod
def run1():
    print("---static method---")

# 给类添加类方法
@classmethod
def run2(cls):
    print("---class method---")

p1 = Person("grubby", 19)
print(p1.name)
print(p1.age)
p1.addr = "荷兰"
print(p1.addr)

p2 = Person("moon", 20)
# print(p2.addr)

print(p1.num)
print(p2.num)

p1.eat()
# p1.run = run  # run()方法是后添加的,p1.run()的时候并没有将p1作为参数传入

# 要将动态添加的实例方法和对象绑定,因为实例方法是由具体对象调用,静态方法和类方法则不需要
p1.run = types.MethodType(run, p1)
p1.run()

Person.run1 = run1
Person.run1()

Person.run2 = run2
Person.run2()


"""
__slots__变量: 在类中可以限制实例对象能添加的属性
"""
class Student(object):
    __slots__ = ("name", "age")

s = Student()
s.name = "fly"
s.age = 19
# s.addr = "beijing"  # AttributeError: 'Student' object has no attribute 'addr'
print(s.name)
print(s.age)
