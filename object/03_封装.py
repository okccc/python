# coding=utf-8
"""
封装: 将方法的实现细节封装在类中,需要使用时让对象调用方法就可以
     一个对象的属性可以是另一个类创建的对象: 比如士兵的枪,士兵可以调用枪做事情
"""


class Gun:
    def __init__(self, model):
        # 枪的型号
        self.model = model

        # 子弹数量
        self.bullet_num = 0

    def __str__(self):
        return "这是一把 %s ,子弹数量 %d 颗" % (self.model, self.bullet_num)

    # 装子弹
    def add_bullet(self, num):
        self.bullet_num += num
        print("装了 %d 颗子弹！" % num)

    # 射击
    def shoot(self):
        # 1、先判断子弹数量
        if self.bullet_num == 0:
            print("没有子弹了,先去装子弹吧！")
            return

        # 2、射击,子弹数-1
        self.bullet_num -= 1

        # 3、提示信息
        print("突突突...子弹还剩 %d 颗" % self.bullet_num)


class Soldier:
    def __init__(self, name):
        # 名字
        self.name = name

        # 枪-新兵还没有枪(定义类的属性时,如果不知道设置什么初始值,可以写None)
        self.gun = None

    def __str__(self):
        return "我是士兵 %s" % self.name

    # 士兵开火
    def fire(self):
        # 1、先判断士兵是否有枪
        if self.gun is None:
            print("%s 还没有枪" % self.name)
            return

        # 2、给枪装子弹
        self.gun.add_bullet(10)

        # 3、射击
        self.gun.shoot()


ak47 = Gun("ak47")
print(ak47)
ak47.add_bullet(5)
print(ak47)
ak47.shoot()

grubby = Soldier("grubby")
print(grubby.gun)
# 给士兵配枪
grubby.gun = ak47
grubby.fire()
print(grubby.gun)
