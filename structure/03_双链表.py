# coding=utf-8
"""
双链表: 每个节点有两个链接,一个指向前一个节点,若是头节点就指向空值;另一个指向下一个节点,若是尾节点就指向空值
       元素域elem存放具体数据
       链接域pre存放上一个节点位置
       链接域next存放下一个节点位置
常用操作:
is_empty() 链表是否为空
length() 链表长度
travel() 遍历链表
add(item) 链表头部添加
append(item) 链表尾部添加
insert(pos, item) 指定位置添加
remove(item) 删除节点
search(item) 查找节点是否存在
"""


# 节点实现
class Node(object):
    """双链表的节点"""

    def __init__(self, item):
        self.item = item
        self.pre = None
        self.next = None


# 双链表实现
class DoubleLinkedList(object):
    """双链表"""

    def __init__(self):
        # 链表头
        self.head = None

    # 判断链表是否为空
    def is_empty(self):
        return self.head is None

    # 求链表长度
    def length(self):
        # 游标开始时指向链表头
        cur = self.head
        count = 0
        # 遍历链表
        while cur is not None:
            count += 1
            # 将游标后移一位
            cur = cur.next
        return count

    # 遍历链表
    def travel(self):
        # 游标开始时指向表头
        cur = self.head
        # 将cur不断后移
        while cur is not None:
            # 打印当前元素
            print(cur.item, end=" ")
            # 将游标后移一位
            cur = cur.next
        print()

    # 头部添加元素
    def add(self, item):
        # 先创建一个保存item值的新节点
        node = Node(item)
        # 将node的next指向原先的链表头head指向的位置
        node.next = self.head
        # 再将链表头的head指向新节点node
        self.head = node

    # 尾部添加元素
    def append(self, item):
        # 先创建一个保存item值得新节点
        node = Node(item)
        # 判断链表是否为空
        if self.is_empty():
            # 直接将链表头指向node
            self.head = node
        # 不为空就先找到尾节点,然后将尾节点的next指向node
        else:
            cur = self.head
            while cur.next is not None:
                cur = cur.next
            # 将尾节点的next指向node
            cur.next = node
            # 将node的pre指向尾节点
            # node.pre = cur

    # 指定位置添加元素
    def insert(self, pos, item):
        # 指定位置在链表头之前,就add
        if pos <= 0:
            self.add(item)
        # 指定位置在链表头之后,就append
        elif pos > (self.length() - 1):
            self.append(item)
        # 中间位置
        else:
            # 先创建保存item的新节点node
            node = Node(item)
            # 游标开始时指向链表头
            cur = self.head
            count = 0
            # 将cur一直往后移,直到指定位置
            while count < (pos - 1):
                count += 1
                cur = cur.next
            # 新节点node的前一个节点
            node.pre = cur
            # 新节点node的后一个节点
            node.next = cur.next
            # 新节点node是后一个节点的前一个节点
            cur.next.pre = node
            # 新节点node是前一个节点的后一个节点
            cur.next = node

    # 删除节点
    def remove(self, item):
        # 游标cur开始时指向链表头
        cur = self.head
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
                    cur.pre.next = cur.next
                break
            # 没找到指定位置
            else:
                # 将pre和cur继续往后移
                cur.pre = cur
                cur = cur.next

    # 查找节点是否存在
    def search(self, item):
        # 游标开始时指向链表头
        cur = self.head
        # 遍历链表
        while cur is not None:
            # 找到了
            if cur.item == item:
                return True
            # 没找到
            else:
                # 继续往后移
                cur = cur.next
        return False


# 测试代码
if __name__ == "__main__":
    dll = DoubleLinkedList()
    print(dll.is_empty())
    print(dll.length())
    dll.add(11)
    dll.add(22)
    dll.append(33)
    dll.insert(2, 44)
    print(dll.is_empty())
    print(dll.length())
    dll.travel()
    print(dll.search(33))
    print(dll.search(55))
    dll.remove(22)
    dll.travel()
