# coding=utf-8
"""
继承: 提高代码复用性
语法: class 子类(父类1,父类2...)
方法重写: 子类和父类方法名相同,调用的是子类自己的方法
多继承: 调用同名方法时会按继承顺序执行(可通过__mro__内置方法查看搜索顺序)
注意点: 子类不能直接访问父类的私有属性和方法
"""


class Animal:

    def __init__(self):
        self.num = 100
        self.__num = 200

    def __test(self):
        print("父类私有方法")

    def test(self):
        print("父类私有属性 %s" % self.__num)
        self.__test()

    def eat(self):
        print("吃")

    def drink(self):
        print("喝")

    def run(self):
        print("跑")


class Dog(Animal):
    def bark(self):
        print("汪汪汪")
        # print("访问父类私有属性 %s" % self.__num)

        # 子类可以通过调用父类的公有方法间接访问父类的私有属性和方法
        self.test()

    # 子类方法重写
    def eat(self):

        # super()仍可调用父类的方法
        super().eat()

        # 子类自己的功能代码
        print("吃骨头")


class Hsq(Dog, Animal):
    pass


dog = Dog()
dog.eat()
dog.run()
dog.bark()

hsq = Hsq()
hsq.eat()
# __mro__方法可以查看对象的方法搜索顺序
print(Hsq.__mro__)
