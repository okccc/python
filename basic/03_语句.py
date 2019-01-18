# coding=utf-8
"""
java三元表达式：res = a > b ? a : b
python三元表达式：res = a if a > b else b

程序开发三大流程:
1、顺序: 从上往下按顺序执行
2、分支(if): 根据条件判断,决定执行代码的分支
3、循环(while): 让特定代码重复执行

break: 跳出当前整个循环
continue: 跳出本次循环继续下次循环
"""


def if01():
    # if判断: 0,(),[],{},"",None都表示条件为假,等价于False;非0表示真
    if 0 or () or [] or {} or "" or None or False:
        print("False")
    if 1 or -1 or 1 == 1:
        print("True")


def while01():
    # break演示
    i = 0
    while i < 5:
        if i == 3:
            break
        print(i)
        i += 1
    print("over")

    # continue演示
    i = 0
    while i < 5:
        if i == 3:
            # 注意:使用continue关键字之前要先对计数器+1,不然会死循环
            i += 1
            continue
        print(i)
        i += 1
    print("over")

    # 演示循环嵌套
    row = 1
    while row <= 5:
        col = 1
        while col <= row:
            print("*", end="")
            col += 1
        print("")
        row += 1

    # 打印99乘法表
    row = 1
    while row <= 9:
        col = 1
        while col <= row:
            print("%d * %d = %d" % (col, row, row * col), end="\t")
            col += 1
        print("")  # 换行
        row += 1


"""
with语句: 只适用于以下支持上下文管理协议(context management protocol)的对象
file
decimal.Context
thread.LockType
threading.Lock
threading.RLock
threading.Condition
threading.Semaphore
threading.BoundedSemaphore
with语句会执行上下文表达式(context_expr)获得上下文管理器,上下文管理器提供一个上下文对象,处理with语句块中的细节:
一旦获得上下文对象,就会调用它的__enter__()方法,将完成with语句块执行前的所有准备工作,如果with语句后面跟了as语句,则用__enter__()方法的返回值来赋值;
当with语句块结束时,无论正常结束还是异常,都会调用上下文对象的__exit__()方法,__exit__()方法有3个参数,如果with语句正常结束,三个参数都是None
如果发生异常,三个参数的值分别等于调用sys.exc_info()函数返回的三个值:类型(异常类)、值(异常实例)和跟踪记录(traceback),相应的跟踪记录对象;
因为上下文管理器主要作用于共享资源,__enter__()和__exit__()方法干的基本是需要分配和释放资源的低层次工作,
比如: 数据库连接、锁分配、信号量加/减、状态管理、文件打开/关闭、异常处理等;
"""

from contextlib import contextmanager
import sys


class A(object):
    """
    给自定义类添加这两个方法配合with语句使用
    """
    def __enter__(self):
        print("__enter__() is called!")

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("__exit__() is called!")

with A() as a:
    print("=" * 30)
# 结果:
# __enter__() is called!
# ==============================
# __exit__() is called!

# contextlib模块实现上下文自动管理
# 锁机制
@contextmanager
def locked(lock):
    lock.acquired()
    try:
        yield
    finally:
        lock.release()

# 数据库操作
@contextmanager
def transaction(db):
    db.begin()

    try:
        yield db
    except:
        db.rollback()
        raise
    else:
        db.commit()

# 标准输出重定向
@contextmanager
def stdout_redirect(new_stdout):
    old_stdout = sys.stdout
    sys.stdout = new_stdout
    try:
        yield
    finally:
        sys.stdout = old_stdout

with open("file.txt", "w") as f:
    with stdout_redirect(f):
        print("hello world")


if __name__ == '__main__':
    if01()
    # while01()