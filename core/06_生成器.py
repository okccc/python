# coding=utf-8
"""
生成器(generator): 通过列表生成式可以直接创建一个列表,但是列表很大的话会占用很大内存,而我可能只用到其中的几个数据,
                  如果列表元素可以通过某种算法推算出来,由循环不断推出后续元素,从而避免创建完整的list,可以节约
                  很大空间,这种边循环边计算的机制就是生成器,因此生成器一定是迭代器
生成器是迭代器的一种,但是只能迭代一次,因为它们不是全部存在内存里,它们只在要调用的时候才在内存里生成
"""

# 创建生成器方式一: 将列表生成式[]改成() ===> []得到的是列表,()得到的是生成器
l = [i * 2 for i in range(5)]
print(l)  # [0, 2, 4, 6, 8]
f = (i * 2 for i in range(5))
print(f)  # <generator object <genexpr> at 0x0000025ED54BD360>
for i in f:
    print(i)

print("=" * 50)

# 创建生成器方式二: 如果推算算法较复杂,类似列表生成式的for循环无法实现,可以用函数实现
# 比如斐波那契数列: 1 1 2 3 5 8 13 21 34 55...
def fib():
    print("---start---")
    a, b = 0, 1
    for i in range(5):
        print(b)
        a, b = b, a + b
    print("---end---")


fib()

print("=" * 50)


# 改成生成器: 加了yield的函数已经不是普通函数,调用该函数不会立即执行而是返回一个生成器
# yield作用: 中断函数并返回后面的值
def fib(n):
    a, b, s = 0, 1, 0
    while s < n:
        a, b = b, a + b
        s += 1
        yield b

f = fib(5)
print(f)  # <generator object fib_generator at 0x00000201A8ADD410>
# for x in f:
#     print(x)

"""
假设f是生成器,next(f)和f.__next__()区别:
第一次调用时: next(f)会从程序第一行执行并返回生成器的第一个值
            f.__next__()只会从第一行执行但是并不会返回生成器的第一个值
            f.__next__()等价于f.send(None)
第一次之后调用时,两者效果一样
"""
# print(next(f))
f.__next__()

print("=" * 50)


def gen():
    i = 0
    while i < 5:
        temp = yield i
        print(temp)
        i += 1


g = gen()
print(next(g))
print(next(g))
g.send("haha")
g.__next__()
g.__next__()

print("=" * 50)

"""
多任务: yield可以切换多个任务同时执行
"""
def test1():
    while True:
        print("---1---")
        yield None

def test2():
    while True:
        print("---2---")
        yield None

t1 = test1()
t2 = test2()
while True:
    t1.__next__()
    t2.__next__()
