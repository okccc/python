# coding=utf-8
"""
并行：cpu核数 > 任务数 ---> 真的多任务
并发：cpu核数 < 任务数 ---> 假的多任务,因为一个cpu在同一时刻只能运行一个任务,只是占用cpu的程序切换速度足够快感觉不出来
同步和异步：请求发出后是否需要等待返回结果才能继续往下走,是一种消息通知机制,异步可通过多线程/协程实现
阻塞和非阻塞：关注的是进程/线程在等待调用结果时的状态,阻塞是同步机制的结果,非阻塞是异步机制的结果
cpu密集型：各种循环、逻辑判断、计数等 ---> 使用多进程充分利用多核cpu并行运算,一个进程会占用一个cpu
io密集型：网络传输、文件读写 ---> 使用多线程在io阻塞时可以切换线程不浪费cpu资源,cpu速度比io快得多所以单cpu足够用多cpu反而开销大不划算

实现多任务3种方式
进程：资源分配的最小单位,进程=代码+资源;系统开销大切换速度慢且进程间相互独立
线程：系统调度的最小单位,一个线程只能干一件事,进程默认会有一个主线程;系统开销小切换速度快且线程间共享数据
协程：协程在线程里面,利用线程中延时操作的等待时间(网络传输、磁盘IO等)运行别的线程
切换资源大小：进程 > 线程 > 协程  ---> 理论上协程消耗资源最少效率最高,进程更稳定
进程池(公园划船)：当不确定需要多少进程才能完成多任务时可以采用进程池,进程池里的进程可以循环使用

python解释器：将python代码翻译成0和1交给cpu执行
GIL：全局解释器锁,保证多线程同一时刻只能有一个线程执行(是python解释器CPython的问题,因为早期计算机都是单核cpu)
多核cpu在运行多线程时甚至比单核cpu运行多线程还慢,因为单核cpu里唤醒的线程能获取GIL无缝连接
而多核cpu的cpu0释放GIL后其他cpu上的线程也会来竞争资源但是GIL可能马上又被cpu0拿到导致其他cpu的线程唤醒后又睡眠造成线程颠簸
为了利用计算机的多核cpu建议使用多进程,因为每个进程都有一个独立的GIL互不干扰从而达到并行效果,多进程才是真正的多任务
"""

import multiprocessing
import threading
import time
import os
import random


def test01():
    for i in range(5):
        print("---test01---%d" % i)
        time.sleep(0.5)

def test02():
    for i in range(5):
        print("---test02---%d" % i)
        time.sleep(0.5)

def main01():
    # 多进程实现多任务
    p1 = multiprocessing.Process(target=test01)
    p2 = multiprocessing.Process(target=test02)
    p1.start()
    p2.start()


def producer(q):
    print("---该进程的pid=%d" % os.getpid())
    # 模拟生产者
    datas = [11, 22, 33, 44, 55]
    for data in datas:
        q.put(data)
    if q.full():
        print("---数据生产完毕,长度为%s---" % q.qsize())

def consumer(q):
    print("---该进程的pid=%d" % os.getpid())
    # 模拟消费者
    datas = []
    while True:
        datas.append(q.get())
        if q.empty():
            print("---数据接收完毕,长度为%s---" % len(datas))
            break

def main02():
    # 创建空队列并指定长度
    q = multiprocessing.Queue(5)
    # 将队列作为参数传递给进程对象,进程间可通过队列完成通信
    p1 = multiprocessing.Process(target=producer, args=(q,))
    p2 = multiprocessing.Process(target=consumer, args=(q,))
    p1.start()
    p2.start()


def work():
    start = time.time()
    time.sleep(random.random()*5)
    end = time.time()
    print("---该进程的pid=%d---该程序执行时间%.2f秒" % (os.getpid(), end - start))  # 至始至终只有3个pid循环使用

def main03():
    # 创建进程池并设置最大进程数
    pool = multiprocessing.Pool(3)
    # 当某个任务要运行很多次且耗时较长或者很多任务要运行,一两个进程显然不够用,就要用到进程池
    for i in range(10):
        # 往进程池中添加任务
        pool.apply_async(work)
    print("---start---")
    # 关闭进程池,此时不能再往里面添加任务
    pool.close()
    # join()：堵塞模式,等待调用join方法的进程及前面的进程都运行完才会继续运行后面的进程
    pool.join()
    print("---end---")


def copy(file, path1, path2, queue):
    # 将一个文件从旧目录拷贝到新目录
    with open(path1 + "/" + file, "rb") as f1:
        with open(path2 + "/" + file, "wb") as f2:
            f2.write(f1.read())
    queue.put(file)

def main04():
    """
    需求：拷贝文件夹下的所有文件并显示进度
    分析：1.拷贝一个文件容易,很多文件属于多任务可以考虑使用进程池
         2.每拷贝一个文件可以向队列里写点啥,进度条=队列长度/文件数
    """

    # 获取原文件夹
    path_old = "D://BaiduNetdiskDownload/02 多任务/02-进程"
    # 创建新文件夹
    path_new = ""
    try:
        # 当文件已存在会报错：给可能出异常的代码块添加try
        path_new = path_old + "【备份】"
        os.mkdir(path_new)
    except:
        # except可以打印异常也可以pass不做处理
        pass
    # 遍历原文件夹获取所有文件
    files = os.listdir(path_old)
    count = len(files)
    # 创建进程池：Pool中能同时运行的最大任务数取决于电脑CPU数量
    pool = multiprocessing.Pool()
    # 创建队列：multiprocessing.Queue()是跨进程通信队列,但是不能用于Pool多进程的通信,Pool多进程通信要使用Manager().Queue()
    queue = multiprocessing.Manager().Queue()
    # 往进程池中添加任务
    for file in files:
        pool.apply_async(copy, args=(file, path_old, path_new, queue))
    # 关闭进程池
    pool.close()
    # 等待子进程结束
    # pool.join()

    # 在主进程中计算进度条
    num = 0
    while True:
        filename = queue.get()
        if filename:
            # print("当前正在拷贝文件%s" % filename)
            num += 1
            # \r表示将输出的内容返回到第一个指针,这样的话如果不换行后面内容会覆盖前面内容,这样就能动态显示进度条
            print("\r当前拷贝进度%.2f %%" % (num*100/count), end="")
            if num == count:
                break


def count(n):
    while n > 0:
        n -= 1

def main05():
    # 单线程
    s1 = time.time()
    count(100000000)
    count(100000000)
    s2 = time.time()
    print(s2 - s1)
    # 多线程
    t1 = threading.Thread(target=count, args=(100000000,))
    t2 = threading.Thread(target=count, args=(100000000,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    s3 = time.time()
    print(s3 - s2)
    # 多进程
    p1 = multiprocessing.Process(target=count, args=(100000000,))
    p2 = multiprocessing.Process(target=count, args=(100000000,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    s4 = time.time()
    print(s4 - s3)


if __name__ == "__main__":
    # main01()
    # main02()
    # main03()
    # main04()
    main05()
