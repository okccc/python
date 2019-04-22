# coding=utf-8
import numpy as np
# 数据集
from sklearn.datasets import load_boston  # 数据案例
from sklearn.model_selection import train_test_split  # 数据集分割
# 特征工程
from sklearn.preprocessing import StandardScaler  # 特征预处理之标准化缩放
# 回归算法
from sklearn.linear_model import LinearRegression, SGDRegressor, Ridge  # 正规方程, 梯度下降, 领回归
# 回归性能评估
from sklearn.metrics import mean_squared_error  # 均方误差


def linear():
    """
    线性回归预测房子价格
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

    # 3.算法预测和模型评估
    # 1).正规方程
    lr = LinearRegression()
    lr.fit(x_train, y_train)
    # 输出权重参数
    print(lr.coef_)
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
    print("梯度下降的预测结果：%s" % y_r_predict)
    print("梯度下降的均方误差：%s" % mean_squared_error(std_y.inverse_transform(y_test), y_r_predict))



if __name__ == '__main__':
    linear()
