# coding=utf-8
"""
字典dict: 用{}表示,存放键值对,key唯一,可以做增删改查操作;是对象的无序集合,用来存放同一种类型的数据
         [keys]、[values]、(key:value)
"""

d = {
    "name": "grubby",
    "age": 18,
    "gender": True,
    "height": 1.75,
    "weight": 65.0
}

# 获取
print(d["name"])  # grubby
print(d.get("name"))  # grubby
print(d.items())  # dict_items([('age', 18), ('gender', True), ('weight', 65.0), ('name', 'grubby'), ('height', 1.75)])
print(d.keys())  # 返回所有键: dict_keys(['age', 'gender', 'weight', 'name', 'height'])
print(d.values())  # 返回所有值: dict_values([18, True, 65.0, 'grubby', 1.75])
print(len(d))  # len(): 统计kv对    5

# 添加/修改
d["age"] = 19  # key存在就修改对应value,不存在就添加键值对

# 删除
d.pop("weight")  # pop(): 删除指定key
d.popitem()  # popitem(): 随机弹出一个元素并在字典中删除

# 合并字典
temp = {
    "score": 90,
    "age": 20
}
d.update(temp)  # 键相同值覆盖

# 清空字典
# dictionary.clear()  # clear(): 清空字典中所有键值对

# 遍历循环字典
for key in d:
    print("%s : %s" % (key, d[key]))

print(d)

# 将多个字典放在一个列表中
card_list = [
    {
        "name": "grubby",
        "age": 18,
        "phone": 110
    },
    {
        "name": "moon",
        "age": 19,
        "phone": 119
    }
]

for card in card_list:
    print(card)

# 完整for循环
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
        print("很抱歉呢没有找到 %s 同学" % find_name)  # 如果for循环过程中没有执行到break语句,循环结束后会执行else语句

