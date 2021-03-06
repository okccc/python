# coding=utf-8
import threading
import time


def test01():
    for i in range(5):
        print("---test01---%d" % i)
        time.sleep(0.5)

def test02():
    for i in range(10):
        print("---test02---%d" % i)
        time.sleep(0.5)

def main01():
    # 多线程实现多任务
    # Thread()方法只是创建实例对象,一个实例对象只能创建一个线程且该线程只能开启一次 RuntimeError: threads can only be started once
    t1 = threading.Thread(target=test01)
    t2 = threading.Thread(target=test02)
    # setDaemon(True)将线程设置为守护线程,当主线程结束时守护线程也结束
    t1.setDaemon(True)
    t2.setDaemon(True)
    # 调用start()方法创建线程并启动线程;该线程会运行target函数,函数运行结束时该子线程结束
    t1.start()
    t2.start()
    # join()方法表示堵塞模式,等待当前已经启动的线程执行完再继续往下执行
    # t1.join()
    # t2.join()
    while True:
        # 统计当前正在运行的线程
        print(threading.enumerate())
        # 当子线程都结束只剩下主线程时中断程序
        if len(threading.enumerate()) == 1:
            break
        # 线程执行没有顺序,主线程和子线程都在抢资源往下运行,可以通过sleep()控制线程执行顺序
        time.sleep(0.5)
    print("主线程over!")


g_num = 0
g_list = [11, 22]

def test03():
    # 如果修改全局变量内存地址发生变化(重新赋值)要加global关键字
    global g_num
    g_num += 100
    print("---in test03---g_num=%d" % g_num)
    # 内存地址不变不用加global
    g_list.append(33)
    print("---in test03---g_list=%s" % g_list)

def test04():
    print("---in test04---g_num=%d" % g_num)
    print("---in test04---g_list=%s" % g_list)

def main02():
    # 多线程之间是共享全局变量的
    t3 = threading.Thread(target=test03)
    t4 = threading.Thread(target=test04)
    t3.start()
    # 等待t3子线程先执行完
    time.sleep(1)
    t4.start()
    print("---in main thread---g_num=%d" % g_num)
    print("---in main thread---g_num=%s" % g_list)


def test05(count):
    global g_num
    for i in range(count):
        # 上锁：如果之前没上锁则上锁成功,如果已经上锁会堵塞直到锁释放;为了避免堵塞太久上锁代码越少越好,只给存在资源竞争的代码上锁即可
        lock.acquire()
        g_num += 1
        # 解锁：操作完共享数据就释放锁等待下一次获取锁再继续操作
        lock.release()
    print("---in test07---num is %d" % g_num)

def test06(count):
    global g_num
    for i in range(count):
        lock.acquire()
        g_num += 1
        lock.release()
    print("---in test08---num is %d" % g_num)

# 创建互斥锁
lock = threading.Lock()

def main03():
    # 当循环次数足够大时,多线程操作全局变量的资源竞争冲突就体现出来了,需要用锁将两个线程同步起来
    t7 = threading.Thread(target=test05, args=(1000000,))
    t8 = threading.Thread(target=test06, args=(1000000,))
    t7.start()
    t8.start()
    # 主线程睡眠3秒等待子线程全部执行完
    time.sleep(3)
    print("---in main thread---num is %d" % g_num)


if __name__ == "__main__":
    # main01()
    # main02()
    main03()

