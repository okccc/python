# coding=utf-8
"""
树: 是一种抽象数据类型,用来模拟具有树状结构的数据集合

常用术语:
节点的度: 节点含有的子树个数
树的度: 最大的节点的度就是树的度
叶节点: 度为0的节点
节点的层次: 根为第一层,下面是第二层,依次类推
树的深度: 树种节点的最大层次

二叉树: 每个节点最多含有两个子节点的树称为二叉树
完全二叉树: 除了最底层,其他各层节点数均达到最大值
满二叉树: 所有层节点数均达到最大值
平衡二叉树: 任何节点的两棵子树高度差不大于1
排序二叉树: 任何节点的左子树都比该节点小,右子树都比该节点大

树的存储与表示
顺序存储: 将数据结构存储在固定数组中,遍历快但是占空间大,不常见
链式存储: 二叉树是最简单的树,任何树都能转换成二叉树,所以树的存储都是转换成二叉树处理
        二叉树一般通过链表来实现

树的应用场景:
1.xml，html等，那么编写这些东西的解析器的时候，不可避免用到树
2.路由协议就是使用了树的算法
3.mysql数据库索引
4.文件系统的目录结构
5.所以很多经典的AI算法其实都是树搜索，此外机器学习中的decision tree也是树结构
"""

# 节点实现
class Node(object):
    """二叉树的节点"""

    def __init__(self, item):
        # 节点上的元素
        self.item = item
        # 左子节点
        self.lchild = None
        # 右子节点
        self.rchild = None

# 二叉树实现
class Tree(object):
    """二叉树"""

    def __init__(self):
        # 开始时根节点为空
        self.root = None

    # 往树的节点添加元素
    def add(self, item):
        # 创建新节点node
        node = Node(item)
        # 先判断树是否为空
        if self.root is None:
            self.root = node
            # 新节点已加上,调用方法结束
            return
        # 弄一个队列,把根节点放进去,每次遍历都从根节点往下走
        queue = [self.root]
        # 遍历树
        while queue:  # []返回False,[..]返回True
            # 每次弹出的都是新队列的头节点
            cur_node = queue.pop(0)  # 0
            # 判断左子节点是否为空
            if cur_node.lchild is None:
                # 为空就将新节点node赋值给左子节点
                cur_node.lchild = node
                # 新节点已加上,调用方法结束
                return
            # 右子节点同理
            elif cur_node.rchild is None:
                cur_node.rchild = node
                return
            # 都不为空就添加到队列,等待下次循环
            else:
                queue.append(cur_node.lchild)
                queue.append(cur_node.rchild)

    # 层次遍历(横向遍历)
    def level_travel(self):
        # 先判断是否为空
        if self.root is None:
            # 空就直接返回
            return
        # 将根节点放入队列
        queue = [self.root]
        # 遍历树
        while queue:
            # 每次弹出的都是新队列的头节点
            cur_node = queue.pop(0)
            # 输出当前节点元素
            print(cur_node.item, end=" ")
            # 判断左子节点
            if cur_node.lchild is not None:
                # 添加到队列,等待后面循环弹出该节点
                queue.append(cur_node.lchild)
            if cur_node.rchild is not None:
                # 添加到队列,等待后面循环弹出该节点
                queue.append(cur_node.rchild)

    # 先序遍历(根-左-右)
    def preorder(self, node):
        if node is None:
            return
        print(node.item, end=" ")
        self.preorder(node.lchild)
        self.preorder(node.rchild)

    # 中序遍历(左-根-右)
    def midorder(self, node):
        if node is None:
            return
        self.midorder(node.lchild)
        print(node.item, end=" ")
        self.midorder(node.rchild)

    # 后序遍历(左-右-根)
    def backorder(self, node):
        if node is None:
            return
        self.backorder(node.lchild)
        self.backorder(node.rchild)
        print(node.item, end=" ")

# 测试代码
if __name__ == "__main__":
    t = Tree()
    t.add(0)
    t.add(1)
    t.add(2)
    t.add(3)
    t.add(4)
    t.add(5)
    t.add(6)
    t.add(7)
    t.add(8)
    t.add(9)
    t.level_travel()
    print("")
    t.preorder(t.root)
    print("")
    t.midorder(t.root)
    print("")
    t.backorder(t.root)


