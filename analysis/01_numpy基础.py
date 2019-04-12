# coding=utf-8
"""
Python数据分析要求:
1、熟悉数据分析的流程,包括数据采集、处理、可视化等
2、掌握Python语言作为数据分析工具
3、掌握非结构化数据的处理与分析
4、掌握数据分析中常用的建模知识

Anaconda: 是一个集成了大量常用扩展包的环境,包含conda、Python等180多个科学计算包及其依赖项,并且支持所有操作系统平台;
与pip对比:
安装包: pip install xxx;conda install xxx
卸载包: pip uninstall xxx;conda uninstall xxx
升级包: pip install upgrade xxx;conda update xxx

打开Anaconda Prompt终端：
conda --version: 查看conda版本号
conda list: 查看已安装的模块列表
conda install numpy: 安装numpy库(conda install失败的话可以用pip install试下)
conda remove numpy: 卸载numpy库
anaconda search -t conda jsonpath: 寻找安装jsonpath库的资源
anaconda show timbr-io/jsonpath-rw(找到的资源,比如win-64下的某个库): 显示安装该资源的命令
conda install --channel https://conda.anaconda.org/timbr-io jsonpath-rw: 安装命令

Numpy: 科学计算库(矩阵)
Pandas: 数据分析处理库(代码库)
Matplotlib: 数据可视化库(画图)
scikit-learn: 机器学习库(算法库)
"""

import numpy as np

# 创建一个2行3列的随机浮点型二维数组,rand()是固定区间0.0~1.0
arr = np.random.rand(2, 3)
type(arr)  # 数组类型
print(arr.ndim)  # 数组维度(一维二维...)
print(arr.shape)  # 数组形状(m行n列)
print(arr.dtype)  # 数组中数据类型
# 创建一个3行4列的随机浮点型二维数组,uniform()可指定区间大小
np.random.uniform(low=-10.0, high=10.0, size=(3, 4))
# 数据类型转换：转换float64为int32时,是取整不是四舍五入,比如5.69063769-->5  -3.80322353-->-3
arr.astype(dtype=int)
# 创建一个3行4列的随机整型二维数组,randint()可指定区间大小
np.random.randint(low=1, high=10, size=(3, 4))
# 创建一个符合正态分布的随机抽样数组,数据个数是10000
np.random.randn(10000)
# 判断函数
np.any(arr > 0), np.all(arr > 0)  # (True, False)
# 将list转换成矩阵
np.array([range(1, 5), range(6, 10)])
# 创建一个所有元素都是0的数组
np.zeros(shape=(2, 3), dtype=float)
# 创建一个所有元素都是1的数组
np.ones(shape=(2, 3), dtype=int)
# 创建一个指定范围的一维数组,类似python中的range()
np.arange(start=1, stop=10, step=2)
# 重组原数组并调整维度(形状): 将15个元素的一维数组重组成二维数组,二维数组有3个一维数组,每个一维数组5个元素
np.reshape(a=np.arange(15), newshape=(3, 5))
# 将多维数组展开成一维数组
arr.flatten()  
# 行列调换
arr.transpose()
# 打乱数组(洗牌)
np.random.shuffle(arr)  # 只给原数组洗牌并不返回新数组
# 先去重再排序
np.unique(arr)
# 一维数组切片与索引
print(arr[3:8])
# 多维数组切片与索引
print(arr[1][1:4])  # 取出指定一维数组的指定区间
print(arr[:, 1:4])  # 取出所有一维数组的指定区间
# 矩阵与矩阵运算
arr + arr, arr - arr, arr * arr, arr / arr
# 矩阵的广播运算
arr + 10, arr + 10., arr * 1, arr * 1.
# 矩阵中元素运算
np.ceil(arr)  # 向上取整
np.floor(arr)  # 向下取整
np.abs(arr)  # 取绝对值
np.rint(arr)  # 四舍五入
np.isnan(arr)  # 判断是否为NaN(not a number)
np.multiply(arr, 10)  # 元素相乘
np.divide(arr, 10)  # 元素相除
np.mean(arr)  # 求全部元素平均值
np.mean(arr[1][1:3])  # 求指定区间元素平均值
np.sum(arr)  # 求所有元素和
np.sum(arr, axis=0)  # 按列求和
np.sum(arr, axis=1)  # 按行求和
np.max(arr)  # 求最大值
np.min(arr)  # 求最小值
np.var(arr)  # 方差: 所有数据分别和平均数的差的平方的平均值
np.std(arr)  # 标准差: 方差的平方根
np.argmax(arr)  # 数组里最大值的下标值(如果有多个重复数据取第一个)
np.argmin(arr)  # 数组里最小值的下标值
np.cumsum(arr)  # 返回一个一维数组,每个元素都是当前元素和前面所有元素的累加和
np.cumprod(arr)  # 返回一个一维数组,每个元素都是当前元素和前面所有元素的累乘积


