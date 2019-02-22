import gevent
from gevent import monkey
import time
import sys
import requests
import random


def test01():
    for i in range(5):
        print("---test01---%d" % i)
        time.sleep(0.5)
        yield

def test02():
    for i in range(5):
        print("---test02---%d" % i)
        time.sleep(0.5)
        yield

def main01():
    # 借助yield实现多任务
    t1 = test01()
    t2 = test02()
    print(t1)  # <generator object test1 at 0x000001BF7FA01048>
    print(t2)  # <generator object test2 at 0x000001BF7FA016D0>
    while True:
        try:
            next(t1)
            next(t2)
        except StopIteration:
            sys.exit()


# 猴子补丁会将程序中所有的阻塞替换成gevent框架的非阻塞(包括socket、time、thread、select等)
monkey.patch_all()

def test03():
    for i in range(5):
        # 打印当前协程
        print(gevent.getcurrent(), i)
        time.sleep(0.5)  # sleep()是一个延时操作

def test04():
    for i in range(5):
        print(gevent.getcurrent(), i)
        time.sleep(0.5)

def main02():
    # 使用协程实现多任务
    # g1 = gevent.spawn(test03)
    # g2 = gevent.spawn(test04)
    # g1.join()
    # g2.join()

    gevent.joinall([
        gevent.spawn(test03),
        gevent.spawn(test04)
    ])


def download(url):
    response = requests.get(url)
    with open(str(random.random())[-5:]+".jpg", "wb") as f:
        f.write(response.content)

def main03():
    urls = [
        "https://rpic.douyucdn.cn/live-cover/appCovers/2018/12/13/5987179_20181213225638_small.jpg",
        "https://rpic.douyucdn.cn/live-cover/appCovers/2018/05/17/1797614_20180517095218_small.jpg"
    ]
    for url in urls:
        g = gevent.spawn(download, url)
        g.join()


if __name__ == '__main__':
    # main01()
    # main02()
    main03()
