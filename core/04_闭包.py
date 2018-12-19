# coding=utf-8
"""
闭包: 在函数里面再定义函数,并且这个函数用到了外面函数的变量,那么这个函数及用到的变量称为闭包
优点: 调用函数时可以减少参数的传递
缺点: 由于闭包引用了外部函数的局部变量,导致局部变量没有及时释放,占用内存
"""


def test(num1):
    print("---1---")

    def test_in(num2):
        print("---2---")
        print(num1 + num2)

    print("---3---")
    return test_in  # 注意: 此处只写函数名,没有()


print(test)  # test表示这是一个函数
res = test(100)  # test()表示调用这个函数
print(res)
print("=" * 50)
res(100)
res(200)


# 案例
def line_conf(a, b):
    def line(x):
        return a * x + b

    return line


l1 = line_conf(3, 5)
l2 = line_conf(2, 10)
print(l1(3))
print(l2(3))
