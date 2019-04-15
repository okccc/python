# coding=utf-8
"""
排序算法：将一串数据按照特定顺序进行排列
常见搜索方法：顺序查找、二分查找、二叉树查找、哈希查找等
备注：python里的/表示传统除法,//表示四舍五入
"""

def bubble_sort(l):
    """1.冒泡排序(复杂度n^2)：将数据两两比较,大的放右边,先确定最大的"""
    n = len(l)
    # 外循环控制循环次数
    for i in range(n-1):
        count = 0
        # 内循环控制每次循环要比较的次数
        for j in range(n-1-i):
            # 两两之间比较大小,大的往后放
            if l[j] > l[j + 1]:
                l[j], l[j + 1] = l[j + 1], l[j]
                # 如果交换位置
                count += 1
        # 如果第一次循环都没有交换位置,说明本身就是有序的(此时即为最优复杂度n)
        if count == 0:
            return


def select_sort(l):
    """2.选择排序(复杂度n^2)：将第一个位置的元素依次与后面的比较大小,先确定最小的"""
    n = len(l)
    # 外循环控制循环次数
    for i in range(n-1):
        # 先假设每次比较的第一个元素就是最小的
        min_index = i
        # 内循环控制每次循环要比较的次数
        for j in range(i+1, n):
            # 拿第一个元素依次与后面元素比较,找到本次循环中数值最小的元素下标
            if l[min_index] > l[j]:
                min_index = j
        # 将本次循环的第一个元素与循环中数值最小的元素互换位置
        l[i], l[min_index] = l[min_index], l[i]


def quick_sort(l, first, last):
    """3.快速排序(复杂度logn)：先找到中间值,再对中间值左右的值分别做快排"""
    if first > last:
        return
    # 先假设第一个元素就是中间值
    mid = l[first]
    low = first
    high = last
    while low < high:
        # high左移
        while low < high and l[high] >= mid:
            high -= 1
        l[low] = l[high]
        while low < high and l[low] < mid:
            low += 1
        l[high] = l[low]
    # 退出循环时low==high
    l[low] = mid

    # 对low左边的列表执行快排
    quick_sort(l, first, low-1)
    # 对low右边的列表执行快排
    quick_sort(l, low+1, last)


def sequence_search(l, i):
    """顺序查找(复杂度n)"""
    for x in range(len(l) - 1):
        if l[x] == i:
            return x
    return -1


def binary_search(l, item):
    """二分查找(复杂度logn：对半分多少次结束-->2的多少次方等于n)：必须作用于有序的顺序表,因为要操作索引"""
    min = 0
    max = len(l) - 1
    while min <= max:
        mid = (min+max)//2
        if l[mid] > item:
            max = mid - 1
        elif l[mid] < item:
            min = mid + 1
        else:
            return mid
    return -1


if __name__ == "__main__":
    # 排序
    L1 = [33, 99, 22, 55, 44, 77, 11, 88]
    # bubble_sort(L1)
    # select_sort(L1)
    quick_sort(L1, 0, len(L1)-1)
    print(L1)  # [11, 22, 33, 44, 55, 77, 88, 99]

    # 搜索
    L2 = [11, 22, 33, 44, 55, 66]
    # result = sequence_search(L2, 33)
    result = binary_search(L2, 33)
    print(result)  # 2
