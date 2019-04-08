# coding=utf-8
"""
pandas最强大的功能就是分组和聚合
分组: groupby()有很多种分组方式,GroupBy对象没有进行实际运算,只是包含分组的中间数据
过程: split(分组依据) --> apply(函数应用) --> combine(合并结果)
pd.concat(): 沿axis轴方向将多个对象拼接到一起
pd.merge(): 根据外键将不同dataframe的行连接起来,类似数据库的连接操作
duplicated(): 判断是否是重复行    drop_duplicates(): 过滤重复行
replace(): 根据值的内容进行替换
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def groupby():
    df = pd.DataFrame({
        "data1": np.random.rand(8),
        "data2": np.random.rand(8),
        "key1": ['a', 'b', 'a', 'a', 'b', 'b', 'b', 'a'],
        "key2": ['One', 'Two', 'Two', 'Three', 'Three', 'Two', 'One', 'Three'],
    })
    # 查看类型
    type(df), type(df.groupby("key1"))
    # 默认对所有数据列按指定key做分组聚合
    df.groupby(by="key1").describe()
    # 对指定数据列按指定key做分组聚合
    df["data1"].groupby(by=df["key1"]).sum()
    # 对所有数据列按自定义key做分组聚合
    df.groupby(by=[10, 20, 30, 40, 40, 30, 20, 10]).sum()
    # 多层分组：先按key1分组再按key2分组,key1和key2均为索引
    df.groupby(by=["key1", "key2"]).sum()

    df = pd.DataFrame(
        np.random.randint(10, 20, (3, 4)), index=["python", "java", "c++"], columns=['a', 'b', 'c', 'd']
    )
    # 利用位置索引iloc将第二行的2~3列值替换成nan(float类型)
    df.iloc[1, 1:3] = np.nan
    # 按数据类型分组：如果表格中有NaN值,需要指定轴方向为行,因为每一列的数据类型是相同的
    df.groupby(by=df.dtypes, axis=1).sum()
    # 按函数分组
    df.groupby(by=lambda index: len(index), axis=1).sum()

    df = pd.DataFrame(
        np.random.randint(10, 20, (3, 4)),
        columns=pd.MultiIndex.from_arrays([['java', 'c', 'java', 'c'], ['A', 'B', 'C', 'D']], names=['language', 'grade'])
    )
    # 按索引级别分组：level指定索引级别,axis指定索引方向
    df.groupby(level=0, axis=1).sum()


def agg():
    df = pd.DataFrame({
        "key1": ['a', 'b', 'a', 'a', 'b', 'b', 'b', 'a'],
        "key2": ['One', 'Two', 'Two', 'Three', 'Three', 'Two', 'One', 'Three'],
        "data1": np.random.rand(8),
        "data2": np.random.rand(8)
    })
    group = df.groupby(by="key1")  # 对所有列数据按key1分组
    # 1.内置聚合函数
    group.sum()
    group.size()  # 统计元素个数
    group.count()  # 统计非nan值个数
    group.describe()
    # 2.自定义聚合函数agg(...)
    group.agg(lambda x: x.max()-x.min())
    # 多个聚合函数：agg([...])传入列表 --> 其中内置聚合函数要加""且函数名不能重复
    group.agg(["sum", "mean", "max", lambda x: x.max()-x.min()])
    # 对不同数据列使用不同聚合函数：agg({...})传入字典 --> "数据列": "聚合函数"
    group.agg({
        "data1": "sum",
        "data2": ["mean", lambda x: x.max()-x.min()]
    })


def transform():
    df = pd.DataFrame({
        "key1": ["a", "b", "b", "a", "a", "b"],
        "key2": ["one", "two", "two", "three", " three", "three"],
        "data1": np.random.randint(1, 20, (6,)),
        "data2": np.random.randint(1, 20, (6,))
    })
    # transform(func): 默认是将所有列都参与运算
    key1_sum_tf = df.groupby(by="key1").transform("sum").add_prefix("sum_")
    print(key1_sum_tf.index, key1_sum_tf.columns)
    # 将聚合运算生成的结果集添加到原先的df中
    df[key1_sum_tf.columns] = key1_sum_tf
    # 也可以指定数据列参与运算
    key1_sum_tf2 = df[["data1", "data2"]].groupby(by=df["key1"]).transform("sum").add_prefix("sum_")
    df[key1_sum_tf2.columns] = key1_sum_tf2


def apply():
    """
    DataFrame对象分组后直接排序会报错,需借助apply()实现：
    AttributeError: Cannot access callable attribute 'sort_values' of 'DataFrameGroupBy' objects, try using the 'apply' method
    """

    # pandas读取csv文件
    file = "D://PycharmProjects/python/analysis/csv/starcraft.csv"
    df = pd.read_csv(file, usecols=['LeagueIndex', 'Age', 'HoursPerWeek', 'TotalHours', 'APM']).dropna()
    df.info()
    print(df.head(10))
    # 需求：按照LeagueIndex列分组,求其他列的topk
    # df.groupby("LeagueIndex").sort_values("APM", ascending=False)

    # 自定义topk函数,传入默认参数值
    def topk(obj, column="APM", k=3):
        # obj是分组后的对象,按column降序排列取前K个值
        return obj.sort_values(column, ascending=False)[:k]
    # 分组后的每组数据都会应用apply()函数
    data1 = df.groupby(by="LeagueIndex").apply(topk)
    # group_keys=False表示禁用层级索引
    data2 = df.groupby(by="LeagueIndex", group_keys=False).apply(topk, column="Age", k=5)
    # matplotlib画图
    data1.plot.bar()
    data2.plot.bar()
    plt.show()


def concat():
    # 1.拼接ndarray: 默认按列拼接
    arr1 = np.random.randint(10, 20, (3, 4))
    arr2 = np.random.randint(10, 20, (3, 4))
    np.concatenate([arr1, arr2])
    np.concatenate([arr1, arr2], axis=1)

    # 2.拼接series: 默认axis=0按列拼接,外连接
    s1 = pd.Series(np.random.randint(10, 20, 2), index=range(0, 2))
    s2 = pd.Series(np.random.randint(10, 20, 3), index=range(2, 5))
    s3 = pd.Series(np.random.randint(10, 20, 4), index=range(5, 9))
    pd.concat([s1, s2, s3])  # 索引号不同的series对象合并
    s4 = pd.Series(np.random.randint(10, 20, 2))
    s5 = pd.Series(np.random.randint(10, 20, 3))
    s6 = pd.Series(np.random.randint(10, 20, 4))
    pd.concat([s4, s5, s6])  # 索引号相同的series对象合并
    pd.concat([s4, s5, s6])
    pd.concat([s4, s5, s6], axis=1, join="inner")

    # 3.拼接dataframe: 默认axis=0按列拼接,外连接
    df1 = pd.DataFrame(np.random.randint(10, 20, (2, 3)), index=["A", "B"], columns=["a", "b", "c"])
    df2 = pd.DataFrame(np.random.randint(10, 20, (3, 4)), index=["A", "B", "C"], columns=["a", "b", "c", "d"])
    pd.concat([df1, df2], sort=True)
    pd.concat([df1, df2], axis=1, join="inner")


def merge():
    df1 = pd.DataFrame({
            "key": ["a", "b", "c", "b", "a", "b", "c"],
            "data1": np.random.randint(low=1, high=10, size=(7,))
        })
    df2 = pd.DataFrame({
            "key": ["a", "b", "c", "d"],
            "data2": np.random.randint(low=10, high=20, size=(4,))
        })
    # 默认使用两个表的相同列名作为外键且how="inner"内连接
    pd.merge(df1, df2)
    # 更改列名
    df1 = df1.rename(columns={"key": "key1"})
    df2 = df2.rename(columns={"key": "key2"})
    # 指定左右表外键
    pd.merge(df1, df2, left_on="key1", right_on="key2")
    # 指定连接方式
    pd.merge(df1, df2, left_on="key1", right_on="key2", how="outer")  # 外连接
    pd.merge(df1, df2, left_on="key1", right_on="key2", how="left")   # 左连接
    pd.merge(df1, df2, left_on="key1", right_on="key2", how="right")  # 右连接
    # 更改列名
    df1 = df1.rename(columns={"data1": "data"})
    df2 = df2.rename(columns={"data2": "data"})
    # 处理两个表重复列名
    pd.merge(df1, df2, left_on="key1", right_on="key2", suffixes=("_left", "_right"))
    # 创建DataFrame对象
    df1 = pd.DataFrame({"key": ["a", "b", "c", "d", "a", "b"], "data1": np.random.randn(6)})
    df2 = pd.DataFrame({"data2": np.random.randint(10, 20, 3)}, index=["a", "b", "c"])
    # 将行索引做为外键连接
    pd.merge(df1, df2, left_on="key", right_index=True, how="left")


def duplicate():
    # 1.创建series对象
    s1 = pd.Series(np.random.randint(10, 15, 8))
    # 判断series对象每行数据是否是重复数据
    s1.duplicated()
    # 可以直接过滤掉重复数据的行,只留数据首次出现的行
    s1.drop_duplicates()

    # 2.创建dataframe对象
    df = pd.DataFrame({"data1": np.random.randint(10, 15, 8), "data2": ["a", "b", "c", "b", "b", "a", "a", "c"]})
    # 将data2列数据的b都替换成d
    df["data2"].replace("b", "d")
    # dataframe对象需要指定列进行判断和过滤
    df.duplicated("data1")
    df.drop_duplicates("data2")
