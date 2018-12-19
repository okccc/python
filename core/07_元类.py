# coding=utf-8
"""
元类(不常用): 创建实例对象的是类,创建类的就是元类,可用type动态创建
格式: 类名 = type(类名,由父类组成的元组(),包含属性的字典{名称和值})
     对象 = 类名()
     __class__属性可以查看当前对象/类是由哪个类创建的
"""

class Test1(object):
    num = 100
    def show(self):
        print("num is %d" % self.num)

t1 = Test1()
t1.show()  # num is 100
print(t1.__class__)  # <class '__main__.Test1'>
print(Test1.__class__)  # <class 'type'>

# 上述普通类可以改写为元类
def show(self):
    print("num is %d" % self.num)

Test2 = type("Test2", (), {"num": 100, "show": show})
t2 = Test2()
t2.show()  # num is 100
print(t2.__class__)  # <class '__main__.Test2'>
print(Test2.__class__)  # <class 'type'>
