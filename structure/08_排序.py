# coding=utf-8
"""
排序算法: 将一串数据按照特定顺序进行排列
"""


# 冒泡排序(复杂度n^2)
def bubble_Sort(list):
    """将数据两两比较,大的放右边,先确定最大的,如此反复;比较的次数会越来越少"""

    n = len(list)
    # 外循环控制循环次数
    for x in range(n-1):
        # 设置计数器
        count = 0
        # 内循环控制每次循环要比较的次数
        for y in range(n-1-x):
            # 两两之间比较大小
            if list[y] > list[y+1]:
                list[y], list[y+1] = list[y+1], list[y]
                # 如果交换位置了
                count += 1
        # 如果没有交换位置,说明本身就是有序的,不用再循环比较大小了(此时即为最优复杂度n)
        if count == 0:
            return

# 选择排序(复杂度n^2)
def select_sort(list):
    """将第一个元素依次与后面的比较大小,小的放左边,先确定最小的,如此反复"""

    n = len(list)
    # 外循环控制循环次数
    for x in range(n-1):
        # 先假设每次比较的第一个元素就是最小的
        min_index = x
        # 内循环控制每次循环要比较的次数
        for y in range(x+1, n):
            if list[min_index] > list[y]:
                min_index = y
        list[x], list[min_index] = list[min_index], list[x]


if __name__ == "__main__":
    l = [33, 99, 22, 55, 44, 77, 11, 88]
    # bubble_Sort(l)
    select_sort(l)
    print(l)
