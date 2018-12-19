# coding=utf-8
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

"""
__getattribute__: 属性访问拦截器
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