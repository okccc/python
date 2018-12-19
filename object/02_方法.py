# coding=utf-8
"""
类本身也是一个实例
类方法：  只需要访问类属性/类方法,第一个参数默认cls,由类调用
实例方法: 需要访问类/对象的属性/方法,第一个参数默认self,由对象调用
静态方法: 既不需要访问类属性/类方法,也不需要访问对象属性/对象方法,不用创建对象而是类名直接调用

            实例方法         类方法              静态方法
  A         不可用        A.class_foo(x)     A.static_foo(x)
a = A()     a.foo(x)     a.class_foo(x)     a.static_foo(x)
"""


class Tool(object):
    # 类属性: 相当于全局变量
    count = 0

    # 实例方法
    def __init__(self, name):
        # 实例属性: 相当于局部变量
        self.name = name
        Tool.count += 1

    # 类方法
    @classmethod
    def show_tool_num(cls):
        # 在类方法内部访问当前类的属性或其他类方法(cls.***)
        print("工具对象数量为 %d" % cls.count)

    # 静态方法
    @staticmethod
    def show():
        print("工具很强大！")


tool1 = Tool("斧头")
tool2 = Tool("锤子")
tool2.count = 99
print(Tool.count)
print(tool1.count)
print(tool2.count)  # 不建议用对象名.变量名,应当用类名.变量名,容易和赋值语句混淆

# 在类的外部调用类方法(类名.类方法)
Tool.show_tool_num()

# 静态方法直接由类名调用,不需要创建对象(类名.静态方法)
Tool.show()

print("=" * 50)

"""
需求分析: 某个游戏,有游戏说明,有历史记录,有玩家
         游戏说明(和类/对象都没关系)--->静态方法
         历史记录(和类有关系)--->类方法
         玩家操作(和对象有关系)--->实例方法
"""


class Game(object):

    # 历史最高分
    record = 100

    # 初始化
    def __init__(self, player):
        self.player = player

    # 游戏说明
    @staticmethod
    def show_help():
        print("游戏提示: 全军出击！")

    # 显示历史记录
    @classmethod
    def show_record(cls):
        print("历史记录是 %d" % cls.record)

    # 开启游戏
    def start_game(self):
        print("%s 已经进入游戏啦！" % self.player)


Game.show_help()
Game.show_record()
grubby = Game("grubby")
grubby.start_game()
