# coding=utf-8
class Stack(object):
    """栈：一种先进后出的线性表,只能在一端插入/删除,可以用顺序表或链表实现"""
    def __init__(self):
        # 用list(顺序表)实现栈,私有化属性防止外部直接用insert,remove,append等方法操作[]
        self.__items = []

    # 判断是否为空
    def is_empty(self):
        return self.__items == []

    # 往栈顶添加元素
    def push(self, item):
        # 顺序表结构append方式复杂度1,add方式复杂度n;如果用链表实现add方式复杂度1,append方式复杂度n
        self.__items.append(item)

    # 弹出栈顶元素
    def pop(self):
        return self.__items.pop()

    # 返回栈顶元素
    def peek(self):
        if self.__items:
            return self.__items[-1]
        else:
            return None

    # 栈大小
    def size(self):
        return len(self.__items)


class Queue(object):
    """
    队列：一种先进先出的线性表,一端插入另一端删除,可以用顺序表或链表实现
         插入端即是队尾,删除端即是队头,可以根据插入/删除哪个操作更频繁再具体选择队头/队尾,因为顺序表在头尾增删元素的算法复杂度不一样
    """
    def __init__(self):
        # 用list(顺序表)实现队列,私有化属性防止外部直接用insert,remove,append等方法操作[]
        self.__items = []

    # 判断是否为空
    def is_empty(self):
        return self.__items == []

    # 进队列
    def in_queue(self, item):
        # 尾部添加(入队操作多就选这个,复杂度低)
        self.__items.append(item)

        # 头部添加
        # self.__items.insert(0, item)

    # 出队列
    def out_queue(self):
        # 头部删除
        return self.__items.pop(0)

        # 尾部删除(出队操作多就选这个,复杂度低)
        # return self.__items.pop()

    # 队列大小
    def size(self):
        return len(self.__items)


class DQueue(object):
    """双端队列：可以在队列任意一端插入和删除元素"""
    def __init__(self):
        # 用list(顺序表)实现双端队列,私有化属性防止外部直接用insert,remove,append等方法操作[]
        self.__items = []

    # 判断是否为空
    def is_empty(self):
        return self.__items == []

    # 头部添加
    def add_front(self, item):
        self.__items.insert(0, item)

    # 尾部添加
    def add_back(self, item):
        self.__items.append(item)

    # 头部删除
    def remove_front(self):
        return self.__items.pop(0)

    # 尾部删除
    def remove_back(self):
        return self.__items.pop()

    # 返回大小
    def size(self):
        return len(self.__items)


if __name__ == "__main__":
    s = Stack()
    print(s.is_empty())  # True
    s.push(11)
    s.push(22)
    s.push(33)
    print(s.is_empty())  # False
    print(s.size())  # 3
    print(s.peek())  # 33
    print(s.pop())  # 33
    print(s.peek())  # 22
    print(s.size())  # 2

    q = Queue()
    print(q.is_empty())  # True
    q.in_queue(11)
    q.in_queue(22)
    q.in_queue(33)
    print(q.size())  # 3
    print(q.out_queue())  # 11
    print(q.size())  # 2
    print(q.out_queue())  # 22
    print(q.size())  # 1
    print(q.out_queue())  # 33
    print(q.size())  # 0

    dq = DQueue()
    print(dq.is_empty())  # True
    dq.add_front(11)
    dq.add_front(22)
    dq.add_back(33)
    dq.add_back(44)
    print(dq.size())  # 4
    print(dq.remove_front())  # 22
    print(dq.remove_front())  # 11
    print(dq.remove_back())  # 44
    print(dq.remove_back())  # 33

