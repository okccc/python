# coding=utf-8
"""
队列: 是一种先进先出的线性表,只允许在一端插入另一端删除;
     注意: 插入的一端即是队尾,删除的一端即是队头;
     可以根据插入/删除哪个操作频繁再具体选择队头/队尾,因为顺序表在头尾增删元素的操作算法复杂度不一样
     可以用顺序表或链表实现
队列操作:
Queue() 创建一个空的队列
enqueue(item) 往队列中添加一个item元素
dequeue() 从队列头部删除一个元素
is_empty() 判断一个队列是否为空
size() 返回队列的大小
"""

class Queue(object):
    """队列"""

    def __init__(self):
        # 用list(顺序表)实现队列
        self.__items = []

    # 判断是否为空
    def is_empty(self):
        return self.__items == []

    # 进队列
    def inqueue(self, item):
        # 1、尾部插入(入队操作多就选这个,复杂度低)
        self.__items.append(item)

        # 2、头部插入
        # self.__items.insert(0, item)

    # 出队列
    def outqueue(self):
        # 1、头部删除
        return self.__items.pop(0)

        # 2、尾部删除(出队操作多就选这个,复杂度低)
        # return self.__items.pop()

    # 返回队列大小
    def size(self):
        return len(self.__items)


# 测试代码
if __name__ == "__main__":
    q = Queue()
    print(q.is_empty())  # True
    q.inqueue(11)
    q.inqueue(22)
    q.inqueue(33)
    print(q.size())  # 3
    print(q.outqueue())  # 11
    print(q.size())  # 2
    print(q.outqueue())  # 22
    print(q.size())  # 1
    print(q.outqueue())  # 33
    print(q.size())  # 0
