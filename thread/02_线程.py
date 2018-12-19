# coding=utf-8
from threading import Thread, Lock
from queue import Queue
import time

"""
1、threading模块的Thread类可以创建线程
"""


# 自定义类继承Thread类
class MyThread(Thread):
    # 重写run方法
    def run(self):
        # 功能代码块
        for i in range(3):
            print("---我是线程%s---%d" % (self.name, i))
            time.sleep(1)


# if __name__ == "__main__":
#     for i in range(3):
#         t = MyThread()
#         t.start()


"""
2、threading模块的Lock类可以给线程上锁
同步: 当多个线程同时修改某一共享变量时,需要进行同步控制(加锁),保证线程安全
创建锁: lock = Lock()
上锁: lock.acquire([block]) -- block = True/False 表示阻塞/非阻塞,默认为True
解锁: lock.release()

锁的好处: 保证数据安全
锁的坏处: 阻止了多线程的并发执行,上锁的代码实际上是单线程执行完的,效率低
         由于可以存在多个锁,不同线程持有不同锁并试图获取对方持有的锁时会导致死锁 
"""
num = 0


def test01():
    global num
    for i in range(1000000):
        # 获取锁: True表示阻塞,即如果这个锁已经锁上了,那么这个线程会卡在这里一直等到解锁为止
        #        False表示非阻塞,即不管本次上锁是否成功,线程都不会卡在这里,而是继续往下走
        flag = lock.acquire(True)
        if flag:
            num += 1
            # 操作完共享数据记得释放锁
            lock.release()
    print("test01---the num is %d" % num)


def test02():
    global num
    for i in range(1000000):
        flag = lock.acquire(True)
        if flag:
            num += 1
            lock.release()
    print("test02---the num is %d" % num)


# 创建一个锁对象,此时是未锁上的
lock = Lock()

# t1 = Thread(target=test01)
# t1.start()
#
# t2 = Thread(target=test02)
# t2.start()

"""
3、queue可以实现多线程之间的通信(数据交换)
Producer/Consumer模式: 通过一个容器(阻塞队列)解决生产者和消费者的强耦合问题,生产者直接将数据扔给阻塞队列,
                      消费者直接从阻塞队列取数据,就相当于一个缓冲区,给producer/consumer解耦
创建队列: queue = Queue()
queue.put(): 往队列添加数据
queue.get(): 从队列取出数据
queue.qsize(): 判断队列是否有数据
"""


class Producer(Thread):
    global queue

    def run(self):
        count = 0
        # 先判断队列大小
        if queue.qsize() < 10:
            # 生产数据
            for i in range(10):
                msg = self.name + "---正在生产---product---" + str(i)
                count += 1
                # 往队列添加数据
                queue.put(msg)
                print(msg)
        time.sleep(1)


class Consumer(Thread):
    global queue

    def run(self):
        # 先判断队列大小
        if queue.qsize() > 0:
            # 消费数据
            for i in range(5):
                # 从队列获取数据
                msg = self.name + "---正在消费---" + queue.get()
                print(msg)
        time.sleep(1)


if __name__ == "__main__":
    # 创建队列
    queue = Queue()
    # 往初始队列添加数据
    for i in range(5):
        queue.put("product---%d" % i)
    # 创建多个生产者
    for i in range(2):
        p = Producer()
        p.start()
    # 创建多个消费者
    for i in range(3):
        c = Consumer()
        c.start()
