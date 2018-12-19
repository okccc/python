# coding=utf-8
"""
列表list: 用[]表示,通常存放同一种类型数据,可以CRUD
集合set: 用{}表示,可以对元组或列表去重,可以CRUD
"""

name_list = ["grubby", "sky", "moon"]
# 获取数据
print(name_list[1])
print(name_list.index("sky"))  # index(): 元素索引
print(len(name_list))  # len(): 计算列表长度
print(name_list.count("grubby"))  # count(): 统计列表中某个元素出现的次数

# 添加数据
name_list.append("fly")  # append(): 追加数据
name_list.insert(1, "ted")  # insert(): 指定索引插入
temp_list = ["faker", "pawn", "fov"]
name_list.extend(temp_list)  # extend(): 可以追加其他完整列表(扩展)

# 修改数据
# name_list[1] = "grubby"  # 指定索引修改元素

# 删除数据
name_list.remove("fov")  # remove(): 删除列表中第一次出现的数据
name_list.pop()
name_list.pop(1)  # pop(): 默认删除列表最后一个元素,也可以指定索引删除
# name_list.clear()  # clear(): 清空所有数据
del name_list[1]  # del本质上是将变量从内存中删除(不建议使用,一般都用列表本身删除方法)

# 排序
name_list.sort()
name_list.sort(reverse=True)  # sort.md(): 默认升序,可设置reverse参数为降序
name_list.reverse()  # reverse(): 逆序(翻转)

# 遍历
for name in name_list:
    print("我的名字叫 %s" % name)

print(name_list)

# set: 去重,无序
a = (22, 22, 11, 33, "grubby", True)
b = [22, 22, 11, 33]
c = set(a)
d = set(b)
print(a)  # (22, 22, 11, 33, 'grubby', True)
print(c)  # {33, 'grubby', 11, 22, True}
print(b)  # [22, 22, 11, 33]
print(d)  # {33, 11, 22}

e = {'a', 'b', 'c', 'd', 'e', 'f'}
f = {'d', 'e', 'f', 'g'}
# 交集
print(e & f)  # {'d', 'e', 'f'}
# 并集
print(e | f)  # {'d', 'g', 'a', 'f', 'e', 'c', 'b'}
# 差集
print(e - f)  # {'c', 'a', 'b'}
# 异或
print(e ^ f)  # {'c', 'g', 'a', 'b'}

print("=" * 50)

"""
列表生成器: 轻量级循环创建列表
range()使用风险: 
python2的range(a,b)返回的是包含所有值的list,如果list足够长会占用大量内存空间,可能会MemoryError
python3的range(a,b)返回的不是list,只有循环才会返回所有值,不存在该问题
range(a,b): 包左不包右
"""
a = [10, 11, 12]
print(a)
a = [i for i in range(1, 10)]  # for语句控制循环次数,每循环一次都会执行i
print(a)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
a = [i for i in range(1, 10, 2)]  # 第三个参数表示步长
print(a)  # [1, 3, 5, 7, 9]
a = [5 for i in range(1, 10)]
print(a)  # [5, 5, 5, 5, 5, 5, 5, 5, 5]
a = [i for i in range(1, 10) if i % 2 == 0]
print(a)  # [2, 4, 6, 8]
a = [(x, y) for x in range(1, 3) for y in range(1, 4)]  # 嵌套for循环
print(a)  # [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)]
a = [[x, y, z] for x in range(1, 2) for y in range(2, 4) for z in range(3, 5)]
print(a)  # [[1, 2, 3], [1, 2, 4], [1, 3, 3], [1, 3, 4]]

# 需求1: 生成一个[[1,2,3],[4,5,6]....]的列表最大值在100以内
a = [[i, i + 1, i + 2] for i in range(1, 98, 3)]
print(a)

# 需求2: 将[1,2,3,...100]变成[[1,2,3],[4,5,6]....]
a = [i for i in range(1, 101)]
print(a)
b = [[a[x], a[x + 1], a[x + 2]] for x in range(0, 98, 3)]
b.append([100])
print(b)

# 快速生成列表：列表生成器/range()
list1 = [i for i in range(1, 10)]
print(list1)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
list2 = list(range(1, 10))
print(list2)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

