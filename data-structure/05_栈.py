# coding=utf-8
class Stack(object):
    """
    栈：一种先进后出的线性表,只能在一端插入/删除,可以用顺序表或链表实现
    """

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

