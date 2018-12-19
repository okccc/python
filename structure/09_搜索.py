# coding=utf-8
"""
常见搜索方法: 顺序查找、二分查找、二叉树查找、哈希查找等
注释：python里的/表示传统除法,//表示四舍五入
"""


# 顺序查找
def sequence_search(l, i):
    for x in range(len(l) - 1):
        if l[x] == i:
            return x
    return -1


# 二分查找
def binary_search(l, i):
    min = 0
    max = len(l) - 1
    while min <= max:
        mid = (min+max)//2
        if l[mid] > i:
            max = mid - 1
        elif l[mid] < i:
            min = mid + 1
        else:
            return mid
    return -1


# 测试代码
if __name__ == "__main__":
    l = [11, 22, 33, 44, 55, 66]
    # result = sequence_search(l, 33)
    result = binary_search(l, 33)
    print(result)
