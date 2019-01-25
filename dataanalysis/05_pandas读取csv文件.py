# coding=utf-8
import pandas as pd
import matplotlib.pyplot as plt


def demo01():
    file_path = "D://PycharmProjects/python/analysis/html/FoodFacts.html"
    # 加载csv文件并删除nan值
    df = pd.read_csv(file_path, usecols=["countries_en", "additives_n"], encoding="gbk").dropna()
    print(df.info())
    """
    <class 'pandas.core.frame.DataFrame'>
    Int64Index: 43616 entries, 5 to 65501
    Data columns (total 2 columns):
    countries_en    43616 non-null object
    additives_n     43616 non-null float64
    dtypes: float64(1), object(1)
    memory usage: 1022.2+ KB
    None
    """
    print(df.head(10))
    """
          countries_en  additives_n
    5   United Kingdom          0.0
    6           France          0.0
    8           France          0.0
    10  United Kingdom          5.0
    11  United Kingdom          5.0
    13          France          2.0
    14  United Kingdom          0.0
    15           Spain          0.0
    16          France          3.0
    17  United Kingdom          0.0
    """

    # 取出添加剂列的数据并按国家列分组,返回groupby对象
    group = df["additives_n"].groupby(df["countries_en"])
    print(type(group))  # <class 'pandas.core.groupby.SeriesGroupBy'>

    # 对groupby对象做统计处理
    data = group.mean().sort_values(ascending=False)[:10]
    data.index.name = "country"
    print(type(data))  # <class 'pandas.core.series.Series'>
    print(data)
    """
    countries_en
    Australia,Indonesia,United States     12.0
    France,Saudi Arabia                   10.0
    Denmark,France,Portugal                9.0
    Togo                                   8.0
    France,Greece,Netherlands              8.0
    Qatar                                  7.5
    Denmark,France,Switzerland             7.0
    France,Luxembourg                      6.5
    Egypt,United Kingdom,United States     6.0
    Australia,New Zealand                  5.5
    Name: additives_n, dtype: float64
    """

    # 画图
    data.plot.bar()
    # 显示绘图结果
    plt.show()


if __name__ == "__main__":
    demo01()