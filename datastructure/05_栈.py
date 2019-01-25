# coding=utf-8
"""
栈: 是一种先进后出的线性表,只允许在一端进行操作
   可以用顺序表或链表实现
栈的操作:
Stack() 创建一个新的空栈
push(item) 添加一个新的元素item到栈顶
pop() 弹出栈顶元素
peek() 返回栈顶元素
is_empty() 判断栈是否为空
size() 返回栈的元素个数
"""

class Stack(object):
    """栈"""

    def __init__(self):
        # 用list(顺序表)来实现栈,私有化属性防止外部直接用insert,remove,append等方法操作[]
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
        return self.__items[len(self.__items) - 1]

    # 返回栈大小
    def size(self):
        return len(self.__items)


# 测试代码
if __name__ == "__main__":
    s = Stack()
    print(s.is_empty())
    s.push(11)
    s.push(22)
    s.push(33)
    print(s.is_empty())
    print(s.size())
    print(s.peek())
    print(s.pop())
    print(s.peek())
    print(s.size())

