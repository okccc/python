"""
pandas数据结构
Series：类似一维数组的对象,由数据和索引组成,索引是自动创建的
DataFrame：类似excel的表格型数据结构,每列数据可以是不同类型,索引包括列索引和行索引
区别：numpy只能处理数值型数据,pandas可以处理非数值型数据
"""

import numpy as np
import pandas as pd


def series():
    # 1.通过list创建,不指定行索引(默认是自增int类型)
    ser = pd.Series(range(1, 5))
    type(ser)  # 对象数据类型
    print(ser.dtypes)  # 对象中元素数据类型
    ser.astype(float)  # 数据类型转换
    print(ser.index, ser.values, ser[3])  # 查看索引和值,根据索引取值
    ser.head(), ser.tail(), ser.head(2)  # 默认查看对象的前/后5条数据,也可以指定条数

    # 通过list创建,指定行索引
    ser = pd.Series(range(10, 15), index=["a", "b", "c", "d", "e"])
    print(ser.index, ser.values)
    print(ser[2], ser["c"])  # 索引分标签索引(label)和位置索引(pos)
    print(ser[1:3], ser["b":"d"])  # 连续索引(切片索引)：标签索引会包含末尾位置
    print(ser[[0, 2]], ser[["a", "c"]])  # 不连续索引

    # series合并
    s1 = pd.Series(range(10, 15))
    s2 = pd.Series(range(20, 23))
    s1.add(s2)  # 两个Series对象合并,缺失值以NAN代替
    s1.add(s2, fill_value=0)  # 两个Series对象合并,先将缺失值以0填充再参与运算

    # 2.通过dict创建(key是行索引)
    pd.Series({"a": 11.1, "b": 22.2, "c": 33.3})


def dataframe():
    # 1.通过numpy创建,不指定行/列索引,默认是自增int类型
    df = pd.DataFrame(np.random.rand(3, 4))
    type(df)  # 对象数据类型
    print(df.shape)  # 对象形状(m行n列)
    print(df.dtypes)  # 对象中元素数据类型
    print(df.index, df.columns, df.values, df[2])  # 对象的行/列索引和值,默认按列索引取值
    df.info()  # 展示当前df在内存中的信息
    df.head(2)  # 指定行数取值

    # 通过numpy创建,指定行/列索引
    df = pd.DataFrame(np.random.rand(3, 4), index=["A", "B", "C"], columns=["a", "b", "c", "d"])
    print(df["c"], df["c"].values)
    # 连续索引(切片索引)：loc标签索引[]、iloc位置索引[)
    print(df.loc["A": "B", "c": "d"])
    print(df.iloc[0:2, 2:4])
    print(df[["a", "c"]])  # 不连续索引

    # dataframe合并
    df1 = pd.DataFrame(np.random.rand(2, 3))
    df2 = pd.DataFrame(np.random.rand(3, 4))
    df1.add(df2)  # 两个DataFrame对象合并,缺失值以NAN代替
    df1.add(df2, fill_value=0)  # 两个DataFrame对象合并,先将缺失值以0填充再参与运算

    # 2.通过dict创建(key是列索引,行索引默认是自增int类型)
    df = pd.DataFrame({
            "A": 1.0,  # float
            "B": pd.to_datetime("20170625"),  # timestamp
            "C": pd.Series(range(10, 14)),  # Series
            "D": ["python", "C", "C++", "Java"],  # list
            "E": np.array([10] * 4),  # ndarray
            "F": "orc"  # str
        })
    print(df["D"])  # 查找指定列
    print(df["D"][3])  # 查找指定列的指定行
    df["G"] = df["C"] * 2  # 添加列
    del(df["F"])  # 删除列


