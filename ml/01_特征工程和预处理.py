"""
pandas：一个数据读取非常方便以及基本的处理格式的工具
scikit-learn：python的机器学习工具,包含很多算法,对于特征的处理提供强大的接口
特征工程：将原始数据转换为更好地代表预测模型的潜在问题的特征的过程,从而提高预测准确性
特征处理：通过特定数学方法将数值型数据转换成算法要求的数据
"""

# 特征抽取
from sklearn.feature_extraction import DictVectorizer  # 字典特征抽取
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer  # 文本特征抽取
# 特征预处理
from sklearn.preprocessing import MinMaxScaler, StandardScaler  # 归一化和标准化
from sklearn.impute import SimpleImputer  # 缺失值处理
import jieba
import numpy as np


def dict_vector():
    """字典特征抽取：将字典中字符串类型数据转换成one-hot编码的特征值,数值类型不会转换"""
    data = [
        {"city": "北京", "temperature": 40},
        {"city": "上海", "temperature": 50},
        {"city": "深圳", "temperature": 60},
    ]
    # 实例化：默认返回sparse矩阵
    dv = DictVectorizer(sparse=False)
    # 转换数据：X=字典或者包含字典的迭代器
    data = dv.fit_transform(X=data)
    # 特征名称
    print(dv.get_feature_names())  # ['city=上海', 'city=北京', 'city=深圳', 'temperature']
    # 转换结果
    print(data)  # [[ 0.  1.  0. 40.] [ 1.  0.  0. 50.] [ 0.  0.  1. 60.]]


def count_vector01():
    """
    文本特征抽取
    1.统计所有文章出现的所有词,重复的只记录一次,单个字母/汉字忽略因为没有分类依据,返回列表
    2.统计每篇文章里列表中词的出现次数
    """
    data = ["life is short, i like python", "life is long, i dislike python"]
    # 实例化
    cv = CountVectorizer()
    # 转换数据：raw_documents=可迭代的字符串文本
    data = cv.fit_transform(raw_documents=data)
    # 特征名称
    print(cv.get_feature_names())  # ['dislike', 'is', 'life', 'like', 'long', 'python', 'short']
    # 将sparse矩阵转换成array数组
    print(data.toarray())  # [[0 1 1 1 0 1 1] [1 1 1 0 1 1 0]]


def count_vector02():
    """中文文本需要先分词"""
    str1 = " ".join(jieba.cut("昨天已经不重要啦"))
    str2 = " ".join(jieba.cut("今天又在混日子啊"))
    str3 = " ".join(jieba.cut("明天会慢慢变好哒"))
    cv = CountVectorizer()
    data = cv.fit_transform(raw_documents=[str1, str2, str3])
    print(cv.get_feature_names())  # ['今天', '变好', '已经', '慢慢', '明天', '昨天', '混日子', '重要']
    print(data.toarray())  # [[0 0 1 0 0 1 0 1] [1 0 0 0 0 0 1 0] [0 1 0 1 1 0 0 0]]


def tf_idf():
    """tf-idf是分类机器学习算法的重要依据"""
    str1 = " ".join(jieba.cut("昨天已经不重要啦"))
    str2 = " ".join(jieba.cut("今天又在混日子啊"))
    str3 = " ".join(jieba.cut("明天会慢慢变好哒"))
    # 实例化tf-idf对象
    cv = TfidfVectorizer()
    data = cv.fit_transform(raw_documents=[str1, str2, str3])
    print(cv.get_feature_names())  # ['今天', '变好', '已经', '慢慢', '明天', '昨天', '混日子', '重要']
    print(data.toarray())  # ...


def mmscaler():
    """归一化处理"""
    mms = MinMaxScaler(feature_range=(0, 1))
    # 数据转换：X=ndarray
    data = mms.fit_transform(X=[[90,2,10,40], [60,4,15,45], [75,3,13,46]])
    # 转换结果
    print(data)  # [[1.  0.  0.  0.  ] [0.  1.  1.  0.83333333] [0.5  0.5  0.6  1.  ]]


def sscaler():
    """标准化缩放"""
    ss = StandardScaler()
    # 转换数据：X=ndarray
    data = ss.fit_transform(X=[[1.,-1.,3.], [2.,4.,2.], [4.,6.,-1.]])
    # 转换结果
    print(data)  # [[-1.06904497 -1.35873244  0.98058068][-0.26726124  0.33968311  0.39223227][ 1.33630621  1.01904933 -1.37281295]]


def imputer():
    """缺失值处理"""
    si = SimpleImputer(missing_values=np.nan, strategy="mean")
    # 转换数据
    data = si.fit_transform(X=[[1, 2], [np.nan, 5], [7, 6]])
    # 转换结果
    print(data)  # [[1. 2.] [4. 5.] [7. 6.]]


if __name__ == '__main__':
    imputer()
