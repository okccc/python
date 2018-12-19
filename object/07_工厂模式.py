# coding=utf-8
"""
简单工厂模式: 解耦
工厂方法模式: 在父类定义接口(方法),由子类实现
"""


class Store(object):
    def order(self, name):
        return Factory().select_car(name)


class Factory(object):
    def select_car(self, name):
        if name == '帕萨特':
            return Pasate(name)
        if name == '朗逸':
            return Langyi(name)
        if name == '宝莱':
            return Baolai(name)


class Car(object):
    def __init__(self, name):
        self.name = name

    def run(self):
        print("%s 在行驶" % self.name)

    def music(self):
        print("%s 在放歌" % self.name)


class Pasate(Car):
    pass


class Langyi(Car):
    pass


class Baolai(Car):
    pass


store = Store()
car = store.order("帕萨特")
car.run()
car.music()
