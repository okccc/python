# coding=utf-8
"""
try:
    # 尝试执行的代码
    num = int(input("输入整数:"))
    result = 1 / num
    print(result)
except ZeroDivisionError:
    # 捕获已知异常
    print("已知错误: division by zero")
except Exception as result:
    # 捕获未知异常
    print("未知错误: %s" % result)
    # 不做处理只抛出异常
    raise
else:
    # 没有异常才会执行的代码
    print("代码ok没有问题！")
finally:
    # 最终一定会执行的代码
    print("=" * 50)
"""

# 异常传递性: 比如一个函数代码块里可能有异常,可以在调用这个函数时再处理异常
class Test(object):
    def __init__(self, switch):
        self.switch = switch

    def cal(self, a, b):
        try:
            return a / b
        except Exception as result:
            if self.switch:
                # 将异常打印在控制台
                print("捕获到的异常：%s" % result)
            else:
                # 抛出异常给方法调用者
                raise

t = Test(True)
t.cal(10, 0)
t.switch = False
t.cal(10, 0)


