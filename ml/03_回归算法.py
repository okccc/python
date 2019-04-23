# coding=utf-8
import numpy as np
import pandas as pd
# 数据集
from sklearn.datasets import load_boston  # 数据案例
from sklearn.model_selection import train_test_split  # 数据集分割
# 特征工程
from sklearn.preprocessing import StandardScaler  # 特征预处理之标准化缩放
# 回归算法
from sklearn.linear_model import LinearRegression, SGDRegressor, Ridge, LogisticRegression  # 正规方程, 梯度下降, 岭回归, 逻辑回归
# 模型性能评估
from sklearn.metrics import mean_squared_error, classification_report  # 均方误差, 分类报告
# 模型保存和加载
from sklearn.externals import joblib


def linear():
    """
    线性回归预测房价
    """

    # 1.原始数据
    lb = load_boston()

    # 2.特征工程
    # 数据集划分
    x_train, x_test, y_train, y_test = train_test_split(lb.data, lb.target, test_size=0.25)
    # 对特征值和目标值都做标准化处理(和分类不一样,回归的目标值也要做标准化处理,因为目标值是由特征值线性计算出来的)
    std_x = StandardScaler()
    std_x.fit_transform(x_train)
    std_x.transform(x_test)
    # 由于特征值和目标值的特征数量(列数)不一样,所以需要使用不同的标准化对象
    std_y = StandardScaler()
    # transform(X=多维数组)而数据集分割的目标值是一维数组,需要reshape成(-1, 1)
    std_y.fit_transform(np.reshape(y_train, newshape=(-1, 1)))
    std_y.transform(np.reshape(y_test, newshape=(-1, 1)))

    # 加载之前保存的模型进行预测
    # model = joblib.load("./lr.pkl")
    # y_predict = std_y.inverse_transform(model.predict(x_test))
    # print("保存的模型的预测结果：%s" % y_predict)

    # 3.算法预测和模型评估
    # 1).正规方程
    lr = LinearRegression()
    lr.fit(x_train, y_train)
    # 输出权重参数
    print(lr.coef_)

    # 保存训练好的模型,下次就可以不用训练直接使用该模型
    joblib.dump(lr, "./lr.pkl")

    # 预测测试集的房子价格
    y_lr_predict = std_y.inverse_transform(lr.predict(x_test))
    print("正规方程的预测结果：%s" % y_lr_predict)
    print("正规方程的均方误差：%s" % mean_squared_error(std_y.inverse_transform(y_test), y_lr_predict))
    # 2).梯度下降
    sr = SGDRegressor()
    sr.fit(x_train, y_train)
    # 输出权重参数
    print(sr.coef_)
    # 预测测试集的房子价格
    y_sr_predict = std_y.inverse_transform(sr.predict(x_test))
    print("梯度下降的预测结果：%s" % y_sr_predict)
    print("梯度下降的均方误差：%s" % mean_squared_error(std_y.inverse_transform(y_test), y_sr_predict))
    # 3).改用岭回归预测
    r = Ridge(alpha=1.0)
    r.fit(x_train, y_train)
    # 输出权重参数
    print(r.coef_)
    # 预测测试集的房子价格
    y_r_predict = std_y.inverse_transform(r.predict(x_test))
    print("岭回归的预测结果：%s" % y_r_predict)
    print("岭回归的均方误差：%s" % mean_squared_error(std_y.inverse_transform(y_test), y_r_predict))


def logistic():
    """
    逻辑回归做二分类癌症预测
    """
    # 1.原始数据
    columns = ['Sample code number', 'Clump Thickness', 'Uniformity of Cell Size', 'Uniformity of Cell Shape',
              'Marginal Adhesion', 'Single Epithelial Cell Size', 'Bare Nuclei', 'Bland Chromatin', 'Normal Nucleoli',
              'Mitoses', 'Class']
    df = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/breast-cancer-wisconsin.data", names=columns)
    print(df)

    # 2.pandas处理数据
    # 报错：ValueError: could not convert string to float: '?'
    # 先根据df.dtypes确定是哪一列的数据会有?值,然后删除包含?的行
    df = df[df["Bare Nuclei"].apply(lambda x: x != "?")]
    df.dropna()

    # 3.特征工程
    # 数据集分割
    x_train, x_test, y_train, y_test = train_test_split(df[columns[1:10]], df[columns[10]], test_size=0.25)
    # 对特征值做标准化处理
    std = StandardScaler()
    std.fit_transform(x_train)
    std.transform(x_test)

    # 4.算法预测和模型评估
    lr = LogisticRegression(penalty="l2", C=1.0)
    lr.fit(x_train, y_train)
    y_predict = lr.predict(x_test)
    print("预测结果：%s" % y_predict)
    score = lr.score(x_test, y_test)
    print("准确率：%s" % score)
    report = classification_report(y_test, y_predict, labels=[2, 4], target_names=["良性", "恶性"])
    print("召回率：%s" % report)


if __name__ == '__main__':
    logistic()
