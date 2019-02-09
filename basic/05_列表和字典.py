# coding=utf-8
"""
tuple()：元祖()通常存放不同类型数据,元素不能被修改,格式化输出的内容其实就是元组
list()：列表[]通常存放同一种类型数据,可以CRUD
set(): 集合{}可以对元组或列表去重,可以CRUD
dict()：字典{}存放键值对,key会做hash处理所以唯一,可以做增删改查操作;是对象的无序集合,用来存放同一种类型的数据 [keys]、[values]、(key:value)
"""


def tuple01():
    T = ("grubby", 33, True, "grubby")

    print(T[0])  # grubby
    print(T.index(33))  # 1
    print(T.count("grubby"))  # 2
    print(len(T))  # 4

    # 遍历循环元组
    for t in T:
        print(t, end=" ")
    print()

    # 元组和列表相互转换
    num_list = [1, 2, 3, 4]
    print(type(num_list))
    num_tuple = tuple(num_list)  # tuple()/list()转换数据类型的时候其实也用到了迭代器,先生成新的空元组/列表再往里面append值
    print(type(num_tuple))


def list01():
    L = ["grubby", "sky", "moon"]

    # 获取数据
    print(L[1])
    print(L.index("sky"))  # 1
    print(len(L))  # 3
    print(L.count("grubby"))  # 1

    # 添加数据
    L.append("fly")
    L.insert(1, "ted")
    print(L)  # ['grubby', 'ted', 'sky', 'moon', 'fly']
    temp_list = ["faker", "pawn"]
    L.extend(temp_list)
    print(L)  # ['grubby', 'ted', 'sky', 'moon', 'fly', 'faker', 'pawn']

    # 修改数据
    L[1] = "uzi"
    print(L)  # ['grubby', 'uzi', 'sky', 'moon', 'fly', 'faker', 'pawn']

    # 排序
    L.sort()
    print(L)  # ['faker', 'fly', 'grubby', 'moon', 'pawn', 'sky', 'uzi']
    L.sort(reverse=True)
    print(L)  # ['uzi', 'sky', 'pawn', 'moon', 'grubby', 'fly', 'faker']

    # 删除数据
    L.remove("uzi")
    L.pop()
    L.pop(1)
    print(L)  # ['faker', 'grubby', 'moon', 'pawn']
    L.clear()
    print(L)  # []


def dict01():
    D = {"name": "grubby", "age": 18, "gender": True}

    # 获取
    print(D["name"])  # grubby
    print(D.get("name"))  # grubby
    print(D.items())  # dict_items([('age', 18), ('gender', True), ('name', 'grubby')])
    print(D.keys())  # dict_keys(['age', 'gender', 'name'])
    print(D.values())  # dict_values([18, True, 'grubby'])
    print(len(D))  # 3

    # 添加/修改
    D["age"] = 19  # key存在就修改对应value,不存在就添加键值对

    # 删除
    D.pop("gender")
    D.popitem()  # 随机弹出一个元素并在字典中删除
    print(D)  # {'age': 19}

    # 合并字典
    temp = {"score": 90, "age": 20}
    D.update(temp)  # 键相同值覆盖
    print(D)  # {'score': 90, 'age': 20}

    # 清空字典
    D.clear()  # clear(): 清空字典中所有键值对
    print(D)  # {}


def list02():
    # set: 去重且无序,通过__hash__()和__equal__()方法保证唯一性
    a = (22, 22, 11, 33, "grubby", True)
    b = set(a)
    c = [22, 22, 11, 33]
    d = set(c)
    print(a)  # (22, 22, 11, 33, 'grubby', True)
    print(b)  # {33, 11, 'grubby', 22, True}
    print(c)  # [22, 22, 11, 33]
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


def list03():
    """
    range()使用风险:
    python2的range(a,b)返回的是包含所有值的list,如果list足够长会占用大量内存空间,可能会MemoryError
    python3的range(a,b)返回的不是list而是迭代器,相当于python2的xrange()
    """
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


def list04():
    """
    需求：列表中的字典排序
    """
    L = [{"name": "grubby", "age": 18}, {"name": "moon", "age": 19}, {"name": "fly", "age": 20}]
    # L.sort()  # TypeError: unorderable types: dict() < dict()  -- 字典无法直接排序
    L.sort(key=lambda x: x["name"])
    print(L)  # [{'age': 20, 'name': 'fly'}, {'age': 18, 'name': 'grubby'}, {'age': 19, 'name': 'moon'}]
    L.sort(key=lambda x: x["age"])
    print(L)  # [{'age': 18, 'name': 'grubby'}, {'age': 19, 'name': 'moon'}, {'age': 20, 'name': 'fly'}]


def list05():
    """
    需求：列表中的字典去重
    分析：字典是可变类型,直接set()会报错 TypeError: unhashable type: 'dict', 得先变成不可变类型
         如果直接tuple(dict)只能返回字典里的key,因为key是不可变类型而value是可变类型,还好有dict.items()
    """
    l = [{"a": 11, "b": 22}, {"a": 33, "b": 44}, {"a": 11, "b": 22}]
    # print(set(l))
    print([tuple(d.items()) for d in l])  # [(('b', 22), ('a', 11)), (('b', 44), ('a', 33)), (('b', 22), ('a', 11))]
    print({tuple(d.items()) for d in l})  # {(('b', 22), ('a', 11)), (('b', 44), ('a', 33))}
    print([dict(t) for t in {tuple(d.items()) for d in l}])  # [{'b': 22, 'a': 11}, {'b': 44, 'a': 33}]

    # 由于set是无序的,如果去重的同时还要保留顺序不变可用list.add()
    s = set()
    l_new = []
    for d in l:
        t = tuple(d.items())
        if t not in s:
            s.add(t)
            l_new.append(d)
    print(s)  # {(('b', 44), ('a', 33)), (('b', 22), ('a', 11))}
    print(l_new)  # [{'b': 22, 'a': 11}, {'b': 44, 'a': 33}]


if __name__ == '__main__':
    # tuple01()
    # list01()
    # dict01()
    # list02()
    # list03()
    # list04()
    list05()
