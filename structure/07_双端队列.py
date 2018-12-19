# coding=utf-8
"""
双端队列: 可以在队列任意一端插入和删除元素
常用操作:
Dqueue() 创建一个空的双端队列
add_front(item) 从队头加入一个item元素
add_back(item) 从队尾加入一个item元素
remove_front() 从队头删除一个item元素
remove_back() 从队尾删除一个item元素
is_empty() 判断双端队列是否为空
size() 返回队列的大小
"""

class Dqueue(object):
    """双端队列"""

    def __init__(self):
        # 用list(顺序表)实现双端队列
        self.__items = []

    # 判断是否为空
    def is_empty(self):
        return self.__items == []

    # 队头加入元素
    def add_front(self, item):
        self.__items.insert(0, item)

    # 队尾加入元素
    def add_back(self, item):
        self.__items.append(item)

    # 队头删除元素
    def remove_front(self):
        return self.__items.pop(0)

    # 队尾删除元素
    def remove_back(self):
        return self.__items.pop()

    # 返回大小
    def size(self):
        return len(self.__items)


# 测试代码
if __name__ == "__main__":
    d = Dqueue()
    print(d.is_empty())  # True
    d.add_front(11)
    d.add_front(22)
    d.add_back(33)
    d.add_back(44)
    print(d.size())  # 4
    print(d.remove_front())  # 22
    print(d.remove_front())  # 11
    print(d.remove_back())  # 44
    print(d.remove_back())  # 33
