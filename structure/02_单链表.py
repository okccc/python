# coding=utf-8
"""
单链表: 是链表中最简单一种形式,每个节点包含元素和链接两部分,这个链接指向链表中的下一个节点,最后一个节点的链接指向空值
       元素域elem存放具体数据
       链接域next存放下一个节点位置
       变量p指向链表的头节点位置,从p出发能找到表中的任意节点

常用操作:
is_empty() 链表是否为空
length() 链表长度
travel() 遍历整个链表
add(item) 链表头部添加元素
append(item) 链表尾部添加元素
insert(pos, item) 指定位置添加元素
remove(item) 删除节点
search(item) 查找节点是否存在
"""

# 节点实现
class Node(object):
    """单链表的节点"""

    def __init__(self, item):
        # item存放元素
        self.item = item
        # next是下一个节点的标识
        self.next = None

# 单链表实现
class SingleLinkedList(object):
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
            print(cur.item, end=" ")
            # 将cur移至下一位
            cur = cur.next
        print()

    # 头部添加元素
    def add(self, item):
        # 先创建一个保存item值的新节点node
        node = Node(item)
        # 将node的链接域指向原先的链表头head指向的位置
        node.next = self.head
        # 再将链表头head指向新节点node
        self.head = node

    # 尾部添加元素
    def append(self, item):
        # 先创建一个保存item值的node
        node = Node(item)
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
    def insert(self, pos, item):
        # 若指定位置在链表头之前,就add
        if pos <= 0:
            self.add(item)
        # 若指定位置在链表尾之后,就append
        elif pos > (self.length() - 1):
            self.append(item)
        # 中间位置
        else:
            # 先创建保存item的节点
            node = Node(item)
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
    def remove(self, item):
        # 游标cur开始时指向链表头
        cur = self.head
        # 定义要删除位置的前一个位置pre
        pre = None
        # 循环链表
        while cur is not None:
            # 找到指定位置
            if cur.item == item:
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
    def search(self, item):
        # 游标cur开始时指向头节点
        cur = self.head
        # 循环链表
        while cur is not None:
            # 如果找到了
            if cur.item == item:
                return True
            # 如果没找到
            else:
                # 继续往后移
                cur = cur.next
        return False


# 测试代码
if __name__ == "__main__":
    sll = SingleLinkedList()
    print(sll.is_empty())
    print(sll.length())
    sll.add(11)
    sll.append(33)
    sll.insert(1, 22)
    print(sll.is_empty())
    print(sll.length())
    sll.travel()
    print(sll.search(11))
    print(sll.search(10))
    sll.remove(22)
    sll.travel()
