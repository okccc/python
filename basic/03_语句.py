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


def except01():
    # 异常处理
    try:
        # 尝试执行的代码
        num = int(input("输入整数:"))
        result = 1 / num
        print(result)
    except (ZeroDivisionError, OSError, TimeoutError):
        # 捕获已知异常
        print('error')
    except Exception as e:
        # 捕获未知异常
        print(e)
        # 抛出异常不作任何处理,程序中断
        raise
    except:
        # 忽略异常,程序继续往下执行
        pass
    else:
        # 没有异常才会执行的代码
        print("代码ok没有问题！")
    finally:
        # 最终一定会执行的代码
        print("=" * 50)


if __name__ == '__main__':
    # if01()
    # while01()
    except01()