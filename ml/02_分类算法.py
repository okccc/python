# coding=utf-8
import pandas as pd
# 数据集
from sklearn.datasets import load_iris, load_boston, fetch_20newsgroups  # 分类、回归数据集案例
from sklearn.model_selection import train_test_split  # 数据集分割
# 特征工程
from sklearn.feature_extraction.text import TfidfVectorizer  # 文本特征抽取
from sklearn.preprocessing import StandardScaler  # 特征预处理之标准化缩放
# 分类算法
from sklearn.neighbors import KNeighborsClassifier  # k近邻算法
from sklearn.model_selection import GridSearchCV  # 网格搜索+交叉验证
from sklearn.naive_bayes import MultinomialNB  # 朴素贝叶斯算法
from sklearn.metrics import classification_report  # 分类模型评估报告


def dataset():
    # 分类案例
    li = load_iris()
    print(li.DESCR)  # 数据描述
    print(li.data)  # 特征值
    print(li.target)  # 目标值
    # 数据集划分
    x_train, x_test, y_train, y_test = train_test_split(li.data, li.target, test_size=0.25)
    # 训练数据集：构建模型
    print("训练集的特征值和目标值：%s, %s" % (x_train, y_train))
    # 测试数据集：评估模型是否有效
    print("测试集的特征值和目标值：%s, %s" % (x_test, y_test))

    news = fetch_20newsgroups(subset='all')
    print(news.data)
    print(news.target)

    # 回归案例
    lb = load_boston()
    print(lb.data)
    print(lb.target)


def knn():
    """
    K-近邻算法预测用户签到位置
    """
    # 1.读取原始数据
    df = pd.read_csv("D://datasets/train.csv")
    # print(df.head())
    """
       row_id       x       y  accuracy    time    place_id
    0       0  0.7941  9.0809        54  470702  8523065625
    1       1  5.9567  4.7968        13  186555  1757726713
    2       2  8.3078  7.0407        74  322648  1137537235
    3       3  7.3665  2.5165        65  704587  6567393236
    4       4  4.0961  1.1307        31  472130  7440663949
    """

    # 2.pandas处理数据
    # 1).缩小数据范围
    df = df.query("1.0 < x < 1.5 & 2.5 < y < 3.0")
    # print(df.head())
    """
         row_id       x       y  accuracy    time    place_id
    600     600  1.2214  2.7023        17   65380  6683426742
    635     635  1.1629  2.7871       160  502525  5819997871
    863     863  1.3828  2.6444        64  245591  5784939944
    867     867  1.0853  2.9063        66  250814  3782126005
    923     923  1.2344  2.8746        73  580132  6398867840
    """
    # 2).时间列处理
    time_value = pd.to_datetime(df["time"], unit="s")
    # print(time_value)
    time_value = pd.DatetimeIndex(time_value)
    # 构造新特征
    df["day"] = time_value.day
    df["hour"] = time_value.hour
    df["weekday"] = time_value.weekday
    # 删除原有时间列
    df.drop(["time"], axis=1)
    # 3).删除标签数量少于n的place_id
    count = df.groupby("place_id").count()
    df_new = count[count.row_id > 3].reset_index()
    df = df[df["place_id"].isin(df_new["place_id"])]
    print(df)

    # 3.特征工程
    # 取出dataframe的特征值和目标值
    x = df.drop(["place_id"], axis=1)
    y = df["place_id"]
    # 数据集分割
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
    # 对训练集和测试集的特征值做标准化缩放(重要,一般预测准确率低时必须做这一步)
    ss = StandardScaler()
    x_train = ss.fit_transform(x_train)
    x_test = ss.transform(x_test)

    # 4.算法预测和模型评估
    knc = KNeighborsClassifier()
    # # 1).输入训练数据
    # knc.fit(x_train, y_train)
    # # 2).预测结果
    # y_predict = knc.predict(x_test)
    # print("预测结果：%s" % y_predict)
    # # 3).预测准确率
    # score = knc.score(x_test, y_test)
    # print("预测准确率：%s" % score)

    # 5.算法调优
    # 设置超参数
    param_grid = {"n_neighbors": [3, 5, 10]}
    # 网格搜索
    gs = GridSearchCV(estimator=knc, param_grid=param_grid, cv=4)
    # 输入训练数据
    gs.fit(x_train, y_train)
    # 预测准确率
    score = gs.score(x_test, y_test)
    print("预测准确率：%s" % score)
    # 结果分析
    print("交叉验证中最好的结果：%s" % gs.best_score_)
    print("最好的参数模型：%s" % gs.best_estimator_)
    print("每个超参数每次交叉验证的结果：%s" % gs.cv_results_)







if __name__ == '__main__':
    knn()
