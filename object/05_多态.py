# coding=utf-8
"""
多态: 定义时和运行时的数据类型不一样
     和java/c++不同,python是弱类型语言,传参时不需要指定数据类型,所以python中多态体现的不明显
"""


class Dog(object):
    def __init__(self, name):
        self.name = name

    def bark(self):
        print("我是 %s" % self.name)


class Hsq(Dog):
    def __init__(self, name):
        self.name = name

    def bark(self):
        print("我是 %s" % self.name)


class Person(object):
    def __init__(self, name):
        self.name = name

    def play_to_dog(self, dog):
        print("%s 和 %s 一起玩耍" % (self.name, dog.name))
        dog.bark()


sky = Dog("sky")
infi = Hsq("infi")

moon = Person("moon")
moon.play_to_dog(sky)
moon.play_to_dog(infi)
