# coding=utf-8
from multiprocessing import Process, Pool, Manager, Queue
import os
import time
import random

"""
1、multiprocessing模块里的Process类可以用来创建子进程
target: 表示这个进程实例要调用的对象
start(): 启动进程
run(): 创建Process实例对象时如果没有给target参数,调用start方法就会执行对象中的run方法
join([timeout]): 阻塞,在timeout时间内等待子进程执行完再继续往下执行,不写timeout就是默认等子进程执行完

os.getpid(): 获取当前进程的进程号
os.getppid(): 获取当前进程父进程的进程号
"""

# 自定义类继承Process类
class MyProcess(Process):
    # 重写run方法
    def run(self):
        for i in range(5):
            print("pid=%d,ppid=%d" % (os.getpid(), os.getppid()))
            time.sleep(1)

# if __name__ == "__main__":
#     m = MyProcess()
#     # 创建Process实例时没有给定target参数,此时start方法就是调用run方法
#     m.start()
#
#     for i in range(5):
#         print("pid=%d" % os.getpid())
#         time.sleep(1)


"""
2、进程池: 可以同时执行任务的最大进程数
"""

def test():
    for i in range(5):
        print("pid=%d" % os.getpid())
        time.sleep(1)

# if __name__ == "__main__":
#     # 创建进程池,指定最大进程数
#     p = Pool(3)
#
#     for i in range(5):
#         print("---%d---" % i)
#         time.sleep(1)
#         # 往进程池中添加子进程
#         p.apply_async(test)
#
#     # 关闭进程池,此时不能再往进程池添加任务
#     p.close()
#     # 等待子进程结束
#     p.join()

"""
3、multiprocessing模块的Queue可以实现多进程之间的数据通信
Queue是一个消息列队,先进先出
Queue.qsize(): 返回当前队列包含的消息数量
Queue.empty(): 判断队列是否为空
Queue.full(): 判断队列是否已满
Queue.put(): 往队列中添加消息
Queue.get(): 从队列中获取消息
"""

# q = Queue(3)
# print(q.empty())
# q.put(11)
# q.put(22)
# q.put(33)
# print(q.full())
# print(q.qsize())
# print(q.get())
# print(q.get())
# print(q.get())

def writer(q):
    for value in ['grubby', 'moon', 'sky']:
        print("put into queue %s" % value)
        q.put(value)
        time.sleep(random.random())

def read(q):
    while True:
        if not q.empty():
            value = q.get()
            print("get from queue %s" % value)
            time.sleep(random.random())
        else:
            break

if __name__ == "__main__":
    # # 创建一个消息队列,指定最大消息数
    # q = Queue(3)
    # # 创建进程
    # pw = Process(target=writer, args=(q,))
    # pr = Process(target=read, args=(q,))
    # # 启动子进程,并等待运行结束
    # pw.start()
    # pw.join()
    # pr.start()
    # pr.join()

    # 使用进程池
    q = Manager().Queue()
    p = Pool()
    p.apply_async(writer, (q,))
    p.apply_async(read, (q,))
    p.close()
    p.join()

    print("data communicate success!")
