# coding=utf-8
class Node(object):
    """节点"""
    def __init__(self, elem):
        self.elem = elem
        self.next = None


class SingleCycleLinkList(object):
    """单向循环链表"""
    def __init__(self, node=None):
        self.head = node
        if node:
            node.next = node

    def is_empty(self):
        """链表是否为空"""
        return self.head == None

    def length(self):
        """链表长度"""
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

    def travel(self):
        """遍历整个链表"""
        if self.is_empty():
            return
        cur = self.head
        while cur.next != self.head:
            print(cur.elem, end=" ")
            cur = cur.next
        # 退出循环，cur指向尾节点，但尾节点的元素未打印
        print(cur.elem)

    def add(self, item):
        """链表头部添加元素，头插法"""
        node = Node(item)
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

    def append(self, item):
        """链表尾部添加元素, 尾插法"""
        node = Node(item)
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

    def insert(self, pos, item):
        """指定位置添加元素
        :param  pos 从0开始
        """
        if pos <= 0:
            self.add(item)
        elif pos > (self.length()-1):
            self.append(item)
        else:
            pre = self.head
            count = 0
            while count < (pos-1):
                count += 1
                pre = pre.next
            # 当循环退出后，pre指向pos-1位置
            node = Node(item)
            node.next = pre.next
            pre.next = node

    def remove(self, item):
        """删除节点"""
        if self.is_empty():
            return

        cur = self.head
        pre = None

        while cur.next != self.head:
            if cur.elem == item:
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
        if cur.elem == item:
            if cur == self.head:
                # 链表只有一个节点
                self.head = None
            else:
                # pre.next = cur.next
                pre.next = self.head

    def search(self, item):
        """查找节点是否存在"""
        if self.is_empty():
            return False
        cur = self.head
        while cur.next != self.head:
            if cur.elem == item:
                return True
            else:
                cur = cur.next
        # 退出循环，cur指向尾节点
        if cur.elem == item:
            return True
        return False


if __name__ == "__main__":
    ll = SingleCycleLinkList()
    print(ll.is_empty())
    print(ll.length())

    ll.add(11)
    ll.add(22)
    ll.append(33)
    ll.insert(2, 44)
    print(ll.is_empty())
    print(ll.length())
    ll.travel()
    ll.remove(33)
    print(ll.search(11))
    ll.travel()
















