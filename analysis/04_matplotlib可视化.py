# coding=utf-8
"""
Matplotlib是Python的2D绘图库,可以生成绘图,直方图,功率谱,条形图,错误图,散点图等
pyplot模块包含了常用的matplotlib API函数,承担了大部分的绘图任务

1.figure对象
Matplotlib的图像均位于figure对象中,matplotlib会自动生成fig = plt.figure()

2.subplot分隔区域(子图)
subplot命令是将图片窗口划分成若干区域,按照一定顺序使得图形在每个小区域内呈现
figure对象可以包含一个或者多个Axes(ax)对象,每个Axes对象都是一个拥有自己坐标系统的绘图区域,Axes对象有很多方法
方式一:
ax = plt.subplot(2, 2, 1): 表示将fig分割成2 * 2的区域,1表示当前选中区域的编号,编号从1开始
ax.plot()
plt.show()
方式二:
fig, axs = plt.subplots(2, 2): 同时返回新创建的figure和subplot数组  (2, 2)表示2 * 2的区域
axs[0, 0].plot() --> [0, 0]表示2 * 2区域的第一块区域
plt.show()

注意: 不能使用关键字或保留字作为变量名和方法名，会报错 AttributeError: 'function' object has no attribute '***'
"""

import numpy as np
import matplotlib.pyplot as plt

def single():
    arr = np.random.randint(low=10, high=100, size=(15,))
    # 折线图plot
    plt.plot(arr)
    # plt.savefig("aaa.png")  # 保存图片(暂不支持jpg格式)
    plt.show()  # 注意：show()方法放在最后,因为关闭图片程序才会停止

    # 单柱形图hist
    # hist(): bins是柱子个数,color是柱子颜色,alpha是柱子透明度(默认是1)
    plt.hist(arr, bins=10, color='r', alpha=0.5)
    plt.show()

    # 多柱形图bar
    # 创建x、y坐标
    x = np.arange(5)
    y1, y2 = np.random.randint(low=10, high=20, size=(2, 5))
    # bar(): 指定x和y1的柱子,width是柱子宽度,color是柱子颜色,alpha是柱子透明度
    plt.bar(x, y1, width=0.25, color='r', alpha=0.5)
    # 指定x和y2柱子,x轴基于原点向右偏移0.25个单位
    plt.bar(x + 0.25, y2, width=0.25, color='b')
    plt.show()

    # 散点图scatter
    # 创建x、y坐标
    x = np.random.randint(low=10, high=100, size=200)
    y = x + 10 * np.random.randn(200)
    # scatter(): 指定x和y坐标,根据坐标位置绘制图形
    plt.scatter(x, y, edgecolors='r', alpha=0.5)
    plt.show()

    # 矩阵绘图imshow
    arr = np.random.rand(3, 4)
    # imshow(): 创建一个混淆矩阵,和二维数组数据分布相同,cmap可以选择混淆矩阵的主题
    plt.imshow(arr, cmap=None)
    plt.colorbar()  # 显示颜色条,用来表示数据大小
    plt.show()


def subgraph():
    arr = np.random.randint(low=10, high=50, size=15)
    # plt.subplot()将figure对象划分为2*2个小画板,第三个参数表示使用哪一块
    ax1 = plt.subplot(2, 2, 1)
    ax2 = plt.subplot(2, 2, 2)
    ax3 = plt.subplot(2, 2, 3)
    ax4 = plt.subplot(2, 2, 4)
    type(ax1), ax1
    # 在划分好的不同区域做图
    ax1.plot(arr)
    ax2.plot(arr)
    ax3.plot(arr)
    ax4.plot(arr)
    plt.show()

    # plt.subplots()创建一个2*2区域的figure对象和subplot对象数组
    fig, axs = plt.subplots(nrows=2, ncols=2)
    type(fig), fig, type(axs), axs
    # 在指定区域作图: 当figure图像被分成了>2块个子图,数组的索引要包含行索引和列索引
    axs[0, 1].plot(arr)
    axs[1, 1].hist(arr)
    plt.show()

def legend():
    # 解决matplotlib中文显示问题
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像时负号'-'显示为方块的问题
    # 创建子图: 111表示该子图就是单个图,目的是为了使用Axes对象的很多方法
    ax = plt.subplot(111)
    # 给当前绘图命名
    ax.set_title("西门大酒店销售额年度报表")
    # 给x、y轴添加名称
    ax.set_xlabel("月份")
    ax.set_ylabel("销售额(万)")
    # 给x轴添加刻度标签和步长
    # ax.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    ax.set_xticklabels(range(1, 13))
    ax.set_xticks(range(0, 12, 1))
    # 给y轴添加刻度范围和步长
    ax.set_ylim(0, 100)
    ax.set_yticks(range(0, 100, 20))
    # 设置图例: label是该条线的标签,会在图例中显示
    ax.plot(np.random.randint(10, 70, 12), label="黄焖鸡饭", color="r", alpha=0.5)
    ax.plot(np.random.randint(20, 80, 12), label="沙县小吃", color="g", alpha=0.5)
    ax.plot(np.random.randint(30, 90, 12), label="兰州拉面", color="y", alpha=0.5)
    # 显示图例并且自动调整位置
    ax.legend()
    plt.show()


if __name__ == '__main__':
    legend()
