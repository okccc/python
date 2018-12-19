# coding=utf-8
"""
元组tuple: 用()表示,通常存放不同类型数据,元素不能被修改,格式化输出的内容其实就是元组
"""

info_tuple = ("grubby", 33, True, "grubby")
print(info_tuple[0])
print(info_tuple.index(33))
print(info_tuple.count("grubby"))  # count(): 统计元素次数
print(len(info_tuple))  # len(): 计算元组长度

# 遍历循环元组
for info in info_tuple:
    print(info, end=" ")
print()

# 元组和列表相互转换
num_list = [1, 2, 3, 4]
print(type(num_list))
num_tuple = tuple(num_list)  # tuple(): 将列表转换成元组
print(type(num_tuple))       # list(): 将元组转换成列表
