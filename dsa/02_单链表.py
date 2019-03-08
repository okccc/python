# coding=utf-8
"""
单链表：链表中最简单的一种形式,每个节点包含元素和链接两部分,这个链接指向链表中的下一个节点,最后一个节点的链接指向空值
"""

class Node(object):
    """单链表的节点"""
    def __init__(self, elem):
        # 存放元素
        self.elem = elem
        # 存放下一个节点位置
        self.next = None


class SingleLinkList(object):
    """单链表"""
    def __init__(self):
        # 链表头
        self.head = None

    # 判断链表是否为空
    def is_empty(self):
        return self.head is None

    # 求链表长度
    def length(self):
        # 游标cur一开始指向链表头
        cur = self.head
        count = 0
        # 遍历链表
        while cur is not None:
            count += 1
            # 将cur后移一位
            cur = cur.next
        return count

    # 遍历链表
    def travel(self):
        # 游标开始指向链表头
        cur = self.head
        # 将cur不断往后移
        while cur is not None:
            # 打印当前元素
            print(cur.elem, end=" ")
            # 将cur移至下一位
            cur = cur.next
        print()

    # 头部添加元素
    def add(self, elem):
        # 先创建一个保存elem值的新节点node
        node = Node(elem)
        # 将node的链接域指向原先的链表头head指向的位置
        node.next = self.head
        # 再将链表头head指向新节点node
        self.head = node

    # 尾部添加元素
    def append(self, elem):
        # 先创建一个保存elem值的node
        node = Node(elem)
        # 判断链表是否为空
        if self.is_empty():
            # 直接将链表头指向node
            self.head = node
        # 若不为空,就先找到尾节点,然后将尾节点的next指向node
        else:
            cur = self.head
            while cur.next is not None:
                cur = cur.next
            # 将尾节点的next指向node
            cur.next = node

    # 指定位置添加元素
    def insert(self, pos, elem):
        # 若指定位置在链表头之前,就add
        if pos <= 0:
            self.add(elem)
        # 若指定位置在链表尾之后,就append
        elif pos > (self.length() - 1):
            self.append(elem)
        # 中间位置
        else:
            # 先创建保存elem的节点
            node = Node(elem)
            # pre表示指定位置pos的前一个位置pos-1,从头节点慢慢往后移
            pre = self.head
            count = 0
            while count < (pos - 1):
                count += 1
                pre = pre.next
            # 先将node的next指向插入位置的节点
            node.next = pre.next
            # 再将插入位置的前一个节点指向node
            pre.next = node

    # 删除节点
    def remove(self, elem):
        # 游标cur开始时指向链表头
        cur = self.head
        # 定义要删除位置的前一个位置pre
        pre = None
        # 循环链表
        while cur is not None:
            # 找到指定位置
            if cur.elem == elem:
                # 如果当前节点是头节点
                if cur == self.head:
                    self.head = cur.next
                # 如果当前节点不是头节点
                else:
                    # 将前一个位置的next指向指定位置的next即可
                    pre.next = cur.next
                break
            # 没找到指定位置
            else:
                # 将pre和cur继续往后移
                pre = cur
                cur = cur.next

    # 查找节点是否存在
    def search(self, elem):
        # 游标cur开始时指向头节点
        cur = self.head
        # 循环链表
        while cur is not None:
            # 如果找到了
            if cur.elem == elem:
                return True
            # 如果没找到
            else:
                # 继续往后移
                cur = cur.next
        return False


class SingleCycleLinkList(object):
    """单向循环链表"""
    def __init__(self, node=None):
        self.head = node
        if node:
            node.next = node

    # 判空
    def is_empty(self):
        return self.head is None

    # 链表长度
    def length(self):
        if self.is_empty():
            return 0
        # cur游标，用来移动遍历节点
        cur = self.head
        # count记录数量
        count = 1
        while cur.next != self.head:
            count += 1
            cur = cur.next
        return count

    # 遍历链表
    def travel(self):
        if self.is_empty():
            return
        cur = self.head
        while cur.next != self.head:
            print(cur.elem, end=" ")
            cur = cur.next
        # 退出循环，cur指向尾节点，但尾节点的元素未打印
        print(cur.elem)

    # 链表头部插入元素
    def add(self, elem):
        node = Node(elem)
        if self.is_empty():
            self.head = node
            node.next = node
        else:
            cur = self.head
            while cur.next != self.head:
                cur = cur.next
            # 退出循环，cur指向尾节点
            node.next = self.head
            self.head = node
            # cur.next = node
            cur.next = self.head

    # 链表尾部添加元素
    def append(self, elem):
        node = Node(elem)
        if self.is_empty():
            self.head = node
            node.next = node
        else:
            cur = self.head
            while cur.next != self.head:
                cur = cur.next
            # node.next = cur.next
            node.next = self.head
            cur.next = node

    # 指定位置添加元素
    def insert(self, pos, elem):
        if pos <= 0:
            self.add(elem)
        elif pos > (self.length()-1):
            self.append(elem)
        else:
            pre = self.head
            count = 0
            while count < (pos-1):
                count += 1
                pre = pre.next
            # 当循环退出后，pre指向pos-1位置
            node = Node(elem)
            node.next = pre.next
            pre.next = node

    # 删除节点
    def remove(self, elem):
        if self.is_empty():
            return

        cur = self.head
        pre = None

        while cur.next != self.head:
            if cur.elem == elem:
                # 先判断此结点是否是头节点
                if cur == self.head:
                    # 头节点的情况
                    # 找尾节点
                    rear = self.head
                    while rear.next != self.head:
                        rear = rear.next
                    self.head = cur.next
                    rear.next = self.head
                else:
                    # 中间节点
                    pre.next = cur.next
                return
            else:
                pre = cur
                cur = cur.next
        # 退出循环，cur指向尾节点
        if cur.elem == elem:
            if cur == self.head:
                # 链表只有一个节点
                self.head = None
            else:
                # pre.next = cur.next
                pre.next = self.head

    # 查找节点是否存在
    def search(self, elem):
        if self.is_empty():
            return False
        cur = self.head
        while cur.next != self.head:
            if cur.elem == elem:
                return True
            else:
                cur = cur.next
        # 退出循环，cur指向尾节点
        if cur.elem == elem:
            return True
        return False


if __name__ == "__main__":
    # 单链表
    sll = SingleLinkList()
    print(sll.is_empty())  # True
    print(sll.length())  # 0
    sll.add(11)
    sll.append(33)
    sll.insert(1, 22)
    print(sll.is_empty())  # False
    print(sll.length())  # 3
    sll.travel()  # 11 22 33
    print(sll.search(11))  # True
    print(sll.search(10))  # False
    sll.remove(22)
    sll.travel()  # 11 33

    # 单向循环链表
    ll = SingleCycleLinkList()
    print(ll.is_empty())  # True
    print(ll.length())  # 0
    ll.add(11)
    ll.add(22)
    ll.append(33)
    ll.insert(2, 44)
    print(ll.is_empty())  # False
    print(ll.length())  # 4
    ll.travel()  # 22 11 44 33
    ll.remove(33)
    print(ll.search(11))  # True
    ll.travel()  # 22 11 44
