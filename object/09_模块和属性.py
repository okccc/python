# coding=utf-8
"""
模块: 每个python文件(.py)都是模块,所以自己写的模块名称不能和系统自带的重名
import A as a(大驼峰命名规则): 导入模块所有内容,使用方法:模块名.*
from A import test: 导入模块部分内容,直接使用,不需要写模块名,如果有同名变量/函数,后面的会覆盖前面的,
                    因为python解释器是从上往下执行的,所以可以用as添加别名区分开
from A import *: 导入所有工具(不推荐,重名时无法排查错误)

循环导入问题: 如果两个模块a导入b,b也导入a,这样就会死循环,尽量避免这种情况,可以另写一个模块,分别导入a和b

包: 将有关联的模块放在同一个文件夹下,并创建__init__.py文件,这个文件夹就称为包
    __init__.py文件控制包的导入行为,定义一个__all__变量,控制from A import *导入的模块
"""

import random
import sys

"""
__file__属性: 查看文件路径
"""

print(random.__file__)  # 可以通过内置属性__file__查看导入的模块路径,防止和系统模块重名

"""
__name__属性: .py文件可以直接运行,也可以被当做模块导入,不管直接运行还是导入,顶层代码(不缩进部分)都会被执行,
              所以如果想让某些功能只在本类运行时可以加上if __name__ == "__main__":
"""


class A(object):
    def __init__(self):
        pass

    def func(self):
        pass

    if __name__ == "__main__":
        # 测试用代码
        func()


"""
__all__属性: 如果导入模块方式是from A import *,那么仅会导入__all__列表中包含的名字
"""
__all__ = ["Test", "test01"]


class Test(object):
    def test(self):
        pass


def test01(self):
    pass


def test02(self):
    pass


"""
给程序传参数: 导入sys模块,sys.argv会返回一个参数列表['','',''],第一个参数是当前模块路径名,后续为传入参数
"""
# print(sys.argv)
# name = sys.argv[1]
# print("欢迎 %s 到访！" % name)


"""
常用模块:
os: 使用操作系统的函数
sys: 与解释器交互时使用到的函数
"""

