import multiprocessing
import time
import os
import random


def test01():
    for i in range(5):
        print("---test01---%d" % i)
        time.sleep(1)

def test02():
    for i in range(5):
        print("---test02---%d" % i)
        time.sleep(1)

def main01():
    """
    进程和线程区别：
    进程是资源分配的单位,线程是操作系统执行调度的单位;线程在进程里面,一个进程里至少有一个主线程
    程序运行时会产生进程,一个程序可以开启多个进程,进程=代码+资源
    进程之间相互独立,线程之间共享资源
    进程池(公园划船)：当不确定需要多少进程才能完成多任务时可以采用进程池,进程池中放入多个进程,且进程可以循环使用
    """

    # 使用进程实现多任务
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
    # join()：阻塞模式,默认等子进程执行完再往下走,必须在close()后面
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
        # print("当前正在拷贝文件%s" % filename)
        num += 1
        # \r表示将输出的内容返回到第一个指针,这样的话如果不换行后面内容会覆盖前面内容,这样就能动态显示进度条
        print("\r当前拷贝进度%.2f %%" % (num*100/count), end="")
        if num == count:
            break


if __name__ == "__main__":
    # main01()
    # main02()
    # main03()
    main04()