def func():
    # describe()
    ser = pd.Series(range(10, 15))
    ser.sum()
    ser.describe()  # 统计描述
    df = pd.DataFrame(np.random.rand(3, 4))
    df.sum()  # 默认axis=0按列计算
    df.sum(axis=1, skipna=False)  # 可以指定axis=1按行计算,skipna是否排除缺失值
    df.describe()

    # df.apply(func): 作用于指定的行/列,func可以是内置函数也可以是自定义函数
    df.max(), df.apply(lambda x: x.max())  # 默认按列计算
    df.max(axis=1), df.apply(lambda x: x.max(), axis=1)  # 按行计算
    # df.applymap(func): 作用于每一个元素
    df.applymap(lambda x: "%.2f" % x)  # 将每个元素保留两位小数

    # 排序
    ser = pd.Series(range(10, 15), index=[np.random.randint(low=1, high=20, size=(5,))])
    ser.sort_index(), ser.sort_index(ascending=False)  # 按索引排序(默认升序)
    ser.sort_values(), ser.sort_values(ascending=False)  # 按值排序(默认升序)
    df = pd.DataFrame(np.random.rand(3, 4), index=["A", "C", "B"], columns=["b", "d", "a", "c"])
    df.sort_index()   # 默认axis=0按行索引升序排序(此处axis特殊)
    df.sort_index(axis=1, ascending=False)
    df.sort_values(by="c")  # 按值排序：by=列名,默认升序
    df.sort_values(by="c", ascending=False)

    # nan值
    df = pd.DataFrame([np.random.randn(4), [10., np.nan, 20., np.nan], [30., np.nan, np.nan, 40.]])
    df.isna()  # 判断是否是缺失值
    df.dropna()  # 丢弃缺失数据的行/列(默认axis=0按行处理,how="any"只要有nan值就删除所在行/列)
    df.dropna(axis=1, how="all")  # 指定how="all"只有全部为nan时才删除该行/列
    df.fillna(50)  # 填充缺失值

    # 多层索引
    ser = pd.Series(range(10, 15), index=[["a", "a", "b", "c", "c"], [10, 20, 30, 10, 20]])
    type(ser.index)  # 查看索引类型
    print(ser.index)  # 查看索引
    print(ser["b"])  # 根据外层索引取值
    print(ser["a", 10])  # 取出外层索引为a内层索引为10的值
    print(ser[:, 20])  # 取出所有外层索引其内层索引为20的值
    ser.swaplevel()  # 交换分层索引：0最外层、1次外层,只有两层就不用写参数,就是最外层与次外层交换
    ser.sort_index()  # 按层索引排序：默认level=0最外层、level=1次外层...
    ser.sort_index(level=1)
    ser.swaplevel().sort_index()  # 先交换分层再按索引排序

    # 重构
    ser.unstack()  # 默认level=-1将最内层的索引变成列索引,匹配不到的就给NaN值
    ser.unstack(level=0)  # level=0可以将外层索引变成列索引
    ser.unstack().stack()


def time_series():
    # 1.pandas时间序列
    pd.date_range(start="20190101", end="20190131", freq="D")    # D是每天
    pd.date_range(start="20190101", end="20190501", freq="10D")  # 10D是每10天
    pd.date_range(start="20190101", end="20190131", freq="B")    # B是每工作日
    pd.date_range(start="20190101", periods=10, freq="H")        # H是每小时
    pd.date_range(start="20190101", periods=10, freq="MS")       # MS是每月第一天
    pd.date_range(start="20190101", periods=10, freq="M")        # M是每月最后一天
    pd.date_range(start="20190101", periods=10, freq="BMS")      # BMS是每月第一个工作日
    pd.date_range(start="20190101", periods=10, freq="BM")       # BM是每月最后一个工作日

    # 2.pandas时间戳 --> 将字符串转换为时间类型
    df = pd.DataFrame({"timestamp": "2017-06-25 10:12:23", "C": pd.Series(range(5))})
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    # 将该时间列设置为索引,inplace表示原地替换
    df.set_index("timestamp", inplace=True)
    # pandas重采样 --> 将时间序列从一个频率转化为另一个频率处理,比如 2019-01-01 10:00:00 ~ 2019-01-01
    df["timestamp"] = df.resample("M")

    # 3.pandas时间段
    data = pd.DataFrame({"year": 2019, "month": 3, "day": range(10, 20)})
    period = pd.PeriodIndex(year=data["year"], month=data["month"], day=data["day"], freq="D")
    data.set_index(period).resample("2D").mean()
