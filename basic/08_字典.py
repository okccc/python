# coding=utf-8
"""
字典dict: 用{}表示,存放键值对,key会做hash处理所以唯一,可以做增删改查操作;是对象的无序集合,用来存放同一种类型的数据
         [keys]、[values]、(key:value)
"""


def dict01():
    d = {"name": "grubby", "age": 18, "gender": True}

    # 获取
    print(d["name"])  # grubby
    print(d.get("name"))  # grubby
    print(d.items())  # dict_items([('age', 18), ('gender', True), ('name', 'grubby')])
    print(d.keys())  # 返回所有键: dict_keys(['age', 'gender', 'name'])
    print(d.values())  # 返回所有值: dict_values([18, True, 'grubby'])
    print(len(d))  # len(): 统计kv对   3

    # 添加/修改
    d["age"] = 19  # key存在就修改对应value,不存在就添加键值对

    # 删除
    d.pop("gender")  # pop(): 删除指定key
    d.popitem()  # popitem(): 随机弹出一个元素并在字典中删除
    print(d)  # {'age': 19}

    # 合并字典
    temp = {"score": 90, "age": 20}
    d.update(temp)  # 键相同值覆盖
    print(d)  # {'score': 90, 'age': 20}

    # 清空字典
    d.clear()  # clear(): 清空字典中所有键值对
    print(d)  # {}


def dict02():
    # 列表中嵌入字典
    name_list = [
        {"name": "grubby"},
        {"name": "moon"},
        {"name": "sky"}
    ]
    find_name = "moon"
    for d in name_list:
        print(d)
        if d["name"] == find_name:
            print("找到 %s 同学了" % find_name)
            break
        else:
            print("很抱歉呢没有找到 %s 同学" % find_name)


if __name__ == '__main__':
    # dict01()
    dict02()