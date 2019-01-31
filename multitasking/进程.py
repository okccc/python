"""
进程和线程：进程是资源分配的单位,线程是操作系统执行调度的单位;线程在进程里面,一个进程里至少有一个主线程
程序运行时会产生进程,一个程序可以开启多个进程,进程=代码+资源
进程之间相互独立,线程之间共享资源;线程间可以共享全局变量,进程可以通过队列完成通信
进程池(公园划船)：当不确定需要多少进程才能完成多任务时可以采用进程池,进程池中放入多个进程,一个进程执行完一个任务可以继续执行下一个任务,循环使用
"""
import multiprocessing
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
    # 使用进程实现多任务
    p1 = multiprocessing.Process(target=test01)
    p2 = multiprocessing.Process(target=test02)
    p1.start()
    p2.start()


def producer(q):
    print("---该进程的pid=%d" % os.getpid())
    # 模拟生产者
    datas = [11, 22, 33]
    for data in datas:
        q.put(data)
    if q.full():
        print("---数据生产完毕---")

def consumer(q):
    print("---该进程的pid=%d" % os.getpid())
    # 模拟消费者
    datas = []
    while True:
        datas.append(q.get())
        if q.empty():
            print("---数据接收完毕---")
            break

def main02():
    # 创建队列
    q = multiprocessing.Queue()
    # 将队列作为参数传递给进程对象
    p1 = multiprocessing.Process(target=producer, args=(q,))
    p2 = multiprocessing.Process(target=consumer, args=(q,))
    p1.start()
    p2.start()


def work():
    # print("---该进程的pid=%d" % os.getpid())
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
    # 等待进程池中所有子进程结束,必须在close()后面
    pool.join()
    print("---end---")



if __name__ == "__main__":
    # main01()
    # main02()
    main03()